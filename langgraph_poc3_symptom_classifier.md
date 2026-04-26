# LangGraph PoC #3 — Medical Symptom Classifier
> Este archivo es el inicializador del proyecto. Léelo completo antes de escribir una sola línea de código.

---

## Contexto del proyecto

Tercer PoC de una serie de 5 construidos con **LangGraph** en Python. El foco es **Conditional Edges** — cómo el grafo toma decisiones y deriva el flujo a nodos distintos según el contenido del estado.

**Serie completa:**
1. ✅ News Summarizer *(Graphs + Nodes + Edges)*
2. ✅ RPG Decision Engine *(State Management)*
3. 👉 **Medical Symptom Classifier** *(Conditional Edges)* ← este proyecto
4. ⬜ Human in the Loop
5. ⬜ Multi-agent con LangGraph

---

## ⚠️ Disclaimer importante
Este agente es un **PoC educativo**, no una herramienta médica. El output nunca reemplaza una consulta médica real. Incluir este disclaimer en el README y en el output generado.

---

## Objetivo del PoC

Dado un texto describiendo síntomas, el grafo los clasifica por gravedad y deriva a rutas completamente distintas. El foco está en **definir múltiples conditional edges** que bifurcan el flujo según el estado.

---

## ¿Qué hace el sistema?

```
INPUT: Descripción de síntomas en texto libre

GRAFO:
Node 1 — Intake      → extrae y normaliza los síntomas del texto
Node 2 — Classifier  → evalúa gravedad: leve | moderado | grave
         ↓ conditional edge según gravedad
Node 3a — Leve       → consejos caseros y seguimiento
Node 3b — Moderado   → recomendación de consulta médica + qué decirle
Node 3c — Grave      → derivación a urgencias + qué NO hacer
         ↓ todos convergen
Node 4 — Formatter   → ensambla el output final en MD

OUTPUT: symptom_report_FECHA.md
```

---

## Conditional Edges

```python
def route_by_severity(state: SymptomState) -> str:
    gravedad = state["gravedad"]
    if gravedad == "leve":
        return "leve"
    elif gravedad == "moderado":
        return "moderado"
    else:
        return "grave"

graph.add_conditional_edges(
    "classifier",
    route_by_severity,
    {
        "leve":     "node_leve",
        "moderado": "node_moderado",
        "grave":    "node_grave"
    }
)
```

---

## Estado compartido

```python
class SymptomState(TypedDict):
    input:       str         # Texto raw del usuario
    sintomas:    list[str]   # Síntomas extraídos y normalizados
    gravedad:    str         # leve | moderado | grave
    ruta:        str         # Qué rama tomó el grafo
    respuesta:   str         # Output del nodo de ruta correspondiente
    disclaimer:  str         # Texto legal fijo
    output_md:   str         # Reporte final ensamblado
```

---

## Estructura de carpetas

```
langgraph-poc3-symptom-classifier/
├── main.py              # Entry point — recibe síntomas como argumento
├── graph.py             # Definición del grafo y conditional edges
├── state.py             # SymptomState TypedDict
├── nodes/
│   ├── __init__.py
│   ├── intake_node.py       # Extrae y normaliza síntomas
│   ├── classifier_node.py   # Clasifica gravedad
│   ├── leve_node.py         # Ruta leve → consejos caseros
│   ├── moderado_node.py     # Ruta moderado → ir al médico
│   ├── grave_node.py        # Ruta grave → urgencias
│   └── formatter_node.py    # Ensambla output final
├── prompts/
│   ├── intake.txt
│   ├── classifier.txt
│   ├── leve.txt
│   ├── moderado.txt
│   └── grave.txt
├── outputs/
├── .env.example
├── requirements.txt
└── README.md
```

---

## Cómo se ejecuta

```bash
# Instalar dependencias
pip install langgraph langchain-openai python-dotenv

# Configurar variables de entorno
cp .env.example .env

# Ejecutar
python main.py --input "tengo dolor de cabeza leve y algo de cansancio"
python main.py --input "fiebre de 39.5, dolor de pecho y dificultad para respirar"
python main.py --input "me duele la garganta hace 2 días y tengo mocos"

# Output en: outputs/symptom_report_YYYY-MM-DD.md
```

---

## Variables de entorno

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

---

## Formato del output esperado

```markdown
# Reporte de Síntomas
**Fecha:** YYYY-MM-DD
**Gravedad detectada:** Moderado
**Ruta tomada:** node_moderado

## Síntomas identificados
- Fiebre 38°C
- Dolor de garganta
- Cansancio generalizado

## Recomendación
Consultar con un médico en las próximas 24 horas.
Al llegar, mencionar: fiebre desde hace X horas, intensidad del dolor...

## ⚠️ Disclaimer
Este reporte es generado por una IA con fines educativos.
No reemplaza una consulta médica profesional.
```

---

## Conceptos LangGraph que se practican

| Concepto | Dónde aparece |
|---|---|
| **Conditional edges** | Classifier deriva a 3 rutas distintas |
| **Router function** | `route_by_severity` decide el camino |
| **Branches** | 3 nodos alternativos, solo uno se ejecuta |
| **Convergencia** | Las 3 ramas convergen en Formatter |
| **Estado como decisor** | `gravedad` en el estado determina la ruta |

---

## Diferencia clave vs PoC #2

| | PoC #2 RPG Engine | PoC #3 Symptom Classifier |
|---|---|---|
| Conditional edges | 1 (vivo/muerto) | 3 ramas distintas |
| Propósito | Controlar loop | Bifurcar flujo |
| Nodos alternativos | No | Sí — solo 1 de 3 se ejecuta |
| Convergencia | No | Sí — todas las ramas llegan a Formatter |

---

## Restricciones de scope

- ❌ No hacer diagnóstico médico real
- ❌ No más de 3 niveles de gravedad
- ❌ No loop (flujo lineal con bifurcación)
- ✅ Las 3 rutas deben estar implementadas
- ✅ Foco en que el conditional edge funcione correctamente
- ✅ Disclaimer presente en todo output generado

---

## Definition of Done

- [ ] `SymptomState` definido con todos los campos
- [ ] `classifier_node` asigna correctamente `leve | moderado | grave`
- [ ] `route_by_severity` deriva al nodo correcto
- [ ] Los 3 nodos de ruta generan respuestas distintas y apropiadas
- [ ] Todas las ramas convergen en `formatter_node`
- [ ] Disclaimer incluido en el output
- [ ] Funciona con `python main.py --input "descripción"`

---

## Orden de avance

```
✅ 1 — Graphs + Nodes + Edges    (News Summarizer)
✅ 2 — State Management          (RPG Decision Engine)
👉 3 — Conditional Edges         (Symptom Classifier)  ← estás aquí
⬜ 4 — Human in the Loop
⬜ 5 — Multi-agent con LangGraph
```
