import requests
from bs4 import BeautifulSoup as BS

"""
Это отдельная программа, которая использовалась
для создания списка слов. Сейчас она не используется для
улучшения эффективности
"""
r = requests.get("https://klavogonki.ru/vocs/559/")
html = BS(r.text, 'html.parser')

words = html.find_all("td", class_='text')

with open("dictionary.txt", "w") as f:
    for word in words:
        f.write(str(word.text) + "\n")
