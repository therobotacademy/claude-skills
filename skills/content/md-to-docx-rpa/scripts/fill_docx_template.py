#!/usr/bin/env python3
"""
fill_docx_template.py — Motor RPA para generar propuestas Word (.docx) con fidelidad tipográfica al 100%.

Clona una plantilla de referencia (por defecto la plantilla corporativa limpia con Verdana/Poppins/Segoe UI)
e inyecta el contenido de una propuesta o documento Markdown preservando estilos, portadas, encabezados
y evitando la regresión a Times New Roman.
"""

import argparse
import os
import shutil
import zipfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

DEFAULT_TEMPLATE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "templates",
    "plantilla_propuesta_lorem.docx"
)

def set_run_font(run, font_name="Verdana", size_pt=9.5, bold=None, italic=None, color_rgb=None):
    """Aplica formato a nivel de run forzando los atributos w:rFonts en el OpenXML."""
    run.font.name = font_name
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    if size_pt is not None:
        run.font.size = Pt(size_pt)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color_rgb is not None:
        run.font.color.rgb = color_rgb

def set_p_text(p, text, font_name="Verdana", size_pt=9.5, bold=None, italic=None, color_rgb=None):
    """Establece el texto de un párrafo con un único run tipográficamente blindado."""
    p.text = ""
    r = p.add_run(text)
    set_run_font(r, font_name=font_name, size_pt=size_pt, bold=bold, italic=italic, color_rgb=color_rgb)
    return r

def set_paragraph_spacing(p, before_pt=None, after_pt=None, line_mult=1.15):
    """Aplica espaciado exacto en twips e interlineado proporcional según el estándar corporativo."""
    from docx.oxml import OxmlElement
    pPr = p._p.get_or_add_pPr()
    sp = pPr.find(qn('w:spacing'))
    if sp is None:
        sp = OxmlElement('w:spacing')
        pPr.append(sp)
    if before_pt is not None:
        sp.set(qn('w:before'), str(int(before_pt * 20)))
    if after_pt is not None:
        sp.set(qn('w:after'), str(int(after_pt * 20)))
    if line_mult is not None:
        sp.set(qn('w:line'), str(int(line_mult * 240)))
        sp.set(qn('w:lineRule'), 'auto')

def set_paragraph_indent(p, left_twips=714, hanging_twips=357):
    """Aplica sangría milimétrica a nivel OpenXML (por defecto 1,26 cm izquierda, 0,63 cm francesa)."""
    from docx.oxml import OxmlElement
    pPr = p._p.get_or_add_pPr()
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind')
        pPr.append(ind)
    if left_twips is not None:
        ind.set(qn('w:left'), str(left_twips))
    if hanging_twips is not None:
        ind.set(qn('w:hanging'), str(hanging_twips))

def set_paragraph_numpr(p, num_id=14, ilvl=0):
    """Vincula el párrafo a la lista nativa de Word (numPr) sin carácter de viñeta en el run."""
    from docx.oxml import OxmlElement
    pPr = p._p.get_or_add_pPr()
    numPr = pPr.find(qn('w:numPr'))
    if numPr is None:
        numPr = OxmlElement('w:numPr')
        ilvl_elm = OxmlElement('w:ilvl')
        ilvl_elm.set(qn('w:val'), str(ilvl))
        numId_elm = OxmlElement('w:numId')
        numId_elm.set(qn('w:val'), str(num_id))
        numPr.append(ilvl_elm)
        numPr.append(numId_elm)
        pPr.append(numPr)

def add_page_break_before_paragraph(p):
    """Inserta un salto de página forzado antes del párrafo especificado."""
    from docx.oxml import OxmlElement
    p_elm = p._p
    new_p_elm = OxmlElement('w:p')
    r_elm = OxmlElement('w:r')
    br_elm = OxmlElement('w:br')
    br_elm.set(qn('w:type'), 'page')
    r_elm.append(br_elm)
    new_p_elm.append(r_elm)
    p_elm.addprevious(new_p_elm)

