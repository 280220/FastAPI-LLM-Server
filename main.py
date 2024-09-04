from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import QuestionClassificationAgent, ResponseGenerationAgent

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="API de Clasificación y Respuesta de Preguntas",
    description="Una API para clasificar preguntas y generar respuestas utilizando OpenAI",
    version="1.0.0"
)

# Instancia de los agentes
classification_agent = QuestionClassificationAgent()
response_agent = ResponseGenerationAgent(client=classification_agent.client)

# Modelos Pydantic para la solicitud y respuesta
class QuestionRequest(BaseModel):
    pregunta: str

class QuestionResponse(BaseModel):
    pregunta: str
    tipo: str
    respuesta: str

@app.get("/")
async def read_root():
    return {"message": "Bienvendidos a la API de Clasificación y Respuesta de Preguntas"}

@app.post("/preguntar/", response_model=QuestionResponse)
async def preguntar(request: QuestionRequest):
    
    print(f"Received question: {request.pregunta}")
    
    tipo_pregunta = classification_agent.run(request.pregunta)
    print(f"Classified type: {tipo_pregunta}")
    
    if tipo_pregunta == "Cualquier otro tipo de pregunta.":
        raise HTTPException(status_code=400, detail="No se pudo clasificar la pregunta.")
    
    respuesta = response_agent.run(request.pregunta, tipo_pregunta)
    print(f"Generated response: {respuesta}")

    return QuestionResponse(
        pregunta=request.pregunta,
        tipo=tipo_pregunta,
        respuesta=respuesta.strip()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)