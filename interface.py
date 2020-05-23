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
dimage = ["diceImage/d1.bmp", "diceImage/d2.bmp", "diceImage/d3.bmp", "diceImage/d4.bmp", "diceImage/d5.bmp", "diceImage/d6.bmp"]
limage = []
for it in dimage:
    image = pygame.image.load(it)
    limage.append(pygame.transform.scale(image, (50, 50)))

def less(a, b):
    if(b == 1):
        return True
    else:
        return a <= b

def drawDices(game, p, hoff, woff):
    if p == 0:
        pr = game.p1
    elif p == 1:
        pr = game.p2
    else:
        p1name = getPname(game, 0)
        p2name = getPname(game, 1)
        p1info = font.render("{0} has won: {1} times".format(p1name, game.wontally[0]), 1, (255, 0, 0), True)
        p2info = font.render("{0} has won: {1} times".format(p2name, game.wontally[1]), 1, (0, 0, 255), True)
        win.blit(p1info, (hoff, woff))
        win.blit(p2info, (hoff, woff + 70))
        return
    for i in range(len(pr.diceroll)):
        nbr = pr.diceroll[i]
        win.blit(limage[nbr-1], (hoff+i*70, woff))
    return
        
    
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
    print("this is a valid move with val: {0}, amt: {1}, z: {2}".format(nv, namt, nz))
    return True

def getPname(game, p):
    if p == 0:
        player = game.p1.name
    elif p == 1:
        player = game.p2.name
    elif p != -1:
        player = getPname(game, game.currTurn)
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
    
    def recolor(self, ncolor):
        self.color = ncolor

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
                self.renewText()
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
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
    
    def renewText(self):
        self.text = ''
        self.txt_surface = font.render(self.text, True, self.color)

rollbtn = Button((128, 128, 128), 325, 325, 50, 50, "Roll")
zButton = [Button((128, 128, 128), 200, 550, 100, 50, "Zhai"), Button((128, 128, 128), 350, 550, 100, 50, "Fei")]
AButton = [Button((255, 0, 0), 200, 625, 100, 50, "Open"), Button((255, 0, 0), 350, 625, 100, 50, "Call")]

callInput = [InputBox(200, 475, 100, 50), InputBox(350, 475, 100, 50)]

