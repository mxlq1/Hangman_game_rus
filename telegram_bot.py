import telebot
import threading
from telebot import types
from User import User, user_identification
from bot_functions import guess_word, panel_to_string, make_panel, get_random_gif, get_hamster_gif
from random import choice
from Scheduler import send_reminder_to_play

with open("bot_key.txt") as file:
    """
    Для сохранности, ключ бота хранится в файле, 
    который не выкладывается в открытый доступ
    """
    bot = telebot.TeleBot(file.readline())

"""Словарь, в котором храянтся пользователи. Реализован как chat_id: class User()"""
user_dictionary = dict()

"""Здесь реализована рассылка в отдельном потоке как на лекции. Функция реализовна в файле Scheduler.py"""
thread_scheduler = threading.Thread(target=send_reminder_to_play, args=(bot, user_dictionary))
thread_scheduler.start()

@bot.message_handler(commands=['start'])
def start(message):
    """
    Открывающее сообщение. Оно реализовывает кнопки и приветствует игрока
    Также, в каждой функции обработчике реализован поиск игрока в списке игроков.
    В каждой функции игрок называется player. player - это объект класса User,
    который нужен для избежания коллизий между двумя игроками, использующими бота
    одновременно.
    """
    player = user_identification(message, user_dictionary)
    player.flag = False

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/play")
    btn2 = types.KeyboardButton("/help")
    markup.add(btn1, btn2)
    bot.send_message(player.user_id, "Добро пожаловать в игру виселица", reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    """
    Здесь приведен список команд, доступных пользователю и пояснения к ним
    """
    player = user_identification(message, user_dictionary)
    player.flag = False
    bot.send_message(player.user_id, f"Списиок команд:\n"
                                     "/play - начать игру в виселицу\n"
                                     "/help - запросить список команд\n"
                                     "/subscription - включить/выключить рассылку, по умолчанию включена\n"
                                     "/rules - правила игры\n"
                                     "/examples - примеры слов, которые могут быть загаданы\n"
                                     "/register - зарегестрироваться (необязательно)\n"
                                     "/setname - установить себе имя. Имя будет выбрано автоматически из "
                                     "секретного списка"
                     )


@bot.message_handler(commands=['subscription'])
def subscription_switch(message):
    """
    Смена подписки. Меняет поле класса User
    """
    player = user_identification(message, user_dictionary)
    player.flag = False
    player.subscription = not player.subscription
    if player.subscription:
        bot.send_message(player.user_id, "Подписка активна")
    else:
        bot.send_message(player.user_id, "Подписка неактивна")


@bot.message_handler(commands=['rules'])
def rules(message):
    """
    Отправляет правила игры
    """

    player = user_identification(message, user_dictionary)
    player.flag = False

    bot.send_message(player.user_id, "Виселица - игра, где я загадываю слово, а Вы пытаетесь его отгадать.")
    bot.send_message(player.user_id, "Если названной буквы в слове нет, то человечек на виселице постепенно"
                                      " дорисовывается, иначе - открывается угаданная буква."
                                      " Если отгаданная буква в слове не одна, то открываются сразу все эти буквы"
                     )
    bot.send_message(player.user_id, "Для начала игры напишите /play . Буквы можно угадывать по одной, а можно "
                                     "написать все слово целиком. За непраивльно угаданное слово или букву в обоих"
                                     "случаях рисуется одна конечность. Регистр не важен."
                    )


@bot.message_handler(commands=['examples'])
def examples(message):
    """
    Примеры первых нескольких слов, которые могут
    быть загаданы
    """
    player = user_identification(message, user_dictionary)
    player.flag = False
    bot.send_message(player.user_id, f"Слово, которое я могу загадать:\n {guess_word()}")


@bot.message_handler(commands=['register'])
def register(message):
    """
    Заново регистрирует игрока
    """
    player = user_identification(message, user_dictionary)
    player.flag = False
    bot.send_message(player.user_id, "Вы успешно зарегестрированы. Начать игру: /play")


@bot.message_handler(commands=['setname'])
def setname(message):
    """
    Здесь можно установить имя, которое будет показано при
    отгадовании слова (имена - отсылка на MIB)
    """
    player = user_identification(message, user_dictionary)
    player.flag = False

    name = choice(["K", "J", "L"])
    player.username = name
    bot.send_message(player.user_id, f"Вам присвоено кодовое имя: {name}")
    user_dictionary[message.chat.id] = player



@bot.message_handler(commands=['play'])
def play(message):
    """
    Здесь происходит начало игры. Классу игрока присваиваются
    ключевы занчения. Подробнее о полях можно прочитать в файле User.py
    Также, здесь и в последующих функциях реализованы картинкы,
    которые показывают сколько было сделано ошибок, дорисовывя человеска
    """
    player = user_identification(message, user_dictionary)
    player.word = guess_word()
    player.guess_panel = make_panel(player.word)
    player.mistake_counter = 0
    player.flag = True

    bot.send_message(player.user_id, "Сейчас я загадаю слово.")
    bot.send_message(player.user_id, panel_to_string(player.guess_panel))

    with open("hangman_images/hangman_0.png", "rb") as photo:
        bot.send_photo(player.user_id, photo)

    print(player.word)


@bot.message_handler(func=lambda msg: len(msg.text) == 1)
def game_letters(message):
    """
    Эта функция обрабатывает буквы, которые пытается отгадать пользователь
    """
    current_player = user_identification(message, user_dictionary)
    letter = message.text.lower()

    if not current_player.flag:
        bot.send_message(current_player.user_id, "Чтобы начать игру заново, напишите: /play")
    else:
        if len(letter) > 1:
            bot.send_message(current_player.user_id, "Можно угадать только одну букву")

        else:
            if letter not in current_player.word:
                bot.send_message(current_player.user_id, "Такой буквы нет")
                current_player.mistake_counter += 1

                with open("hangman_images/hangman_" + str(current_player.mistake_counter) + ".png", "rb") as photo:
                    bot.send_photo(current_player.user_id, photo)

                if current_player.mistake_counter >= 6:
                    bot.send_message(current_player.user_id, "Вы проиграли")
                    bot.send_message(current_player.user_id, f'Я загадал слово: {current_player.word}')
                    bot.send_message(current_player.user_id, "Чтобы начать игру заново, напишите: /play")
                    current_player.flag = False
                else:
                    bot.send_message(current_player.user_id, panel_to_string(current_player.guess_panel))

            else:
                for i in range(len(current_player.word)):
                    if current_player.word[i] == letter:
                        current_player.guess_panel[i] = current_player.word[i]
                bot.send_message(current_player.user_id, panel_to_string(current_player.guess_panel))

            if "_ " not in current_player.guess_panel:
                if not current_player.username:
                    bot.send_message(current_player.user_id, "Поздравляю, Вы победили!")
                else:
                    bot.send_message(current_player.user_id, f"Поздравляю, {current_player.username}, Вы победили!")
                link = get_random_gif()
                bot.send_animation(current_player.user_id, link)
                bot.send_message(current_player.user_id, "Чтобы начать игру заново, напишите: /play")
                current_player.flag = False


@bot.message_handler(func=lambda msg: len(msg.text) > 1)
def game_word(message):
    """
    Здесь реализована возможность отгадать слово целиком, если
    игрок уже может догодаться, что загадал бот
    """
    current_player = user_identification(message, user_dictionary)
    word = message.text.lower()

    if not current_player.flag:
        bot.send_message(current_player.user_id, "Чтобы начать игру заново, напишите: /play")
    else:
        if word == current_player.word:
            if not current_player.username:
                bot.send_message(current_player.user_id, "Поздравляю, Вы победили!")
            else:
                bot.send_message(current_player.user_id, f"Поздравляю, {current_player.username}, Вы победили!")
            link = get_random_gif()
            bot.send_animation(current_player.user_id, link)
            bot.send_message(current_player.user_id, "Чтобы начать игру заново, напишите: /play")
            current_player.flag = False
        else:
            bot.send_message(current_player.user_id, "Я загадал не это слово")
            current_player.mistake_counter += 1

            with open("hangman_images/hangman_" + str(current_player.mistake_counter) + ".png", "rb") as photo:
                bot.send_photo(current_player.user_id, photo)

            if current_player.mistake_counter >= 6:
                bot.send_message(current_player.user_id, "Вы проиграли")
                bot.send_message(current_player.user_id, f'Я загадал слово: {current_player.word}')
                bot.send_message(current_player.user_id, "Чтобы начать игру заново, напишите: /play")
                current_player.flag = False
            else:
                bot.send_message(current_player.user_id, panel_to_string(current_player.guess_panel))


bot.polling(none_stop=True)
