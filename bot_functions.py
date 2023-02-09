from random import randint
from dictionary_list import dict_list


def guess_word():
    word = dict_list[randint(0, len(dict_list) - 1)]
    return word


def panel_to_string(panel):
    line = ""
    for i in panel:
        line += i

    return line

