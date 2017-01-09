#Starting code from http://qq.readthedocs.io/en/latest/tiles.html
import pygame
from pygame.locals import *
import ConfigParser
from Dank_FloorGenerator import *
from Monster import *
from Itemlist import *
from Game_Sprite import *
import Tkinter as tk
def Debug():
    #print("Monsters:", monsters)
    print("Sprites:", sprites)
    print("Fog_Redraw:", overhead.fog_redraw)
    print("Gameover:", game_over)
    print("Has_won:", has_won)
    
class Level(object):
    def load_file(self, filename="level.txt"):
        self.map = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

        #11/21 insert
        self.items = {}
        for y, line in enumerate(self.map):
            for x, c in enumerate(line):
                if not self.is_wall(x, y) and 'sprite' in self.key[c]:
                    self.items[(x, y)] = self.key[c]

    def get_tile(self, x, y):
        """Tell what's at the specified position of the map."""

        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def set_tile(self, x, y, form):
        self.map[y][x] = form

    def get_bool(self, x, y, name):
        """Tell if the specified flag is set for position on the map."""

        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def is_wall(self, x, y):
        """Is there a wall?"""
        return self.get_bool(x, y, 'wall')
    
    def is_door(self,x,y):
        print("DOOR", self.get_bool(x,y,'door'))
        return self.get_bool(x,y, 'door')

    def is_blocking(self, x, y):
        """Is this place blocking movement?"""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')

    def render(self):
        wall = self.is_wall
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if wall(map_x, map_y):
                    # Draw different tiles depending on neighbourhood
                    if not wall(map_x, map_y+1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            tile = 1, 2
                        elif wall(map_x+1, map_y):
                            tile = 0, 2
                        elif wall(map_x-1, map_y):
                            tile = 2, 2
                        else:
                            tile = 3, 2
                    else:
                        if wall(map_x+1, map_y+1) and wall(map_x-1, map_y+1):
                            tile = 1, 1
                        elif wall(map_x+1, map_y+1):
                            tile = 0, 1
                        elif wall(map_x-1, map_y+1):
                            tile = 2, 1
                        else:
                            tile = 3, 1
                    # Add overlays if the wall may be obscuring something
                    if not wall(map_x, map_y-1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            over = 1, 0
                        elif wall(map_x+1, map_y):
                            over = 0, 0
                        elif wall(map_x-1, map_y):
                            over = 2, 0
                        else:
                            over = 3, 0
                        overlays[(map_x, map_y)] = tiles[over[0]][over[1]]
                else:
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 0, 3
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
        return image, overlays

class Player:
    def __init__(self, sprite):
        self.sprite = sprite
        self.x = self.sprite.rect.x
        self.y = self.sprite.rect.y
        self.power = 1
        self.health = 3
        self.money = 0
        self.isnet = 0

    def get_pos(self):
        return self.sprite._get_pos()

    def pickup(self,item):
        if item[1]["type"] == "money":
            self.money = self.money + 100
            item[0].kill()
            items.pop(items.index(item))
        if item[1]["type"] == "health":
            self.health += 1
            item[0].kill()
            items.pop(items.index(item))
        if item[1]["type"] == "consumable":
            if len(inventory) < 5:
                Add_Item(item[1]["variant"],inventory)
                item[0].kill()
                items.pop(items.index(item))
            

    def hurt(self):
        self.health = self.health-1
        print("DANGER TAKING DAMAGE! HP:", self.health)
        bleed = pygame.sprite.Sprite()
        bleed.image = pygame.Surface([960, 662])
        bleed.image.fill((255,0,0))
        screen.blit(bleed.image, (0,0))

    def attack(self,monster):
        print("attacking", monster.name,monster.health, self.power)
        monster.health = monster.health - self.power
        attack = Sprite(monster.sprite._get_pos(), SPRITE_CACHE["attack.png"])
        attack.expire = 10 #battle animation
        sprites.add(attack)
        overhead.sound = pygame.mixer.Sound('playerhit.wav')
        overhead.sound.play()
        if monster.health <= 0:
            monster.death(sprites, monsters, items, doors, self, overhead, SPRITE_CACHE)
            monster.sprite.kill()
            monsters.pop(monsters.index(monster))
            overhead.fog_redraw = 1
        return
    
    def move(self, key):
        if player.isnet:
            player.isnet -= 1
            net = Sprite(player.get_pos(), SPRITE_CACHE["net.png"])
            net.expire = 10 #battle animation
            sprites.add(net)
            return

        pos = self.sprite._get_pos()
        pos = list(pos)
        dest = [-1,-1]
        if key == "UP": #40x40 map,  24x16 blocks, 
            dest = [pos[0],pos[1]-1]
        elif key == "DOWN":
            dest = [pos[0],pos[1]+1]
        elif key == "LEFT":
            dest = [pos[0]-1,pos[1]]
        elif key == "RIGHT":
            dest = [pos[0]+1,pos[1]]

        cont = False
        if not level.is_wall(dest[0],dest[1]):
            for x in stairs:
                if x._get_pos() == (dest[0],dest[1]):
                    overhead.player = player
                    Generate_Level(overhead) #TODO - Mem leak?
            for x in doors: #used to detect if fog redraw is necessary
                if x._get_pos() == (dest[0],dest[1]) or x._get_pos() == (pos[0],pos[1]):
                    overhead.fog_redraw = 1
            for x in items: #Pickup items!
                if x[0]._get_pos() == (dest[0],dest[1]):
                    self.pickup(x)
            for x in monsters: #Kill baddies!
                if x.get_pos() == (dest[0],dest[1]):
                    self.attack(x)
                    cont = True
            
                    
          #for x in items:
            if not cont:
                self.sprite.rect.x = dest[0]*24-4
                self.sprite.rect.y = dest[1]*16-16
                    
        pos = self.sprite._get_pos()
        print(pos)
        print("Player pos new:" ,self.sprite.rect.x, self.sprite.rect.y)
    
def fog_trace(pos, is_lit, has_traced):
    #print("has traced",has_traced)
    if pos[0] < 0 or  pos[0] > level.width:
        return
    if pos[1] < 0 or pos[1] > level.height:
        return
    if level.is_wall(pos[0],pos[1]) == False:
        for x in doors:
            doorpos = x._get_pos()
            if [doorpos[0],doorpos[1]] == pos:
               is_lit.append([pos[0],pos[1]])
               has_traced.append([pos[0],pos[1]])
               return
        is_lit.append([pos[0],pos[1]])
        has_traced.append([pos[0],pos[1]])
        #print(pos)
        if [pos[0],pos[1]+1] not in has_traced:
            fog_trace([pos[0],pos[1]+1], is_lit, has_traced)
        if [pos[0],pos[1]-1] not in has_traced:
            fog_trace([pos[0],pos[1]-1], is_lit, has_traced)
        if [pos[0]+1,pos[1]] not in has_traced:
            fog_trace([pos[0]+1,pos[1]], is_lit, has_traced)
        if [pos[0]-1,pos[1]] not in has_traced:
            fog_trace([pos[0]-1,pos[1]], is_lit, has_traced)
    else:
        is_lit.append([pos[0],pos[1]])
        has_traced.append([pos[0],pos[1]])

    overhead.fog_redraw = 0


def fog_calc(pos):
    pos = player.sprite._get_pos()
    global is_lit
    is_lit = []
    global has_traced
    has_traced = []
    if overhead.fog_redraw == 1:
        fog_trace(pos, is_lit, has_traced)
    if len(is_lit) != 0:
        overhead.cur_fog = is_lit
        for x in has_traced:
            if x not in fog_visited:
                fog_visited.append(x)
    else:
        is_lit = overhead.cur_fog

    #is_lit contains all lit spots, fill all other spots with fog
    #TODO - Fog performance can be improved with globbing, ain't noone got time for that tho
    for i in range(0,level.width):
        for j in range(0,level.height+1): 
            if [i,j] not in is_lit:
                fog = pygame.sprite.Sprite()
                fog.image = pygame.Surface([24, 16])
                if [i,j] not in fog_visited:
                    fog.image.fill((0,0,0))
                else:
                    fog.image.fill((50,50,50))
                screen.blit(fog.image, (i*24, j*16-12))

def Make_Monster(sprite,tile):
    mon_type = tile["variant"]
    newmon = None
    if mon_type == "crate":
        newmon = Monster(sprite)
    elif mon_type == "chicken":
        newmon = Raw_Chicken(sprite)
    elif mon_type == "a_chicken":
        newmon = Mad_Chicken(sprite)
    elif mon_type == "breakable":
        newmon = Breakable(sprite)
    elif mon_type == "gordon":
        newmon = Gordon(sprite)
    elif mon_type == "sanic":
        newmon = Sanic(sprite)
    elif mon_type == "shrek":
        newmon = Shrek(sprite)
    elif mon_type == "one":
        newmon = One(sprite)
    elif mon_type == "food_good":
        newmon = Food_Good(sprite)
    elif mon_type == "food_bad":
        newmon = Food_Bad(sprite)
    elif mon_type == "illuminati":
        newmon = Illuminati(sprite,overhead)
    elif mon_type == "dorito":
        newmon = Dorito(sprite)
    newmon.name = tile["variant"]
    newmon.health = int(tile["health"])
    newmon.speed = int(tile["speed"])
    newmon.power = int(tile["power"])
    monsters.append(newmon)
    overhead.monsters = monsters
    
def Generate_Level(overhead):
    Full_Create()
    overhead.fog_redraw = 1
    overhead.floor_num += 1
    global overlay_dict
    global background
    global MAP_CACHE
    global SPRITE_CACHE
    global sprites
    global fog_visited
    fog_visited = []
    overhead.Fog_Enable = True

    if overhead.floor_num == 1:
        overhead.Fog_Enable = False
        level.load_file('level.txt')
    elif overhead.floor_num == 3:
        level.load_file('boss1map.txt')
    elif overhead.floor_num == 4:
        level.load_file('boss2map.txt')
        overhead.Fog_Enable = False
        pygame.mixer.music.stop()
        pygame.mixer.music.load('illuminati.mp3')
        pygame.mixer.music.play(-1)
    elif overhead.floor_num == 5:
        print("You won!")
        has_won = True
        game_over = True
        root1 = tk.Tk()
        photo = tk.PhotoImage(file = "important.gif")
        root1.title("Dankest Dungeon Start")
        root1.geometry("1080x608")
        root1.configure(background = '')
       
        panel = tk.Label(root1,image = photo)
        panel.pack(side = 'top', fill = 'both', expand = 'yes')
        #pygame.mixer.music.stop()
        pygame.mixer.music.load("End_music.mp3")
        pygame.mixer.music.play(-1)
        root1.mainloop()
        pygame.quit()
        return
        #End the game
    else:
        level.load_file('level.txt')
    MAP_CACHE = TileCache(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)
    SPRITE_CACHE = TileCache(32, 32)
    overhead.SPRITE_CACHE = SPRITE_CACHE
    sprites = pygame.sprite.RenderUpdates()
    overhead.sprites = sprites
    global doors
    global monsters
    global stairs
    global player
    global items
    if overhead.First_Run == True:
        global inventory
        inventory = []
    monsters = []
    doors = []
    stairs = []
    items = []

    for pos, tile in level.items.iteritems():
        sprite = Sprite(pos, SPRITE_CACHE[tile["sprite"]])
        print(tile["name"])
        if tile["name"] == "player":
            if overhead.First_Run == True:
                player = Player(sprite)
                overhead.First_Run = False
            else:
                player = Player(sprite)
                player.money = overhead.player.money
                player.health = overhead.player.health
                player.power = overhead.player.power
        if tile["name"] == "door":
            doors.append(sprite)
        if tile["name"] == "breakable":
            doors.append(sprite)
            Make_Monster(sprite,tile)
        if tile["name"] == "monster":
            Make_Monster(sprite,tile)     
        if tile["name"] == "stair":
            stairs.append(sprite)
        if tile["name"] == "item":
            items.append((sprite,tile))
        sprites.add(sprite)

    background, overlay_dict = level.render()
    overhead.doors = doors

def HUD_Display():
    #Reset bleed from taking damage
    hudbar = pygame.sprite.Sprite()
    hudbar.image = pygame.Surface([960, 662])
    hudbar.image.fill((100,100,100))
    screen.blit(hudbar.image, (0,0))

    invbar = pygame.sprite.Sprite()
    invbar.image = pygame.Surface([116, 18])
    invbar.image.fill((150,150,150))
    screen.blit(invbar.image, (300,643))
    for i in range(0,player.health): #Health
        life = pygame.sprite.Sprite()
        life.image = pygame.image.load("heart.png")
        screen.blit(life.image, (30 + (i*24),645))
    #Inventory
    for i in range(0,len(inventory)):
        screen.blit(inventory[i].image, (300 + (i*24), 645))
        inventory[i].rect.x = 300 + (i*24)
        inventory[i].rect.y = 645

    font = pygame.font.Font(None,26)
    scoretext = font.render("Money:"+str(player.money), 1,(255,255,255))
    powertext = font.render("Power:"+str(player.power), 1,(255,255,255))
    invtext = font.render("Inv:", 1,(255,255,255))
    hptext = font.render("HP:", 1,(255,255,255))
    screen.blit(scoretext, (800, 645))
    screen.blit(powertext, (700, 645))
    screen.blit(invtext, (270, 645))
    screen.blit(hptext, (0, 645))


def One_Tick():
    if overhead.prog_level == True:
        overhead.prog_level = False
        Generate_Level(overhead)
        return
    for x in monsters:
        x.move(player,level,monsters,overhead)
    HUD_Display()
    Debug()
    return

class Game_obj():
    def __init__(self):
        self.First_Run = True
        self.player = Player
        self.floor_num = 0
        self.fog_redraw = 1
        self.cur_fog = []
        self.prog_level = False
        self.SPRITE_CACHE = False
        self.sprites = None
        self.doors = None
        self.monsters = None
        self.sound = None
        self.Fog_Enable = True

def Update_Screen():
    overlays = pygame.sprite.RenderUpdates()
    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
    screen.blit(background, (0, 0))
    sprites.clear(screen, background)
    sprites.update()
    dirty = sprites.draw(screen)
    overlays.draw(screen)
    overhead.sprites = sprites
    if overhead.Fog_Enable:
        fog_calc(player.sprite._get_pos())
    pygame.display.flip()

pygame.mixer.init()
#Pulling in User Data
f = open('init.txt','r')
global user
volume = f.readline()
user = f.readline()
f.close()
volume = float(volume)
pygame.mixer.music.set_volume(volume)
def SettingsCall():
   def Saveuser():
      global user
      user = name.get()
      newwin.destroy()
      
   global user
   global toclose
   newwin = tk.Toplevel(root1)
   volumeup = tk.Button(newwin, text = "Volume up", command = Volup)
   volumedown = tk.Button(newwin, text = "Volume down", command = Voldown)
   name = tk.Entry(newwin,textvariable = user)
   save = tk.Button(newwin, text = "Save current Settings",command = Saveuser)
   volumeup.pack(side = "top")
   volumedown.pack(side="top")
   name.pack()
   save.pack()
   
def writedata():
   global volume
   global user
   #write user data
   volume = str(volume)
   f = open('init.txt','w')
   f.write(volume + '\n')
   f.write(user + '\n')
   f.close()

def Volup():
   global volume
   if volume == 1.0:
      return
   volume = volume + 0.1
   pygame.mixer.music.set_volume(volume)

def Voldown():
   global volume
   if volume > 0.1:
      volume = volume - 0.1
      pygame.mixer.music.set_volume(volume)
global pauselimit
pauselimit = 0
root1= tk.Tk()
def CallBack():
   root1.destroy()
def Volmenu():
   def lit():
    newwin1.destroy()
   newwin1 = tk.Tk()
   volumeup = tk.Button(newwin1, text = "Volume up", command = Volup)
   volumedown = tk.Button(newwin1, text = "Volume down", command = Voldown)
   lit = tk.Button(newwin1, text = "Exit", command = lit)
   volumeup.pack(side="top")
   volumedown.pack(side="top")
   lit.pack(side="top")
   newwin1.mainloop()
   pygame.event.get()
def Playair():
    pygame.mixer.init()
    airhorn = pygame.mixer.Sound('airhorn.wav')
    airhorn.play(0)

photo = tk.PhotoImage(file = "open_screen_done7.gif")
root1.title("Dankest Dungeon Start")
root1.geometry("600x450")
root1.configure(background = '')

panel = tk.Label(root1,image = photo)
panel.pack(side = 'top', fill = 'both', expand = 'yes')

hello = tk.Button(root1, text = "Click here to begin", command = CallBack)
hello1 = tk.Button(root1, text = "1 Click = 1 pray 4 haramb", command = Playair)
hello2 = tk.Button(root1, text = "Open 1337 settings" , command = SettingsCall)
hello.pack(side="top")
hello1.pack(side="top")
hello2.pack(side ="top")
pygame.mixer.music.load("Start_music.mp3")
pygame.mixer.music.play(-1)
root1.mainloop()
pygame.mixer.music.stop()

        
if __name__=='__main__':
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    volume = float(volume)
    pygame.mixer.music.set_volume(volume)
    
    screen = pygame.display.set_mode((960, 662))
    level = Level()
    Initialize_Floor()
    pygame.mixer.music.load('kirby.mp3')
    pygame.mixer.music.play(-1)
    overhead = Game_obj()
    MAP_TILE_WIDTH = 24
    MAP_TILE_HEIGHT = 16
    global game_over
    game_over = False
    global has_won
    has_won = False
    Generate_Level(overhead)
    overhead.player = player
    clock = pygame.time.Clock()
    HUD_Display()
    o = False
    while not game_over:
        Update_Screen()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
                pygame.quit() #TODO - MOVE THIS SOON
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key
                if pressed_key == pygame.K_UP:
                    player.move("UP")
                if pressed_key == pygame.K_DOWN:
                    player.move("DOWN")
                if pressed_key == pygame.K_LEFT:
                    player.move("LEFT")
                if pressed_key == pygame.K_RIGHT:
                    player.move("RIGHT")
                if event.key == pygame.K_s:
                    if o:
                        continue
                    o = True
                    Volmenu()
                    o= False
                    continue
                One_Tick()
            elif event.type == pygame.MOUSEBUTTONDOWN: #Inventory click
              mouse_pos = pygame.mouse.get_pos()
              for x in inventory:
                  print(x.rect, mouse_pos, x.rect.collidepoint(mouse_pos))
                  if x.rect.collidepoint(mouse_pos):
                      Use_Item(x.name,player,sprites, monsters, items, doors, SPRITE_CACHE, overhead)
                      x.kill()
                      inventory.pop(inventory.index(x))
                      One_Tick()
              


        if player.health <= 0:
            game_over = True
        
    print("You are ded scrub get rekt")
    def Exitn():
        root1.destroy()
    pygame.mixer.music.load('dead.mp3')
    pygame.mixer.music.play(0)
    root1= tk.Tk()
    photo = tk.PhotoImage(file = "game_over.gif")
    name = tk.Button(root1,text = "Exit Game", command = Exitn)
    root1.title("G3T N0 SK0P3D")
    root1.geometry("1140x1019")
    root1.configure(background = '')
       
    panel = tk.Label(root1,image = photo)
    name.pack()
    panel.pack()
    root1.mainloop()
    volume = str(volume)
    global user
    f = open('init.txt','w')
    f.write(volume + '\n')
    f.write(user + '\n')
    f.close()
    pygame.quit()
                
