import telebot
from telebot import types
from bak import createmas, create_variant, User
from inf import spare_mas, users

bot = telebot.TeleBot('6775360728:AAE9zNChL9RIIR6qW74uVSYnYJ_MMgFIMT4')


@bot.message_handler(commands=['stop'])
def stop(message):
    a = telebot.types.ReplyKeyboardRemove()
    if users[message.chat.id].count == 0:
        bot.send_message(message.chat.id, f'Введите /practice, чтобы начать практику\n'
                                          f'Введите /help, чтобы узнать что умеет это бот', reply_markup=a)
    else:
        bot.send_message(message.chat.id, f'Введите /practice, чтобы начать практику\n'
                                          f'Введите /help, чтобы узнать что умеет это бот\n'
                                          f'вы решили {users[message.chat.id].count} подряд', reply_markup=a)
        users[message.chat.id].count = 0


@bot.message_handler(commands=['new_practice_menu'])
def new_function(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, f'Это новый режим тренировки! Здесь дается выбор из одного слова с разным ударением\n'
                                      f'Для этого режима доступна отдельная статистика /statistics_new'
                                      f'Чтобы начать нажмите /new_practice', reply_markup=a)

@bot.message_handler(commands=['new_practice'])
def new_practice(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)


@bot.message_handler(commands=['statistics'])
def statistic(message):
    a = telebot.types.ReplyKeyboardRemove()
    count_games = users[message.chat.id].count_games
    wrong_answers = users[message.chat.id].wrong_choise
    right_answers = users[message.chat.id].right_choise
    record = users[message.chat.id].record
    bot.send_message(message.chat.id, f'Ваша статистика:\n\n'
                                      f'Всего было {count_games} вопросов🤩\n\n'
                                      f'Верно ответили на {right_answers} вопросов\n\n'
                                      f'Неверно ответили на {wrong_answers} вопросов\n\n'
                                      f'Ваш рекорд {record}', reply_markup=a)


@bot.message_handler(commands=['start'])
def start(message):
    if users.get(message.chat.id) is None:
        users[message.chat.id] = User(message.chat.id, message.from_user.first_name)
    bot.send_message(message.chat.id, f'Введите /practice, чтобы начать практику\n'
                                      f'Введите /help, чтобы узнать что умеет это бот')


@bot.message_handler(commands=['practice'])
def questoin(message):
    words = create_variant()
    users[message.chat.id].new_variants(words)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton(words[0])
    btn2 = types.KeyboardButton(words[1])
    btn3 = types.KeyboardButton(words[2])
    btn4 = types.KeyboardButton(words[3])
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    bot.send_message(message.chat.id, 'Выберите слово с правильным ударением:', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'Это бот для удачной подготовки к 4 заданию ЕГЭ💩 по русскому языку\n\n'
                                      f'/practice - Начало тренировки\n'
                                      f'/stop - Прекращение тренировки\n'
                                      f'/statistics - Ваша персональная статистика🙈')


@bot.message_handler(content_types=['text'])
def on_click(message):
    users[message.chat.id].print_words()
    b = users[message.chat.id].now_variants
    if message.text in b:
        users[message.chat.id].count_games += 1
        if message.text in spare_mas:
            users[message.chat.id].right_choise += 1
            users[message.chat.id].count += 1
            bot.send_message(message.chat.id, f'✅Правильно! Если хотите закончить введите /stop.\n'
                                              f'Сейчас вы решили {users[message.chat.id].count} подряд')
            users[message.chat.id].new_variants([])
            questoin(message)
        else:
            users[message.chat.id].wrong_choise += 1
            a = telebot.types.ReplyKeyboardRemove()
            if users[message.chat.id].record < users[message.chat.id].count:
                users[message.chat.id].record = users[message.chat.id].count
            users[message.chat.id].new_variants([])
            bot.send_message(message.chat.id, f'❌Неверно! Ваш счет: {users[message.chat.id].count}\n'
                                              f'Попробуйте заново!\n'
                                              f'Если хотите закончить нажмите /stop', reply_markup=a)
            users[message.chat.id].count = 0
            questoin(message)
    else:
        a = telebot.types.ReplyKeyboardRemove()
        users[message.chat.id].count = 0
        users[message.chat.id].new_variants([])
        bot.send_message(message.chat.id,
                         'Вы ввели неправильное слово начните заново, чтобы начать заново, введите /practice',
                         reply_markup=a)


bot.polling(non_stop=True)
