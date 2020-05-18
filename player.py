import random

class Player():
    def __init__(self, name):
        self.name = name
        self.diceroll = []
        self.amt = [0, 0, 0, 0, 0, 0] #1-6

    def rename(self, name):
        self.name = name
    
    def roll(self):
        self.diceroll = []
        self.amt = [0, 0, 0, 0, 0, 0]
        for i in range(6):
            r = random.randint(1, 6)
            self.amt[r-1] += 1
            self.diceroll.append(r)
        while(self.checkreroll()):
            self.roll()
        self.checkbz()

    def checkreroll(self): #consecutive dice we reroll
        for i in range(6):
            if self.amt[i-1] > 1:
                return False
        return True

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
            

            
    