def remove_page_breaks_from_paragraph(p):
    """Elimina cualquier elemento w:br con tipo 'page' o propiedad pageBreakBefore del párrafo."""
    pPr = p._p.find(qn('w:pPr'))
    if pPr is not None:
        pbb = pPr.find(qn('w:pageBreakBefore'))
        if pbb is not None:
            pPr.remove(pbb)
    for r in p._p.findall(qn('w:r')):
        for br in r.findall(qn('w:br')):
            if br.get(qn('w:type')) == 'page':
                r.remove(br)

def patch_doc_defaults(docx_path, fallback_font="Verdana"):
    """Parchea el archivo word/styles.xml del docx para que docDefaults apunte al font deseado."""
    temp_zip = docx_path + ".temp.zip"
    os.rename(docx_path, temp_zip)
    try:
        with zipfile.ZipFile(temp_zip, 'r') as zin:
            with zipfile.ZipFile(docx_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    content = zin.read(item.filename)
                    if item.filename == 'word/styles.xml':
                        xml_str = content.decode('utf-8')
                        xml_str = xml_str.replace('w:ascii="Times New Roman"', f'w:ascii="{fallback_font}"')
                        xml_str = xml_str.replace('w:hAnsi="Times New Roman"', f'w:hAnsi="{fallback_font}"')
                        xml_str = xml_str.replace('w:cs="Times New Roman"', f'w:cs="{fallback_font}"')
                        content = xml_str.encode('utf-8')
                    zout.writestr(item, content)
    finally:
        if os.path.exists(temp_zip):
            os.remove(temp_zip)

def main():
    parser = argparse.ArgumentParser(description="Generador RPA de propuestas Word (.docx) a partir de plantilla.")
    parser.add_argument("--output", "-o", required=True, help="Ruta del archivo .docx de salida.")
    parser.add_argument("--template", "-t", default=DEFAULT_TEMPLATE, help="Ruta de la plantilla .docx de referencia.")
    parser.add_argument("--client", "-c", help="Nombre del cliente para la portada.")
    parser.add_argument("--title", help="Título principal de la propuesta.")
    parser.add_argument("--subtitle", help="Subtítulo de la propuesta.")
    parser.add_argument("--image", "-i", help="Ruta de la imagen/diagrama a incrustar en Sección 1.")
    parser.add_argument("--price", "-p", default="600", help="Importe económico en euros (por defecto 600).")

    args = parser.parse_args()

    # Validar plantilla
    if not os.path.exists(args.template):
        raise FileNotFoundError(f"No se encontró la plantilla base: {args.template}")

    # Copiar plantilla al destino
    shutil.copyfile(args.template, args.output)

    # Parchear docDefaults
    patch_doc_defaults(args.output, fallback_font="Verdana")

    doc = docx.Document(args.output)

    # Actualizar portada si se pasan argumentos
    if args.client:
        set_p_text(doc.paragraphs[2], f"Cliente: {args.client}", font_name="Calibri", size_pt=11)
    if args.title:
        set_p_text(doc.paragraphs[6], args.title, font_name="Calibri", size_pt=36, bold=True)
        # Encabezado
        if doc.sections and doc.sections[0].header.paragraphs:
            hp = doc.sections[0].header.paragraphs[0]
            if hp.runs:
                set_run_font(hp.runs[0], font_name="Calibri", size_pt=9)
                hp.runs[0].text = args.title
    if args.subtitle:
        set_p_text(doc.paragraphs[7], args.subtitle, font_name="Calibri", size_pt=13, italic=True)

    # Imagen
    if args.image and os.path.exists(args.image):
        p_img = doc.paragraphs[37]
        p_img.text = ""
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(args.image, width=Inches(5.6))

    # Condiciones económicas
    if args.price:
        set_p_text(
            doc.paragraphs[77],
            f"El precio de la producción de las píldoras formativas de vídeo según el alcance descrito en las secciones previas es de {args.price} EUROS.",
            font_name="Verdana",
            size_pt=9.5
        )

    doc.save(args.output)
    print(f"Propuesta generada con éxito en: {args.output}")

if __name__ == "__main__":
    main()
