from configTelegram import *
from openai import OpenAI
import telebot
import time
import threading

#instancia del bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Función para enviar mensajes con reintentos
def enviar_mensaje_con_reintentos(bot, chat_id, texto, max_reintentos=3):
    reintentos = 0
    while reintentos < max_reintentos:
        try:
            bot.send_message(chat_id, texto)
            break  # Salir del bucle si el mensaje se envía correctamente
        except Exception as e:
            reintentos += 1
            print(f"Error al enviar mensaje (reintento {reintentos}): {e}")
            if "429" in str(e):  # Si el error es por límite de solicitudes
                tiempo_espera = 40  # Esperar 40 segundos (ajusta según el mensaje de error)
                print(f"Esperando {tiempo_espera} segundos antes de reintentar...")
                time.sleep(tiempo_espera)
            else:
                raise  # Relanzar la excepción si no es un error 429

#Acciones del bot de telegram

#Responde al comando /start
@bot.message_handler(commands=["start","ayuda", "help"])

def cmd_start(message):
    #Da la bienvenida al usuario del bot
    bot.reply_to(message, "Bienvenido a Pulmolabs")

@bot.message_handler(commands=["mision"])

def cmd_mision(message):
    bot.reply_to(message,MISION_TXT)

@bot.message_handler(commands=["vision"])

def cmd_vision(message):
    bot.reply_to(message,VISION_TXT)

@bot.message_handler(commands=["info"])

def cmd_info(message):
    bot.reply_to(message,INFO_TXT)

#Responde a mensajes que no son comandos
@bot.message_handler(content_types=["text"])

def bot_mensajes_texto(message):
    texto_usuario = message.text
    print(f"El usuario escribio: {texto_usuario}")
    texto_usuario += ", da una respuesta corta de menos de 3500 caracteres."

    if message.text.startswith("/"):
        bot.send_message(message.chat.id, "Comando no disponible")
    else:
        error_enviado = False
        try:
            RespuestaIA = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=[
                    {
                        "role": "user",
                        "content": texto_usuario
                    }
                ]
            )
            
            # Imprimir la respuesta completa de la API para depuración
            #print("Respuesta de la API:", RespuestaIA)

            if RespuestaIA and RespuestaIA.choices:
                respuesta = RespuestaIA.choices[0].message.content
                print(respuesta)
            #if respuesta != None:
                #respuesta = f"Recibi el mensaje: {texto_usuario}"
                enviar_mensaje_con_reintentos(bot,message.chat.id,respuesta)
            else:
                respuesta = "Servidor IA ocupado"
                bot.send_message(message.chat.id, respuesta)
        
            print(texto_usuario)
        except Exception as e:
            if not error_enviado:
            

                if "429" in str(e):
                    print("Servicio ocupado")
                else:
                    bot.send_message(message.chat.id,"Error al procesar la solicitud, intentar mas tarde")
                error_enviado = True

def recibir_mensajes():
    bot.infinity_polling()

#########        MAIN
if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "da la bienvenida"),
        telebot.types.BotCommand("/info", "da la informacion"),
        telebot.types.BotCommand("/mision","muestra la mision de la empresa"),
        telebot.types.BotCommand("/vision","muestra la vision de la empresa"),
    ])
    print('iniciando conexion con IA')
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=DEEPSEEK_TOKEN,
    )

    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start()
    print('Bot iniciado correctamente')