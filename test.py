from enum import Enum

#Render text
# Renders text to the screen with a lot of customisation to choose from:
# (required) font:          the font to use
# (required) text:          the text string that should be drawn on the screen itself
# (required) colour_rgb:    the text colour, please use either white (255,255,255) or black (0,0,0) for convenience
# (optional) x:             the horizontal position of the text, none centers the text on screen
# (optional) y:             the vertical position of the text, none centers the text on screen
# (optional) offsetx:       how much the text should be moved left or right from its current position
# (optional) offsety:       how much the text should be moved up or down from its current position
# (optional) alignment:     how the text should be placed on screen in an easy manner, multiple can be used; left, right, top, bottom
# (optional) effects:       what effects should be applied to the text, multiple can be used; bold, italic, underline
# (optional) relative:      makes the text relative to another object in case of defined x and y value
def render_text(font, text, color_rgb, x = None, y = None, offsetx = 0, offsety = 0, alignment=None, effects=None, relative = False):

    # Draw effects if any are defined
    if (effects is not None):
        if ("bold" in effects):
            font.set_bold(True)
        if("italic" in effects):
            font.set_italic()
        if("underline" in effects):
            font.set_underline(True)

    # creates the font object and the x and y coordinates based on the arguments used
    renderfont = font.render(text, True, color_rgb)
    x = (win_x / 2 - renderfont.get_width() / 2) if(x is None) else (x - renderfont.get_width() / 2) if(relative) else x # Text horizontal position: center | relative | absolute
    y = (win_y / 2 - renderfont.get_height() / 2) if (y is None) else (y - renderfont.get_height() / 2) if(relative) else y # Text vertical position: center | relative | absolute

    # Aligns the text if any are defined
    if(alignment is not None):
        if("left" in alignment):
            x = 0
        elif("right" in alignment):
            x = win_x - renderfont.get_width()
        if("top" in alignment):
            y = 0
        elif("bottom" in alignment):
            y = win_y - renderfont.get_height()

    # Renders the text to screen
    win.blit(renderfont, (x + offsetx, y + offsety))


self.font_h1 = pygame.font.SysFont('comicsans', 100) # All of the different types of font objects and sizes available
self.font_h2 = pygame.font.SysFont('comicsans', 80)
self.font_h3 = pygame.font.SysFont('comicsans', 60)
self.font_h4 = pygame.font.SysFont('comicsans', 40)
self.font_h5 = pygame.font.SysFont('comicsans', 20)
self.font_p1 = pygame.font.SysFont('Roboto', 100)
self.font_p2 = pygame.font.SysFont('Roboto', 80)
self.font_p3 = pygame.font.SysFont('Roboto', 60)
self.font_p4 = pygame.font.SysFont('Roboto', 40)
self.font_p5 = pygame.font.SysFont('Roboto', 20)

# Player Test

import pygame 
import os

pygame.init()

#folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

#Variabler
win_y = 1000
win_x = 1000
win_c = [win_x/2, win_y/2]
FPS = 60


m = 50

w = 50
h = 50

right = False
left = False
down = False
up = False

walk = 0
walk_right = pygame.image.load(os.path.join(img_folder, "player1r.png"))
walk_left = pygame.image.load(os.path.join(img_folder, "player1.png"))
walk_down = pygame.image.load(os.path.join(img_folder, "player1d.png"))
walk_up = pygame.image.load(os.path.join(img_folder, "player1u.png"))
#colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
graey = (128,128,128)
yellow = (255,216,0)
purple = (178,0,255)

#Surface
win=pygame.display
surf = win.set_mode([win_x,win_y])
win.set_caption("Sprites test")
clock = pygame.time.Clock()

