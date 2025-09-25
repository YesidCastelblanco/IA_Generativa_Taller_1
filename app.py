import argparse
import json
import logging
import os
import time
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
# 3. Configuración de logging
# ==============================
logging.basicConfig(
    filename=SETTINGS["logging"]["log_file"],
    level=getattr(logging, SETTINGS["logging"]["log_level"]),
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ==============================
# 4. Definición de argumentos CLI
# ==============================
def parse_args() -> argparse.Namespace:
    """Analiza los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(description="Asistente EcoMarket con Mistral (Ollama)")
    parser.add_argument("file_path", type=Path, help="Ruta al archivo con la base de datos de ejemplo (JSON)")
    parser.add_argument("user_query", type=str, help="La consulta del usuario")
    parser.add_argument(
        "--mode",
        choices=["tracking", "return", "auto"],
        default="auto",
        help="Modo de operación: tracking (seguimiento de pedidos), return (devoluciones), o auto (clasificación automática)",
    )
    return parser.parse_args()

# ==============================
# 5. Funciones de interacción
# ==============================
def classify_query(query: str) -> str:
    """Clasifica la consulta del usuario en 'tracking', 'return' o 'complex'."""
    messages = [
        {"role": "system", "content": "Clasifica la consulta en 'tracking', 'return' o 'complex'."},
        {"role": "user", "content": SETTINGS["prompts"]["classifier"]["classify_prompt"].format(query=query)},
    ]
    try:
        response = client.chat.completions.create(
            model=SETTINGS["general"]["model"],
            messages=messages,
            temperature=SETTINGS["general"]["temperature"]["complex"],
        )
        category = response.choices[0].message.content.strip()
        logging.info(f"Consulta clasificada: '{query}' -> {category}")
        return category
    except Exception as e:
        logging.error(f"Error al clasificar consulta: {e}")
        return "complex"  # Por defecto, escalar a humano en caso de error

def generate_summary(query: str) -> str:
    """Genera un resumen de la consulta para un agente humano."""
    messages = [
        {"role": "system", "content": SETTINGS["prompts"]["role_prompt"]},
        {"role": "user", "content": SETTINGS["prompts"]["summary"]["summary_prompt"].format(query=query)},
    ]
    try:
        response = client.chat.completions.create(
            model=SETTINGS["general"]["model"],
            messages=messages,
            temperature=SETTINGS["general"]["temperature"]["complex"],
        )
        summary = response.choices[0].message.content
        logging.info(f"Resumen generado para consulta: '{query}' -> {summary}")
        return summary
    except Exception as e:
        logging.error(f"Error al generar resumen: {e}")
        return f"Error al generar resumen: {e}"

def retrieve_relevant_data(db_info: str, query: str) -> str:
    """Simula la recuperación de datos relevantes (RAG) de la base de datos."""
    try:
        # Asumimos que db_info es un JSON con una lista de registros
        db_records = json.loads(db_info)
        # Simulación simple: buscar coincidencias básicas en el texto de la consulta
        for record in db_records:
            if any(keyword in query.lower() for keyword in [str(record.get("order_id", "")), record.get("product", "")]):
                return json.dumps(record)
        return ""  # No se encontraron datos relevantes
    except json.JSONDecodeError:
        logging.error("Error al parsear la base de datos como JSON")
        return ""

def run_order_tracking(db_info: str, user_query: str) -> str:
    """Ejercicio de seguimiento de pedidos."""
    start_time = time.time()
    # Simular RAG: recuperar solo datos relevantes
    relevant_data = retrieve_relevant_data(db_info, user_query)
    if not relevant_data:
        logging.warning(f"No se encontraron datos relevantes para la consulta: '{user_query}'")
        return "Lo siento, no encontré información sobre ese pedido. ¿Deseas que un agente te asista?"

    messages = [
        {"role": "system", "content": SETTINGS["prompts"]["role_prompt"]},
        {
            "role": "user",
            "content": f"""
{SETTINGS["prompts"]["instruction_prompt"]}
{SETTINGS["prompts"]["rag"]["retrieval_prompt"]}

Utiliza la siguiente información recuperada de la base de datos:

\"\"\"{relevant_data}\"\"\"

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
            temperature=SETTINGS["general"]["temperature"]["tracking"],
        )
        result = response.choices[0].message.content
        elapsed_time = time.time() - start_time
        logging.info(f"Consulta tracking: '{user_query}', Respuesta: {result}, Tiempo: {elapsed_time:.2f}s")
        return result
    except Exception as e:
        logging.error(f"Error al generar respuesta de tracking: {e}")
        return f"❌ Error al generar respuesta: {e}"

