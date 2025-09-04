
from app.gpt import GPTHandler
from app.utils import (
    match_question,
    generate_prompt,
    detect_intent
)
from pandas import DataFrame

detect_sentiment=True
site = "https://bliwork.com"

def conversation_handler(catalog_df: DataFrame, products_df: DataFrame, user_msg: str, gpt_handler: GPTHandler):
    """Solo se delega a un función fuera de API"""
    intent = detect_intent(user_msg, gpt_handler)

    if intent == "saludar":
        reply = "¡Hola! Soy Blinky, tu peer para que puedas hacerme preguntas y te pueda orientar."
    
    elif intent == "despedirse":
        reply = "¡Gracias por contactarme! Que tengas un excelente día."

    elif intent == "ayuda":
        reply = ("😅 Puedo ayudarte a:\n"
                 "- Entender que es Bliwork\n"
                 "- Conocer el portal y productos disponibles"
                 "- Dudas sobre los procesos internos y contactos\n"
                 "- Conocer nuestra propuesta de valor\n\n"
                 "Dime en que puedo ayudarte. 😊")

    elif intent == "consultar_sitio":
        reply = (f"🧭 Puedes consultar nuestro sitio web aquí:\n{site}")
    
    elif intent in ("propuesta_valor","que_es_bliwork"):
        prompt = (f"Usa el sitio: \n{site}")
        input = (f"Extrae la propuesta de valor, sintetizalo lo mejor posible con enfoque de negocio. Incluye un emoji.\"")

        reply = gpt_handler.exec_response_api(prompt, input)

    elif intent == "portal_y_productos":
        best_match = match_question(user_msg, products_df)
        prompt = generate_prompt(user_msg, products_df, best_match)
        messages = [{"role": "user", "content": prompt}]

        reply = gpt_handler.exec_chat_api(messages)

        if detect_sentiment:
            prompt = (f"Clasifica el sentimiento en una de las siguientes: enojo, normal. Solo responde con el sentimiento, sin explicaciones.")

            sentiment = gpt_handler.exec_response_api(prompt, user_msg, 0.0).lower()
            print(sentiment)

            if sentiment == 'enojo':
                reply = f"Parece que no encontramos lo que buscas.\n Te recomiendo visitar [nuestro sitio de contacto]({site}/contact) para más información, o en slack en el canal #preguntas. 😊"

    elif intent == "procesos_internos":
        question = match_question(user_msg, catalog_df)
        if question:
            reply = (f"🤓 {question['question']}:\n"
                     f"- {question['answer']}\n"
                     f"- {question['additional_info']}\n")
        else:
            reply = "🫠 No tengo información sobre eso. ¿Puedes escribirlo nuevamente? 😅"

            if detect_sentiment:
                prompt = (f"Detecta el sentimiento del mensaje y si sientes frustración o que es más de una ocasión la pregunta"
                          f"Usa el sitio: \n{site} para comunicarse y genera un mensaje cálido para el usuario diciendo mencionando que no tenemos información, puedes recomendar comunicarse al canal #preguntas de slack, agrega un emoji.")

                reply = gpt_handler.exec_response_api(prompt, user_msg)
    else:
        reply = "🫣 No entendí tu mensaje. ¿Podrías repetirlo con más detalle?"
    
    return reply