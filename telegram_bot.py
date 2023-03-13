import telebot
from User import User
from bot_functions import guess_word, panel_to_string

with open("bot_key.txt") as file:
    bot = telebot.TeleBot(file.readline())

user_dictionary = dict()

@bot.message_handler(commands=['start'])
def start(message):

    person = User(message.chat.id)
    user_dictionary[message.chat.id] = person
    bot.send_message(person.user_id, "Сейчас я загадаю слово.")
    bot.send_message(person.user_id, panel_to_string(person.guess_panel))

    with open("hangman_images/hangman_0.png", "rb") as photo:
        bot.send_photo(person.user_id, photo)

    print(person.word)


@bot.message_handler(commands=['help'])
def bot_help(message):

    person = User(message.chat.id)
    user_dictionary[message.chat.id] = person
    person.flag = False

    bot.send_message(person.user_id, "Виселица - игра, где я загадываю слово, а Вы пытаетесь его отгадать.")
    bot.send_message(person.user_id, "Если названной буквы в слове нет, то человечек на виселице постепенно"
                                      " дорисовывается, иначе - открывается угаданная буква."
                                      " Если отгаданная буква в слове не одна, то открываются сразу все эти буквы")
    bot.send_message(person.user_id, "Для начала игры напишите /start . Буквы можно угадывать только по одной."
                                      " Регистр не важен.")



@bot.message_handler()
def game(letter):

    current_player = user_dictionary[letter.chat.id] # связываем переменную и класс игрока
    letter = letter.text.lower()

    if not current_player.flag:
        bot.send_message(current_player.user_id, "Чтобы начать игру заново, напишите: /start")
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
                    bot.send_message(current_player.user_id, "Чтобы начать игру заново, напишите: /start")
                    current_player.flag = False
                else:
                    bot.send_message(current_player.user_id, panel_to_string(current_player.guess_panel))

            else:
                for i in range(len(current_player.word)):
                    if current_player.word[i] == letter:
                        current_player.guess_panel[i] = current_player.word[i]
                bot.send_message(current_player.user_id, panel_to_string(current_player.guess_panel))

            if "_ " not in current_player.guess_panel:
                bot.send_message(current_player.user_id, "Поздравляю, Вы победили!")
                bot.send_message(current_player.user_id, "Чтобы начать игру заново, напишите: /start")
                current_player.flag = False


bot.polling(none_stop=True)


# надо сделать:
# 1. список использанных букв
# 2. добавить предложение начать игру заново после выигрыша/проигрыша
# 3. возможно, добавить угадывание слова целиком