#Class
class Player(pygame.sprite.Sprite):
    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = walk_down
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(x,y)
        
    def move(self, key):
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= m
            self.image = walk_left
            print("left")

        elif key[pygame.K_RIGHT] and self.rect.x < win_x - w:
            self.rect.x += m
            self.image = walk_right
            print("right")

        elif key[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= m
            self.image = walk_up
            print("up")

        elif key[pygame.K_DOWN] and self.rect.y < win_y - h:
            self.rect.y += m
            self.image = walk_down
            print("down")

#Sprites
all_sprites = pygame.sprite.Group()
player1 = Player(0,0)
all_sprites.add(player1)

class DIRECTION(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class entity(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)
        self.image.set_colorkey(colour)
        self.colour = colour
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class player1(entity):
    def __init__(self,x,y):
        entity.__init__(x*50, y*50, (69,255,0), "sprites/player1Down.png")
    
    def move(self, move_direction):
        Road(self.rect.x,self.rect.y)

        if(move_direction == DIRECTION.UP and self.rect.y > 0):
            self.rect.y = self.rect.y-50
            self.simage = "sprites/player1Up.png"

        elif(move_direction == DIRECTION.RIGHT and (self.rect.x+50) < screenSize[0]):
            self.rect.x = self.rect.x+50
            self.simage = "sprites/player1Right.png"

        elif(move_direction == DIRECTION.DOWN and self.rect.y < (screenSize[1]-300)):
            self.rect.y = self.rect.y+50
            self.simage = "sprites/player1Down.png"

        elif(move_direction == DIRECTION.LEFT and not (self.rect.x-50) < 0):
            self.rect.x = self.rect.x-50
            self.simage = "sprites/player1Left.png"

    self.image = pygame.image.load(self.simage)
    self.image.set_colorkey(self.colour)

    if pygame.sprite.groupcollide(player_sprites, background_sprites, False, False):
        self.rect.x = self.rect.x-50
        middle_sprites.draw(game_screen)

    
    def moveRight(self):
        Road(self.rect.x,self.rect.y)
        
        self.image = pygame.image.load("sprites/player1Right.png")
        self.image.set_colorkey((69,255,0))

        if self.rect.x+50 < screenSize[0]:
            self.rect.x = self.rect.x+50
            collision = pygame.sprite.groupcollide(player_sprites, background_sprites, False, False)
            if collision:
                print("Collided")
                self.rect.x = self.rect.x-50
            middle_sprites.draw(game_screen)


    def moveLeft(self):
        Road(self.rect.x,self.rect.y)
        
        self.image = pygame.image.load("sprites/player1Left.png")
        self.image.set_colorkey((69,255,0))
        
        if not self.rect.x-50 < 0:
            self.rect.x = self.rect.x-50
            collsion = pygame.sprite.groupcollide(player_sprites, background_sprites, False, False)
            if collsion:
                print("Collided")
                self.rect.x = self.rect.x+50
            middle_sprites.draw(game_screen)


    def moveDown(self):
        Road(self.rect.x,self.rect.y)
        
        self.image = pygame.image.load("sprites/player1Down.png")
        self.image.set_colorkey((69,255,0))
        if self.rect.y < screenSize[1]-300:
            self.rect.y = self.rect.y+50
            collsion = pygame.sprite.groupcollide(player_sprites, background_sprites, False, False)
            if collsion:
                print("Collided")
                self.rect.y = self.rect.y-50
            middle_sprites.draw(game_screen)


    def moveUp(self):
        Road(self.rect.x,self.rect.y)
        
        self.image = pygame.image.load("sprites/player1Up.png")
        self.image.set_colorkey((69,255,0))
        if self.rect.y > 0:
            self.rect.y = self.rect.y-50
            collsion = pygame.sprite.groupcollide(player_sprites, background_sprites, False, False)
            if collsion:
                print("Collided")
                self.rect.y = self.rect.y+50    
            middle_sprites.draw(game_screen)


#Game loop
loop = True

while loop:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop=False

        key1 = pygame.key.get_pressed()
        player1.move(key1)


    #Draw
    surf.fill(green)
    all_sprites.draw(surf)

    #Update
    all_sprites.update()
    
    #som det sidste opdater vinduet
    win.update()
    
pygame.quit()
quit()



