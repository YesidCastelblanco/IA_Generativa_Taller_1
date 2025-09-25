# IA_Generativa_Taller_1

# 📌 Introducción  

EcoMarket es una empresa de e-commerce dedicada a la venta de productos sostenibles, que actualmente enfrenta un **cuello de botella en su servicio de atención al cliente**.  

- El **80% de las consultas** son repetitivas (estado de pedidos, devoluciones, características de productos).  
- El **20% restante** corresponde a casos complejos que requieren empatía, creatividad o resolución de problemas especiales.  
- El tiempo promedio de respuesta es de **24 horas**, lo que impacta negativamente la satisfacción de los clientes.  

El objetivo del taller es **diseñar una solución de IA generativa** que permita:  
- Reducir los tiempos de respuesta.  
- Mantener la información siempre actualizada.  
- Escalar la atención al ritmo del crecimiento de la empresa.  
- Empoderar a los agentes humanos para enfocarse en los casos complejos.  

A continuación, se presentan las fases de desarrollo de la solución propuesta.  

---
# 📌 Fase 1  
**Selección y Justificación del Modelo de IA para EcoMarket**

---

## ✅ Modelo Seleccionado  
Se propone un **Large Language Model (LLM) de código abierto**, específicamente **Mistral** (Mistral-7B o Mixtral-8x7B), afinado con datos propios de EcoMarket mediante **fine-tuning ligero** (LoRA/PEFT) e integrado con la base de datos en tiempo real a través de **Retrieval-Augmented Generation (RAG)**.  

La arquitectura incluye:  
- **LLM base**: Mistral, eficiente y con bajo costo computacional frente a modelos propietarios.  
- **Fine-tuning ligero**: Con historial de consultas, catálogo de productos, políticas y FAQs (anonimizados).  
- **Integración RAG**: Para acceder a información estructurada como pedidos, inventario y envíos, evitando alucinaciones.  
- **Sistema de routing híbrido**: Middleware que clasifica consultas; el **80% repetitivo** se maneja con IA y el **20% complejo** se escala a agentes humanos con un resumen generado por el modelo.  

Esta arquitectura reduce el tiempo de respuesta de **24h a minutos**, mejora la satisfacción del cliente y empodera al equipo humano.

---

## 🔎 Justificación de la Elección  

### 1. Tipo de Modelo Adecuado  
Un **LLM fine-tuned open-source** como Mistral es más adecuado que:  
- **GPT-4 u otros modelos propietarios**: Mayor fluidez, pero con costos elevados (≈0.03 USD/1k tokens → >10k USD/mes en alto volumen) y menos control sobre datos privados.  
- **LLMs pequeños (ej. DistilBERT)**: Más económicos, pero insuficientes para conversaciones multiturno o empatía en casos complejos.  
- **Híbridos sin fine-tuning**: No capturan el tono y necesidades específicas de EcoMarket (sostenibilidad, amabilidad).  

Mistral combina precisión factual (gracias a RAG) con fluidez y empatía (gracias al fine-tuning).  

---

### 2. Precisión vs. Fluidez  
- **Precisión en consultas críticas (80%)**: RAG permite consultar la base de datos de EcoMarket en tiempo real (pedidos, envíos, catálogo). Esto reduce errores factuales y evita inventar información.  
- **Fluidez en preguntas generales (20%)**: Mistral genera respuestas naturales y empáticas, alineadas con el branding sostenible de EcoMarket.  

---

### 3. Arquitectura Propuesta  
1. **Modelo Base**: Mistral-7B, fine-tuned con interacciones pasadas (etiquetadas por tipo de consulta).  
2. **Capa RAG**: Embeddings (ej. Sentence Transformers) para recuperar datos de la BD antes de la generación.  
3. **Flujo de Operación**:  
   - Usuario envía consulta (chat/email/redes).  
   - Clasificador detecta tipo de consulta.  
   - Repetitivas → RAG + LLM responden.  
   - Complejas → Escalamiento a humano con resumen IA.  
4. **Despliegue**: En la nube (ej. AWS, Hugging Face Spaces) con optimizaciones como cuantización para reducir latencia y costos.  
5. **Integración**: Vía APIs/Webhooks (ej. LangChain, Zapier) → rápida implementación en <1 mes.  

---

### 4. Justificación Basada en Criterios  

| **Criterio**        | **Argumento**                                                                 | **Beneficio para EcoMarket**                                    |
|----------------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------|
| **Costo**           | Open-source sin licencias; fine-tuning inicial (~500–1000 USD) y hosting (~0.001 USD/inferencia). | Ahorro de ~70% frente a APIs propietarias (>10k USD/mes). |
| **Escalabilidad**   | >10k consultas/día con auto-escalado y LoRA para actualizaciones rápidas.       | Soporta el crecimiento sin cuellos de botella, disponible 24/7. |
| **Integración**     | APIs estándar (LangChain, LlamaIndex) y conexión directa a BD y canales.       | Implementación ágil sin reemplazar infraestructura legacy.      |
| **Calidad**         | Fine-tuning + RAG reducen errores en 90%; IA maneja 80% de casos, humano 20%. | Respuestas en <5 min; satisfacción +20-30% (NPS).              |
| **Ética y Control de Datos** | Cumplimiento de normativas (GDPR, Habeas Data) y anonimización de información sensible. | Protección de la privacidad del cliente y mayor confianza en el uso de la IA. |

