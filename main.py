from bs4 import BeautifulSoup
from requests import get
import sys

before = sys.argv[1]
after = sys.argv[2]
word = sys.argv[3]

x = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french', '6': 'hebrew', '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese', '11': 'romanian', '12': 'russian', '13': 'turkish'}
reversed_x = dict((v, k) for k, v in x.items())
supported = list(x.values()) + ['all']

if before not in supported:
    print(f"Sorry, the program doesn't support {before}")
    exit()
if after not in supported:
    print(f"Sorry, the program doesn't support {after}")
    exit()
if after != 'all':
    l = after[0].upper() + after[1:]
    language = f'{before}-{after}'
    
    url = f'https://context.reverso.net/translation/{language}/{word}'
    response = get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    if response.status_code == 404:
        print(f'Sorry, unable to find {word}')
        exit()
    if response.status_code != 200:
        print('Something wrong with your internet connection')
        exit()
    soup = BeautifulSoup(response.text, 'html.parser')
    m = [char.text for char in soup.find_all('a', class_='translation')]
    print(l, 'Translations:')
    for c in m:
        if "'" in c:
            g = c.replace("'", "")
        else:
            g = c
        if "," in c:
            g = c.replace(",", "")
        else:
            if "'" in c:
                g = c.replace("'", "")
            else:
                g = c
        print(g.strip("\n"))
    print(l, 'Examples:')
    for c in [char.text for char in soup.find_all(class_='example')]:
        print(c.strip('\n'))
else:
    mp = ''
    before = reversed_x[before]
    for char in range(1, len(x) + 1):
        if x[str(char)] == x[before]:
            continue
        l = x[str(char)][0].upper() + x[str(char)][1:]
        language = f'{x[before]}-{x[str(char)]}'
        print(language)
        url = f'https://context.reverso.net/translation/{language}/{word}'
        response = get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        if response.status_code == 404:
            print(f'Sorry, unable to find {word}')
            exit()
        if response.status_code != 200:
            print('Something wrong with your internet connection')
            exit()
        soup = BeautifulSoup(response.text, 'html.parser')
        containment = [char.text for char in soup.find_all('a', class_='translation')][1]
        mp += l + ' Translations:\n'
        print(l, 'Translations:')

        mp += containment.strip('\n') + '\n'
        print(containment.strip('\n'))

        print(l, 'Examples:')
        mp += l + ' Examples:\n'
        containment = [char.text for char in soup.find_all(class_='example')][1]
        mp += containment.strip('\n') + '\n'
        print(containment.strip('\n'))
    with open(f'{word}.txt', 'w') as file:
        file.write(mp)