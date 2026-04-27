import argparse
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from graph import build_graph


def main():
    parser = argparse.ArgumentParser(description="Medical Symptom Classifier — PoC #3")
    parser.add_argument("--input", required=True, help="Descripción de síntomas en texto libre")
    args = parser.parse_args()

    app = build_graph()
    result = app.invoke({"input": args.input})

    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/symptom_report_{date.today()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result["output_md"])

    print(f"\nReporte generado: {filename}\n")
    print(result["output_md"])


if __name__ == "__main__":
    main()
