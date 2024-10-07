from random import randrange

class Dice:
    @staticmethod
    def roll():
        while True:
            a, b = randrange(1,7), randrange(1,7)
            yield a+b, (a, b)
