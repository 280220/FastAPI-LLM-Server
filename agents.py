import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

# Inicializa el cliente de LLM con la clave API de Groq
# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Recupera la clave API de las variables de entorno
groq_api_key = os.getenv("GROQ_API_KEY")

# Inicializa el cliente de Groq
client = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.8,
    api_key=groq_api_key
)

class QuestionClassificationAgent:
    """
    Agente para clasificar preguntas en categorías predefinidas.
    """

    def __init__(self):
        self.client = client
        self.predefined_categories = [
            "legal", 
            "contable", 
            "médica"
        ]
        self.template = PromptTemplate(
            template=f"""
            Clasifica la siguente pregunta en una de las siguientes categorías temáticas: {self.predefined_categories}.
            Las categorías son:
            - legal: cuestiones relacionadas con leyes, derechos o procesos judiciales.
            - contable: cuestiones relacionadas con contabilidad, impuestos o finanzas.
            - médica: cuestiones relacionadas con medicina, salud o síntomas.
            Responde únicamente con una de estas categorías sin ninguna explicación adicional.
    
            Pregunta: '{{pregunta}}'
            La categoría a la que pertenece esta pregunta es:
            """,
            input_variables=["pregunta"]
            )
        self.llm_chain = LLMChain(prompt=self.template, llm=self.client)

    def run(self, pregunta):
        """
        Ejecuta la clasificación de la pregunta proporcionada.
        
        :param pregunta: La pregunta a clasificar.
        :return: La categoría de la pregunta o un mensaje de error si la clasificación falla.
        """
        input_data = {'pregunta': pregunta}
        try:
            result = self.llm_chain.invoke(input_data)
            category = result['text'].strip().strip("'").lower()

            # Normaliza 'médico' a 'médica'
            if category == "médico":
                category = "médica"

            # Verifica si la categoría es válida
            if category in self.predefined_categories:
                return category
            else:
                return "Cualquier otro tipo de pregunta."

        except Exception as e:
            return f"Un error ocurrió durante el proceso de clasificación: {str(e)}."
    
class ResponseGenerationAgent:
    """
    Agente para generar respuestas basadas en el tipo de pregunta.
    """

    def __init__(self, client):
        self.client = client

    def generate_prompt(self, tipo_pregunta):
        """
        Genera una plantilla de prompt según el tipo de pregunta.
        
        :param tipo_pregunta: El tipo de pregunta (legal, contable, médica).
        :return: Una instancia de PromptTemplate o None si el tipo no es válido.
        """
        if tipo_pregunta == "legal":
            return PromptTemplate(
                template="""
                Eres un abogado especializado en derecho civil y comercial. A continuación, se te proporcionará una pregunta legal. Responde únicamente a esta pregunta de manera clara y concisa en dos frases:
                Pregunta: {pregunta}
                Respuesta:
                """,
                input_variables=["pregunta"]
            )
        elif tipo_pregunta == "contable":
            return PromptTemplate(
                template="""
                Eres un contador con experiencia en impuestos y finanzas. A continuación, se te proporcionará una pregunta contable. Responde únicamente a esta pregunta de manera clara y concisa en dos frases:
                Pregunta: {pregunta}
                Respuesta:
                """,
                input_variables=["pregunta"]
            )
        elif tipo_pregunta == "médica":
            return PromptTemplate(
                template="""
                Eres un médico profesional con años de experiencia. A continuación, se te proporcionará una pregunta médica. Responde únicamente a esta pregunta de manera clara y concisa en dos frases:
                Pregunta: {pregunta}
                Respuesta:
                """,
                input_variables=["pregunta"]
            )
        else:
            return None

    def run(self, pregunta, tipo_pregunta):
        """
        Genera una respuesta para la pregunta proporcionada según su tipo.
        
        :param pregunta: La pregunta a la que se debe responder.
        :param tipo_pregunta: El tipo de pregunta (legal, contable, médico).
        :return: La respuesta generada o un mensaje de error si la generación falla.
        """
        # Genera la plantilla de prompt adecuada según el tipo de pregunta
        prompt = self.generate_prompt(tipo_pregunta)

        if not prompt:
            return "No se pudo clasificar la pregunta."

        # Crea una cadena LLM con la plantilla de prompt seleccionada
        llm_chain = LLMChain(prompt=prompt, llm=self.client)

        input_data = {'pregunta': pregunta}
        try:
            # Genera la respuesta utilizando la cadena LLM
            result = llm_chain.invoke(input_data)
            response = result['text'].strip()
            return response

        except Exception as e:
            return f"Un error ocurrió durante la generación de la respuesta: {str(e)}."