import re
import pandas as pd
from rapidfuzz import process
import random
from app.gpt import GPTHandler

def match_question(user_msg: str, catalog_df: pd.DataFrame, threshold=80):
    questions = catalog_df["question"].tolist()
    best_match, score, idx = process.extractOne(user_msg, questions)
    if score >= threshold:
        return catalog_df.iloc[idx].to_dict()
    return None

def generate_prompt(user_msg: str, catalog_df: pd.DataFrame, match: dict = None) -> str:
    if match:
        question = f"{match['question']}"
        prompt = (f"Eres un compañero de onboarding a la empresa y apoyas a tus compañeros nuevos.\n"
                  f"Tu compañero quiere saber sobre: {question}.\n"
                  f"Ofrece información clara sobre sus características y beneficios.")
    else:
        questions = "\n".join(catalog_df["question"].tolist())
        prompt = (f"Eres un compañero de onboarding a la empresa y apoyas a tus compañeros nuevos.\n"
                  f"El compañero preguntó, pero no fué claro.\n"
                  f"Este es el catálogo:\n{questions}\n"
                  f"Recomienda algunas opciones según lo que dice el compañero: \"{user_msg}\"")
    return prompt


def detect_intent(user_msg: str, client: GPTHandler) -> str:
    instruction = f"""Clasifica esta intención de usuario en una de las siguientes: 
    portal_y_productos, procesos_internos, saludar, despedirse, ayuda, consultar_sitio, propuesta_valor, que_es_bliwork. Solo responde con el intent exacto, sin explicaciones."""

    response = client.exec_response_api(instruction, user_msg, 0.0) # Pasa 0 para evitar alucinaciones

    return response
