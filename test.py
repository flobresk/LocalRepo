from minisom import MiniSom
import numpy as np
import re


ILOSC_HASEL = 100000

def get_alphabet() -> dict:
    index = 0
    alphabet = dict()

    characters = list()
    characters.append(ord(' '))
    # characters.extend(list(range(ord('0'), ord('9'))))
    # characters.extend(list(range(ord('A'), ord('Z'))))
    characters.extend(list(range(ord('a'), ord('z') + 1)))
    for char in characters:
        alphabet[chr(char)] = index
        index += 1
    #print(str(len(alphabet)) + "znakow")
    return alphabet

def myencode(word: str, alphabet: dict) -> np.array:
    _matrix = np.zeros((len(alphabet)* 64), dtype=np.int32)
    index = 0
    for char in word[:64]:
        _matrix[alphabet[char]+index*27] = 1
        index += 1
    return _matrix

def changeaLittle(row):
    randomLetter = random.choice(string.ascii_letters)
    randomIndex = randint(1, len(row) - 1)
    noiseWord = row[:randomIndex] + randomLetter + row[randomIndex + 1:]
    return str(noiseWord).lower()

import random
import string
from random import randint

def myload() -> (np.array, np.array):
    _labels = list()
    _data = np.array
    _clear_data = list()
    alphabet = get_alphabet()
    with open('Labels231.txt', 'r', encoding="utf8") as f:
        for row in f:
            _labels.append(re.sub("[^a-z ]", '', row))
    _labels = filter(lambda x: 64 > len(x) > 0, _labels)
    _data = list()
    for row in list(_labels)[:ILOSC_HASEL]:
        _matrix = myencode(row.lower(), alphabet)
        _clear_data.append((_matrix))
        for i in range(1,10):
            randomLetter = random.choice(string.ascii_letters)
            if len(row)>1:
                randomIndex =  randint(1, len(row)-1)
            else:
                randomIndex=0
            noiseWord = row[:randomIndex] + randomLetter + row[randomIndex + 1:]
            matrixOfNewWord = myencode(noiseWord.lower(), alphabet)
            _data.append(matrixOfNewWord)

    _data.extend(_clear_data)
    _data = np.array(_data)

    return _data, np.array(_clear_data)

_labels = list()
data = np.array
alphabet = get_alphabet()
with open('Labels231.txt', 'r', encoding="utf8") as f:
    for row in f:
        _labels.append(re.sub("[^a-z ]", '', row))
_labels = _labels[:ILOSC_HASEL]
full_data, clear_data = myload()

som = MiniSom(20, 2, 27*64, sigma=0.000001, learning_rate=0.3 )
print("Training...")
som.random_weights_init(full_data)
som.train_batch(full_data, 500)

print("...ready!")

le=list()
nois = list()
f = open('workfile', 'w')
alphabet = get_alphabet()
for row in list(_labels)[:ILOSC_HASEL]:
    res = myencode(row.lower(),alphabet)
    le.append(res)
    if (len(row)>1):
        res2 = myencode(changeaLittle(row.lower()),alphabet)
    nois.append(res2)

Mapped=list()
for row in le:
    winner = som.winner(row)
    Mapped.append(winner)

Mapped2 = list()
for row2 in nois:
    winner2 = som.winner(row2)
    Mapped2.append(winner2)
sum1=0
correct=0
w, h = 2, 20;
Matrix = [[0 for x in range(w)] for y in range(h)]
for i in range (0,len(_labels)):
    temp = str(list(Mapped[i]))
    f.write(_labels[i] + "; " + temp + "; "+str(list(Mapped2[i])) + "\r\n")
    sum1+=1
    Matrix[Mapped[i][0]][Mapped[i][1]]+=1
    if temp == str(list(Mapped2[i])):
        correct+=1
print(str(correct) + " / "+ str(sum1))
for i in range(0,20):
    print(str(Matrix[i][0]))
    print(str(Matrix[i][1]))

f.close()