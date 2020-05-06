import sys, pygame, options, os, random
from enum import Enum

screen_size_x = 1000
screen_size_y = 1000
screenSize = (screen_size_x, screen_size_y)

player_sprites = pygame.sprite.Group() #Playeren
middle_sprites = pygame.sprite.Group() # Alle sprites som aldrig bevægere sig men opdateres
background_sprites = pygame.sprite.Group() # Vægge, alle sprites som aldrig bevæger sig eller skal opdateres
entity_sprites = pygame.sprite.Group() #Sprites som opdateres på en bestemt måde

move_exec = [] #Indeholder elementer som bliver executed når player bevæger sig f.eks. en dør lukker
time_exec = [] #Indeholder elementer som bliver executed efter et stykke tid

class FIELDTYPE(Enum):
    NONE = None
    BACKGROUND = "b"
    DOOR = "d"
    PLAYER = "p"
    WALL = "w"
    ROAD = "r"
    ORC = "o"

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
def render_text(display, font, text, color_rgb, x = None, y = None, offsetx = 0, offsety = 0, alignment=None, effects=None, relative = False):

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
    x = (screen_size_x / 2 - renderfont.get_width() / 2) if(x is None) else (x - renderfont.get_width() / 2) if(relative) else x # Text horizontal position: center | relative | absolute
    y = (screen_size_y / 2 - renderfont.get_height() / 2) if (y is None) else (y - renderfont.get_height() / 2) if(relative) else y # Text vertical position: center | relative | absolute

    # Aligns the text if any are defined
    if(alignment is not None):
        if("left" in alignment):
            x = 0
        elif("right" in alignment):
            x = screen_size_x - renderfont.get_width()
        if("top" in alignment):
            y = 0
        elif("bottom" in alignment):
            y = screen_size_y - renderfont.get_height()

    # Renders the text to screen
    display.blit(renderfont, (x + offsetx, y + offsety))

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

    def move_to(self, x, y):
        self.rect.x = x*50
        self.rect.y = y*50

    def __str__(self):
        return self.__class__.__name__

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
        self.opened = False
        self.solid = True
    
    def use(self):
        if(not self.opened):
            self.open()
        else:
            self.close()
    
    def open(self):
        self.image = pygame.image.load("sprites/open_door.png")
        self.solid = False
        self.opened = True
        
    def close(self):
        self.image = pygame.image.load("sprites/door.png")
        self.solid = True
        self.opened = False

class Trap(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y, "sprites/road.png")
        self.solid = False
        self.visible = False
    
    def release(self):
        self.visible = True
        self.image = pygame.image.load("sprites/trap.png")
        player.damage(1)
        player.frozen = True
        time_exec.append({"start_time": pygame.time.get_ticks(), "delay": 1000, "func": self.destroy})
    
    def destroy(self):
        player.frozen = False
        self.kill()

    def use(self):
        if(not self.visible):
            self.visible = True
            self.image = pygame.image.load("sprites/trap.png")
        else:
            self.kill()

