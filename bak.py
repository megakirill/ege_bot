import codecs
from random import choice
from inf import spare_mas, spare_mas_wrong, users

mas = []
file = codecs.open("wrongwords.txt", "r", "utf-8").readlines()


def createmas():
    mas = []
    for i in file:
        mas.append(i[:-2])
    return mas


def create_variant():
    variants = []
    for i in range(3):
        variants.append(choice(spare_mas_wrong))
    b = choice(spare_mas)
    for i in variants:
        if b.lower() == i.lower():
            return createmas()
    variants.append(b)
    a = set(variants)
    if len(variants) == len(a):
        return variants
    return create_variant()


class User(object):
    def __init__(self, id, name):
        self.record = 0
        self.now_variants = []
        self.ip = id
        self.name = name
        self.true_variant = ''
        self.count = 0
        self.count_games = 0
        self.right_choise = 0
        self.wrong_choise = 0

    def new_variants(self, variants):
        self.now_variants = variants
        self.find_true_word()

    def find_true_word(self):
        for i in self.now_variants:
            if i in spare_mas:
                self.true_variant = i

    def print_words(self):
        print(self.now_variants)
