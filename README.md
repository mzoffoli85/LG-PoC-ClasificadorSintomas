# LangGraph PoC #3 — Medical Symptom Classifier

> **PoC educativo** — No reemplaza una consulta médica profesional.

Clasificador de síntomas médicos construido con LangGraph. Dado un texto describiendo síntomas, el grafo los clasifica por gravedad y deriva a rutas distintas usando **Conditional Edges**.

## Flujo del grafo

```
intake → classifier → (conditional edge por gravedad)
                         ├── node_leve     → consejos caseros
                         ├── node_moderado → consultar médico
                         └── node_grave    → urgencias
                                ↓
                           formatter → outputs/symptom_report_FECHA.md
```

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tu DEEPSEEK_API_KEY
```

## Uso

```bash
python main.py --input "tengo dolor de cabeza leve y algo de cansancio"
python main.py --input "fiebre de 39.5, dolor de pecho y dificultad para respirar"
python main.py --input "me duele la garganta hace 2 días y tengo mocos"
```

El reporte se guarda en `outputs/symptom_report_YYYY-MM-DD.md`.

## Estructura

```
├── main.py              # Entry point
├── graph.py             # Grafo y conditional edges
├── state.py             # SymptomState TypedDict
├── nodes/
│   ├── intake_node.py
│   ├── classifier_node.py
│   ├── leve_node.py
│   ├── moderado_node.py
│   ├── grave_node.py
│   └── formatter_node.py
├── prompts/             # Prompts por nodo
├── outputs/             # Reportes generados
└── .env.example
```

## Variables de entorno

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## Serie LangGraph PoCs

| # | Proyecto | Concepto |
|---|---|---|
| 1 | News Summarizer | Graphs + Nodes + Edges |
| 2 | RPG Decision Engine | State Management |
| **3** | **Symptom Classifier** | **Conditional Edges** |
| 4 | Human in the Loop | — |
| 5 | Multi-agent | — |
