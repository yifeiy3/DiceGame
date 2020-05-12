import random

class Player():
    def __init__(self, name):
        self.name = name
        self.diceroll = []
        self.amt = [0, 0, 0, 0, 0, 0] #1-6

    def roll(self):
        for i in range(6):
            r = random.randrange(1, 6)
            self.amt[r-1] += 1
            self.diceroll.append(r)
        self.checkbz()
    
    def checkbz(self):
        ones = self.amt[0]
        if ones == 5:
            self.amt[0] += 2
            return
        for i in range(1, 6):
            if self.amt[i] == 5:
                self.amt[i] += 2 #pure bz
                break
            elif ones + self.amt[i] == 5:
                self.amt[0] += 1 #not pure bz
                break
            

            
    
