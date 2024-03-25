
class User:

    def __init__(self, user_id):
        """
        user_id: содержит id данного пользователя

        flag: булевая переменная, показывающая статус игры.
        Если во время отгадывания игрок вызовет лююую другую команду или игра будет завершена,
        то flag становится False.

        subscription: булевая переменная наличия подписки

        mistake_counter: количество ошибок данного игрока в отдлеьной игре

        word: загаданное слово. Назначается в функции /game

        guess_panel: загадывающая анель нужна для вывода отгаданных и скрытых букв

        username: имя пользователя, назначается командой /setname
        """
        self.user_id = user_id
        self.flag = True
        self.subscription = True
        self.mistake_counter = 0
        self.word = None
        self.guess_panel = None
        self.username = None


def user_identification(message, dictionary):
    """
    Проверяет наличие игрока в списке и возвращает экземпляр класса User
    """
    if message.chat.id not in dictionary:
        person = User(message.chat.id)
        dictionary[message.chat.id] = person
        print("not found")

    user = dictionary[message.chat.id]
    return user
