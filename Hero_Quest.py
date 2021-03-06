﻿#Importerer de forskellige biblioteker brugt i programmet
import sys, pygame, options, os, random

#Slå debug beskeder fra eller til
debug = False
class null():
    def write(self, arg):
        pass

if not debug:
    sys.stdout = null()

#Starter pygame 
pygame.init()
pygame.font.init()

# Definerer spillets vindues størrelse
screen_size_x = 1000
screen_size_y = 1000
screensize = (screen_size_x, screen_size_y)

# Sprite grupper der hver især indeholder forskellige typer af sprites adskildt af funktionalitet
player_sprites = pygame.sprite.Group() #Playeren
middle_sprites = pygame.sprite.Group() # Alle sprites som aldrig bevægere sig men opdateres
background_sprites = pygame.sprite.Group() # Vægge, alle sprites som aldrig bevæger sig eller skal opdateres
entity_sprites = pygame.sprite.Group() #Sprites som opdateres på en bestemt måde

# Globale variabler der indeholder variabler der skal sættes eller funktioner som skal kaldes ved specielle serværdigheder
move_exec = [] #Indeholder elementer som bliver executed når player bevæger sig f.eks. en dør lukker
time_exec = [] #Indeholder elementer som bliver executed efter et stykke tid

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

    # Tegner effekter på teksten hvis noget er blevet defineret
    if (effects is not None):
        if ("bold" in effects):
            font.set_bold(True)
        if("italic" in effects):
            font.set_italic()
        if("underline" in effects):
            font.set_underline(True)

    # Skaber font objektet og x og y koordinaterne baseret på argumenterne brugt
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

#Virker som et blueprint på hvordan vores sprite objekter er bygget op som vi kan referer til
#Når refere til csprite så arver objektet vi refere i, alle variablerne fra csprite
class csprite(pygame.sprite.Sprite):
    def __init__(self,x,y,image, rotate=None):
        pygame.sprite.Sprite.__init__(self)

        # Sætter objektets variabler
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x*50
        self.rect.y = y*50
        self.solid = False
        self.image.set_colorkey((69,255,0))

        # Roter spritens billede hvis defineret
        if(rotate is not None):
            self.image = pygame.transform.rotate(self.image, rotate)
    
    # Retunerer et objekts position i verdenen i forhold til strukturen af mapfilen
    # Hvert bane er opbygget i et 20x20 grid hvor hvert sprite i rækken læses fra venstre mod højre, oppe til ned
    # Objekt (2,2) ville derfor være 2*20 + 2 = 42'erne objekt i rækken fra top-venstre hjørne
    def get_pos(self):
        return int(self.rect.y/50 * 20 + self.rect.x/50)
    
    # Fallback, da alle objekter kan teknisk set bruges af spilleren, selvom at som standard alle objekter har ingen funktion
    # Bruges når spilleren bruger et objekt med ingen funktionalitet
    def use(self):
        pass

    # Flytter et objekt til denne given position på brættet
    def move_to(self, x, y):
        self.rect.x = x*50
        self.rect.y = y*50

    # Hvis objektet printes til skærmen, returnere objektets navn
    def __str__(self):
        return self.__class__.__name__

# Et fallback objekt, bruges når intet andet kan retuneres af objekter
class none(csprite):
    def __init__(self):
        pass

# En menu baggrund for hvor spillerens informationer befinder sig i bund baren
class backgroundmenutile(csprite):
    def __init__(self,x,y, rotate):
        super().__init__(x,y,"sprites/background.png", rotate)

