# Rúbrica de Cuadrantes — Ejemplos calibrados

Esta referencia contiene ejemplos clasificados del digest 2026-05-09, agrupados por cuadrante con razonamiento explícito. Úsala cuando dudes entre dos cuadrantes adyacentes o cuando un artículo no encaje obviamente en ninguna categoría.

Los cuadrantes adyacentes —los pares que más se confunden— son:

- **HUM·NO-SLOP ↔ HUM·SLOP**: ¿el texto humano tiene tesis propia o es formato vacío?
- **IA·NO-SLOP ↔ IA·SLOP**: ¿la IA agrega valor con datos primarios o solo llena volumen?
- **IA·SLOP ↔ HUM·SLOP**: ¿esto se generó automáticamente o es un humano escribiendo dentro de un molde vacío?

El cruce más raro y diagnóstico es **HUM·NO-SLOP ↔ IA·SLOP**, los polos opuestos. Si dudas entre ellos, vuelve a leer las señales — probablemente faltan datos.

---

## CUADRANTE 1 · HUM·NO-SLOP

El ideal. Argumento irreemplazable, voz editorial, datos primarios o reporting in situ.

### Ejemplo: "Notes from inside China's AI labs" (Nathan Lambert)
**Por qué humano**: Reporting de presencia. El autor visitó Moonshot, Z.ai, Meituan, Xiaomi, 01.ai y Tsinghua. Las observaciones específicas (developers chinos usan Claude aunque está prohibido, DeepSeek lidera técnicamente pero ByteDance domina mercado) no se pueden generar sin haber estado allí.
**Por qué no-slop**: Tesis con fricción contraintuitiva. Datos primarios que rompen la narrativa simple. Test de intercambio: si reemplazaras "Moonshot" por "otra empresa china", la tesis no funcionaría — los detalles son la sustancia.

### Ejemplo: "Three Model Organisms For Taste" (Scott Alexander)
**Por qué humano**: Marco conceptual original (vexilología + agujeros de guión + nombres tech como organismos modelo). Voz Scott Alexander reconocible: la conexión inesperada entre dominios distintos es marca de la casa.
**Por qué no-slop**: La tesis depende de los tres ejemplos específicos. Cualquier sustitución la rompe. Imposible de generar sin la idea conceptual.

### Ejemplo: "What Words Are Made Of" (terryu, The Intrinsic Perspective)
**Por qué humano**: Densidad bibliográfica real. Cita Paivio (dual coding theory), embodied cognition, preprint específico de Iaia et al. (2025). Tesis declarada como abierta — *"sigue siendo cuestión abierta"* — no resuelve con bow-tie retórico.
**Por qué no-slop**: Contradicción productiva no resuelta. Datos académicos primarios. Lo opuesto al slop por construcción.

### Caso límite: "271 bugs found in Firefox" (Nate's Newsletter)
**Cuadrante**: HUM·NO-SLOP
**Por qué dudoso**: Nate's Newsletter publica con cadencia alta y formato similar entre posts. Podría parecer AI-assisted.
**Por qué se decide humano**: La tesis estructural (271 vs 22) y la implicación específica (giro de autoría del código) requieren posición editorial. El número raro es ancla. Si fuera AI-assisted no sería slop por el dato primario; en cualquier caso, no-slop está claro.

---

## CUADRANTE 2 · IA·NO-SLOP

IA usada como herramienta de síntesis o cobertura, no como fuente de tesis. Datos verificables.

### Ejemplo: "Anthropic growing 10x/year" (Latent Space / AINews)
**Por qué IA**: Latent Space publica AINews con cadencia diaria y cobertura exhaustiva. Workflow AI-assisted documentado por swyx.
**Por qué no-slop**: Cifras concretas verificables (valoración $1-1.2T, crecimiento 80x Q1 2026, ZAYA1-74B, FrontierMath Tier 4 al 48%). La IA es síntesis, los datos son primarios. Test de intercambio: si reemplazaras "Anthropic" por otra empresa, los datos serían distintos — son específicos al asunto.

### Ejemplo: "Container Design Patterns for Distributed Systems" (ByteByteGo)
**Por qué IA**: ByteByteGo opera con producción AI-assisted documentada. Cadencia y formato uniformes.
**Por qué no-slop**: Marco taxonómico claro (6 patrones específicos: sidecar, ambassador, adapter, etc.). Comparación histórica concreta con OOP de los 90. Útil técnicamente.