class Orc(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/orc.png")
        self.health = 2
        self.solid = True
        self.direction = "left"
    
    def move_random(self):
        open_areas_around = drawmap.getblocksaround(self, Road, returnobject=True, returnarray=True)
        random_area = random.choice(open_areas_around)
        entity_area = drawmap.getblockfield(random_area.rect.x/50, random_area.rect.y/50)

        if(isinstance(entity_area, Road)):
            self.move_to(random_area.rect.x/50, random_area.rect.y/50)
    
    def hide(self):
        pass

    def damage(self, damage):
        self.health -= damage

        if(self.health <= 0):
            self.kill()
    
class Player1(Csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/player1Down.png")
        self.steps = 0
        self.health = 6
        self.attack = 1
        self.solid = True
        self.frozen = False
        self.direction = "left"

    def move(self, direction):
        image = pygame.image.load("sprites/player1Down.png")
        self.direction = direction

        print("steps: " + str(self.steps))
        
        if self.steps > 0:
            front_sprite = drawmap.getblockfront(self, direction)
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
        length = max(abs(x_1 - x_0), abs(y_1 - y_0))
        for i in range(0, length):
            t = float(i)/length

            x = round(x_0 * (1.0 * t) + x_1 * t)
            y = round(y_0 * (1.0 * t) + y_1 * t)
            print(drawmap.getBlockField(x,y))

    def damage(self, damage):
        self.health -= damage

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

    def reset(self):
        self.image = pygame.image.load("sprites/T_start.png")

    def roll(self):
        self.nr = random.randint(1,6)
        self.image = pygame.image.load("sprites/T_start.png")

        if self.nr < 4:
            self.image = pygame.image.load("sprites/T_damage.png")

        elif self.nr == 4 or self.nr == 5:
            self.image = pygame.image.load("sprites/T_deffent.png")

        elif self.nr == 6:
            self.image = pygame.image.load("sprites/T_eveldeffet.png")
        
        return self.nr

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
    
    # form (0=around, 1=cross)
    def getblocksaround(self, sprite1, sprite2type, radius=1, returnobject=False, returnarray=False,form=0):
        entity_array = []
        form_cross_disallowed = [(-1,-1),(1,1),(-1,1),(1,-1)]

        for i in range(-1 * radius, radius + 1):
            for j in range(-1 * radius, radius + 1):
                if(form == 0 or ((i, j) not in form_cross_disallowed and form == 1)):
                    entity_coord = [sprite1.rect.x/50, sprite1.rect.y/50]
                    entity_coord_new = [a + b for a, b in zip(entity_coord, [i, j])]
                    entity_around = self.getblockfield(entity_coord_new[0], entity_coord_new[1])
                    
                    if(isinstance(entity_around, sprite2type)):
                        if(returnarray and returnobject):
                            entity_array.append(entity_around)
                        else:
                            return (True if(not returnobject) else entity_around)
        
        return entity_array

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
        trapObjs = list()
        orcNum = 0
        doorNum = 0
        diceNum = 0
        trapNum = 0

        for y in range(20):
            for x in range(20):
                #Road
                if char[i] == "r":
                    road = Road(x,y)
                    middle_sprites.add(road)

                    if not bool(random.randint(0,20)):
                        orcObjs.append(Orc(x,y))
                        entity_sprites.add(orcObjs[orcNum])
                        orcNum += 1

                    elif not bool(random.randint(0,50)):
                        trapObjs.append(Trap(x,y))
                        entity_sprites.add(trapObjs[trapNum])
                        trapNum += 1
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

        self.font_p1 = pygame.font.SysFont('Roboto', 100)
        self.font_p2 = pygame.font.SysFont('Roboto', 80)
        self.font_p3 = pygame.font.SysFont('Roboto', 60)
        self.font_p4 = pygame.font.SysFont('Roboto', 40)
        self.font_p5 = pygame.font.SysFont('Roboto', 20)

        self.game_screen = pygame.display.set_mode(screenSize)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.player_turn = True
        self.dice_round_step_rolled = False
        self.battlemode = False
        self.bar_message = "Movement - Press 'r' to roll dice"
        self.prepare_test()
        self.loop()

    # Kører spillet i et loop indtil spilleren trykker esc, hvilket lukker spillet
    def loop(self):
        global time_exec

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

            for i in list(time_exec):
                if(len(time_exec) and (i["start_time"] + i["delay"]) < pygame.time.get_ticks()):
                    i["func"]()
                    time_exec.remove(i)
    
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
        render_text(self.game_screen, self.font_p4, self.bar_message, (255,255,255), y=775)
        render_text(self.game_screen, self.font_p4, "arrow keys = movement", (255,255,255), y=800, offsetx=10, alignment="left")
        render_text(self.game_screen, self.font_p4, "r=dice roll", (255,255,255), y=835, offsetx=10, alignment="left")
        render_text(self.game_screen, self.font_p4, "a=attack roll", (255,255,255), y=870, offsetx=10, alignment="left")
        render_text(self.game_screen, self.font_p4, "e=use", (255,255,255), y=905, offsetx=10, alignment="left")
        pygame.display.update()

    def handle_input(self, key_name):
        if(self.player_turn):
            if(not self.battlemode):
                if((key_name == "right" or key_name == "left" or key_name =="up" or key_name == "down") and self.dice_round_step_rolled and not player.frozen):
                    front_sprite = drawmap.getblockfront(player, key_name)
                    for func in move_exec:
                        func()
                    move_exec.clear()
                    player.move(key_name)
                    front_sprite.release() if(isinstance(front_sprite, Trap)) else None
                    self.player_turn = (True if(player.steps > 0) else False)
                    self.bar_message = "Movement - Press 'r' to roll dice" if(not self.player_turn) else None
                    self.handle_input(None) if(not self.player_turn) else None
                    battle_enemy = drawmap.getblocksaround(player, Orc, returnobject=True)

                    if(battle_enemy):
                        self.battlemode = True
                        self.battleenemy = battle_enemy
                        self.bar_message = "In battle - Press 'a' to roll dice"
                
                if key_name == "r":
                    if(player.steps == 0):
                        player.steps = diceObjs[0].T_move() + diceObjs[1].T_move()
                        self.dice_round_step_rolled = True
                        self.bar_message = ""
                        background_sprites.draw(self.game_screen)
                
                if key_name == "e":
                    drawmap.getblockfront(player, player.direction).use()

                #debug output
                if key_name == "p":
                    print(diceObjs)
                    print(doorObjs)
                    print(pygame.sprite.groupcollide(player_sprites, entity_sprites, False, False))
                    print(background_sprites.sprites())
            else:
                if key_name == "a":
                    player_roll = diceObjs[2].roll()
                    enemy_roll = diceObjs[3].roll()
                    player.damage(1) if(enemy_roll < 4 and (enemy_roll != 4 or enemy_roll != 5)) else None
                    self.battleenemy.damage(1) if(player_roll < 4 and (player_roll != 4 or player_roll != 5)) else None
                    print("phealth: " + str(player.health) + ", ehealth:" + str(self.battleenemy.health))
                    
                    if(player.health == 0 or self.battleenemy.health == 0):
                        diceObjs[2].reset()
                        diceObjs[3].reset()
                        self.battlemode = False
                        self.battleenemy = None
                        self.bar_message = ""
                        background_sprites.draw(self.game_screen)

        else:
            for entities in entity_sprites.sprites():
                entities.move_random() if(isinstance(entities, Orc)) else None

            self.player_turn = True
            self.dice_round_step_rolled = False

        if key_name == "escape":
            pygame.quit()
            sys.exit(0)
        
        #if key_name == 'h':
        #    for x in orcObjs:
        #        x.hide()

main()