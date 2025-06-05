from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_whatsapp_endpoint():
    response = client.post(
        "/chatbot/http",
        data={"Body": "Hola", "From": "whatsapp:+521234567890"}
    )
    assert response.status_code == 200
    assert "message" in response.json()