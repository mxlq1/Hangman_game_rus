import requests
from random import randint
from dictionary_list import dict_list


def guess_word():
    """
    Эта функция загадывает слово из списка.
    Реализация старая и неэффективная, лучше использовать
    random.choice(), но я оставил ее для демостранции возможных улучшений
    """
    word = dict_list[randint(0, len(dict_list) - 1)]
    return word


def panel_to_string(panel):
    """
    Эта функция нужна для певращения
    загадывающей панели в слово (превычный вид)
    """
    line = ""
    for i in panel:
        line += i

    return line


def make_panel(word):
    """
    Функция для создания словарной панели
    """
    panel = ["_ "] * len(word)
    return panel


def get_random_gif():
    """
    Функция, которая получает одну случайную гифку.
    Взята из лекции
    """
    token = "gOpoqHc6ki4dLxFmFFB7VzMurfe8jg2O"
    url = "http://api.giphy.com/v1/gifs/random"

    param = {
        "api_key": token,
        "rating": "g"
    }

    result = requests.get(url, params=param)
    result_dict = result.json()

    link_origin = result_dict["data"]["images"]["original"]["url"]

    return link_origin


def get_hamster_gif():
    """
    Эта функция достает гифку с хомяком.
    Она нужна в функции напоминания Scheduler.py
    """
    token = "gOpoqHc6ki4dLxFmFFB7VzMurfe8jg2O"
    url = "http://api.giphy.com/v1/gifs/IccxLhyz1IjswrjLOl"

    param = {
        "api_key": token,
        "rating": "g"
    }

    result = requests.get(url, params=param)
    result_dict = result.json()

    link_origin = result_dict["data"]["images"]["original"]["url"]

    return link_origin