### Ejemplo: "In Defense of AI Slop" (The Leverage)
**Por qué IA**: El autor declara explícitamente haber usado Claude Code para los gráficos y la estructura. Transparency disclosure.
**Por qué no-slop**: Datos primarios (top 50 Substacks por categoría, 25-32% del contenido marcado IA). Tesis autoincriminatoria — la transparencia es la fricción. La pieza no podría existir sin los datos.

### Caso límite: "Google's Multi-Token Prediction Drafters" (Mehul Gupta)
**Cuadrante**: IA·NO-SLOP
**Por qué dudoso**: Mehul Gupta tiene patrón documentado de slop (otros posts del mismo autor están en IA·SLOP). El título incluye "The Simple Trick That Makes Gemma 4 Feel Faster" — clickbait que en otras combinaciones sería slop.
**Por qué se decide no-slop**: Explica un mecanismo técnico real (modelo borrador predice múltiples tokens) con cifra concreta (3x throughput) y consecuencia verificable. La señal "Simple Trick" es debil sola; las señales de sustancia ganan.

---

## CUADRANTE 3 · HUM·SLOP

Humano + sin fricción. Slop premaquinal. Existe desde antes de los LLMs.

### Ejemplo: "Why Experience and Intuition Are the Human Moat" (Towards Data Science)
**Por qué humano**: Sin marcas claras de generación AI. Probablemente escrito por un autor humano dentro de un género saturado.
**Por qué slop**: Tesis incapturablemente vaga. Usa "moat" — la metáfora corporativa del momento. Existe en mil versiones idénticas (sustituye "experience and intuition" por "creativity", "empathy", "judgment" — funciona igual). Test de intercambio: cualquier rasgo humano funcionaría como sujeto. La tesis es estructural, no específica.

### Ejemplo: "Fifteen tiny ideas that quickly drain stress from my life" (Untethered Mind)
**Por qué humano**: Tono personal, formato bloguero clásico. Probablemente humano genuino.
**Por qué slop**: Listicle de wellness con número grande. Quince microhábitos que funcionarían en cualquier lista de cualquier año. Sin posicionamiento. Sin admisión de que algunos no funcionan. Género completamente saturado.

### Ejemplo: "If I Lost My Job Tomorrow, Here's My Plan" (Cordero Core)
**Por qué humano**: Tono personal en primera persona.
**Por qué slop**: Resiliencia laboral con gancho IA decorativo. Pasos numerados aplicables a cualquier crisis laboral de cualquier época. La coletilla "en la era IA" es ornamental — el contenido sería idéntico sin ella.

### Caso límite: "Your 3-step guide to setting better boundaries at work" (TED Recommends)
**Cuadrante**: HUM·SLOP
**Por qué dudoso**: TED tiene estándares editoriales. No todo lo que publican es slop.
**Por qué se decide slop**: El formato específico "N-step guide" sobre wellness laboral es el molde más reproducido por slop. La tesis es del género, no del autor. Sin posición controvertida, sin caso límite.

---

## CUADRANTE 4 · IA·SLOP

El caso paradigmático. Producción automatizada + sin tesis.

### Ejemplo: "Best Free AI Website Builders I Actually Use" (Mehul Gupta)
**Por qué IA**: Patrón Mehul Gupta documentado: cadencia alta, listicles de herramientas. AI-assisted probable.
**Por qué slop**: "I Actually Use" es la señal clásica del slop que finge autoría. Listado de herramientas gratuitas — formato máximamente replicable. Sin caso, sin contraste, sin opinión que pueda fallar.

### Ejemplo: "How Much Can You Extend Your Life with Drugs?" (AI Forever)
**Por qué IA**: Patrón clásico de slop generativo: "le pregunté a todos los modelos frontier X y comparé las respuestas". El mecanismo es automatizable.
**Por qué slop**: Sin investigación primaria, sin tesis del autor. La pieza es un wrapper sobre output de modelos. Si reemplazaras "drugs" por "exercise" o "sleep" funcionaría idéntica.

### Ejemplo: "I Tried 100 Claude Skills. These Are The Best" (PyCoach, vía digest Medium)
**Por qué IA**: Número alto + autor con catálogo extenso de listicles + patrón "I Tried N things" = generación industrializable.
**Por qué slop**: La tesis es del formato, no del contenido. El test de intercambio falla trivialmente: "100" puede ser 50, 200, 1000 — no cambia nada. Las "best" son intercambiables.

