import argparse
import os
import tomllib
from pathlib import Path
from openai import OpenAI

# ==============================
# 1. Configuración del cliente para usar Ollama localmente
# ==============================
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Placeholder para Ollama
)

# ==============================
# 2. Carga del archivo de configuración
# ==============================
SETTINGS_PATH = Path("settings.toml")
if not SETTINGS_PATH.exists():
    raise FileNotFoundError("❌ No se encontró settings.toml en el directorio actual.")

with SETTINGS_PATH.open("rb") as settings_file:
    SETTINGS = tomllib.load(settings_file)


# ==============================
# 3. Definición de argumentos CLI
# ==============================
def parse_args() -> argparse.Namespace:
    """Analiza los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(description="Asistente EcoMarket con Mistral (Ollama)")
    parser.add_argument("file_path", type=Path, help="Ruta al archivo con la base de datos de ejemplo")
    parser.add_argument("user_query", type=str, help="La consulta del usuario")
    parser.add_argument(
        "--mode",
        choices=["tracking", "return"],
        default="tracking",
        help="Modo de operación: tracking (seguimiento de pedidos) o return (devoluciones)",
    )
    return parser.parse_args()


# ==============================
# 4. Funciones de interacción
# ==============================
def run_order_tracking(db_info: str, user_query: str) -> str:
    """Ejercicio de seguimiento de pedidos."""
    messages = [
        {"role": "system", "content": SETTINGS["prompts"]["role_prompt"]},
        {
            "role": "user",
            "content": f"""
Utiliza la siguiente base de datos de pedidos entre comillas triples:

\"\"\"{db_info}\"\"\"

Responde la consulta siguiendo estas reglas:
1. Busca el número de seguimiento en la base de datos.
2. Proporciona el estado actual y la fecha de entrega.
3. Incluye el enlace de rastreo en tiempo real.
4. Si el pedido está "Retrasado", ofrece disculpas y una breve explicación.
5. Mantén siempre un tono amable y servicial.

Consulta del usuario:
\"\"\"{user_query}\"\"\"
""",
        },
    ]
    try:
        response = client.chat.completions.create(
            model=SETTINGS["general"]["model"],
            messages=messages,
            temperature=SETTINGS["general"]["temperature"],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error al generar respuesta: {e}"


def run_return_process(db_info: str, user_query: str) -> str:
    """Ejercicio de devolución de productos."""
    messages = [
        {"role": "system", "content": SETTINGS["prompts"]["role_prompt"]},
        {
            "role": "user",
            "content": f"""
Eres un agente de servicio al cliente empático de EcoMarket. Tu objetivo es ayudar a los clientes con sus solicitudes de devolución.

Reglas de elegibilidad:
- No elegibles: productos perecederos, de higiene personal o personalizados.
- Elegibles: cualquier otro producto en un plazo de 30 días, sin usar y en su empaque original.

Sigue estos pasos:
1. Identifica el producto a devolver.
2. Verifica si es elegible según las reglas.
3. Si es elegible, da una lista numerada con los pasos de devolución.
4. Si no es elegible, explica la razón claramente y con empatía.
5. Mantén siempre un tono amable y servicial.

Consulta del usuario:
\"\"\"{user_query}\"\"\"
""",
        },
    ]
    try:
        response = client.chat.completions.create(
            model=SETTINGS["general"]["model"],
            messages=messages,
            temperature=SETTINGS["general"]["temperature"],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error al generar respuesta: {e}"


# ==============================
# 5. Función principal
# ==============================
def main(args: argparse.Namespace) -> None:
    """Ejecuta el asistente según el modo elegido."""
    if not args.file_path.exists():
        print(f"❌ No se encontró el archivo: {args.file_path}")
        return

    db_content = args.file_path.read_text("utf-8").strip()
    if not db_content:
        print("⚠️ La base de datos está vacía.")
        return

    if not args.user_query.strip():
        print("⚠️ La consulta del usuario está vacía.")
        return

    if args.mode == "tracking":
        result = run_order_tracking(db_content, args.user_query)
    else:
        result = run_return_process(db_content, args.user_query)

    print("\n=== 📋 Respuesta del asistente ===\n")
    print(result)


if __name__ == "__main__":
    main(parse_args())
