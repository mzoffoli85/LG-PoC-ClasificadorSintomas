from typing import TypedDict


class SymptomState(TypedDict):
    input:      str          # Texto raw del usuario
    sintomas:   list[str]    # Síntomas extraídos y normalizados
    gravedad:   str          # leve | moderado | grave
    ruta:       str          # Qué rama tomó el grafo
    respuesta:  str          # Output del nodo de ruta correspondiente
    disclaimer: str          # Texto legal fijo
    output_md:  str          # Reporte final ensamblado
