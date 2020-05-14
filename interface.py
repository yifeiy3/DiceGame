import pygame
from network import Network
import pickle
from game import Game

pygame.init()
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
font = pygame.font.SysFont('comicsans', 40)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

def less(a, b):
    if(b == 1):
        return True
    else:
        return a <= b

def checkValidMove(game, nv, namt, nz):
    if nz > game.z: #nz = True, z = False
        if namt < game.currAmt - 1:
            return False
    elif nz < game.z:
        if namt < game.currAmt + 2 or nv == 1:
            return False
    else:
        if namt < game.currAmt or (namt == game.currAmt and less(nv, game.currV)):
            return False
        if not nz and nv == 1:
            return False
    return True

def getPname(game, p):
    if p == 0:
        player = game.p1.name
    elif p == 1:
        player = game.p2.name
    else:
        player = "Spectator"
    return player

class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    
    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class InputBox():
    def __init__(self, x, y, w, h, text=''):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = COLOR_INACTIVE
            self.text = text
            self.txt_surface = font.render(text, True, self.color)
            self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

rollbtn = Button((128, 128, 128), 325, 325, 50, 50, "Roll")
zButton = [Button((128, 128, 128), 550, 200, 50, 100, "Zhai"), Button((128, 128, 128), 550, 300, 50, 100, "Fei")]
AButton = [Button((255, 0, 0), 625, 200, 50, 100, "Open"), Button((255, 0, 0), 625, 300, 50, 100, "Call")]

callInput = [InputBox(400, 300, 50, 100), InputBox(400, 500, 50, 100)]

def redrawWindow(game, p):
    win.fill((255,255,255)) #white bg
    player = getPname(game, p)
    usernm = font.render("You are player: {0}".format(player), 1, (0,0,0), True)
    win.blit(usernm, (60, 100))

    if not game.ready:
        text = font.render("Waiting for players", 1, (0,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    elif not game.roll:
        if game.currTurn == p:
            text1 = font.render("Roll the dice?", 1, (0,0,0), True)
            rollbtn.draw(win)
        else:
            text1 = font.render("Waiting for player {0} to roll".format(player), 1, (0,0,0), True)
        win.blit(text1, (100, 200))
    else:
        #TODO: draw the dice, somehow..
        info = font.render("Current amt: {0}, val: {1}, zhai? :{2}".format(game.currAmt, game.currV, game.z), 1, (0,0,0), True)
        win.blit(info, (50, 50))
        if game.currTurn == p:
            for i in range(2):
                zButton[i].draw(win)
                AButton[i].draw(win)
                callInput[i].draw(win)
            t1 = font.render("Number?", 1, (0, 0, 0), True)
            t2 = font.render("Val?", 1, (0,0,0), True)
            win.blit(t1, (350, 320))
            win.blit(t2, (350, 520))
        else:
            t1 = font.render("Waiting for the other player to perform action", 1, (0,0,0), True)
            win.blit(t1, (350, 100))

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getPlayer())
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("couldnt get game")
            break
        
        if game.opened:
            if game.winner == player:
                ttext = font.render("You Won!", 1, (255, 0, 0), True)
            elif player == 2:
                winner = getPname(game, game.winner)
                ttext = font.render("Winner is: {0}".format(winner), 1, (255, 0, 0), True)
            else:
                ttext = font.render("Sorry, you lost.", 1, (0, 0, 255), True)
            win.blit(ttext, (100, 100))
            p1 = getPname(game, 0)
            p2 = getPname(game, 1)
            tt1 = font.render(p1 + " has: ", 1, (255, 255, 255), True)
            #TODO: draw dice here
            tt2 = font.render(p2 + " has: ", 1, (255, 255, 255), True)
            #TODO: draw dice here
            win.blit(tt1, (150, 100))
            win.blit(tt2, (300, 100))
            res = font.render("Opened under condition: Amt: {0}, Val: {1}: Zhai?: {2}".format(game.currAmt, game.currV, game.z), 1, (255, 255, 255), True)
            win.blit(res, (500, 100))
            pygame.display.update()
            pygame.time.delay(5000) #show the screen for 5 seconds
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player == game.currTurn:
                    pos = pygame.mouse.get_pos()
                    if not game.roll:
                        if rollbtn.isOver(pos):
                            n.send("start")
                    else:
                        if AButton[0].isOver(pos):
                            n.send("kai")
                        else:
                            zflag = False
                            if zButton[0].isOver(pos):
                                zflag = True
                            elif AButton[1].isOver(pos):
                                #number, value, zhai or not to play
                                if checkValidMove(game, int(callInput[1].text), int(callInput[0].text), zflag):
                                    data = callInput[0].text + "," + callInput[1].text + "," + str(zflag)
                                    n.send(data)
                                else:
                                    txt = font.render("Invalid Move, check the current called amount and value", 1, (255,0,0), True)
                                    win.blit(txt, (50, 100))
        redrawWindow(game, player)
    
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()