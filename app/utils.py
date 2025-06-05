import re
import pandas as pd
from rapidfuzz import process
import random
from app.gpt import GPTHandler


def generar_folio():
    numeros = ''.join(str(random.randint(0, 9)) for _ in range(6))
    return f"KVK25-{numeros}"


def match_car_model(user_msg: str, catalog_df: pd.DataFrame, threshold=80):
    modelos = catalog_df["model"].tolist()
    best_match, score, idx = process.extractOne(user_msg, modelos)
    if score >= threshold:
        return catalog_df.iloc[idx].to_dict()
    return None

def extract_financing_parameters(user_msg: str):
    try:
        years_match = re.search(r'(\d)\s*años?', user_msg)
        enganche_match = re.search(r'(\d{2,3}[,\.\d]*)\s*(mil|k)?', user_msg)

        years = int(years_match.group(1)) if years_match else 3

        if enganche_match:
            raw = enganche_match.group(1).replace(',', '').replace('.', '')
            factor = 1000 if enganche_match.group(2) else 1
            enganche = int(raw) * factor
        else:
            enganche = 30000

        return {'years': years, 'enganche': enganche}
    
    except Exception as e:
        return {'years': 3, 'enganche': 30000}

def calculate_financing(precio: float, enganche: float, plazo: int, tasa: float = 0.10) -> float:
    monto = precio - enganche
    meses = plazo * 12
    tasa_mensual = tasa / 12
    pago = monto * (tasa_mensual * (1 + tasa_mensual) ** meses) / ((1 + tasa_mensual) ** meses - 1)
    return pago


def generate_prompt(user_msg: str, catalog_df: pd.DataFrame, match: dict = None) -> str:
    if match:
        auto_line = f"{match['make']} {match['model']} {match['year']}, ${match['price']:,.0f} MXN"
        prompt = (f"Eres un asesor experto en autos.\n"
                  f"El cliente está interesado en: {auto_line}.\n"
                  f"Ofrece información clara sobre sus características y beneficios.")
    else:
        autos = "\n".join([
            f"- {row['make']} {row['model']} {row['year']}, ${row['price']:,.0f} MXN"
            for _, row in catalog_df.iterrows()
        ])
        prompt = (f"Eres un asesor experto en autos.\n"
                  f"El cliente busca un auto, pero no fue claro.\n"
                  f"Este es el catálogo:\n{autos}\n"
                  f"Recomienda algunas opciones según lo que dice el cliente: \"{user_msg}\"")
    return prompt


def detect_intent(user_msg: str, client: GPTHandler) -> str:
    instruction = f"""Clasifica esta intención de usuario en una de las siguientes: 
    buscar_auto, calcular_financiamiento, saludar, despedirse, ayuda, consultar_sedes, propuesta_valor, generar_orden. Solo responde con el intent exacto, sin explicaciones."""

    response = client.exec_response_api(instruction, user_msg, 0.0) # Pasa 0 para evitar alucinaciones

    return response
