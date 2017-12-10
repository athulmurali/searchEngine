from nltk import ngrams
import os

unigram = []
indexer = {}
tf = {}


def generate_index(files, gram):
    temp = gram
    for item in gram:
        if item in indexer:
            for one in indexer[item]:
                equal = 1
                if files == one[0]:
                    equal *= 0
                else:
                    equal *= 1
            if equal == 1:
                indexer[item] += [[files,counter(item,temp)]]
        else:
            indexer[item] = [[files,counter(item,temp)]]


def counter(term, grams):
    total = 0
    for items in grams:
        if term == items:
            total += 1
    return total


def index_creation(dir):
    global unigram, indexer
    indexer = {}
    for file in os.listdir(dir):
        if ".DS_Store" not in file:
            for item in ngrams((open(dir + file, 'r').read()).split(),1):
                unigram.append(item[0])
            generate_index(file, unigram)
            unigram = []
    return indexer
