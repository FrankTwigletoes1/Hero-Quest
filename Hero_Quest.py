import sys
import pygame
import options 
import os


fps = 60
screenSize = (int(1000), int(1000))


player_sprites = pygame.sprite.Group()
middle_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()

class Road():
    def __init__(self,x,y):
        
        super().__init__()

        self.image = pygame.image.load("sprites/road.png").convert()


        game_screen.blit(self.image, (x,y))
        

class Wall():
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


class player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.playerUp = pygame.image.load("sprites/player1Up.png")
        self.image = pygame.image.load("sprites/player1Down.png")
        self.playerRight = pygame.image.load("sprites/player1Right.png")
        self.playerLeft = pygame.image.load("sprites/player1Left.png")

        self.image.set_colorkey((69,255,0))
        
        self.rect = self.image.get_rect()


class player2():
    def __init__(self):
        self.playerUp = pygame.image.load("")
        self.playerDown = pygame.image.load("")
        self.playerRight = pygame.image.load("")
        self.playerLeft = pygame.image.load("")
        
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
        player = player1()
        player_sprites.add(player)

        pass

    def handle_input(key_name):
        # Alt input
        
        pass

    def update(screen, time):
        # Kode som køre hver update cyklus
        #  screen for at kunne få adgang til "surface"
        # time sørger for adgang til sidste opdatering af skærm


        front_sprites.draw(game_screen)
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