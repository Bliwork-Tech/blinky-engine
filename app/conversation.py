
from app.gpt import GPTHandler
from app.utils import (
    match_car_model,
    calculate_financing,
    generate_prompt,
    detect_intent,
    generar_folio,
    extract_financing_parameters
)
from pandas import DataFrame

detect_sentiment=True
kavac_site = "https://www.kavak.com/mx/blog/sedes-de-kavak-en-mexico"

def conversation_handler(catalog_df: DataFrame, user_msg: str, gpt_handler: GPTHandler):
    """Solo se delega a un función fuera de API"""
    intent = detect_intent(user_msg, gpt_handler)

    if intent == "saludar":
        reply = "¡Hola! Soy tu asesor KVKy. ¿Buscas un auto o necesitas financiamiento?"
    
    elif intent == "despedirse":
        reply = "¡Gracias por contactarnos! 🚗 Que tengas un excelente día."

    elif intent == "ayuda":
        reply = ("😅 Puedo ayudarte a:\n"
                 "- 🚙 Buscar autos disponibles\n"
                 "- 🤔 Calcular tu financiamiento\n"
                 "- 🗺️ Compartirte las sedes de Kavak\n"
                 "- 😎 Conocer nuestra propuesta de valor\n\n"
                 "Que dices, ¿Te interesa? 😊")

    elif intent == "consultar_sedes":
        reply = (f"🧭 Puedes consultar las sedes de Kavak en México aquí:\n{kavac_site}")
    
    elif intent == "propuesta_valor":
        prompt = (f"Usa el sitio: \n{kavac_site}")
        input = (f"Extrae la propuesta de valor, pero no incluyas las sedes, sintetizalo lo mejor posible con enfoque de negocio. Incluye un emoji.\"")

        reply = gpt_handler.exec_response_api(prompt, input)

    elif intent == "buscar_auto":
        best_match = match_car_model(user_msg, catalog_df)
        prompt = generate_prompt(user_msg, catalog_df, best_match)
        messages = [{"role": "user", "content": prompt}]

        reply = gpt_handler.exec_chat_api(messages)

        if detect_sentiment:
            prompt = (f"Clasifica el sentimiento en una de las siguientes: enojo, normal. Solo responde con el sentimiento, sin explicaciones.")

            sentiment = gpt_handler.exec_response_api(prompt, user_msg, 0.0).lower()
            print(sentiment)

            if sentiment == 'enojo':
                reply = "Parece que no encontramos el modelo que buscas.\n Te recomiendo visitar [nuestro sitio de contacto](https://www.kavak.com/mx/contacto) para más información. ¡Estamos aquí para ayudarte! 😊"

    elif intent == "calcular_financiamiento":
        best_match = match_car_model(user_msg, catalog_df)
        if best_match:
            price = best_match["price"]
            investment = extract_financing_parameters(user_msg)
            enganche = investment['enganche']
            plazo = investment['years']
            mensualidad = calculate_financing(price, enganche, plazo, tasa=0.10)
            reply = (f"🤓 Plan de financiamiento para {best_match['model']}:\n"
                     f"- Precio: ${price:,.0f} MXN\n"
                     f"- Enganche (20%): ${enganche:,.0f} MXN\n"
                     f"- Plazo: {plazo} años\n"
                     f"- Mensualidad estimada: ${mensualidad:,.0f} MXN\n")
        else:
            reply = "🫠 No pude encontrar el modelo que mencionas. ¿Puedes escribirlo nuevamente? 😅"

            if detect_sentiment:
                prompt = (f"Detecta el sentimiento del mensaje y si sientes frustración o que es más de una ocasión la pregunta"
                          f"Usa el sitio: \nhttps://www.kavak.com/mx/contacto para comunicarse y genera un mensaje cálido para el usuario diciendo que no encontramos el modelo y recomendandole hablar con un asesor telefónico, agrega un emoji.\"")

                reply = gpt_handler.exec_response_api(prompt, user_msg)
            
    elif intent == "generar_orden":
        reply = f"🫶 Super, nos encantará acompañarte durante la adquisición del auto 🎉, para tu seguimiento utiliza el siguiente folio: {generar_folio()}\n📱 Nos contactaremos contigo para continuar el proceso."  

    else:
        reply = "🫣 No entendí tu mensaje. ¿Podrías repetirlo con más detalle?"
    
    return reply