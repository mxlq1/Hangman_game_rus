import telebot
from bot_functions import guess_word, panel_to_string
with open("bot_key.txt") as file:
    bot = telebot.TeleBot(file.readline())
word = ""
guess_panel = []
mistake_counter = 0
flag = False             # flag нужен, чтобы отслеживать конец и начало игры


@bot.message_handler(commands=['start'])
def start(message):
    global word
    global guess_panel
    global flag
    global mistake_counter
    flag = True
    mistake_counter = 0

    bot.send_message(message.chat.id, "Сейчас я загадаю слово.")
    word = guess_word()
    guess_panel = ["_ "] * len(word)
    bot.send_message(message.chat.id, panel_to_string(guess_panel))
    with open("hangman_images/hangman_0.png", "rb") as photo:
        bot.send_photo(message.chat.id, photo)
    print(word)


@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_message(message.chat.id, "Виселица - игра, где я загадываю слово, а Вы пытаетесь его отгадать.")
    bot.send_message(message.chat.id, "Если названной буквы в слове нет, то человечек на виселице постепенно"
                                      " дорисовывается, иначе - открывается угаданная буква."
                                      " Если отгаданная буква в слове не одна, то открываются сразу все эти буквы")
    bot.send_message(message.chat.id, "Для начала игры напишите /start . Буквы можно угадывать только по одной."
                                      " Регистр не важен.")



@bot.message_handler()
def game(letter):
    global mistake_counter
    global flag
    chat_id = letter.chat.id
    letter = letter.text.lower()

    if not flag:
        bot.send_message(chat_id, "Чтобы начать игру заново, напишите: /start")
    else:
        if len(letter) > 1:
            bot.send_message(chat_id, "Можно угадать только одну букву")

        else:
            if letter not in word:
                bot.send_message(chat_id, "Такой буквы нет")
                mistake_counter += 1

                with open("hangman_images/hangman_" + str(mistake_counter) + ".png", "rb") as photo:
                    bot.send_photo(chat_id, photo)

                if mistake_counter >= 6:
                    bot.send_message(chat_id, "Вы проиграли")
                    bot.send_message(chat_id, f'Я загадал слово: {word}')
                    flag = False
                else:
                    bot.send_message(chat_id, panel_to_string(guess_panel))

            else:
                for i in range(len(word)):
                    if word[i] == letter:
                        guess_panel[i] = word[i]
                bot.send_message(chat_id, panel_to_string(guess_panel))

            if "_ " not in guess_panel:
                bot.send_message(chat_id, "Поздравляю, Вы победили!")
                flag = False


bot.polling(none_stop=True)


# надо сделать:

# 3. список использанных букв
# 5. добавить в хендлер /help

