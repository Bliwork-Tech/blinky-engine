import pytest
from app.utils import match_car_model, calculate_financing, extract_params
import pandas as pd

@pytest.fixture
def sample_catalog():
    data = {
        "marca": ["Toyota", "Nissan"],
        "modelo": ["Corolla", "Versa"],
        "anio": [2022, 2023],
        "precio": [350000, 280000]
    }
    return pd.DataFrame(data)

def test_match_car_model(sample_catalog):
    result = match_car_model("Busco un corola", sample_catalog)
    assert result is not None
    assert "Corolla" in result["modelo"]

def test_calculate_financing():
    mensualidad = calculate_financing(300000, 60000, 4, tasa=0.10)
    assert mensualidad > 0

def test_extract_params():
    text = "Quiero pagarlo a 5 años con un enganche de 60 mil"
    result = extract_params(text)
    assert result["years"] == 5
    assert result["enganche"] == 60000
