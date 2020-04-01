import sys
import pygame
import options 
import os

fps = 60
screenSize = (int(1000), int(1000))

player_steps = 12
player_sprites = pygame.sprite.Group() # Playeren
middle_sprites = pygame.sprite.Group() # Alle sprites som aldrig bevægere sig men opdateres
background_sprites = pygame.sprite.Group() # Vægge, alle sprites som aldrig bevæger sig eller skal opdateres
entity_sprites = pygame.sprite.Group() #Sprites som opdateres på en bestemt måde

global player_steps

class Csprite(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert()

        self.rect = self.image.get_rect()
        self.rect.x = x*50
        self.rect.y = y*50

class Road(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/road.png")

class Background(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/baggrund.png")

class Wall(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/wall.png")

class Door(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/door.png")

class Door(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/door.png")

class Chest(Csprite):
    def __init__(self,x,y):
        pass

class Trap(Csprite):
    def __init__(self,x,y):
        pass

class Orc(Csprite):
    def __init__(self,x,y):
        pass

class BackgroundMenuTile(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/background.png")

class Player1(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/player1Down.png")
        self.image.set_colorkey((69,255,0))

    def move(self, direction):
        image = pygame.image.load("sprites/player1Down.png")
        global player_steps
        if player_steps > 0:
            
            if direction == "right" and self.rect.x+50 < screenSize[0]:
                image = pygame.image.load("sprites/player1Right.png")
                self.rect.x = self.rect.x+50
                if pygame.sprite.groupcollide(player_sprites, background_sprites, False, False):
                    print("Collided")
                    self.rect.x = self.rect.x-50
                else:
                    player_steps -= 1

            elif direction == "left" and not self.rect.x-50 < 0:
                image = pygame.image.load("sprites/player1Left.png")
                self.rect.x = self.rect.x-50
                if pygame.sprite.groupcollide(player_sprites, background_sprites, False, False):
                    print("Collided")
                    self.rect.x = self.rect.x+50
                else:
                    player_steps -= 1
            
            elif direction == "up" and not self.rect.y-50 < 0 :
                image = pygame.image.load("sprites/player1Up.png")
                self.rect.y = self.rect.y-50
                if pygame.sprite.groupcollide(player_sprites, background_sprites, False, False):
                    print("Collided")
                    self.rect.y = self.rect.y+50
            
            elif direction == "down" and not self.rect.y-50 > screenSize[1]-400:
                image = pygame.image.load("sprites/player1Down.png")
                self.rect.y = self.rect.y+50
                if pygame.sprite.groupcollide(player_sprites, background_sprites, False, False):
                    print("Collided")
                    self.rect.y = self.rect.y-50
                else:
                    player_steps -= 1
        
            self.image = image
            self.image.set_colorkey((69,255,0))
            middle_sprites.draw(game_screen)
        
        def steps():
            pass



class Terning(Csprite):
    def __init__(self, x, y):
        super().__init__(x,y,"sprites/T_start.png")

    def Roll (self):
        self.roll = random.randint(1,6)

        if self.roll == 1 or 2 or 3:
            Damage = pygame.image.load("sprites/T_damage.png")
            self.image = Damage

        elif self.roll == 4 or 5:
            Deffent = pygame.image.load("sprites/T_deffent.png")
            self.image = Deffent

        elif self.roll == 6:
            Eeveldeffent = pygame.image.load("sprites/T_eveldeffet.png")
            self.image = Eeveldeffent

        else:
            self.image = Start

    def T_move (self):
        self.nr = random.randint(1,6)
        self.image = pygame.image.load("sprites/T_" + self.nr + ".png")
        player_steps += self.nr

class map():
    def read(self, file):
        mapchars = []
        self.doorNum = 1

        with open(file, "r") as f:
            for line in f:
                for each in line.rstrip("\n"):
                    if each != " ":
                        mapchars.append(each)
                        if each == "d":
                            self.doorNum += 1
        return mapchars
    
    def getblockfield(self, x, y):
        mapRead.read("map.txt")[x*y]
        
    def assignblocks(self):
        global player
        global doorObjs
        
        mapRead = map()
        char = mapRead.read("map.txt")
        i = 0
        
        doorObjs = list()
        doorNum = 0

        for y in range(20):
            for x in range(20):
                #Road
                if char[i] == "r":
                    road = Road(x,y)
                    middle_sprites.add(road)
                    i += 1
                #Wall
                elif char[i] == "w":
                    wall = Wall(x,y)
                    background_sprites.add(wall)
                    i += 1
                #Door
                elif char[i] == "d":
                    doorObjs.append(Door(x,y))
                    entity_sprites.add(doorObjs[doorNum])
                    doorNum += 1
                    i += 1
                #player
                elif char[i] == "p":
                    road = Road(x,y)
                    middle_sprites.add(road)
                    player = Player1(x,y)
                    player_sprites.add(player)    
                    i += 1
                #baggrund
                elif char[i] == "b":
                    backgroundTile = BackgroundMenuTile(x,y)
                    background_sprites.add(backgroundTile)
                    i += 1
    
    def checkblocks(self, player_movement_direction):
        #player_coord = (player.x/50, player.y/50)
        #player_change = (1 if(player_movement_direction == "right") else -1, 1 if(player_movement_direction == "down") else -1)
        pass

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

    def prepare_test():
        # Kode som skal køre inden game loop
        drawmap = map()
        drawmap.assignblocks()
        background_sprites.draw(game_screen)
        middle_sprites.draw(game_screen)
        entity_sprites.draw(game_screen)

    def handle_input(key_name):
        print(key_name)
        if key_name == "right" or "left" or "up" or "down":
            drawmap = map()
            drawmap.checkblocks(key_name)
            player.move(key_name)
        
        if key_name == "space":
            terning1.Roll()
            terning2.Roll()
            terning3.Roll()
            terning4.Roll()
        
        if key_name == "r":
            erning_move1.T_move()
            terning_move2.T_move()

        #debug output
        if key_name == "p":
            print(doorObjs)
            print(pygame.sprite.groupcollide(player_sprites, entity_sprites, False, False))

        if key_name == "escape":
            pygame.quit()
            sys.exit(0)

    def update(screen, time):
        # Kode som køre hver update cyklus
        #  screen for at kunne få adgang til "surface"
        # time sørger for adgang til sidste opdatering af skærm
        #door.entityUpdate()
        entity_sprites.draw(game_screen)
        player_sprites.draw(game_screen)
        pygame.display.update()

   
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #           LAD VÆR MED AT RØR DET NEDEN UNDER!!!
    #
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def main():
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