import random

class Player():
    def __init__(self, name):
        self.name = name
        self.diceroll = []

    def roll(self):
        for i in range(6):
            r = random.randrange(1, 6)
            self.diceroll.append(r)
    