---

## ✅ Conclusión  
La mejor solución para EcoMarket es un **modelo híbrido basado en Mistral, fine-tuned con datos propios e integrado vía RAG**, con un sistema de escalamiento humano para casos complejos.  

Esta arquitectura equilibra **calidad de respuesta, costo, escalabilidad, integración y control total sobre los datos**, alineándose plenamente con los objetivos del caso de estudio.  

---

# 📌 Fase 2  
**Evaluación de Fortalezas, Limitaciones y Riesgos Éticos del modelo de IA propuesto para EcoMarket**

---

## 💪 Fortalezas  

1. **Reducción del tiempo de respuesta**  
   - El modelo puede manejar de forma autónoma el **80% de las consultas repetitivas** (estado de pedidos, devoluciones, características de productos).  
   - Esto reduciría el tiempo promedio de **24 horas a segundos**, elevando significativamente la satisfacción del cliente.  

2. **Disponibilidad 24/7 y escalabilidad**  
   - La IA ofrece soporte ininterrumpido, incluyendo fines de semana y horarios nocturnos.  
   - Puede gestionar miles de consultas simultáneas sin necesidad de contratar más personal, soportando el rápido crecimiento de EcoMarket.  

3. **Consistencia en las respuestas**  
   - Garantiza uniformidad en la información y en el tono de la comunicación, reduciendo variaciones o errores comunes en la atención humana.  

4. **Empoderamiento de los agentes humanos**  
   - Al automatizar las tareas repetitivas, libera a los agentes para que se enfoquen en el **20% de casos complejos** que requieren empatía, negociación o creatividad.  
   - El modelo puede además entregar un **resumen contextual** al agente, agilizando la atención y mejorando la eficiencia del equipo.  

---

## ⚠️ Limitaciones  

1. **Incapacidad para manejar casos complejos**  
   - No puede replicar la empatía genuina ni el pensamiento crítico necesario para resolver quejas graves, compensaciones especiales o problemas técnicos no estandarizados.  

2. **Dependencia de la calidad de los datos**  
   - Funciona bajo el principio *“Garbage In, Garbage Out”*: si la información en la base de datos está desactualizada o es incorrecta, replicará ese error.  

3. **Falta de comprensión emocional real**  
   - Aunque puede simular un tono empático, no comprende emociones humanas complejas, lo que puede frustrar a clientes en situaciones delicadas.  

4. **Necesidad de mantenimiento y supervisión**  
   - Requiere reentrenamiento, monitoreo y ajustes constantes para evitar respuestas inadecuadas o fuera de contexto.  

5. **Cobertura limitada en escenarios atípicos**  
   - Consultas nuevas o combinaciones inusuales de problemas pueden superar su capacidad y requerir escalamiento temprano a un humano.  

---

## ⚖️ Riesgos Éticos  

1. **Alucinaciones**  
   - *Riesgo*: El modelo podría inventar información (ej. números de seguimiento falsos o políticas inexistentes).  
   - *Mitigación*: Integrar RAG para limitar respuestas a información oficial y usar expresiones como *“Según nuestro sistema…”* para dar transparencia.  

2. **Sesgo en las respuestas**  
   - *Riesgo*: Si los datos de entrenamiento contienen sesgos (ej. trato preferencial a ciertos clientes), el modelo puede amplificarlos.  
   - *Mitigación*: Auditoría y curación de datos antes del entrenamiento, además de revisiones periódicas para monitorear sesgos en producción.  

3. **Privacidad de datos**  
   - *Riesgo*: Uso de información sensible (direcciones, historial de compras) podría exponer datos personales.  
   - *Mitigación*: Aplicar **anonimización/pseudoanonimización**, encriptación, controles de acceso y cumplimiento estricto con normativas como **GDPR** y la **Ley de Protección de Datos Personales en Colombia (Habeas Data)**.  

4. **Impacto laboral**  
   - *Riesgo*: Los agentes de servicio al cliente pueden percibir la IA como una amenaza a sus empleos.  
   - *Mitigación*: Comunicar desde el inicio que la IA busca **empoderar, no reemplazar**. Capacitar a los agentes para tareas de mayor valor (gestión de crisis, fidelización, supervisión del sistema de IA).  

5. **Responsabilidad y supervisión**  
   - *Riesgo*: En caso de error del modelo, surge la pregunta de quién asume la responsabilidad.  
   - *Mitigación*: Establecer protocolos claros de supervisión humana, trazabilidad de decisiones y mecanismos de corrección rápida.  

---

## ✅ Conclusión  

El modelo propuesto ofrece **fortalezas clave en eficiencia, escalabilidad y calidad de servicio**, pero también presenta **limitaciones y riesgos éticos** que deben gestionarse con cuidado.  

La implementación debe hacerse con un enfoque **híbrido y supervisado**, donde la IA automatice las consultas repetitivas y los agentes humanos atiendan los casos complejos. Con auditorías de datos, protocolos de privacidad y estrategias de empoderamiento laboral, EcoMarket puede construir un sistema equilibrado que combine lo mejor de la **automatización + factor humano**, cumpliendo con estándares técnicos y éticos.  

---

