# Hangman_game
bot: @PlayNewHangManBot
# Criteria
Основной функционал бота реализован в файле telegram_bot.py

Количество функций обработчиков: 10, все реализованы в telegram_bot.py

Инструкция для комнад реализована с помощью /help в файле telegram_bot.py (строчка 42)

Поясняющие комментарии есть к каждому файлу и функции

Рефакторинг кода есть (что бы это не значило)

Один запрос с Giphy реализован при победе в игре, бот отправляет случайную гифку. 
Реализовано в функции telegram_bot.py -> game_letters/game_word (строчки 196 и 219)

Два дополнительных запрса: 
1. В файле Scheduler есть запрос на гифку с хомяком, которая отпарвляется при напоминании (подробнее далее)
2. В файле create_dictionary.py реализован запрос на сайт со словами. Этот файл использовался для создания базы слов
для отгадывания, но чтобы не делать каждый раз запрос на сайт, все слова сохранены в файле dictionary_list. 

Кнопки с использованием inline клавиатуры реализованы для команд /play и /help в файле
telegram_bot.py -> start (строчка 35)

Рассылка реализована в файле telegram_bot.py (строчка 20) в отдельном потоке. 
В нем используется функция из файла Scheduler

Pep8 учтен
