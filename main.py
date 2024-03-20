import time
import requests
from bs4 import BeautifulSoup as bs
import telebot
from telebot import *

TOKEN = ' YOUR TOKEN '
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет этот бот нужен для поиска настольных игр с сайта hobby games🔎")


@bot.message_handler(commands=['search'])
def search(message):
    mes = bot.send_message(message.chat.id, '🔍Введите запрос')
    bot.register_next_step_handler(mes, get_title)


@bot.message_handler(type=['text'])
def get_title(message):
    bot.send_message(message.chat.id, "начинаю  поиск⏰")
    parser(message)


def parser(message):
    req = requests.get("https://hobbygames.ru/catalog/search?keyword=" + message.text)
    soup = bs(req.text, "html.parser")

    time.sleep(1)

    data = (soup.findAll("a", class_="name"))
    price_span = (soup.findAll("span", class_="price"))


    for links_and_title, price in zip(data, price_span):
        bot.send_message(message.chat.id, f"Link: {links_and_title.get('href')} Title: {links_and_title.get('title')} Price: {price.get_text()}")


bot.infinity_polling()
