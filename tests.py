from fastapi.testclient import TestClient
from main import app

# Configurar el cliente de FastAPI para realizar pruebas
client = TestClient(app)

def test_classification_and_response():
    """
    Prueba para verificar la clasificación y generación de respuestas para preguntas predefinidas. Con preguntas ejemplares.
    """
    questions = [
        {"pregunta": "¿Cuáles son los derechos de un trabajador?", "expected_tipo": "legal"},
        {"pregunta": "¿Cómo se calcula el IVA?", "expected_tipo": "contable"},
        {"pregunta": "¿Cuáles son los síntomas de la gripe?", "expected_tipo": "médica"},
        {"pregunta": "¿Cuál es la capital de Francia?", "expected_tipo": "Cualquier otro tipo de pregunta"}
    ]

    for question_data in questions:
        pregunta = question_data["pregunta"]
        expected_tipo = question_data["expected_tipo"]

        # Hacer la solicitud a la API
        response = client.post("/preguntar/", json={"pregunta": pregunta})

        # Verificar si la pregunta se clasificó correctamente
        if expected_tipo == "Cualquier otro tipo de pregunta":
            # Si es una pregunta no clasificable, esperamos un código 400 y que se levanta "No se pudo clasificar la pregunta."
            assert response.status_code == 400
            assert response.json()['detail'] == "No se pudo clasificar la pregunta."
        else:
            # Si es una pregunta clasificable, se verifica la respuesta y la categoría
            assert response.status_code == 200
            response_json = response.json()
            tipo_pregunta = response_json['tipo']
            generated_response = response_json['respuesta']

            # Verificar que la clasificación sea correcta y la respuesta no esté vacía
            assert tipo_pregunta == expected_tipo
            assert generated_response != ""

        print("-" * 40)

if __name__ == "__main__":
    test_classification_and_response()
