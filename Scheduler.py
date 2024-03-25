import schedule
import time
from bot_functions import get_hamster_gif

"""
Здесь реализована напоминалка как в лекции.
Она отправляет гифку с хомяком в 19:00 и предлагает поиграть.
"""


def send_reminder_to_play(bot, dictionary):
    """Планировщик для отправки сообщений по времени"""
    def send_gif():
        """Функция для отправки сообщения"""

        for client_id in dictionary.keys():
            player = dictionary[client_id]
            if player.subscription:
                bot.send_message(client_id, "Как насчет поиграть?")
                bot.send_animation(client_id, get_hamster_gif())

    schedule.every().day.at("19:00").do(send_gif)

    while True:
        schedule.run_pending()
        time.sleep(1)