# En ikke-solid vej, alle objekter med funktioner kan stå her
class road(csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/road.png")

# En ikke-solid trappe, alle objekter med funktioner kan stå her go er hvor spilleren starter
class staircase(csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/trappe.png")

# En menu baggrund for bund baren 
class background(csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/baggrund.png")

# En solid væg, ingen kan bevæge sig igennem dette objekt
class wall(csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/wall.png")
        self.solid = True

# En kiste, spilleren skal transporter dette objekt fra dets position til spawnpoint
class chest(csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/chest.png")
        self.solid = True
    
    # Hvis spilleren bruger kisten, angiv at spilleren har samlet den op
    def use(self):
        player.goalpickup = True
        self.kill()

# Dører spilleren kan åbne/lukke og gå igennem
class door(csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/door.png")
        self.locked = False
        self.opened = False
        self.solid = True
    
    # tillader spileren at åbne døren hvis den er lukket, ellers luk døren hvis åben
    def use(self):
        self.open() if(not self.opened) else self.close()
    
    # Åbner døren så spilleren kan gå igennem
    def open(self):
        self.image = pygame.image.load("sprites/open_door.png")
        self.solid = False
        self.opened = True
    
    # Luk døren så spilleren ikke kan gå igennem
    def close(self):
        self.image = pygame.image.load("sprites/door.png")
        self.solid = True
        self.opened = False

# En fælde spilleren kan træde i som vil skade
# Spilleren kan også disarmerer fælden ved at trykke 'e' foran to gange i træk
class trap(csprite):
    def __init__(self,x,y):
        super().__init__(x,y, "sprites/road.png")
        self.solid = False
        self.visible = False
    
    # Hvis spilleren træder i fælden, skad spilleren 
    # Fryser spillerens position for en bestemt mængde tid
    def release(self):
        self.visible = True
        self.image = pygame.image.load("sprites/trap.png")
        player.damage(1)
        player.frozen = True
        time_exec.append({"start_time": pygame.time.get_ticks(), "delay": 1000, "func": self.destroy})
    
    # Ødelægger fælden og optøger spilleren
    def destroy(self):
        player.frozen = False
        self.kill()

    # Spilleren kan disarmerer fælden som vil fjerne den permanent
    def use(self):
        if(not self.visible):
            self.visible = True
            self.image = pygame.image.load("sprites/trap.png")
        else:
            self.kill()

# En ogre, fjende imod spilleren
class orc(csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/orc.png")
        self.health = 2
        self.solid = True
        self.direction = "left"
    
    # Bevæger ogren til et tilfældig område af otte fælder omkring sig hvor der er plads (vej)
    def move_random(self):
        movement_blocks = drawmap.getblocksaround(self, road, returnobject=True, returnarray=True)

        if(not len(movement_blocks) or random.randint(0,20)):
            random_area = random.choice(movement_blocks)
            self.move_to(random_area.rect.x/50, random_area.rect.y/50)

    # Skader ogren
    def damage(self, damage):
        self.health -= damage

        # Dræb ogren hvis den intet helbred har tilbage
        if(self.health <= 0):
            self.kill()

#Player objektet, protagonisten i spillet
class player(csprite):
    def __init__(self,x,y):
        super().__init__(x,y,"sprites/player1Down.png")
        self.steps = 0 # Antallet af trin tilbage spilleren kan flytte sig
        self.health = 6 # Spillerens helbred
        self.attack = 1 # Skaden spilleren giver til ogrene
        self.solid = True # Spilleren er solid i forhold til andre objekter og omvendt
        self.frozen = False # En frosset spiller kan ikke bevæge sig
        self.direction = "left" # Hvilken retning spilleren vender
        self.spawnpoint = self.get_pos() # Positionen på brættet spilleren startede
        self.goalpickup = False # Har spilleren opsamlet kisten?

    #Bevægelse funktion som sørger tjekker om prøver at gå igennem en solid eller ej,
    #Den har direction som input altså om den vil gå op eller ned ad y og frem eller tilbage på x
    def move(self, direction):
        image = pygame.image.load("sprites/player1Down.png")
        self.direction = direction
        
        # Flyt kun spilleren hvis der er flere trin tilbage
        if self.steps > 0:
            front_sprite = drawmap.getblockfront(self, direction)
            collided = False

            if direction == "right" and self.rect.x+50 < screensize[0]: #Tjekker retningen og om den går ud over mappet
                image = pygame.image.load("sprites/player1Right.png") #loader et nyt billede som peger i den rigtige retning
                self.rect.x = self.rect.x+50 #Bevæger playeren
                if pygame.sprite.collide_rect(self, front_sprite) and self.solid and front_sprite.solid: #Tjekker om den er gået ind i en solid block/tile
                    collided = True
                    self.rect.x = self.rect.x-50 # Hvis den colider så sætter den playeren tilbage på de tidligere koordinater
                else:
                    self.steps -= 1 # hvis den ikke var solid fjerner det en af stepsene

            elif direction == "left" and not self.rect.x-50 < 0:
                image = pygame.image.load("sprites/player1Left.png")
                self.rect.x = self.rect.x-50
                if pygame.sprite.collide_rect(self, front_sprite) and self.solid and front_sprite.solid:
                    collided = True
                    self.rect.x = self.rect.x+50
                else:
                    self.steps -= 1
            
            elif direction == "up" and not self.rect.y-50 < 0 :
                image = pygame.image.load("sprites/player1Up.png")
                self.rect.y = self.rect.y-50
                if pygame.sprite.collide_rect(self, front_sprite) and self.solid and front_sprite.solid:
                    collided = True
                    self.rect.y = self.rect.y+50
                else:
                    self.steps -= 1
            
            elif direction == "down" and not self.rect.y-50 > screensize[1]-400:
                image = pygame.image.load("sprites/player1Down.png")
                self.rect.y = self.rect.y+50
                if pygame.sprite.collide_rect(self, front_sprite) and self.solid and front_sprite.solid:
                    collided = True
                    self.rect.y = self.rect.y-50
                else:
                    self.steps -= 1

            self.image = image
            self.image.set_colorkey((69,255,0))
            diceObjs[0].subtract(diceObjs[1].subtract()) if(not collided) else None

    #Bliver kaldt af orkerne når playeren skal skades.
    def damage(self, damage):
        self.health -= damage

#Class som håndtere terningerne som kastes når playeren skal have nye skridt.
class NumDice(csprite):
    def __init__(self, x, y):
        super().__init__(x,y,"sprites/T_start.png")

    #Bliver kaldet når playeren har bevæget sig og trækker et tal fra terningerne
    def subtract(self, dice=None):
        if(dice == None):
            if(self.nr > 0):
                self.nr -= 1
                self.image = (pygame.image.load("sprites/T_" + str(self.nr) + ".png") if(self.nr > 0) else pygame.image.load("sprites/T_start.png"))
                return self
        return None

    #Bliver kaldet når playeren ruller med movement terningerne for at give flere playersteps
    def T_move(self):
        self.nr = random.randint(1,6)
        self.image = pygame.image.load("sprites/T_" + str(self.nr) + ".png")
        
        return self.nr

#Angribsterningerne
class Dice(csprite):
    def __init__(self, x, y):
        super().__init__(x,y,"sprites/T_start.png")

    #Resetter terningerne til deres default billede
    def reset(self):
        self.image = pygame.image.load("sprites/T_start.png")

    #Ruller terningnerne og returnere resultatet
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

#Objektet som står for map håndtering, altså indlæsning af map og hente data fra mappet
class map():

    #Læser mappet fra en fil, tilemap baseret
    def read(self, file):
        mapchars = []
        with open(file, "r") as f:
            for line in f:
                for each in line.rstrip("\n"):
                    if each != " ":
                        mapchars.append(each)
        return mapchars

    #Tjekker efter en sprite på et bestemt koordinat
    def getspritefromcoord(self, coord):
        sprite_list = [player_sprites, entity_sprites, middle_sprites, background_sprites]

        #Går igennem alle sprite typerne
        for sprite_type in sprite_list:

            #finder de individuelle sprites
            for sprite_individual in sprite_type.sprites():
                if(sprite_individual.get_pos() == coord): # hvis spriten er på de bestemer koordinater så returner spriten
                    return sprite_individual
        
        return none()

    #Finder sprite på bestemt x og y koordinat i stedet for at tjekke alle koordinater ligesom getspritefromcoord
    def getblockfield(self, x, y):
        return self.getspritefromcoord(int(y * 20 + x))
    
    # Finder alle blocks i enten en radius omkring et objekt eller i et kryds.
    def getblocksaround(self, sprite1, sprite2type, radius=1, returnobject=False, returnarray=False, form=0):
        entity_array = []
        form_cross_disallowed = [(-1,-1),(1,1),(-1,1),(1,-1)]


        for i in range(-1 * radius, radius + 1):
            for j in range(-1 * radius, radius + 1):
                if(form == 0 or ((i, j) not in form_cross_disallowed and form == 1)):
                    entity_coord = [sprite1.rect.x/50, sprite1.rect.y/50]
                    entity_coord_new = [a + b for a, b in zip(entity_coord, [i, j])]
                    
                    if(entity_coord_new[0] >= 0 and entity_coord_new[1] >= 0):
                        entity_around = self.getblockfield(entity_coord_new[0], entity_coord_new[1])
                        
                        if(isinstance(entity_around, sprite2type)):
                            if(returnarray and returnobject):
                                entity_array.append(entity_around)
                            else:
                                return (True if(not returnobject) else entity_around)
        
        return entity_array

    #pladsere tilemappet/alle blocks på mappet
    def assignblocks(self):

        # Globale variabler tilgængeligt overalt
        global player
        global doorObjs
        global diceObjs
        global orcObjs
        
        # Indlæser banen og sætter variabler som bruges ved genereringen af objekterne på kortet
        char = self.read("map.txt")
        i = 0
        goal_spawned = 0
        spawnpoint_created = 0
        x_count = 0
        diceObjs = list()
        doorObjs = list()
        orcObjs = list()
        trapObjs = list()
        orcNum = 0
        doorNum = 0
        diceNum = 0
        trapNum = 0
        
        # Looper igennem rækker og kolonner for kortet og skaber objekter for alle definitionerne afhængig af typen
        for y in range(20):
            for x in range(20):

                # Skaber vejene som elementer kan starte på og spilleren/ogre kan bevæge sig rundt på
                if char[i] == "r":
                    middle_sprites.add(road(x,y))

                    # Der er 1/20 chance for at en ogre starter her
                    if not bool(random.randint(0,20)):
                        orcObjs.append(orc(x,y))
                        entity_sprites.add(orcObjs[orcNum])
                        orcNum += 1

                    # Der er 1/50 chance for at en usynlig fælde starter her
                    elif not bool(random.randint(0,50)):
                        trapObjs.append(trap(x,y))
                        entity_sprites.add(trapObjs[trapNum])
                        trapNum += 1

                # Skaber kisten og trappen hvor spilleren starter, tilfældig indenfor 4 forskellige positioner
                elif char[i] == "x":
                    middle_sprites.add(road(x,y))
                    
                    # Skaber kisten med en sansynlighed på 1/4 hvis spilleren ikke allerede starter her eller hvis det er den næst sidste 
                    if goal_spawned == 0 and spawnpoint_created != x_count and (random.randint(0,1) == 0 or x_count == 2):
                        entity_sprites.add(chest(x,y))
                        goal_spawned = x_count
                    
                    # Skaber spilleren med en sansyndlighed på 1/4 hvis kisten ikke allerede starter her eller hvis det er den sidste position at kunne starte
                    if spawnpoint_created == 0 and goal_spawned != x_count and (random.randint(0,2) == 0 or x_count == 3):
                        entity_sprites.add(staircase(x,y))
                        spawnpoint_created = x_count
                        player = player(x,y)
                        player_sprites.add(player)
                    
                    # Tæller start positionen up
                    x_count += 1
                    
                # Solide vægge ingen kan bevæge sig igennem
                elif char[i] == "w":
                    background_sprites.add(wall(x,y))

                # Skaber døre som spilleren kan åbne/lukke og giver adgang til aflukkede områder
                elif char[i] == "d":
                    doorObjs.append(door(x,y))
                    entity_sprites.add(doorObjs[doorNum])
                    doorNum += 1

                # Skaber en baggrund for menu baren i bunden af skærmen hvor terningerne, tekst information og status fremgår
                elif char[i] == "b" or char[i] == "q":
                    background_sprites.add(backgroundmenutile(x,y, (90 if(char[i] == "q") else None)))

                # Skaber kamp terninger, som spilleren og ogre bruger til at slås med
                elif char[i] == "t":
                    background_sprites.add(backgroundmenutile(x,y, None))
                    diceObjs.append(Dice(x,y))
                    entity_sprites.add(diceObjs[diceNum])
                    diceNum += 1

                # Skaber bevægelsesterninger for spilleren, hvor 
                elif char[i] == "n":
                    background_sprites.add(backgroundmenutile(x,y, None))
                    diceObjs.append(NumDice(x,y))
                    entity_sprites.add(diceObjs[diceNum])
                    diceNum += 1
                
                # Tæller op antallet af objekter skabt
                i += 1
    
    # Retunere objektet i en bestemt retning i forhold til et andet f.eks. højre sprite for spilleren
    def getblockfront(self, entity, movement_direction):
        entity_coord = [entity.rect.x/50, entity.rect.y/50]
        entity_change_horizontal = 1 if(movement_direction == "right") else -1 if(movement_direction == "left") else 0
        entity_change_vertical = 1 if(movement_direction == "down") else -1 if(movement_direction == "up") else 0
        entity_coord_new = [a + b for a, b in zip(entity_coord, [entity_change_horizontal, entity_change_vertical])]
        
        return self.getblockfield(entity_coord_new[0], entity_coord_new[1])

# Den primære spil klasse; opsætter, kører og sammenkobler de forskellige spil elementer der får det til at fungerer
class main():

    # Opsætter spillet og alle de vigtige lokale variabler
    def __init__(self):
        pygame.display.set_caption('Hero Quest Digital')

        self.font_p1 = pygame.font.SysFont('Roboto', 100)
        self.font_p2 = pygame.font.SysFont('Roboto', 80)
        self.font_p3 = pygame.font.SysFont('Roboto', 60)
        self.font_p4 = pygame.font.SysFont('Roboto', 40)
        self.font_p5 = pygame.font.SysFont('Roboto', 20)
        self.game_screen = pygame.display.set_mode(screensize)
        self.clock = pygame.time.Clock()
        self.player_turn = True
        self.game_running = True
        self.dice_round_step_rolled = False
        self.battlemode = False
        self.bar_message = "Movement - Press 'r' to roll dice"
        self.prepare_test()
        self.loop()

    # Kører spillet i et loop indtil spilleren trykker esc eller spilleren dør, hvilket lukker spillet
    def loop(self):
        global time_exec
        
        while self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.handle_input(pygame.key.name(event.key))
                    background_sprites.draw(self.game_screen)

            self.update()

            for i in list(time_exec):
                if(len(time_exec) and (i["start_time"] + i["delay"]) < pygame.time.get_ticks()):
                    if("func" in i):
                        i["func"]()

                    elif("var" in i):
                        i["var"] = i["value"]

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
    def update(self):

        # Tegner alle sprite grupperne til skærmen
        middle_sprites.draw(self.game_screen)
        entity_sprites.draw(self.game_screen)
        player_sprites.draw(self.game_screen)

        # Skriver tekst til skærmen med yderligere formattering der gør det let at kontrollerer
        render_text(self.game_screen, self.font_p4, self.bar_message, (255,255,255), offsety=-50, alignment="bottom")
        render_text(self.game_screen, self.font_p4, "health: " + str(player.health), (255,255,255), offsetx=70, offsety=-160, alignment="left, bottom")
        render_text(self.game_screen, self.font_p4, "damage: " + str(player.attack), (255,255,255), offsetx=70, offsety=-130, alignment="left, bottom")
        render_text(self.game_screen, self.font_p4, "facing: " + player.direction, (255,255,255), offsetx=70, offsety=-100, alignment="left, bottom")
        render_text(self.game_screen, self.font_p5, "movement dice", (255,255,255), offsetx=-305, offsety=-200, alignment="right, bottom")
        render_text(self.game_screen, self.font_p5, "player attack dice", (255,255,255), offsetx=-70, offsety=-200, alignment="right, bottom")
        render_text(self.game_screen, self.font_p5, "enemy attack dice", (255,255,255), offsetx=-70, offsety=-100, alignment="right, bottom")
        render_text(self.game_screen, self.font_p5, "arrow keys: movement", (255,255,255), offsetx=10, offsety=-55, alignment="left, bottom")
        render_text(self.game_screen, self.font_p5, "r: dice roll", (255,255,255), offsetx=10, offsety=-40, alignment="left, bottom")
        render_text(self.game_screen, self.font_p5, "a: attack roll", (255,255,255), offsetx=10, offsety=-25, alignment="left, bottom")
        render_text(self.game_screen, self.font_p5, "e: use", (255,255,255), offsetx=10, offsety=-10, alignment="left, bottom")
        
        # Opdaterer spil displayed, hvilket tegner alle sprites til skærmen
        pygame.display.update()

    #Håndterer alle spiller input
    def handle_input(self, key_name):

        # Hvis spilleren trykker escape, luk spillet
        if key_name == "escape":
            pygame.quit()
            sys.exit(0)

        # Hvis det er spillerens tur
        if(self.player_turn):

            # Hvis spilleren ikke er i en kamp mod en ogre
            if(not self.battlemode):

                # Trykker spilleren piletasterne, og samtidig har rullet bevægelsesterningerne og ikke er fråset af en fælde, flyt spilleren hvis muligt
                if((key_name == "right" or key_name == "left" or key_name =="up" or key_name == "down") and self.dice_round_step_rolled and not player.frozen):

                    # Kør funktioner som skal kaldes når spilleren bevæger sig
                    # For eksempel en spiller kan have åbnet en dør som skal lukke automatisk efterfølgende
                    for func in move_exec:
                        func()
                    move_exec.clear()

                    # Få spriten som spilleren skal til at træde på, er det en fælde så aktiver den
                    front_sprite = drawmap.getblockfront(player, key_name)
                    front_sprite.release() if(isinstance(front_sprite, trap)) else None

                    # Test og flyt spilleren hvis muligt
                    player.move(key_name)

                    # Hvis spilleren ikke har flere trin tilbage fra bevægelsesterningerne, oplys spilleren
                    self.player_turn = (True if(player.steps > 0) else False)
                    self.bar_message = "Movement - Press 'r' to roll dice" if(not self.player_turn) else None
                    self.handle_input(None) if(not self.player_turn) else None

                    # Check efter ogre omkring spilleren, checker i form at et krys
                    battle_enemy = drawmap.getblocksaround(player, orc, returnobject=True, form=1)
                    
                    # Har spilleren stødt på en ogre, start en kamp
                    if(battle_enemy):
                        self.battlemode = True
                        self.battleenemy = battle_enemy
                        self.bar_message = "In battle - Press 'a' to roll dice"
                    
                    # Er spilleren ved spawn med kisten opsamlet, spilleren vinder!, afslut spillet
                    elif(player.spawnpoint == player.get_pos() and player.goalpickup):
                        self.game_running = False
                
                # Hvis spilleren trykker 'r' tasten, genkaster terningerne
                if key_name == "r":

                    # Giv kun tilladelse til at kaste terningerne hvis man ikke har flere trin tilbage
                    if(player.steps == 0):
                        player.steps = diceObjs[0].T_move() + diceObjs[1].T_move()
                        self.dice_round_step_rolled = True
                        self.bar_message = ""
                
                # Trykker bruger knappen 'e' for at bruge objektet foran spillerens karakter
                if key_name == "e":

                    # Finder objektet foran spilleren og ser om spilleren kan bruge det
                    sprite_use = drawmap.getblockfront(player, player.direction)
                    sprite_use.use()

                    # Hvis objektet er en kiste, giv en besked om hvordan man vinder
                    if(isinstance(sprite_use, chest)):
                        self.bar_message = "Chest taken - Get to spawnpoint for victory!"
                        time_exec.append({"start_time": pygame.time.get_ticks(), "delay": 2000, "var": self.bar_message, "value": ""})

            # Hvis spilleren ér i en kamp mod en ogre
            else:
                if key_name == "a":

                    # Kaster kamp terningerne for spilleren og ogren 
                    player_roll = diceObjs[2].roll()
                    enemy_roll = diceObjs[3].roll()

                    # skade < 4, beskyt = 5-6
                    player.damage(1) if(enemy_roll < 4 and (enemy_roll != 4 or enemy_roll != 5)) else None
                    self.battleenemy.damage(1) if(player_roll < 4 and (player_roll != 4 or player_roll != 5)) else None
                    
                    # Hvis spillerens helbred er nul, luk spillet
                    if(player.health == 0):
                        self.game_running = False
                    
                    # Hvis ogrens helbred er nul, nulstil kamp terningerne og fjern kamp modus
                    elif(self.battleenemy.health == 0):
                        diceObjs[2].reset()
                        diceObjs[3].reset()
                        self.battlemode = False
                        self.battleenemy = None
                        self.bar_message = ""
                        background_sprites.draw(self.game_screen)

        # Hvis det er computerens (ogre) tur
        else:

            # Flytter alle ogrene tilfældigt på skærmen
            for entities in entity_sprites.sprites():
                entities.move_random() if(isinstance(entities, orc)) else None
            
            # Gensætter variablerne, indikerer det er spillerens tur og at spilleren kan kaste bevægelsesterningerne igen
            self.player_turn = True
            self.dice_round_step_rolled = False

# Skaber et spil objekt
main()