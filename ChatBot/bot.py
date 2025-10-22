import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Importar nuestra lógica
from agent_core import invoke_agent
from memory_manager import get_chat_history, add_message_to_history

# Cargar variables de entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv("AAHgkR_uAI5VW1vJSm9bdvnPDqphmyxl8ZY")

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('¡Hola! Soy tu agente IA. Pregúntame algo.')

# Función principal que maneja los mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    # 1. Guardar el mensaje del usuario en la memoria
    add_message_to_history(user_id, 'user', user_message)

    # 2. Obtener el historial de chat (incluyendo el nuevo mensaje)
    chat_history = get_chat_history(user_id)

    # 3. Invocar al agente (el cerebro)
    try:
        # Esto puede tardar unos segundos; Telegram puede mostrar "escribiendo..."
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action='typing'
        )

        response = invoke_agent(user_message, chat_history)
        ai_message = response['output']

    except Exception as e:
        print(f"Error invocando al agente: {e}")
        ai_message = "Lo siento, tuve un error al procesar tu solicitud."

    # 4. Guardar la respuesta de la IA en la memoria
    add_message_to_history(user_id, 'ai', ai_message)

    # 5. Enviar la respuesta al usuario
    await update.message.reply_text(ai_message)

def main():
    print("Iniciando el bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Añadir handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciar el bot
    application.run_polling()