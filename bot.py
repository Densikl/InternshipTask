import telebot
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import *


BOT_TOKEN = 'YOUR_TOKEN_HERE'
bot = telebot.TeleBot(BOT_TOKEN)


class BudgetItem:
    """item in budget table class"""

    def __init__(self, userId, isIncome=True, category='', amount=0, description='', date=0):
        self.userId = userId
        self.isIncome = isIncome
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date

    def add(self):
        addData(self.userId, self.category, self.amount if self.isIncome else self.amount * -1, self.date, self.description)


class Category:
    """class for category item"""

    def __init__(self, userId, name):
        self.userId = userId
        self.name = name

    def add(self):
        addCategory(self.userId, self.name)


def addButtons(options):
    return [KeyboardButton(option) for option in options]


def createDefaultKeyboard():
    defaultOptions = ['Добавить расход', 
                    'Добавить доход',
                    'Посмотреть бюджет',
                    'Показать баланс',
                    'Добавить категорию',
                    'Удалить статью бюджета']
    markup = ReplyKeyboardMarkup(True)
    markup.add(*addButtons(defaultOptions), row_width=1)

    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Что вы хотите сделать:', reply_markup=createDefaultKeyboard())


@bot.message_handler(func = lambda m: True)
def answer(message):
    global element
    element = BudgetItem(message.chat.id)

    if message.text == 'Добавить доход':
        msg = bot.reply_to(message, 'Отправьте значение дохода:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, receiveAmount)
    
    elif message.text == 'Добавить расход':
        element.isIncome = False
        msg = bot.reply_to(message, 'Отправьте значение расхода:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, receiveAmount)
    
    elif message.text == 'Показать баланс':
        bot.reply_to(message, f'Ваш баланс: {getBalance(message.chat.id)}')

    elif message.text == 'Добавить категорию':
        msg = bot.reply_to(message, 'Введите название категории:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, getCategoryName)
    
    elif message.text == 'Посмотреть бюджет':
        markup = ReplyKeyboardMarkup(True)
        options = ['День', 'Неделя', 'Месяц', 'Квартал', 'Год']
        markup.add(*addButtons(options), row_width=2)
        msg = bot.reply_to(message, 'Выберите интервал:', reply_markup=markup)
        bot.register_next_step_handler(msg, getInterval)
    
    elif message.text == 'Удалить статью бюджета':
        msg = bot.reply_to(message, 'Напишите id статьи:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, deleteBudgetItem)

    else:
        bot.reply_to(message, 'Попробуйте ещё раз')


def receiveAmount(message):
    try:
        element.amount = float(message.text) * 100 # storing amount in cents 
        markup = ReplyKeyboardMarkup(True)
        options = [row[2] for row in getCategories(message.chat.id)]
        markup.add(*addButtons(options), row_width=2)
        msg = bot.reply_to(message, 'Выберите категорию:', reply_markup=markup)
        bot.register_next_step_handler(msg, getCategory)
    except ValueError:
        msg = bot.reply_to(message, 'Кажется, вы ввели что-то не то', reply_markup=createDefaultKeyboard())
        print(message.text)
        # bot.register_next_step_handler(msg, answer)


def getCategory(message):
    element.category = message.text # changing global variable
    msg = bot.reply_to(message, 'Введите описание:', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, getDescription)


def getDescription(message):
    element.description = message.text # changing global variable
    element.date = int(time.time())
    element.add()
    bot.reply_to(message, 'Добавлено', reply_markup=createDefaultKeyboard())


def getCategoryName(message):
    category = Category(message.chat.id, message.text)
    category.add()
    bot.reply_to(message, 'Добавлено', reply_markup=createDefaultKeyboard())


def getBalance(id):
    rows = getAmountData(id)
    balance = 0
    for row in rows:
        balance += row
    
    return 0 if not balance else balance / 100 # avoiding '0.0' balance


timeInSeconds = {
    'day': 86400,
    'week': 604800,
    'month': 2629746,
    'quarter': 7889238,
    'year': 31556952,
}

def getInterval(message):
    interval = 0
    if message.text == 'День':
        interval = timeInSeconds['day']
    elif message.text == 'Неделя':
        interval = timeInSeconds['week']
    elif message.text == 'Месяц':
        interval = timeInSeconds['month']
    elif message.text == 'Квартал':
        interval = timeInSeconds['quarter']
    elif message.text == 'Год':
        interval = timeInSeconds['year']
    else:
        bot.reply_to(message, 'Попробуйте ещё раз')

    data = getDataInInterval(message.chat.id, interval)
    answer = ''
    for row in data:
        answer += f'<b>id:</b> {row[0]}\n<b>категория:</b> {row[2]}\n<b>значение:</b> {row[3] / 100}\n<b>описание:</b> {row[4]}\n\n'

    bot.send_message(message.chat.id, answer, parse_mode='HTML', reply_markup=createDefaultKeyboard())
    

def deleteBudgetItem(message):
    try:
        id = int(message.text)
        deleteData(id)
        bot.reply_to(message, 'Трата успешно удалена', reply_markup=createDefaultKeyboard())
    except ValueError:
        bot.reply_to(message, 'Попробуйте ещё раз:', reply_markup=createDefaultKeyboard())

bot.polling()
