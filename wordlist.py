import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.wordunscrambler.net/word-list/wordle-word-list")

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    a_tags = soup.find_all('a', href=True)
    words = []
    for a_tag in a_tags:
        href = a_tag['href']
        if '/unscramble/' in href:
            word = href.split('/unscramble/')[1]
            words.append(word)

