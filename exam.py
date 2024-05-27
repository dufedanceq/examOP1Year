from pygame import *
from random import randint
from pygame import mouse

init()
tiles = 50
winWidth, winHeight = tiles * 12, tiles * 12

window = display.set_mode((winWidth, winHeight))
display.set_caption('Kursova (хочу 100 балів :) )')

class GameSprite(sprite.Sprite):

    def __init__(self, img, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (width, height))
        self.weight=width
        self.height=height
        self.speed=speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self,player):
        if player.rect.x >= 5.5 * tiles:
            if player.rect.y >= 5.5 * tiles:
                window.blit(self.image, (self.rect.x - (player.rect.x - tiles * 5.5), self.rect.y - (player.rect.y-tiles * 5.5)))
            else:
                window.blit(self.image, (self.rect.x - (player.rect.x - tiles * 5.5), self.rect.y))
        else:
            if player.rect.y >= 5.5 * tiles:
                window.blit(self.image, (self.rect.x, self.rect.y - (player.rect.y - tiles * 5.5)))
            else:
                window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def __init__(self, img, x, y, width, height, speed, weapon, heart):
        super().__init__(img, x, y, width, height, speed)
        self.weapon = weapon
        self.heart = heart

    def fire(self, ghostList):
        self.img = 'hero_with_weapon.png'
        self.image = transform.scale(image.load(self.img), (self.weight, self.height))
        for i in ghostList:
            if (((i.rect.x - self.rect.x) ** 2) + ((i.rect.y - self.rect.y) ** 2)) ** 0.5 <= 2 * tiles:
                fire.rect.x ,fire.rect.y = i.rect.x, i.rect.y
                fire.reset(player)
                i.health -= 1
                if i.health == 0:
                    ghostList.remove(i)

    def getDamage(self, list):
        for i in list:
            if sprite.collide_rect(self, i):
                self.heart -= 1
                self.rect.x = tiles
                self.rect.y = tiles
        if self.heart <= 0:
            game_over()

    def control(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
            for wall in listWall:
                if sprite.collide_rect(self, wall):
                    self.rect.x += self.speed
                    break
        if keys[K_d]:
            self.rect.x += self.speed
            for wall in listWall:
                if sprite.collide_rect(self, wall):
                    self.rect.x -= self.speed
                    break
        if keys[K_w]:
            self.rect.y -= self.speed
            for wall in listWall:
                if sprite.collide_rect(self, wall):
                    self.rect.y += self.speed
                    break
        if keys[K_s]:
            self.rect.y += self.speed
            for wall in listWall:
                if sprite.collide_rect(self, wall):
                    self.rect.y -= self.speed
                    break

class Wall(GameSprite):
    pass
class Floor(GameSprite):
    pass
class Trap(GameSprite):
    def change(self,trapCounter):
        if trapCounter <= 100:
            self.img = 'trap_on.png'
            self.image = transform.scale(image.load(self.img), (self.weight, self.height))
            if sprite.collide_rect(self, player):
                player.heart -= 1
                player.rect.x, player.rect.y= tiles,tiles
        else:
            self.img = 'trap_off.png'
            self.image = transform.scale(image.load(self.img), (self.weight, self.height))

class Enemy(GameSprite):
    def __init__(self, img, x, y, width, height, speed, type, direction, health):
        super().__init__(img, x, y, width, height, speed)
        self.type = type
        self.direction = direction
        self.health = health
    def control(self, enemyDirection, enemyCount):
        enemyDirection += self.direction
        if enemyDirection == 2 or enemyDirection == 3:
                self.rect.x -= self.speed
                for wall in listWall:
                    if sprite.collide_rect(self, wall):
                        self.rect.x += self.speed * 1.1
                if enemyCount == 99 and self.type == 'teleport':
                    self.rect.x -= tiles
        elif enemyDirection == 3 or enemyDirection == 4:
                self.rect.x += self.speed
                for wall in listWall:
                    if sprite.collide_rect(self, wall):
                        self.rect.x -= self.speed * 1.1
                if enemyCount == 99 and self.type == 'teleport':
                    self.rect.x += tiles * 2
        elif enemyDirection == 5  or enemyDirection == 6:
                self.rect.y += self.speed
                for wall in listWall:
                    if sprite.collide_rect(self, wall):
                        self.rect.y -= self.speed*1.1
                if enemyCount == 99 and self.type == 'teleport':
                    self.rect.y += tiles * 2
        elif enemyDirection == 6 or enemyDirection == 7:
                self.rect.y -= self.speed
                for wall in listWall:
                    if sprite.collide_rect(self, wall):
                        self.rect.y += self.speed * 1.1
                if enemyCount == 99 and self.type == 'teleport':
                    self.rect.y -= tiles * 3
        if self.rect.x < 0 or self.rect.x > 44 * tiles or self.rect.y < 0 or self.rect.y > 23 * tiles:
            self.rect.x = 22 * tiles 
            self.rect.y = 10 * tiles
            
createLab=[
    '1111111111111111111111111111111111111111',
    '1000000001000000000000000000000000100000',
    '1000000001000000000000111111100000100000',
    '1000000001001111111000000000011111100000',
    '1000000001000000000000000000000000100000',
    '1000000001010000000001111000011110100000',
    '1011111111000000000000000111110000100000',
    '1000000000010001111000000000000100100000',
    '1011111111010000001000000011110100100000',
    '1000000000010001001000000000011000100000',
    '1011111111001000001000000111111000100000',
    '1000000000000000001000000000000000100000',
    '1000010011111000001000000010001000100000',
    '1000010000001000100000000000001000100000',
    '1000000100001000100011111000001000100000',
    '1000000100001001000000000000010000100000',
    '1000111110000010100011111000001000100000',
    '1000000000000000100000001000000000100000',
    '1111111111111111111111111111111111111111',
    '1111111111111111111111111111111111111111',
    '1111111111111111111111111111111111111111',
    '1111111111111111111111111111111111111111',
    '1111111111111111111111111111111111111111',
    '1111111111111111111111111111111111111111',  
]
listWall = []
listFloor = []
ghost1 = Enemy('enemy.png', 22 * tiles, 12 * tiles, int(tiles // 1.3), int(tiles // 1.3), tiles // 12, 'teleport', 1, 50)
ghost2 = Enemy('enemy.png', 22 * tiles, 12 * tiles, int(tiles // 1.3), int(tiles // 1.3), tiles // 12, 'teleport', 2, 50)
ghost3 = Enemy('enemy.png', 22 * tiles, 12 * tiles, int(tiles // 1.3), int(tiles // 1.3), tiles // 12, 'teleport', 3, 50)
ghostList = [ghost1, ghost2, ghost3]
enemyCount = 0
enemyDirection = randint(1, 4)

def win():
    counter = 0
    while counter < 200:
        window.blit(transform.scale(image.load('win.png'), (winWidth, winHeight)), (0, 0))
        display.flip()
        counter += 1
    reset_game_state()
    menu()

def game_over():
    counter = 0
    while counter < 200:
        window.blit(transform.scale(image.load('gameover.png'), (winWidth, winHeight)), (0, 0))
        display.flip()
        counter += 1
    reset_game_state()
    menu()

def reset_game_state():
    global ghostList, enemyCount, enemyDirection, weaponVisible, player, fire, traps, trapCounter
    ghost1 = Enemy('enemy.png', 22 * tiles, 12 * tiles, int(tiles // 1.3), int(tiles // 1.3), tiles // 12, 'teleport', 1, 50)
    ghost2 = Enemy('enemy.png', 22 * tiles, 12 * tiles, int(tiles // 1.3), int(tiles // 1.3), tiles // 12, 'teleport', 2, 50)
    ghost3 = Enemy('enemy.png', 22 * tiles, 12 * tiles, int(tiles // 1.3), int(tiles // 1.3), tiles // 12, 'teleport', 3, 50)
    ghostList = [ghost1, ghost2, ghost3]
    enemyCount = 0
    enemyDirection = randint(1, 4)
    weaponVisible = 0
    player = Player('hero.png', tiles, tiles, int(tiles * 0.8), int(tiles * 0.8), tiles // 10, None, 3)
    fire = Floor('weapon.png', tiles * 2, tiles * 2, int(tiles * 0.8), int(tiles * 0.8), tiles // 10)
    traps = [Trap('trap_off.png', tiles * randint(1, 40), tiles * randint(1, 20), tiles, tiles, 0) for _ in range(30)]
    trapCounter = 0

def createWall(createLab, list_wall):
    x = 0
    y = 0
    for i in createLab:
        for j in i:
            if j == '1':
                list_wall.append(Wall('wall.png', x, y, tiles, tiles, 0))
            if j == '0':
                listFloor.append(Floor('floor.png', x, y, tiles, tiles, 0)) 
            x += tiles
        y += tiles
        x = 0
createWall(createLab, listWall)

player=Player('hero.png', tiles, tiles, int(tiles * 0.8),  int(tiles * 0.8), tiles // 10, None, 3)
fire=Floor('weapon.png', tiles * 2, tiles * 2, int(tiles * 0.8),  int(tiles * 0.8) , tiles // 10)

menuImg = transform.scale(image.load('menu.png'), (winWidth, winHeight))
newGame = font.SysFont('verdana', 36).render("New game", True, (206, 212, 218))
newGamePointed = font.SysFont('verdana', 36).render("New game", True, (111,111,200))

settings = font.SysFont('verdana', 36).render("Settings", True, (206, 212, 218))
settingsPointed = font.SysFont('verdana', 36).render("Settings", True, (111,111,200))

exit = font.SysFont('verdana', 36).render("Exit", True, (206, 212, 218))
exitPointed = font.SysFont('verdana', 36).render("Exit", True, (111,111,200))

soundText = font.SysFont('verdana', 40).render("Sound", True, (0,0,0))

square = Rect(tiles * 8,tiles * 5,tiles * 4, tiles * 3)

menuSound = mixer.Sound('menu_sound.mp3')
gameSound = mixer.Sound('game_sound.mp3')
buttonSound = mixer.Sound('button_sound.mp3')
settingsImg = transform.scale(image.load('setting.png'), (winWidth, winHeight))

buttonSoundStop = 0
settingsOn = 0
weaponVisible = 0
heart = Floor('heart.png',tiles * 9, 0, tiles, tiles, 0)
traps = []
for i in range(30):
    traps.append(Trap('trap_off.png', tiles * randint(1, 40), tiles * randint(1, 20), tiles, tiles, 0 ))

trapCounter = 0
def menu():
    global buttonSoundStop, settingsOn
    menuSound.play(-1)
    gameSound.stop()
    player.heart = 3
    while 1:
        time.Clock().tick(100)
        for e in event.get():
            if e.type==QUIT:
                exit()
            if e.type == MOUSEBUTTONDOWN and mouse.get_pos()[0] > tiles * 8 and mouse.get_pos()[1] > tiles * 5 and mouse.get_pos()[0] < tiles * 12 and mouse.get_pos()[1] < tiles * 6:
                game()
            if e.type == MOUSEBUTTONDOWN and mouse.get_pos()[0] > tiles * 8 and mouse.get_pos()[1] > tiles * 7 and mouse.get_pos()[0] < tiles * 12 and mouse.get_pos()[1] < tiles * 8:
                exit()
            if e.type == MOUSEBUTTONDOWN and mouse.get_pos()[0] > tiles * 8 and mouse.get_pos()[1] > tiles * 6 and mouse.get_pos()[0] < tiles * 12 and mouse.get_pos()[1] < tiles * 7:
                settingsOn = 1

        window.blit(menuImg, (0, 0))
        window.blit(newGame, (tiles * 8, tiles * 5))
        draw.rect(window, (33, 37, 41), square)
        window.blit(newGame, (tiles * 8, tiles * 5))
        window.blit(settings, (tiles * 8, tiles * 6))
        window.blit(exit, (tiles * 8, tiles * 7))
        if mouse.get_pos()[0] > tiles * 8 and mouse.get_pos()[1] > tiles * 5 and mouse.get_pos()[0] < tiles * 12 and mouse.get_pos()[1] < tiles * 6:
            window.blit(newGamePointed, (tiles * 8, tiles * 5))
            buttonSoundStop += 1
            if buttonSoundStop == 1:
                buttonSound.play()
        elif mouse.get_pos()[0] > tiles * 8 and mouse.get_pos()[1] > tiles * 7 and mouse.get_pos()[0] < tiles * 12 and mouse.get_pos()[1] < tiles * 8:
            window.blit(exitPointed,(tiles * 8, tiles * 7)) 
            buttonSoundStop += 1
            if buttonSoundStop == 1:
                buttonSound.play()
        elif mouse.get_pos()[0] > tiles * 8 and mouse.get_pos()[1] > tiles * 6 and mouse.get_pos()[0] < tiles * 12 and mouse.get_pos()[1] < tiles * 7:
            window.blit(settingsPointed,(tiles*8, tiles*6)) 
            buttonSoundStop += 1
            if buttonSoundStop == 1:
                buttonSound.play()
        else:
            buttonSoundStop = 0
        if settingsOn == 1:
            window.blit(settingsImg, (0, 0))
            window.blit(soundText, (tiles / 2,tiles * 5))
            polosa = transform.scale(image.load('rect.png'), (int(tiles * 7 * menuSound.get_volume()), tiles))
            number = font.SysFont('verdana', 40).render(str(int(menuSound.get_volume() * 100)), True, (0, 0, 0))
            window.blit(number, (tiles * 10,tiles * 5))

            window.blit(polosa, (tiles * 3, tiles * 5))
            keys = key.get_pressed()
            if keys[K_RIGHT]:
                menuSound.set_volume(menuSound.get_volume() + 0.01)
                gameSound.set_volume(gameSound.get_volume() + 0.01)
            if keys[K_LEFT]:
                menuSound.set_volume(menuSound.get_volume() - 0.01)
                gameSound.set_volume(gameSound.get_volume() - 0.01)
            if keys[K_ESCAPE]:
                settingsOn = 0   
        display.flip()

def game():
    global enemyCount, enemyDirection,weaponVisible, ghostList, trapCounter
    
    menuSound.stop()
    gameSound.play(-1)
    while 1:
        time.Clock().tick(100)

        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                print(player.rect.x)
        
        for floor in listFloor:
            floor.reset(player)
        if trapCounter > 200:
            trapCounter = 0
        for i in traps:
            i.change(trapCounter)
        for i in traps:
            i.reset(player)
        for wall in listWall:
            wall.reset(player)
        trapCounter += 1
        
        keys=key.get_pressed()
        if keys[K_ESCAPE]:
            menu()
        player.control()
        if player.rect.x >= 5.5 * tiles:
            if player.rect.y >= 5.5 * tiles:
                window.blit(player.image, (player.rect.x - (player.rect.x-tiles * 5.5), player.rect.y-(player.rect.y-tiles * 5.5)))
            else:
                window.blit(player.image, (player.rect.x - (player.rect.x-tiles * 5.5), player.rect.y))
        else:
            if player.rect.y >= 5.5 * tiles:
                window.blit(player.image, (player.rect.x, player.rect.y - (player.rect.y - tiles * 5.5)))
            else:
                window.blit(player.image, (player.rect.x, player.rect.y))
        enemyCount += 1
        if enemyCount == 100:
            enemyDirection = randint(1, 4)
            enemyCount = 0

        for i in ghostList:
            i.reset(player)
            i.control(enemyDirection, enemyCount)
        
        if weaponVisible == 0:
            fire.reset(player)
        if sprite.collide_rect(fire, player):
            player.weapon = 'fire'
            weaponVisible = 1
        if player.weapon == 'fire':
            player.fire(ghostList)
        x = heart.rect.x
        for i in range(player.heart):
            window.blit(transform.scale(image.load('heart.png'), (heart.weight, heart.height)), (x, heart.rect.y))
            x += tiles
        player.getDamage(ghostList)
        if len(ghostList) == 0:
            win()

        display.flip()
menu()       