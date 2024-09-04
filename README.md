
# Proyecto: Servidor FastAPI Dockerizado para Clasificación y Respuesta de Preguntas Basadas en LLM

Este repositorio contiene el código fuente para un servidor API que utiliza FastAPI y cliente de LLM con la clave API de Groq para clasificar preguntas en categorías específicas y generar respuestas basadas en prompts.

## Estructura del Repositorio

```bash
📁 /app
├── 📄 main.py               # Archivo principal que ejecuta la API usando FastAPI
├── 📄 agents.py             # Archivo que contiene la lógica de integración con LLM
├── 📄 requirements.txt      # Archivo que contiene las dependencias necesarias para ejecutar el proyecto
├── 📄 tests.py              # Archivo que contiene que incluye pruebas unitarias
├── 📄 Dockerfile            # Archivo para contenerizar la aplicación con Docker
└── 📄 docker-compose.yml    # Archivo para levantar el servicio usando Docker Compose
```

## Descripción de los Archivos

- **main.py**: Define los endpoints de la API y gestiona las solicitudes de clasificación y generación de respuestas.
- **agents.py**: Contiene la lógica para la clasificación de preguntas y generación de respuestas a través del LLM.
- **requirements.txt**: Lista las dependencias del proyecto, incluyendo FastAPI, LangChain, entre otras.
- **Dockerfile**: Define cómo crear la imagen Docker para el proyecto.
- **docker-compose.yml**: Facilita el despliegue del entorno utilizando Docker Compose.

## Requisitos

- Docker instalado en su máquina.
- Python 3.12 o superior.
- Clave de API de Groq.
- Para las pruebas unitarias: Pytest 8.3.2

## Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/usuario/FastAPI-LLM-Server.git
   cd FastAPI-LLM-Server
   ```

2. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar el archivo `.env`**:
   Crear un archivo `.env` en el directorio principal del proyecto con el siguiente contenido, reemplazando `your-groq-api-key` con tu clave de API de Groq:
   ```env
   GROQ_API_KEY='your-groq-api-key'
   ```

4. **Construir y ejecutar con Docker**:
   ```bash
   docker-compose up --build
   ```

5. **Acceder a la API**:
   La API estará disponible en `http://localhost:8000`, para ver la documentación interactiva o enviar peticiones POST al endpoint `/preguntar/`.

   La respuesta será un JSON con la clasificación de la pregunta y la respuesta generada por el LLM.

## Pruebas Unitarias

El proyecto incluye pruebas unitarias para verificar el correcto funcionamiento del servicio, asegurando la clasificación de preguntas y la generación de respuestas en tests.py. Las preguntas utilizadas en las pruebas son preguntas ejemplares que abarcan las categorías legal, contable, médica y preguntas no clasificables.

Para ejecutar las pruebas:

```bash
pytest tests.py
```

Las pruebas verifican:

- La correcta clasificación de las preguntas (legal, contable, médica, y otras preguntas no clasificables).
- La generación de respuestas basadas en los prompts proporcionados.
- El manejo adecuado de preguntas no clasificadas, asegurando que el sistema devuelva un código de estado 400 y el mensaje de error apropiado: "No se pudo clasificar la pregunta.".

También tienes la opción de ejecutar el Test como un script de Python, para ver los resultados específicos de las preguntas ejemplares generados por el LLM:

```bash
python tests.py
```
