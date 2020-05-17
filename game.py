
from player import Player
import random

# def less(a, b):
#     if(b == 1):
#         return True
#     else:
#         return a <= b

class Game():
    def __init__(self, player1='p1', player2='p2', viewer=None):
        self.p1 = Player(player1)
        self.p2 = Player(player2)
        self.v = viewer
        self.ready = False #whether the game is ready to play
        self.roll = False #whether rolled the dice
        self.z = False #include ones or not
        self.nz = False
        self.currV = 0
        self.currAmt = 3 #start with 3, but can have 2 if no ones
        self.currTurn = random.randint(0,1) # 0 or 1, if 0, player 1 first, else player 2 first
        self.opened = False
        self.winner = -1
    
    def yao(self):
        if not self.ready or self.roll: #done rolling or not ready
            return False
        self.p1.roll()
        self.p2.roll()
        self.roll = True
        return True
    
    def kai(self, val, amt):
        #when player opens, player = 0 or 1 for 1st or second player, based on currTurn
        if self.roll:
            if val == 0:
                self.winner = 1 - self.currTurn
            total = self.p1.amt[val-1] + self.p2.amt[val-1]
            if not self.z:
                total += self.p1.amt[0] + self.p2.amt[0] #add 1's if flag false
            if total < amt:
                self.opened = True
                self.winner = self.currTurn
            else:
                self.opened = True
                self.winner = 1 - self.currTurn
        else:
            return
    
    def jiao(self, nv, namt):
        if self.roll:
            # if nz > self.z: #nz = True, z = False
            #     if namt < self.currAmt - 1:
            #         return False
            # elif nz < self.z:
            #     if namt < self.currAmt + 2 or nv == 1:
            #         return False
            # else:
            #     if namt < self.currAmt or (namt == self.currAmt and less(nv, self.currV)):
            #         return False
            #     if not nz and nv == 1:
            #         return False
            self.z = self.nz
            self.currv = nv
            self.currAmt = namt
            self.currTurn = 1 - self.currTurn
            return True
        else:
            return False

    def reset(self):
        #if currPlayer = 0, player 1 wins, if currPlayer = 1, player 2 wins
        self.currTurn = 1-self.winner #losers go first next time
        self.currV = 0
        self.currAmt = 2
        self.roll = False
        self.winner = -1
        self.z = False
        self.nz = False
        self.opened = False