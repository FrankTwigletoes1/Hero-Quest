﻿import sys, pygame, options, os, random
from enum import Enum

screenSize = (int(1000), int(1000))

player_sprites = pygame.sprite.Group() #Playeren
middle_sprites = pygame.sprite.Group() # Alle sprites som aldrig bevægere sig men opdateres
background_sprites = pygame.sprite.Group() # Vægge, alle sprites som aldrig bevæger sig eller skal opdateres
entity_sprites = pygame.sprite.Group() #Sprites som opdateres på en bestemt måde

move_exec = [] #Indeholder elementer som bliver executed når player bevæger sig f.eks. en dør lukker

class FIELDTYPE(Enum):
    NONE = None
    BACKGROUND = "b"
    DOOR = "d"
    PLAYER = "p"
    WALL = "w"
    ROAD = "r"
    ORC = "o"

class Csprite(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert()

        self.rect = self.image.get_rect()
        self.rect.x = x*50
        self.rect.y = y*50
        self.solid = False
        self.image.set_colorkey((69,255,0))
    
    def get_pos(self):
        return int(self.rect.y/50 * 20 + self.rect.x/50)
    
    def use(self):
        pass

class none(Csprite):
    def __init__(self):
        pass

class BackgroundMenuTile(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/background.png")

class Road(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/road.png")

class Background(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/baggrund.png")

class Wall(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/wall.png")
        self.solid = True

class Door(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/door.png")
        self.locked = False
    
    def use(self):
        self.open()
        #move_exec.append(self.close)
    
    def open(self):
        self.image = pygame.image.load("sprites/open_door.png")
        
    def close(self):
        self.image = pygame.image.load("sprites/door.png")
        self.solid = True

class Chest(Csprite):
    def __init__(self,x,y):
        pass

class Trap(Csprite):
    def __init__(self,x,y):
        pass

class Orc(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/orc.png")
        self.orcHealth = 1
        self.solid = True
    
    def ai_move(self):
        #self.moveTypes = ["right", "left", "up", "down"]
        #self.direction = random.choice(self.moveTypes)
        #blockinfront = map.getblockfront()
        pass
    
    def hide(self):
        pass

    def attack(self):
        pass

    def checkhealth(self):
        pass
        #if orcHealth < 0:
        #    self.kill()
    
class Player1(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/player1Down.png")
        self.steps = 0 # MIDERTIDLIG VÆRDIG INDTIL TERNINGER ER IMPLEMENTERET
        self.health = 6
        self.solid = True

    def move(self, direction):
        image = pygame.image.load("sprites/player1Down.png")
        self.direction = direction

        print("steps: " + str(self.steps))
        
        if self.steps > 0:
            front_sprite = drawmap.getblockfront(self, direction)
            front_sprite.use()
            collided = False

            if direction == "right" and self.rect.x+50 < screenSize[0]:
                image = pygame.image.load("sprites/player1Right.png")
                self.rect.x = self.rect.x+50
                if pygame.sprite.collide_rect(self, front_sprite) and self.solid and front_sprite.solid:
                    print("Collided")
                    collided = True
                    self.rect.x = self.rect.x-50
                else:
                    self.steps -= 1

            elif direction == "left" and not self.rect.x-50 < 0:
                image = pygame.image.load("sprites/player1Left.png")
                self.rect.x = self.rect.x-50
                if pygame.sprite.collide_rect(self, front_sprite) and self.solid and front_sprite.solid:
                    print("Collided")
                    collided = True
                    self.rect.x = self.rect.x+50
                else:
                    self.steps -= 1
            
            elif direction == "up" and not self.rect.y-50 < 0 :
                image = pygame.image.load("sprites/player1Up.png")
                self.rect.y = self.rect.y-50
                if pygame.sprite.collide_rect(self, front_sprite) and self.solid and front_sprite.solid:
                    print("Collided")
                    collided = True
                    self.rect.y = self.rect.y+50
                else:
                    self.steps -= 1
            
            elif direction == "down" and not self.rect.y-50 > screenSize[1]-400:
                image = pygame.image.load("sprites/player1Down.png")
                self.rect.y = self.rect.y+50
                if pygame.sprite.collide_rect(self, front_sprite) and self.solid and front_sprite.solid:
                    print("Collided")
                    collided = True
                    self.rect.y = self.rect.y-50
                else:
                    self.steps -= 1

            self.image = image
            self.image.set_colorkey((69,255,0))
            diceObjs[0].subtract(diceObjs[1].subtract()) if(not collided) else None

    def checkSight(self, x_0, y_0, x_1, y_1):
        length = max(abs(x_1 - x_0), abs(y_1-y_0))
        for i in range(0, length):
            t = float(i)/length

            x = round(x_0 * (1.0 * t) + x_1 * t)
            y = round(y_0 * (1.0 * t) + y_1 * t)
            print(drawmap.getBlockField(x,y))

    def attack(self):
        orc = drawmap.getblockfront(entity_sprites, self.direction)
        print(orc)
        
        #orc.checkHealth()
        pass

class NumDice(Csprite):
    def __init__(self, x, y):
        super().__init__(x,y,"sprites/T_start.png")
    
    def reset(self):
        self.image = pygame.image.load("sprites/T_start.png")
    
    def subtract(self, dice=None):
        if(dice == None):
            if(self.nr > 0):
                self.nr -= 1
                self.image = (pygame.image.load("sprites/T_" + str(self.nr) + ".png") if(self.nr > 0) else pygame.image.load("sprites/T_start.png"))
                return self
        return None

    def T_move (self):
        self.nr = random.randint(1,6)
        self.image = pygame.image.load("sprites/T_" + str(self.nr) + ".png")
        
        return self.nr

class Dice(Csprite):
    def __init__(self, x, y):
        super().__init__(x,y,"sprites/T_start.png")

    def Roll (self):
        self.roll = random.randint(1,6)
        if self.roll == 1 or self.roll == 2 or self.roll == 3:
            self.preimage = pygame.image.load("sprites/T_damage.png")

        elif self.roll == 4 or self.roll == 5:
            self.preimage = pygame.image.load("sprites/T_deffent.png")

        elif self.roll == 6:
            self.preimage = pygame.image.load("sprites/T_eveldeffet.png")

        else:
            self.preimage = pygame.image.load("sprites/T_start.png")
        self.image = self.preimage

class map():
    def read(self, file):
        mapchars = []
        self.doorNum = 1
        with open(file, "r") as f:
            for line in f:
                for each in line.rstrip("\n"):
                    if each != " ":
                        mapchars.append(each)
                        if each == FIELDTYPE.DOOR:
                            self.doorNum += 1
        return mapchars

    def getspritefromcoord(self, coord):
        sprite_list = [player_sprites, entity_sprites, middle_sprites, background_sprites]

        for sprite_type in sprite_list:
            for sprite_individual in sprite_type.sprites():
                if(sprite_individual.get_pos() == coord):
                    return sprite_individual
        
        return none()

    def getblockfield(self, x, y):
        return self.getspritefromcoord(int(y * 20 + x))
        
    def assignblocks(self):
        global player
        global doorObjs
        global diceObjs
        global orcObjs
        
        char = self.read("map.txt")
        i = 0
        diceObjs = list()
        doorObjs = list()
        orcObjs = list()
        orcNum = 0
        doorNum = 0
        diceNum = 0

        for y in range(20):
            for x in range(20):
                #Road
                if char[i] == "r":
                    road = Road(x,y)
                    middle_sprites.add(road)

                    if random.randint(1,20) == 1:
                        orcObjs.append(Orc(x,y))
                        entity_sprites.add(orcObjs[orcNum])
                        orcNum += 1
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

                #terning
                elif char[i] == "t":
                    backgroundTile = BackgroundMenuTile(x,y)
                    background_sprites.add(backgroundTile)
                    diceObjs.append(Dice(x,y))
                    entity_sprites.add(diceObjs[diceNum])
                    diceNum += 1
                    i += 1

                #terningNum  
                elif char[i] == "n":
                    backgroundTile = BackgroundMenuTile(x,y)
                    background_sprites.add(backgroundTile)
                    diceObjs.append(NumDice(x,y))
                    entity_sprites.add(diceObjs[diceNum])
                    diceNum += 1
                    i += 1
    
    def getblockfront(self, entity, movement_direction):
        entity_coord = [entity.rect.x/50, entity.rect.y/50]
        entity_change_horizontal = 1 if(movement_direction == "right") else -1 if(movement_direction == "left") else 0
        entity_change_vertical = 1 if(movement_direction == "down") else -1 if(movement_direction == "up") else 0
        entity_coord_new = [a + b for a, b in zip(entity_coord, [entity_change_horizontal, entity_change_vertical])]
        
        return self.getblockfield(entity_coord_new[0], entity_coord_new[1])

class main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Hero Quest Digital')

        self.game_screen = pygame.display.set_mode(screenSize)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.prepare_test()
        self.loop()

    def turn(self):
        if player.steps < 0:
            return "orcTurn"
        elif player.steps > 0:
            return "playerTurn"

    # Kører spillet i et loop indtil spilleren trykker esc, hvilket lukker spillet
    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    self.handle_input(key_name)

            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000.0
            self.update(self.game_screen, seconds)

            sleep_time = (1000.0 / self.fps) - milliseconds
            pygame.time.wait(int(sleep_time)) if(sleep_time > 0.0) else pygame.time.wait(1)
    
    # Kode som skal køre inden game loop
    def prepare_test(self):
        global drawmap 
        drawmap = map()
        drawmap.assignblocks()
        background_sprites.draw(self.game_screen)

    # Kode som køre hver update cyklus
    # screen for at kunne få adgang til "surface"
    # time sørger for adgang til sidste opdatering af skærm
    # door.entityUpdate()
    def update(self, screen, time):
        middle_sprites.draw(self.game_screen)
        entity_sprites.draw(self.game_screen)
        player_sprites.draw(self.game_screen)
        pygame.display.update()

    def handle_input(self, key_name):
        if self.turn() == "playerTurn":
            if key_name == "right" or "left" or "up" or "down":
                for func in move_exec:
                    func()
                move_exec.clear()
                player.move(key_name)
        
        if key_name == "space":
            player.attack()

        if key_name == 'h':
            for x in orcObjs:
                x.hide()
        
        if key_name == "r":
            if(player.steps == 0):
                player.steps = diceObjs[0].T_move() + diceObjs[1].T_move()

        #debug output
        if key_name == "p":
            print(diceObjs)
            print(doorObjs)
            print(pygame.sprite.groupcollide(player_sprites, entity_sprites, False, False))
            print(background_sprites.sprites())

        if key_name == "escape":
            pygame.quit()
            sys.exit(0)

main()