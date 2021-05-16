import sys
import requests
from bs4 import BeautifulSoup

args = sys.argv
source_language = args[1]
target_language = args[2]
word = args[3]

class OnlineTranslator():
    languages = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french', '6': 'hebrew', '7': 'japanese',
                '8': 'dutch', '9': 'polish', '10': 'portuguese', '11': 'romanian', '12': 'russian', '13': 'turkish', '0': 'all'}
    def __init__(self):
        self.translate_from = None
        self.translate_to = None
        self.word = None


def request(translation):
    #connecting with the server

    link = f'https://context.reverso.net/translation/{translation.translate_from}-{translation.translate_to}/{translation.word}'
    try:
        r = requests.get(link,headers={'User-Agent': user_agent})
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        sys.exit()


    # processing the infotmation
    soup = BeautifulSoup(r.content, 'html.parser')

    a = soup.find_all('a', {"class":"translation"})
    no_context = [i.text.strip() for i in a[1:]]
    # print('\n'.join(no_context))
    try:
        no_context[0]
    except IndexError:
        print(f'Sorry, unable to find {translation.word}')
        sys.exit()
    else:
        print(f'\n{translation.translate_to.capitalize()} translations:')
        print(no_context[0])

    print(f'\n{translation.translate_to.capitalize()} Example:')

    examples = [e.text.strip() for e in soup.select('.example .text')]
    print(f'{examples[0]}\n{examples[1]}')
    # for i in range(0, len(examples), 2):
    #     print(examples[i] + '\n' + examples[i+1] + '\n')

    with open(f'{translation.word}.txt', 'a', encoding="utf-8") as file:
        file.write(f'{translation.translate_to.capitalize()} Translations:\n{no_context[0]}\n\n')
        file.write(f'{translation.translate_to.capitalize()} Example:\n{examples[0]}\n{examples[1]}\n\n\n')

def request_multy(native, to, word):
    try:
        r = requests.get(f'https://context.reverso.net/translation/{native}-{to}/{word}',headers={'User-Agent': user_agent})
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        sys.exit()

    soup = BeautifulSoup(r.content, 'html.parser')

    a = soup.find_all('a', {"class":"translation"})
    no_context = [i.text.strip() for i in a[1:]]
    examples = [e.text.strip() for e in soup.select('.example .text')]

    try:
        print(f'{to.capitalize()} Translations:\n{no_context[0]}\n')
        print(f'{to.capitalize()} Example:\n{examples[0]}\n{examples[1]}\n\n')
    except IndexError:
        print(f'Sorry, unable to find {word}')
        sys.exit()

    with open(f'{word}.txt', 'a', encoding="utf-8") as file:
        file.write(f'{to.capitalize()} Translations:\n{no_context[0]}\n\n')
        file.write(f'{to.capitalize()} Example:\n{examples[0]}\n{examples[1]}\n\n\n')

user_agent = 'Mozilla/5.0'
translation = OnlineTranslator()
translation.translate_from = source_language
translation.translate_to = target_language
translation.word = word
# checking for the languages

if list(translation.languages.values()).count(source_language) != 1:
    print(f"Sorry, the program doesn't support {source_language}")
    sys.exit()
if list(translation.languages.values()).count(target_language) != 1:
    print(f"Sorry, the program doesn't support {target_language}")
    sys.exit()

elif target_language != 'all':
    request(translation)
else:
    for k,v in translation.languages.items():
        if v == source_language:
            continue
        request_multy(source_language, v, word)
