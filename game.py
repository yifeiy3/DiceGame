
from player import Player

class Game():
    def __init__(self, player1, player2, viewer, curr):
        self.p1 = player1
        self.p2 = player2
        self.v = viewer
        self.z = False #include ones or not
        self.currV = 0
        self.currAmt = 2 #start with 3, but can have 2 if no ones
        self.currTurn = curr # 0 or 1, if 0, player 1 first, else player 2 first
    
    def checksum(self, val, amt):
        #when player opens, player = 0 or 1 for 1st or second player, based on currTurn
        total = self.p1.amt[val-1] + self.p2.amt[val-1]
        if not self.z:
            total += self.p1.amt[0] + self.p2.amt[0] #add 1's if flag false
        if total < amt:
            self.win(self.currTurn)
        else:
            self.win(1-self.currTurn)
    
    def win(self, currPlayer):
        #if currPlayer = 0, player 1 wins, if currPlayer = 1, player 2 wins

        pass