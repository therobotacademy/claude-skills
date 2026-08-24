"""
Reconstruye el outline (bookmarks) de DIRICHLET_ENERGY_EDUCATION_PAPER.pdf.

Este paper de 8 paginas no trae una pagina de "Contents" impresa: los
encabezados de seccion (1., 2., 2.1., ...) estan incrustados en el cuerpo.
Se identificaron manualmente inspeccionando extract_text() de cada pagina
(ver PROCEDIMIENTO en pdf-TOC-bookmarker/SKILL.md, variante "sin TOC impreso").
"""
from pypdf import PdfReader, PdfWriter

SRC = "DIRICHLET_ENERGY_EDUCATION_PAPER.pdf"
DST = "DIRICHLET_ENERGY_EDUCATION_PAPER_bookmarked.pdf"

# (level, title, pdf_page_index)  -- 0-based, sin offset (documento continuo)
entries = [
    (0, "Abstract", 0),
    (0, "1. Introduction & Theoretical Motivation", 1),
    (0, "2. Mathematical Formulation & Permutation Protocol", 2),
    (1, "2.1. Affiliative Multigraph Definition", 2),
    (1, "2.2. Graph Dirichlet Energy", 2),
    (1, "2.3. Monte Carlo Permutation Test Protocol", 3),
    (0, "3. Dataset & Empirical Implementation", 3),
    (0, "4. Empirical Results & Findings", 4),
    (1, "4.1. Global Trait Homophily Benchmark (361 Classrooms)", 4),
    (1, "4.2. Local Multi-Trait Cohort Signatures", 4),
    (1, "4.3. Developmental Trajectory Across Educational Stages", 5),
    (0, "5. Architectural Implications for Graph Neural Networks", 6),
    (1, "5.1. Why Topology-Only GNNs Fail", 6),
    (1, "5.2. Safeguarding Against Over-Smoothing", 6),
    (0, "6. Conclusion & Future Directions", 7),
    (0, "References", 7),
]

reader = PdfReader(SRC)
writer = PdfWriter()
writer.append(reader)

top_ref = None
for level, title, page in entries:
    if level == 0:
        top_ref = writer.add_outline_item(title, page)
    else:
        writer.add_outline_item(title, page, parent=top_ref)

with open(DST, "wb") as f:
    writer.write(f)

# --- Verificacion ---
check = PdfReader(DST)

def count_nodes(nodes):
    n = 0
    for item in nodes:
        if isinstance(item, list):
            n += count_nodes(item)
        else:
            n += 1
    return n

total = count_nodes(check.outline)
print(f"Bookmarks escritos: {total} (esperados: {len(entries)})")
assert total == len(entries), "Descuadre en el numero de nodos del outline"

for level, title, page in entries[:5]:
    text = check.pages[page].extract_text()[:80].replace("\n", " ")
    print(f"  page {page}: {title!r} -> {text!r}")

print(f"OK -> {DST}")