### Caso límite: "Sulphur-2-Base: Uncensored Free AI Video Generation Model" (Mehul Gupta)
**Cuadrante**: IA·SLOP
**Por qué dudoso**: Anuncio de modelo técnico — podría ser IA·NO-SLOP como Ollama o ByteByteGo.
**Por qué se decide slop**: A diferencia de Ollama/ByteByteGo, no hay análisis del mecanismo, no hay benchmark, no hay caso de uso específico. Es "introducción + cómo usarlo gratis" — formato de SEO content sin sustancia técnica.

---

## CASOS DE FRONTERA · DECISIONES JUSTIFICADAS

### "Anthropic Says It's Buying 100% of Compute From xAI's Colossus" (The Information)
**Cuadrante**: HUM·NO-SLOP
**Por qué no IA**: The Information mantiene rigor periodístico. Reporting con declaración del CEO (Amodei).
**Por qué no slop**: Hecho ancla específico (220K GPUs, 300 MW, 100% capacidad). Cifra que el autor tuvo que verificar.

### "Microsoft Cuts Copilot Bloat" (The Information · Applied AI)
**Cuadrante**: HUM·NO-SLOP
**Diferencia con HUM·SLOP**: Aunque "AI X cuts Y" suena formulaico, hay tesis editorial específica sobre la *estrategia* de Microsoft post-boom. No es genérico — es sobre un actor específico haciendo una cosa específica.

### "DigitalOcean · Deploy 2026" (anuncio corporativo)
**Cuadrante**: HUM·NO-SLOP
**Por qué no slop**: Comunicación operativa de evento. No pretende tesis. Función informativa específica. La brevedad y el origen corporativo no son slop por sí mismos.

### "Substack Weekly Stack" (digest de Substack)
**Cuadrante**: IA·NO-SLOP
**Por qué IA**: Curaduría algorítmica del feed.
**Por qué no slop**: La selección no es slop si los artículos curados no lo son. La IA es agregadora, los textos curados tienen autoría.

---

## ANTI-EJEMPLOS · ERRORES COMUNES

### Error 1: "Lo escribió un humano luego no es slop"
**Ejemplo erróneo**: clasificar "Why Experience and Intuition Are the Human Moat" como HUM·NO-SLOP solo porque no tiene marcas IA.
**Corrección**: la sustancia es eje independiente. Un humano puede escribir slop puro sin asistencia de IA.

### Error 2: "Tiene IA badge luego es slop"
**Ejemplo erróneo**: clasificar Latent Space AINews o ByteByteGo como IA·SLOP por el badge.
**Corrección**: AI-assisted con datos primarios y curaduría editorial es IA·NO-SLOP. El badge es un eje, no un veredicto.

### Error 3: "Es corto luego es superficial"
**Ejemplo erróneo**: clasificar el anuncio de Ollama sobre Gemma 4 acelerado como slop por su brevedad.
**Corrección**: la función operativa específica (cómo usar, comandos directos) es valor real. Brevedad ≠ slop.

### Error 4: "Es largo luego tiene sustancia"
**Ejemplo erróneo**: clasificar un essay largo y bien estructurado como no-slop solo por la longitud.
**Corrección**: la prueba sigue siendo el test de intercambio. Si es largo pero los detalles son intercambiables, sigue siendo slop — solo más caro de leer.

### Error 5: "El autor declara IA luego es slop"
**Ejemplo erróneo**: clasificar "In Defense of AI Slop" como IA·SLOP por la auto-declaración.
**Corrección**: la transparencia *es* fricción humana. Un autor que declara su uso de IA y aporta datos primarios está en IA·NO-SLOP, no en IA·SLOP.

---

## DECISIONES POR DEFECTO ANTE DUDA

Si después de aplicar todos los criterios sigues dudando entre dos cuadrantes:

1. **Aplica el test de intercambio** una vez más con un detalle distinto del artículo. Si la tesis sobrevive a múltiples sustituciones, es slop independientemente del eje IA.
2. **Mira el incentivo del autor**: ¿hay curso, libro, lead magnet, comunidad de pago? El sesgo hacia volumen empuja la balanza hacia slop.
3. **Mira la cadencia**: si el autor publica >3 piezas/día sostenidas, la balanza se inclina hacia IA. Si publica 1-2 veces/semana con piezas largas, se inclina hacia humano.
4. **Cuando todo lo demás falle**, prefiere el cuadrante más conservador (asume slop antes que no-slop, asume IA antes que humano) y declara confianza más baja en lugar de un veredicto inflado. Bernardo puede reclasificar; el atlas debe declarar su incertidumbre.
