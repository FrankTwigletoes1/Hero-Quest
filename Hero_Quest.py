import sys
import pygame
import options 
import os


fps = 60
screenSize = (int(1000), int(1000))


player_sprites = pygame.sprite.Group()
middle_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()



class Road(pygame.sprite.Sprite):
    def __init__(self,x,y):
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/road.png").convert()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/wall.png").convert()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
     

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
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)


        self.image = pygame.image.load("sprites/player1Down.png")
        self.image.set_colorkey((69,255,0))
        
        self.rect = self.image.get_rect()
        self.rect.x = x*50
        self.rect.y = y*50
    
    def moveRight(self):
        Road(self.rect.x,self.rect.y)
        
        self.image = pygame.image.load("sprites/player1Right.png")
        self.image.set_colorkey((69,255,0))

        if self.rect.x+50 < screenSize[0]:
            self.rect.x = self.rect.x+50
            stick = pygame.sprite.groupcollide(player_sprites, background_sprites, False, False)
            if stick:
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
        global player

        char = map.read("map.txt")
        
        i = 0
        
        for y in range(15):
            for x in range(20):
                
                if char[i] == "r":
                    road = Road(x*50,y*50)
                    middle_sprites.add(road)
                    i += 1
                
                elif char[i] == "w":
                    wall = Wall(x*50,y*50)
                    background_sprites.add(wall)
                    i += 1
                
                elif char[i] == "p":
                    road = Road(x*50,y*50)
                    middle_sprites.add(road)
                    player = player1(x,y)
                    player_sprites.add(player)    
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
        background_sprites.draw(game_screen)
        
        pass

    def handle_input(key_name):
        print(key_name)
        if key_name == "right":
            player.moveRight()
        if key_name == "left":
            player.moveLeft()
        if key_name == "down":
            player.moveDown()
        if key_name == "up":
            player.moveUp()
        
        if key_name == "escape":
            pygame.quit()
            sys.exit(0)

    def update(screen, time):
        # Kode som køre hver update cyklus
        #  screen for at kunne få adgang til "surface"
        # time sørger for adgang til sidste opdatering af skærm

        middle_sprites.draw(game_screen)
        player_sprites.draw(game_screen)
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