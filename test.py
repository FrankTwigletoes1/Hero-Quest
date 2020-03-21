
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



