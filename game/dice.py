from random import randrange

class Dice:
    @staticmethod
    def roll():
        while True:
            a, b = randrange(1,7), randrange(1,7)
            # yield 10, (5, 5)
            yield a+b, (a, b)
