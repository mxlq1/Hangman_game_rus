from bot_functions import guess_word


class User:

    def __init__(self, user_id):
        self.user_id = user_id
        self.flag = True
        self.mistake_counter = 0
        self.word = guess_word()
        self.guess_panel = ["_ "] * len(self.word)

