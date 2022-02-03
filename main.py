import re
from unicodedata import category
import config
import telebot
from telebot import types
import json
import os

bot=telebot.TeleBot(config.TOKEN)
global cat 

def start_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Каталог', 'Создать заказ') #Имена кнопок
    return markup

@bot.message_handler(commands=["start"])
def inline(message):
    with open("data.json", "r",encoding='utf-8') as read_file:
      data = json.load(read_file)    
    if data["users"].count(message.chat.id) == 0:
      data["users"].append(message.chat.id)
      with open("data.json", "w") as write_file:
        json.dump(data, write_file)    
    print(message.from_user.username + " has started bot")
    msg = bot.reply_to(message, 'Начнём же. Выберите действие:',reply_markup=start_keyboard())

@bot.message_handler(content_types="text")
def check_answer(message):
  if message.chat.id == 654258355 and message.text.split()[0] == "Изменение":
      with open("data.json", "r",encoding='utf-8') as read_file:
        data = json.load(read_file) 
      for user in data["users"]:
        bot.send_message(user, message.text)

  if message.text == "Каталог":
    with open("items.json", "r",encoding='utf-8') as read_file:
      data = json.load(read_file)
    key = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in data:
      if item != "Эльфбар 1500":
        key.add(item)
    key.add("Отмена")
    sent = bot.send_message(message.chat.id, "Каталог", reply_markup=key)
    bot.register_next_step_handler(sent, show_categories)

  elif message.text == "Создать заказ":
    key = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    key.add("Отмена")
    sent = bot.send_message(message.chat.id, "Введите инфаормацию о заказе:\nФамилию и имя получателя\nНомер телефона получателя\nСпособ доставки(наложенный платёж или предоплата)\nПочту доставки(Новая почта, Justin, Укрпочта)\nГород\nОтделение почты\nУточнение к заказу, либо время оплаты(если требуется)\n\n5355280209854684 - ПУМБ(Для отправки предоплаты)",reply_markup=key)
    bot.register_next_step_handler(sent, save_date)

  elif message.text == "Отмена":
    bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=start_keyboard())

def save_date(message):
  if message.text != "Отмена":
    date = message.from_user.username + "\n" + message.text
    bot.send_message(654258355, date)
    print(message.from_user.username + " has added order")
    bot.send_message(message.chat.id, 'Заказ успешно сохранён, для подтверждения с вами свяжется менеджер',reply_markup=start_keyboard())

  else:
    bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=start_keyboard())

def show_categories(message):
  if message.text != "Отмена":
    with open("items.json", "r",encoding='utf-8') as read_file:
      data = json.load(read_file)    
    key = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for type in data[message.text]:
      if type != "Эльфбар 1500":
        key.add(type)
    key.add("Отмена")
    cat = message.text
    sent = bot.send_message(message.chat.id, "Выберите категорию", reply_markup=key)
    bot.register_next_step_handler(sent, show_item, cat)
    print(cat)

  else:
    bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=start_keyboard())

def show_item(message, cat):
  if message.text != "Отмена":
    with open("items.json", "r",encoding='utf-8') as read_file:
      data = json.load(read_file)    
    key = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for type in data[cat]:
      if type != "Эльфбар 1500":
        key.add(type)
    key.add("Отмена")
    data = data[cat][message.text]
    bot.send_message(message.chat.id, "Цена - " + data["price"] + "грн",reply_markup=key)
    if data["types"] != 0:
      for type in data["types"]:
        bot.send_message(message.chat.id, type)
    sent = bot.send_message(message.chat.id, data["describe"], )
    for photo in os.listdir(data["images"]):
      f = open(data["images"] + "/" + photo,"rb")
      bot.send_document(message.chat.id, f)
    print(message.from_user.username + " has looked " + message.text)
    bot.register_next_step_handler(sent, show_item,cat)
  else:
    bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=start_keyboard())
if __name__ == "__main__":
    bot.infinity_polling()
