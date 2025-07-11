from telebot.types import Message
import telebot
import requests

API_URL = "http://127.0.0.1:8000/api"
BOT_TOKEN = "7781641058:AAHZ1-gHQrZvSxYk-murPvIR1gwyomiCQLw"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username
    }
    response = requests.post(API_URL + "/register/", json=data)
    if response.status_code == 200:
        if response.json().get('message'):
            bot.send_message(message.chat.id, "Вы уже были зарегистрированы ранее!")
        else:
            bot.send_message(message.chat.id, f"Вы успешно зарегистрированы! Ваш уникальный номер: {response.json()['id']}")
    else:
        bot.send_message(message.chat.id, f"Произошла ошибка при регистрации!")
        print(response.json())
        print(response.status_code)
        print(response.text)

@bot.message_handler(commands=['myinfo'])
def user_info(message: Message):
    response = requests.get(f"{API_URL}/user/{message.from_user.id}/")
    if response.status_code == 200:
        bot.reply_to(message, f"Ваша регистрация:\n\n{response.json()}")
    elif response.status_code == 404:
        bot.send_message(message.chat.id, text= "Вы не зарегистрированы!")
    else:
        bot.send_message(message.chat.id, text= "Непредвиденная ошибка!")
        print("Код:", response.status_code)
        print("Ответ:", response.text)

if __name__== "__main__":
    bot.polling(none_stop=True)