def run_return_process(db_info: str, user_query: str) -> str:
    """Ejercicio de devolución de productos."""
    start_time = time.time()
    # Simular RAG: recuperar solo datos relevantes
    relevant_data = retrieve_relevant_data(db_info, user_query)
    if not relevant_data:
        logging.warning(f"No se encontraron datos relevantes para la consulta: '{user_query}'")
        return "Lo siento, no encontré información sobre ese producto. ¿Deseas que un agente te asista?"

    messages = [
        {"role": "system", "content": SETTINGS["prompts"]["role_prompt"]},
        {
            "role": "user",
            "content": f"""
{SETTINGS["prompts"]["instruction_prompt"]}
{SETTINGS["prompts"]["rag"]["retrieval_prompt"]}

Ejemplo positivo:
Consulta: {SETTINGS["prompts"]["positive_example"]}
Razonamiento: {SETTINGS["prompts"]["positive_reasoning"]}
Respuesta: {SETTINGS["prompts"]["positive_output"]}

Ejemplo negativo:
Consulta: {SETTINGS["prompts"]["negative_example"]}
Razonamiento: {SETTINGS["prompts"]["negative_reasoning"]}
Respuesta: {SETTINGS["prompts"]["negative_output"]}

Utiliza la siguiente información recuperada de la base de datos:

\"\"\"{relevant_data}\"\"\"

Responde la consulta siguiendo estas reglas:
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
            temperature=SETTINGS["general"]["temperature"]["return"],
        )
        result = response.choices[0].message.content
        elapsed_time = time.time() - start_time
        logging.info(f"Consulta return: '{user_query}', Respuesta: {result}, Tiempo: {elapsed_time:.2f}s")
        return result
    except Exception as e:
        logging.error(f"Error al generar respuesta de return: {e}")
        return f"❌ Error al generar respuesta: {e}"

# ==============================
# 6. Función principal
# ==============================
def main(args: argparse.Namespace) -> None:
    """Ejecuta el asistente según el modo elegido."""
    if not args.file_path.exists():
        print(f"❌ No se encontró el archivo: {args.file_path}")
        logging.error(f"No se encontró el archivo: {args.file_path}")
        return

    db_content = args.file_path.read_text("utf-8").strip()
    if not db_content:
        print("⚠️ La base de datos está vacía.")
        logging.warning("La base de datos está vacía.")
        return

    if not args.user_query.strip():
        print("⚠️ La consulta del usuario está vacía.")
        logging.warning("La consulta del usuario está vacía.")
        return

    mode = args.mode
    if mode == "auto":
        mode = classify_query(args.user_query)
        print(f"📋 Consulta clasificada como: {mode}")

    if mode == "tracking":
        result = run_order_tracking(db_content, args.user_query)
    elif mode == "return":
        result = run_return_process(db_content, args.user_query)
    else:  # mode == "complex"
        result = generate_summary(args.user_query)
        result = f"⚠️ Consulta compleja: esta consulta será escalada a un agente humano.\nResumen: {result}"

    print("\n=== 📋 Respuesta del asistente ===\n")
    print(result)

if __name__ == "__main__":
    main(parse_args())
