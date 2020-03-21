
import sys
import pygame
import options 


fps = 60
screenSize = (int(1000), int(1000))


"""
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

    """


   
class Road():
    def __init__(self,x,y):
        
        super().__init__()

        self.image = pygame.image.load("sprites/road.png").convert()


        game_screen.blit(self.image, (x,y))
        

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        
        super().__init__()

        self.image = pygame.image.load("sprites/wall.png").convert()

        game_screen.blit(self.image, (x,y))


        
        

class door():
    def __init__(self):
        return None


class chest():
    def __init__(self):
        return None



class trap():
    def __init__(self):
        return None


class player1():
    def __init__(self):
        return None


class player2():
    def __init__(self):
        return None


class orc():
    def __init__(self):
        return None




class map():
    def read(file):
        mapchars = []
        with open(file, "r") as f:
            for line in f:
                for each in line.rstrip("\n"):
                    if each != " ":
                        mapchars.append(each)
        return mapchars

    def assignblocks():
        char = map.read("map.txt")
        i = 0
        for y in range(15):
            for x in range(20):
                if char[i] == "r":
                    Road(x*50,y*50)
                    i += 1
                elif char[i] == "w":
                    Wall(x*50,y*50)
                    i += 1
                    







def pygame_modules_have_loaded():
    success = True

    if not pygame.display.get_init:
        success = False

    return success

pygame.init()


if pygame_modules_have_loaded():
    game_screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('Hero Quest Digital')
    clock = pygame.time.Clock()

    def declare_globals():
        #Alle globale variabler
        pass

    def prepare_test():
        # Kode som skal køre inden game loop
        map.assignblocks()

        pass

    def handle_input(key_name):
        # Alt input
        pass

    def update(screen, time):
        # Kode som køre hver update cyklus
        #  screen for at kunne få adgang til "surface"
        # time sørger for adgang til sidste opdatering af skærm
 
        pygame.display.update()

   
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #           LAD VÆR MED AT RØR DET NEDEN UNDER!!!
    #
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def main():
        declare_globals()
        prepare_test()

        while True:
            for event in pygame.event.get():
                if event.type == quit:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    handle_input(key_name)

            milliseconds = clock.tick(fps)
            seconds = milliseconds / 1000.0
            update(game_screen, seconds)

            sleep_time = (1000.0 / fps) - milliseconds
            if sleep_time > 0.0:
                pygame.time.wait(int(sleep_time))
            else:
                pygame.time.wait(1)

    main()