def redrawWindow(game, p):
    win.fill((255,255,255)) #white bg
    player = getPname(game, p)
    usernm = font.render("You are player: {0}".format(player), 1, (0,0,0), True)
    gid = font.render("Game Id: {0}".format(str(game.id)), 1, (0,0,0), True)
    win.blit(usernm, (60, 100))
    win.blit(gid, (530, 20))

    if not game.ready:
        text = font.render("Waiting for players", 1, (0,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    elif not game.roll:
        if game.currTurn == p:
            text1 = font.render("Roll the dice?", 1, (0,0,0), True)
            rollbtn.draw(win)
        else:
            text1 = font.render("Waiting for player {0} to roll".format(getPname(game, 1-p)), 1, (0,0,0), True)
        win.blit(text1, (100, 200))
    elif game.opened:
        if game.winner == p:
            ttext = font.render("You Won!", 1, (255, 0, 0), True)
        elif p == -1:
            winner = getPname(game, game.winner)
            ttext = font.render("Winner is: {0}".format(winner), 1, (0, 0, 0), True)
        else:
            ttext = font.render("Sorry, you lost.", 1, (0, 0, 255), True)
        win.blit(ttext, (100, 600))
        p1 = getPname(game, 0)
        p2 = getPname(game, 1)
        tt1 = font.render(p1 + " has: ", 1, (0, 0, 0), True)

        drawDices(game, 0, 100, 230)
        tt2 = font.render(p2 + " has: ", 1, (0, 0, 0), True)
        drawDices(game, 1, 100, 380)
        win.blit(tt1, (100, 170))
        win.blit(tt2, (100, 300))

        res1 = font.render("Opened under condition:", 1, (0, 0, 0), True)
        res2 = font.render("Amt: {0}, Val: {1}: Zhai?: {2}".format(game.currAmt, game.currV, game.z), 1, (0, 0, 0), True)
        win.blit(res1, (100, 500))
        win.blit(res2, (100, 550))
        pygame.display.update()
    else:
        info = font.render("Current amt: {0}, val: {1}, zhai? :{2}".format(game.currAmt, game.currV, game.z), 1, (0,0,0), True)
        win.blit(info, (50, 50))
        drawDices(game, p, 130, 230)

        if game.currTurn == p:
            for i in range(2):
                zButton[i].draw(win)
                AButton[i].draw(win)
                callInput[i].draw(win)
            t1 = font.render("Number?", 1, (0, 0, 0), True)
            t2 = font.render("Val?", 1, (0,0,0), True)
            win.blit(t1, (195, 440))
            win.blit(t2, (370, 440))
        else:
            t1 = font.render("Waiting for the other player to perform action", 1, (0,0,0), True)
            win.blit(t1, (50, 500))

    pygame.display.update()

def spectate_menuscreen(net):
    run = True
    clock = pygame.time.Clock()
    try:
        numgames = int(net.totalgames)
    except:
        return -1
    else:
        if numgames == 0:
            return -1
        numid = net.getId()
        gamebtns = [Button((255, 255, 255), 230, 200+i*70, 200, 50, "Game {0}".format(numid[i])) for i in range(numgames)]

        while run:
            clock.tick(60)
            win.fill((128, 128, 128))
            for btns in gamebtns:
                btns.draw(win)
            
            pygame.display.update()

            res = -1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(gamebtns)):
                        if gamebtns[i].isOver(event.pos):
                            res = i
                            break
                    run = False
        return numid[res]

def player_menuscreen(n):
    run = True
    clock = pygame.time.Clock()
    abutns = [Button((255, 255, 255), 230, 200, 200, 50, "New"), Button((255, 255, 255), 230, 300, 200, 50, "Join"),
    Button((255, 255, 255), 230, 400, 200, 50, "Back")]

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        for btns in abutns:
            btns.draw(win)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if abutns[0].isOver(event.pos):
                    return 0
                elif abutns[1].isOver(event.pos):
                    return 1
                elif abutns[2].isOver(event.pos):
                    return 2
    return 0

def main(username, viewer):
    run = True
    clock = pygame.time.Clock()

    n = Network(viewer)
    if not n.totalgames:
        exit() #if bad connection, exit
    gid = -1
    if not viewer:
        pr = player_menuscreen(n)
        if pr == 1:
            gid = spectate_menuscreen(n)
            if gid == -1:
                win.fill((128, 128, 128))
                fontt = pygame.font.SysFont("comicsans", 60)
                text = fontt.render("No games yet!", 1, (255,0,0))
                win.blit(text, (200,200))
                pygame.display.update()
                pygame.time.delay(2000)
                n.client.send(str.encode("reset"))
                menu_screen()
            try:
                player = int(n.getPlayer(int(gid), viewer))
            except:
                win.fill((128, 128, 128))
                fontt = pygame.font.SysFont("comicsans", 60)
                text = fontt.render("Room Full!", 1, (255,0,0))
                win.blit(text, (200,200))
                pygame.display.update()
                pygame.time.delay(2000)
                n.client.send(str.encode("reset"))
                menu_screen()
        elif pr == 2:
                win.fill((128, 128, 128))
                n.client.send(str.encode("reset"))
                menu_screen()
        else:
            gid = n.sendstr("new")
            if gid == "NAN":
                win.fill((128, 128, 128))
                text1 = font.render("The server has reached max games.", 1, (255,0,0))
                win.blit(text1, (100,200))
                text2 = font.render("Please wait.", 1, (255,0,0))
                win.blit(text2, (250,300))
                pygame.display.update()
                pygame.time.delay(2000)
                n.client.send(str.encode("reset"))
                menu_screen()
            player = 0
    else:
        gid = spectate_menuscreen(n)
        if gid == -1:
            win.fill((128, 128, 128))
            fontt = pygame.font.SysFont("comicsans", 60)
            text = fontt.render("No games yet!", 1, (255,0,0))
            win.blit(text, (200,200))
            pygame.display.update()
            pygame.time.delay(2000)
            n.client.send(str.encode("reset"))
            menu_screen()
        try:
            player = int(n.getPlayer(int(gid), viewer))
            print(player)
        except:
            win.fill((128, 128, 128))
            fontt = pygame.font.SysFont("comicsans", 60)
            text = fontt.render("No games yet!", 1, (255,0,0))
            win.blit(text, (200,200))
            pygame.display.update()
            pygame.time.delay(2000)
            n.sendstr("reset")
            menu_screen()

    zhai = False

    if username != '':
        try:
            game = n.send("u{0}".format(username))
        except:
            run = False
            print("couldnt get game!")
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("couldnt get game!")
            break
        if game.opened:
            redrawWindow(game, player)
            pygame.time.delay(7000) #show the screen for 7 seconds
            if player == 1:
                try:
                    zhai = False
                    for cii in callInput:
                        cii.renewText()
                    zButton[0].recolor((128, 128, 128))
                    zButton[1].recolor((128, 128, 128))
                    game = n.send("reset")
                except:
                    run = False
                    print("Couldn't get game!")
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            for ci in callInput:
                ci.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player == game.currTurn:
                    pos = pygame.mouse.get_pos()
                    if not game.roll:
                        if rollbtn.isOver(pos):
                            game = n.send("start")
                    else:
                        if AButton[0].isOver(pos):
                            game = n.send("kai")
                        else:
                            if zButton[0].isOver(pos):
                                zhai = True
                                zButton[0].recolor((0, 255, 0))
                                zButton[1].recolor((128, 128, 128))

                            elif zButton[1].isOver(pos):
                                zhai = False
                                zButton[1].recolor((0, 255, 0))
                                zButton[0].recolor((128, 128, 128))
                            elif AButton[1].isOver(pos):
                                #number, value, zhai or not to play
                                try:
                                    valid = checkValidMove(game, int(callInput[1].text), int(callInput[0].text), zhai)
                                    if valid:
                                        data = callInput[0].text + "," + callInput[1].text + "," + str(zhai)
                                        for cii in callInput:
                                            cii.renewText()
                                        zButton[0].recolor((128, 128, 128))
                                        zButton[1].recolor((128, 128, 128))
                                        game = n.send(data)
                                    else:
                                        txt = font.render("Invalid Move, check amount and value", 1, (255,0,0), True)
                                        win.blit(txt, (40, 400))
                                        pygame.display.update()
                                        pygame.time.delay(2000)
                                except:
                                    txt = font.render("Invalid Move, check amount and value", 1, (255,0,0), True)
                                    win.blit(txt, (40, 400))
                                    pygame.display.update()
                                    pygame.time.delay(2000)

        redrawWindow(game, player)
    
def menu_screen():
    run = True
    viewer = False
    clock = pygame.time.Clock()
    unameInput = InputBox(230, 500, 200, 50)
    spectate = Button((255, 255, 255), 230, 560, 200, 50, "Spectate")

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        fontt = pygame.font.SysFont("comicsans", 60)
        text = fontt.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (200,200))
        text2 = font.render("Username(Optional)", 1, (255, 0, 0))
        win.blit(text2, (200, 450))

        unameInput.draw(win)
        spectate.draw(win)
        pygame.display.update()

        username = ''
        for event in pygame.event.get():
            unameInput.handle_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if unameInput.text != '':
                    username = unameInput.text
                if spectate.isOver(event.pos):
                    viewer = True
                    run = False
                if not unameInput.rect.collidepoint(event.pos):
                    run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if unameInput.text != '':
                        username = unameInput.text
                    run = False

    main(username, viewer)

while True:
    menu_screen()