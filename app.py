import argparse
import os
import tomllib
from pathlib import Path
from openai import OpenAI

# 1. Configuración del cliente para usar Ollama localmente
# La biblioteca de OpenAI es compatible con Ollama, solo necesitamos
# cambiar la URL base y la clave de API.
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # La clave de API es un placeholder para Ollama
)

# 2. Carga del archivo de configuración
SETTINGS_PATH = Path("settings.toml")
with SETTINGS_PATH.open("rb") as settings_file:
    SETTINGS = tomllib.load(settings_file)

def parse_args() -> argparse.Namespace:
    """Analiza los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path, help="Ruta al archivo con la base de datos de ejemplo")
    parser.add_argument("user_query", type=str, help="La consulta del usuario")
    return parser.parse_args()

def run_order_tracking(db_info: str, user_query: str) -> str:
    """Envía un prompt para el ejercicio de seguimiento de pedidos."""
    messages = [
        {"role": "system", "content": SETTINGS["prompts"]["role_prompt"]},
        {"role": "user", "content": f"""
Utiliza la siguiente base de datos para responder, que se encuentra entre comillas triples:

"""{db_info}"""

Sigue estos pasos para responder la consulta del usuario, que también está entre comillas triples:
1. Busca el número de seguimiento en la base de datos de pedidos.
2. Proporciona el estado actual y la fecha de entrega.
3. Incluye el enlace para rastrear el paquete en tiempo real.
4. Si el pedido está "Retrasado", ofrece una disculpa y una breve explicación.
5. Mantén siempre un tono amable y servicial.

Consulta del usuario:
"""{user_query}"""
"""},
    ]
    response = client.chat.completions.create(
        model=SETTINGS["general"]["model"],
        messages=messages,
        temperature=SETTINGS["general"]["temperature"],
    )
    return response.choices[0].message.content

def run_return_process(db_info: str, user_query: str) -> str:
    """Envía un prompt para el ejercicio de devolución de productos."""
    messages = [
        {"role": "system", "content": SETTINGS["prompts"]["role_prompt"]},
        {"role": "user", "content": f"""
Eres un agente de servicio al cliente empático de EcoMarket. Tu objetivo es ayudar a los clientes con sus solicitudes de devolución de productos.

Reglas de elegibilidad de devolución:
- No elegibles: productos perecederos, de higiene personal o personalizados.
- Elegibles: cualquier otro producto en un plazo de 30 días, sin usar y en su empaque original.

Sigue estos pasos para responder:
1. Identifica el producto que el usuario quiere devolver.
2. Basándote en las reglas de elegibilidad, determina si el producto puede devolverse.
3. Si es elegible, proporciona una lista clara y numerada con los pasos para iniciar la devolución.
4. Si no es elegible, explica la razón de manera clara y empática.
5. Muestra comprensión y amabilidad en toda tu respuesta.

Consulta del usuario:
"""{user_query}"""
"""},
    ]
    response = client.chat.completions.create(
        model=SETTINGS["general"]["model"],
        messages=messages,
        temperature=SETTINGS["general"]["temperature"],
    )
    return response.choices[0].message.content

def main(args: argparse.Namespace) -> None:
    """Función principal para ejecutar el script."""
    db_content = args.file_path.read_text("utf-8")
    
    # Aquí puedes cambiar la función que quieres ejecutar para tu presentación
    # Descomenta la línea que te interese y comenta la otra
    
    # Para el ejercicio de seguimiento de pedidos:
    # result = run_order_tracking(db_content, args.user_query)

    # Para el ejercicio de devolución de productos:
    result = run_return_process(db_content, args.user_query)
    
    print(result)

if __name__ == "__main__":
    main(parse_args())
