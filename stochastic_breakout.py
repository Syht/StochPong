# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:43:14 2017

@author: Syht
"""
try:
    from peyetribe import EyeTribe
    TRACK_EYE = True
except:
    TRACK_EYE = False

import math, os, random, time, pygame, ezmenu, configparser, ast, sys
import numpy as np

# loading of the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
scrsize = config['screensize']
pdlsize = config['paddlesize']
orb = config['ball']
level = config['levels']
bricksprite = config['bricks']

# retrieving of the data in config.ini
HEIGHT = int(scrsize['height'])
WIDTH = int(scrsize['width'])
TLSIDE = int(scrsize['tileside'])
PADDLESIZE = int(pdlsize['size'])
SPD = int(orb['speed'])
AGLL = int(orb['anglel'])
AGLH = int(orb['angleh'])

# Game constants
SCREENRECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

def imgcolorkey(image, colorkey):
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

def load_image(filename, colorkey = None):
    filename = os.path.join('data', filename)
    image = pygame.image.load(filename).convert()
    return imgcolorkey(image, colorkey)

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = load_image(filename)
    def imgat(self, rect, colorkey = None):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return imgcolorkey(image, colorkey)
    def imgsat(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs

def hborders(spritesheet):
    # plain border - 4, special border - 5, upper left - 6, upper right - 7
    rects = [(449, 35, 31, 9), (129, 289, 31, 13), (129, 193, 31, 13), (193, 193, 31, 13)]
    # the plain border had to be extracted
    # two pixels away from the edge to remove the background
    offsets = [2, 0, 0, 0]
    borders = []
    for x in range(len(rects)):
        borders.append(pygame.Surface((31, 31)).convert())
        # draw border at the bottom part of the tile, and add the offset if necessary
        # to ensure that the borders will remain aligned
        # -1 index refers to the most recently appended element in the list
        borders[-1].blit(spritesheet.imgat(rects[x]), (0, 18 + offsets[x]))
    return borders

def paddleimage(spritesheet):
    paddle = pygame.Surface((PADDLESIZE, 11)).convert()
    paddle.blit(spritesheet.imgat((351, 457, (PADDLESIZE-28), 11)), (0, 0))    # left half
    paddle.blit(spritesheet.imgat((289, 143, 28, 11)), ((PADDLESIZE-28), 0))   # right half
    return imgcolorkey(paddle, -1)

class Arena:
    tileside = TLSIDE
    # when drawing tiles, the origin is at (topx, topy),
    # so that a filled tile map will be centered on the screen
    # (since 640 x 480 is not divisible by 31 x 31, so the remainder
    # was distributed over the edges of the screen, centering the resulting image)
    topx = 10
    topy = 7
    # numxtiles, numytiles, and rect refer to the region where the ball is allowed to be in
    numxtiles = int((WIDTH-62)/TLSIDE)
    numytiles = int((HEIGHT-68)/TLSIDE)
    rect = pygame.Rect(topx + tileside, topy + tileside, tileside*(numxtiles), tileside*(numytiles))
    def __init__(self, levels):
        self.levels = levels
        self.background = pygame.Surface(SCREENRECT.size).convert()
        self.makebg(1)
    def drawtile(self, tile, x, y):
        self.background.blit(tile, (self.topx + self.tileside*x, self.topy + self.tileside*y))
    def makebg(self, tilenum):
        # numbers refer to border images
        bordertop = [6, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 5, 4, 4, 4, 5, 4, 4, 5, 4, 4, 4, 5, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 7]
        borderleft = [0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0]
        borderright = [1, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1]
        for x in range(len(bordertop)):
            self.drawtile(self.borders[bordertop[x]], x, 0)
        for y in range(len(borderleft)):
            self.drawtile(self.borders[borderleft[y]], 0 , 1 + y)
            self.drawtile(self.borders[borderright[y]], self.numxtiles + 1, 1 + y)
        for x in range(self.numxtiles):
            for y in range(self.numytiles):
                # draw tiles within the border
                self.drawtile(self.tiles[tilenum], x + 1, y + 1)
    def makelevel(self, levelnum):
        for y in range(len(self.levels[levelnum])):
            for x in range(len(self.levels[levelnum][y])):
                color = self.levels[levelnum][y][x] - 1
                if color > -1:
                    Brick(self, x, y, color)

# each type of game object gets an init and an
# update function. the update function is called
# once per frame, and it is when each object should
# change its current position and state

class Paddle(pygame.sprite.Sprite):
    def __init__(self, arena):
        Paddle.lenPP = len(os.listdir('PaddlePos'))
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.arena = arena
        self.rect.bottom = arena.rect.bottom - arena.tileside
    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        if not self.arena.rect.contains(self.rect):
            if self.rect.left < self.arena.rect.left:
                self.rect.left = self.arena.rect.left
            elif self.rect.right > self.arena.rect.right:
                self.rect.right = self.arena.rect.right
        with open(os.path.join('PaddlePos', 'data_paddle_position_%d.txt' %Paddle.lenPP), 'a') as data:
            data.write('%d;%d;%d\n' %(int(time.time()*1000), self.rect.centerx, self.rect.centery))

class Ball(pygame.sprite.Sprite):
    # the speed should be less than
    # the smallest dimension
    # used in the game
    # to prevent teleporting
    speed = SPD
    # anglel = 45, angleh = 135
    anglel = AGLL
    angleh = AGLH
    def __init__(self, arena, paddle, bricks):
        Ball.lenBP = len(os.listdir('BallPos'))
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.arena = arena
        self.paddle = paddle
        self.update = self.start
        self.bricks = bricks
    def start(self):
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top
        if pygame.mouse.get_pressed()[0] == 1:
            self.fpx = self.rect.centerx
            self.fpy = self.rect.centery
            self.fpdx = 5
            self.fpdy = 1
            self.update = self.move
    def setfp(self):
        """use whenever usual integer rect values are adjusted"""
        self.fpx = self.rect.centerx
        self.fpy = self.rect.centery
    def setint(self):
        """use whenever floating point rect values are adjusted"""
        self.rect.centerx = self.fpx
        self.rect.centery = self.fpy
    def move(self):
        # bounce from paddle and print coordinates: (Ball Paddle [Yes/No]->if paddle touched or not)
        if self.rect.bottom > self.paddle.rect.top:
            if self.rect.colliderect(self.paddle.rect) and self.fpdy > 0:
                ballpos = self.rect.width + self.rect.left - self.paddle.rect.left - 1
                ballmax = self.rect.width + self.paddle.rect.width - 2
                factor = float(ballpos)/ballmax
                angle = math.radians(self.angleh - factor*(self.angleh - self.anglel))
                self.fpdx = self.speed*math.cos(angle)
                self.fpdy = -self.speed*math.sin(angle)
                hit = "Yes"
            if (self.paddle.rect.left>self.rect.right or self.paddle.rect.right<self.rect.left) and self.rect.top < (self.paddle.rect.bottom - 26):
                hit = "No"
            try:
                print (self.rect.centerx, self.paddle.rect.centerx, hit)
            except UnboundLocalError:
                pass

        # usual movement
        self.fpx = self.fpx + self.fpdx
        self.fpy = self.fpy + self.fpdy
        self.setint()

        # keep inside arena
        if self.rect.left < self.arena.rect.left:
            self.rect.left = self.arena.rect.left
            self.setfp()
            self.fpdx = -self.fpdx
        if self.rect.right > self.arena.rect.right:
            self.rect.right = self.arena.rect.right
            self.setfp()
            self.fpdx = -self.fpdx
        if self.rect.top < self.arena.rect.top:
            self.rect.top = self.arena.rect.top
            self.setfp()
            self.fpdy = -self.fpdy
        if self.rect.top > self.arena.rect.bottom:
            self.update = self.start

        # destroy bricks
        brickscollided = pygame.sprite.spritecollide(self, self.bricks, False)
        if brickscollided:
            oldrect = self.rect
            left = right = up = down = 0
            for brick in brickscollided:
                # [] - brick, () - ball

                # ([)]
                if oldrect.left < brick.rect.left < oldrect.right < brick.rect.right:
                    self.rect.right = brick.rect.left
                    self.setint()
                    if not (oldrect.top < brick.rect.top < oldrect.bottom < brick.rect.bottom or brick.rect.top < oldrect.top < brick.rect.bottom < oldrect.bottom):
                        left = -1
                    if brick.color == 0:
                        pass
                    if brick.color == 1:
                        if random.randint(0,100) < 25:
                            up = -1
                    if brick.color == 2:
                        if random.randint(0,100) < 50:
                            up = -1
                    if brick.color == 3:
                        if random.randint(0,100) < 75:
                            up = -1
                    if brick.color == 4:
                        up = -1

                # [(])
                if brick.rect.left < oldrect.left < brick.rect.right < oldrect.right:
                    self.rect.left = brick.rect.right
                    self.setint()
                    if not (oldrect.top < brick.rect.top < oldrect.bottom < brick.rect.bottom or brick.rect.top < oldrect.top < brick.rect.bottom < oldrect.bottom):
                        right = -1
                    if brick.color == 0:
                        pass
                    if brick.color == 1:
                        if random.randint(0,100) < 25:
                            up = -1
                    if brick.color == 2:
                        if random.randint(0,100) < 50:
                            up = -1
                    if brick.color == 3:
                        if random.randint(0,100) < 75:
                            up = -1
                    if brick.color == 4:
                        up = -1

                # top ([)] bottom
                if oldrect.top < brick.rect.top < oldrect.bottom < brick.rect.bottom:
                    self.rect.bottom = brick.rect.top
                    self.setint()
                    up = -1
                    if brick.color == 0:
                        pass
                    if brick.color == 1:
                        if random.randint(0,100) < 25:
                            right = -1
                    if brick.color == 2:
                        if random.randint(0,100) < 50:
                            right = -1
                    if brick.color == 3:
                        if random.randint(0,100) < 75:
                            right = -1
                    if brick.color == 4:
                        right = -1

                # top [(]) bottom
                if brick.rect.top < oldrect.top < brick.rect.bottom < oldrect.bottom:
                    self.rect.top = brick.rect.bottom
                    self.setint()
                    #down = 1
                    up = -1
                    if brick.color == 0:
                        pass
                    if brick.color == 1:
                        if random.randint(0,100) < 25:
                            right = -1
                    if brick.color == 2:
                        if random.randint(0,100) < 50:
                            right = -1
                    if brick.color == 3:
                        if random.randint(0,100) < 75:
                            right = -1
                    if brick.color == 4:
                        right = -1

                brick.kill()

            # if the ball is asked to go both ways, then do not change direction
            if left + right != 0:
                self.fpdx = (left + right)*self.fpdx/abs(left + right)
            if up + down != 0:
                self.fpdy = (up + down)*self.fpdy/abs(up + down)

        # write the ball position in a .dat file
        with open(os.path.join('BallPos', 'data_ball_position_%d.txt' %Ball.lenBP), 'a') as data:
            data.write('%d;%d;%d\n' %(int(time.time()*1000), self.rect.centerx, self.rect.centery))

class Brick(pygame.sprite.Sprite):
    def __init__(self, arena, x, y, color):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[color]
        self.rect = self.image.get_rect()
        self.rect.left = arena.rect.left + x*self.rect.width
        self.rect.top = arena.rect.top + y*self.rect.height
        self.color = color

def main_menu():
    pygame.init()
    pygame.display.set_caption('Welcome to Stochastic Pong')
    screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.DOUBLEBUF)
    pygame.mouse.set_visible(1)

    def option1():
        main()
    def option2():
        pygame.quit()
        os._exit(1)


    font = pygame.font.Font(os.path.join('data', 'freesansbold.ttf'), 60)

    titletext = font.render('A Stochastic Pong', True, (255,255,255))
    titletextrect = titletext.get_rect()
    titletextrect.centerx = WIDTH/2; titletextrect.y = HEIGHT/4

    menu = ezmenu.EzMenu(
        ['New Game', option1],
        ['Quit Game', option2])

    menu.center_at((WIDTH/2), (HEIGHT/2))
    menu.set_normal_color((255,255,255))

    screen.blit(titletext, titletextrect)

    clock = pygame.time.Clock()
    pygame.display.flip()

    while 1:
        clock.tick(30)
        events = pygame.event.get()

        menu.update(events)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(1)

        screen.fill((0,0,0))
        menu.draw(screen)
        screen.blit(titletext, titletextrect)
        pygame.display.flip()

def main():
    pygame.init()

    # set the display mode
    winstyle = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE # | FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    # Set the windows size
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    # load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    spritesheet = SpriteSheet('arinoid_master.bmp')
    #bg = pygame.image.load(os.path.join('data', 'test_berserk.png'))
    Arena.tiles = spritesheet.imgsat([(129, 321, 31, 31),   # purple - 0
                                      (161, 321, 31, 31),   # dark blue - 1
                                      (129, 353, 31, 31),   # red - 2
                                      (161, 353, 31, 31),   # green - 3
                                      (129, 385, 31, 31)])  # blue - 4

    # left border - 0, right border - 1,
    # special left border - 2, special right border - 3
    Arena.borders = spritesheet.imgsat([(129, 257, 31, 31),
                                        (193, 257, 31, 31),
                                        (129, 225, 31, 31),
                                        (193, 225, 31, 31)]) + hborders(spritesheet)

    Paddle.image = paddleimage(spritesheet)
    Ball.image = spritesheet.imgat((391, 297, 18, 17), -1) # 428, 300, 11, 11 - little ball / 483, 420, 26, 25 - bigger ball

    # yellow - 1, green - 2, red - 3, dark orange - 4,
    # purple - 5, orange - 6, light blue - 7, dark blue - 8
    # Three size options -> 'littlebricks', 'mediumbricks', 'bigbricks'
    Brick.images = spritesheet.imgsat(ast.literal_eval(bricksprite['bigbricks']))

    # loads the different levels reading config.ini (ast.literal_eval: allows to read lists from config.ini files)
    levels = ast.literal_eval(level['lvls'])

    # decorate the game window
    pygame.display.set_caption('Welcome to Stochastic Pong')

    # create the background
    arena = Arena(levels)
    screen.blit(arena.background, (0, 0))
    #screen.blit(bg, (40, 37))
    pygame.display.flip()

    # initialize game groups
    balls = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()

    # assign default groups to each sprite class
    Paddle.containers = all
    Ball.containers = all, balls
    Brick.containers = all, bricks

    clock = pygame.time.Clock()

    # initialize our starting sprites
    paddle = Paddle(arena)
    Ball(arena, paddle, bricks)

    lvl = 0
    arena.makelevel(lvl)

    try:
        TRACK_EYE = True
        tracker = EyeTribe()
        tracker.connect()
        n = tracker.next()
        print("eT;dT;aT;Fix;State;Rwx;Rwy;Avx;Avy;LRwx;LRwy;LAvx;LAvy;LPSz;LCx;LCy;RRwx;RRwy;RAvx;RAvy;RPSz;RCx;RCy")
        tracker.pushmode()
        # Count the number of file in the GazeData folder
        lenGD = len(os.listdir('GazeData'))
    except:
        TRACK_EYE = False

    done = False
    pygame.mouse.set_visible(0)

    while not done:
        # get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True

        # go to next lvl if no more bricks
        if len(bricks) == 0:
            try:
                # put the paddle and the ball in the initial position
                all = pygame.sprite.RenderUpdates()
                Paddle.containers = all
                Ball.containers = all, balls
                Brick.containers = all, bricks
                screen.blit(arena.background, (0, 0))
                #screen.blit(bg, (40, 37))
                pygame.display.flip()
                paddle = Paddle(arena)
                Ball(arena, paddle, bricks)
                # induce a delay of XXX(ms)
                pygame.time.delay(1000)
                # make the next level
                lvl += 1
                arena.makelevel(lvl)
            except IndexError:
                main_menu()

        # clear/erase the last drawn sprites
        all.clear(screen, arena.background)
        #screen.blit(bg, (40, 37))
        # update all the sprites
        all.update()

        # draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        # cap the framerate
        clock.tick(30)
        try:
            TRACK_EYE = True
            n = tracker.next()
            #print(n)
            with open(os.path.join('GazeData', 'data_eye_tracking_%d.txt' %lenGD), 'a') as data:
                data.write('%s\n' %n)
        except:
            TRACK_EYE = False

    try:
        TRACK_EYE = True
        tracker.pullmode()
        tracker.close()
    except:
        TRACK_EYE = False

if __name__ == '__main__': main_menu()
