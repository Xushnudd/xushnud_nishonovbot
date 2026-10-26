import os

from dotenv import load_dotenv
from flask import Flask, request
from telebot import TeleBot, types

load_dotenv()

token = os.getenv("BOT_TOKEN")
admin = os.getenv("ADMIN")

app = Flask(__name__)
bot = TeleBot(token, threaded=False)

# start the conversation
@bot.message_handler(commands=['start'])
def start(m):
    chat_id = str(m.chat.id)
    
    if chat_id == admin:
        bot.send_message(
            chat_id=chat_id,
            text="Salom Manager !"
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text="Assalomu alaykum. Qanday savolingiz bor?"
        )
        
@bot.message_handler(content_types=['text'])
def messages(m):
    chat_id = str(m.chat.id)
    text = str(m.text)
    reply_to_message = m.reply_to_message
    
    if chat_id == admin:
        if reply_to_message:
            origin = reply_to_message.forward_origin
            
            bot.send_message(
                chat_id=origin.sender_user.id,
                text=text
            )
    else:
        bot.forward_message(
            chat_id=admin,
            from_chat_id=chat_id,
            message_id=m.message_id
        )
        bot.send_message(
            chat_id=chat_id,
            text="Xabaringiz adminga yuboildi. Tez orada javob olasiz !"
        )
    
@app.route("/", methods=['POST'])
def home():
    update = types.Update.de_json(request.get_data().decode('utf-8'))
    bot.process_new_updates([update])
    return "ok", 200

if __name__ == "__main__":
    app.run()