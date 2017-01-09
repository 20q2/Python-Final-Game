from Game_Sprite import *
import os

class Monster:
    def __init__(self,sprite): #Most of this will remain the same, unless monster has
        #A special variable to keep track of
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self, sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        drop = Sprite(self.get_pos(),SPRITE_CACHE["money.png"])
        tile = {"name":"item","type":"money","sprite":"money.png"}
        sprites.add(drop)
        items.append((drop,tile))
        return #If monster does something on death, make it happen here
    
    def attack(self,player):
        #run appropriate space checks, hurt the player if its appropriate
        pos = self.get_pos()
        if (pos[0],pos[1]+1) == player.get_pos():
            player.hurt()
        if (pos[0],pos[1]-1) == player.get_pos():
            player.hurt()
        if (pos[0]+1,pos[1]) == player.get_pos():
            player.hurt()
        if (pos[0]-1,pos[1]) == player.get_pos():
            player.hurt()
        
        
        return

    def move(self,player,level,monsters, overhead):
        #Movement code, usually should run a collission check
        #Recommend running attack before moving, this will give the player the opportunity
        #To make the outplays against the moving monsters
        self.attack(player)
        
        ppos = player.get_pos()
        mypos = list(self.get_pos()) #shitty pathfinding
        if ppos[0] > mypos[0] and not level.is_wall(mypos[0]+1,mypos[1]):
            mypos[0] = mypos[0] + 1
        elif ppos[0] < mypos[0] and not level.is_wall(mypos[0]-1,mypos[1]):
            mypos[0] = mypos[0] - 1
        elif ppos[1] > mypos[1] and not level.is_wall(mypos[0],mypos[1]+1):
            mypos[1] = mypos[1] + 1
        elif ppos[1] < mypos[1] and not level.is_wall(mypos[0],mypos[1]-1):
            mypos[1] = mypos[1] - 1

        for x in monsters: #dont share square with other monsters
            if tuple(mypos) == x.get_pos():
                if self == x:
                    continue
                return
            
        if not player.get_pos() == (mypos[0],mypos[1]): #dont go inside the player
            self.sprite.rect.x = mypos[0]*24-4
            self.sprite.rect.y = mypos[1]*16-16
        return
    
class Raw_Chicken:
    def __init__(self,sprite):
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self,sprites,monsters, items, doors, player, overhead, SPRITE_CACHE):
        chickity = Sprite(self.get_pos(),SPRITE_CACHE["chicken.png"])
        chick = Mad_Chicken(chickity)
        chick.name = "chickity"
        chick.health = 3
        chick.speed = 1
        chick.power = 1
        sprites.add(chickity)
        monsters.append(chick)
        return

    def attack(self,player):
        #run appropriate space checks        
        return

    def move(self,player,level,monsters, overhead):
        #Movement code, usually should run a collission check
        #self.sprite._set_pos([0,0])
        #End with call to attack function
        return
    


class Mad_Chicken:
    def __init__(self,sprite):
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self,sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        drop = Sprite(self.get_pos(),SPRITE_CACHE["doge.png"])
        tile = {"name":"item","type":"consumable","variant":"potion-health","sprite":"doge.png"}
        sprites.add(drop)
        items.append((drop,tile))
        return

    def attack(self,player,overhead):
        #run appropriate space checks
        if self.alerted:
            pos = self.get_pos()
            if (pos[0],pos[1]+1) == player.get_pos():
                player.hurt()
                overhead.sound = pygame.mixer.Sound('chickenattack.wav')
                overhead.sound.play()
            if (pos[0],pos[1]-1) == player.get_pos():
                player.hurt()
                overhead.sound = pygame.mixer.Sound('chickenattack.wav')
                overhead.sound.play()
            if (pos[0]+1,pos[1]) == player.get_pos():
                player.hurt()
                overhead.sound = pygame.mixer.Sound('chickenattack.wav')
                overhead.sound.play()
            if (pos[0]-1,pos[1]) == player.get_pos():
                player.hurt()
                overhead.sound = pygame.mixer.Sound('chickenattack.wav')
                overhead.sound.play()
        return

    def move(self,player,level,monsters, overhead):
        #Movement code, usually should run a collission check
        #self.sprite._set_pos([0,0])
        #End with call to attack function            
        if not self.alerted:
            self.alerted = True

        elif self.alerted:
            self.attack(player,overhead)
            
            ppos = player.get_pos()
            mypos = list(self.get_pos())
            if ppos[0] > mypos[0] and not level.is_wall(mypos[0]+1,mypos[1]):
                mypos[0] = mypos[0] + 1
            elif ppos[0] < mypos[0] and not level.is_wall(mypos[0]-1,mypos[1]):
                mypos[0] = mypos[0] - 1
            elif ppos[1] > mypos[1] and not level.is_wall(mypos[0],mypos[1]+1):
                mypos[1] = mypos[1] + 1
            elif ppos[1] < mypos[1] and not level.is_wall(mypos[0],mypos[1]-1):
                mypos[1] = mypos[1] - 1

            for x in monsters: #Dont share square with other monsters
                if tuple(mypos) == x.get_pos():
                    if self == x:
                        continue
                    return

            if not player.get_pos() == (mypos[0],mypos[1]):
                self.sprite.rect.x = mypos[0]*24-4
                self.sprite.rect.y = mypos[1]*16-16
        return
    

class Breakable:
    def __init__(self,sprite): #Most of this will remain the same, unless monster has
        #A special variable to keep track of
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self, sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        doors.pop(doors.index(self.sprite))
        return #If monster does something on death, make it happen here
    
    def attack(self,player):
        return

    def move(self,player,level,monsters, overhead):
        return

class Gordon:
    def __init__(self,sprite): #Most of this will remain the same, unless monster has
        #A special variable to keep track of
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite
        self.stage = 0

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self, sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        drop = Sprite(self.get_pos(),SPRITE_CACHE["bee.png"])
        tile = {"name":"item","type":"consumable","variant":"bee","sprite":"bee.png"}
        sprites.add(drop)
        items.append((drop,tile))
        return #If monster does something on death, make it happen here
    
    def attack(self,player,overhead):
        #run appropriate space checks, hurt the player if its appropriate
        if self.alerted:
            if self.stage == 0:
                overhead.sound = pygame.mixer.Sound('chicken.wav')
            elif self.stage == 1:
                overhead.sound = pygame.mixer.Sound('eggs.wav')
            elif self.stage == 2:
                overhead.sound = pygame.mixer.Sound('lime.wav')
            elif self.stage == 3:
                overhead.sound = pygame.mixer.Sound('taste_good1.wav')
                self.health = 1
            overhead.sound.play()
        return

    def move(self,player,level,monsters, overhead):
        #Movement code, usually should run a collission check
        #Recommend running attack before moving, this will give the player the opportunity
        #To make the outplays against the moving monsters
        if self.health < 999:
            self.alerted = True

        if self.alerted:
            self.attack(player,overhead)       
            ppos = player.get_pos()
            mypos = list(self.get_pos()) #shitty pathfinding
            if ppos[0] > mypos[0] and not level.is_wall(mypos[0]+1,mypos[1]):
                mypos[0] = mypos[0] + 1
            elif ppos[0] < mypos[0] and not level.is_wall(mypos[0]-1,mypos[1]):
                mypos[0] = mypos[0] - 1
            elif ppos[1] > mypos[1] and not level.is_wall(mypos[0],mypos[1]+1):
                mypos[1] = mypos[1] + 1
            elif ppos[1] < mypos[1] and not level.is_wall(mypos[0],mypos[1]-1):
                mypos[1] = mypos[1] - 1

            for x in monsters: #dont share square with other monsters
                if tuple(mypos) == x.get_pos():
                    if self == x:
                        continue
                    return
                
            if not player.get_pos() == (mypos[0],mypos[1]): #dont go inside the player
                self.sprite.rect.x = mypos[0]*24-4
                self.sprite.rect.y = mypos[1]*16-16
        return

class Sanic:
    def __init__(self,sprite):
        self.name = "dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = True
        self.sprite = sprite
        self.moves = 2

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self,sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        return

    def attack(self,player,overhead):
        #run appropriate space checks
        if self.alerted:
            pos = self.get_pos()
            if (pos[0],pos[1]+1) == player.get_pos():
                player.hurt()
                overhead.sound = pygame.mixer.Sound('slow.wav')
                overhead.sound.play()
            if (pos[0],pos[1]-1) == player.get_pos():
                player.hurt()
                overhead.sound = pygame.mixer.Sound('slow.wav')
                overhead.sound.play()
            if (pos[0]+1,pos[1]) == player.get_pos():
                player.hurt()
                overhead.sound = pygame.mixer.Sound('slow.wav')
                overhead.sound.play()
            if (pos[0]-1,pos[1]) == player.get_pos():
                player.hurt()
                overhead.sound = pygame.mixer.Sound('slow.wav')
                overhead.sound.play()
        return

    def move(self,player,level, monsters, overhead):
        #Movement code, usually should run a collission check
        #self.sprite._set_pos([0,0])
        #End with call to attack function
        self.moves = 0
        while self.moves < 2:
                self.moves += 1
   
                ppos = player.get_pos()
                mypos = list(self.get_pos())
                if ppos[0] > mypos[0] and not level.is_wall(mypos[0]+1,mypos[1]):
                    mypos[0] = mypos[0] + 1
                elif ppos[0] < mypos[0] and not level.is_wall(mypos[0]-1,mypos[1]):
                    mypos[0] = mypos[0] - 1
                elif ppos[1] > mypos[1] and not level.is_wall(mypos[0],mypos[1]+1):
                    mypos[1] = mypos[1] + 1
                elif ppos[1] < mypos[1] and not level.is_wall(mypos[0],mypos[1]-1):
                    mypos[1] = mypos[1] - 1

                for x in monsters: #dont share square with other monsters
                    if tuple(mypos) == x.get_pos():
                        if self == x:
                            continue
                        return
                
                if not player.get_pos() == (mypos[0],mypos[1]):
                    self.sprite.rect.x = mypos[0]*24-4
                    self.sprite.rect.y = mypos[1]*16-16

        self.attack(player, overhead)
        return


class Shrek:
    def __init__(self,sprite): #Most of this will remain the same, unless monster has
        #A special variable to keep track of
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite
        self.moveallow = False

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self, sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        drop = Sprite(self.get_pos(),SPRITE_CACHE["money.png"])
        tile = {"name":"item","type":"money","sprite":"money.png"}
        sprites.add(drop)
        items.append((drop,tile))
        return #If monster does something on death, make it happen here
    
    def attack(self,player,overhead):
        #run appropriate space checks, hurt the player if its appropriate
        pos = self.get_pos()
        if (pos[0],pos[1]+1) == player.get_pos():
            player.hurt()
            overhead.sound = pygame.mixer.Sound('ogrenow.wav')
            overhead.sound.play()
        if (pos[0],pos[1]-1) == player.get_pos():
            player.hurt()
            overhead.sound = pygame.mixer.Sound('ogrenow.wav')
            overhead.sound.play()
        if (pos[0]+1,pos[1]) == player.get_pos():
            player.hurt()
            overhead.sound = pygame.mixer.Sound('ogrenow.wav')
            overhead.sound.play()
        if (pos[0]-1,pos[1]) == player.get_pos():
            player.hurt()
            overhead.sound = pygame.mixer.Sound('ogrenow.wav')
            overhead.sound.play()
        
        
        return

    def move(self,player,level, monsters, overhead):    
        #Movement code, usually should run a collission check
        #Recommend running attack before moving, this will give the player the opportunity
        #To make the outplays against the moving monsters
        if not self.moveallow:
            self.moveallow = True
            return  
        self.attack(player,overhead)
        self.attack(player,overhead)
        
        ppos = player.get_pos()
        mypos = list(self.get_pos()) #shitty pathfinding
        if ppos[0] > mypos[0] and not level.is_wall(mypos[0]+1,mypos[1]):
            mypos[0] = mypos[0] + 1
        elif ppos[0] < mypos[0] and not level.is_wall(mypos[0]-1,mypos[1]):
            mypos[0] = mypos[0] - 1
        elif ppos[1] > mypos[1] and not level.is_wall(mypos[0],mypos[1]+1):
            mypos[1] = mypos[1] + 1
        elif ppos[1] < mypos[1] and not level.is_wall(mypos[0],mypos[1]-1):
            mypos[1] = mypos[1] - 1

        for x in monsters: #dont share square with other monsters
            if tuple(mypos) == x.get_pos():
                if self == x:
                    continue
                return

        if not player.get_pos() == (mypos[0],mypos[1]): #dont go inside the player
            self.sprite.rect.x = mypos[0]*24-4
            self.sprite.rect.y = mypos[1]*16-16

        self.moveallow = False

class One:
    def __init__(self,sprite): #Most of this will remain the same, unless monster has
        #A special variable to keep track of
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite
        self.hasnet = True

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self, sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        return #If monster does something on death, make it happen here
    
    def attack(self,player,overhead):
        #run appropriate space checks, hurt the player if its appropriate
        print("one net:",self.hasnet)
        pos = self.get_pos()
        if self.hasnet == False:
            return

        if (pos[0],pos[1]+1) == player.get_pos():
            player.isnet = 3
            self.hasnet = False
            overhead.sound = pygame.mixer.Sound('we#1.wav')
            overhead.sound.play()
        elif (pos[0],pos[1]-1) == player.get_pos():
            player.isnet = 3
            self.hasnet = False
            overhead.sound = pygame.mixer.Sound('we#1.wav')
            overhead.sound.play()
        elif (pos[0]+1,pos[1]) == player.get_pos():
            player.isnet = 3
            self.hasnet = False
            overhead.sound = pygame.mixer.Sound('we#1.wav')
            overhead.sound.play()
        elif (pos[0]-1,pos[1]) == player.get_pos():
            player.isnet = 3
            self.hasnet = False
            overhead.sound = pygame.mixer.Sound('we#1.wav')
            overhead.sound.play()
        else:
            return

        print("WE ARE NUMBER ONE ATTACK!")
        nonet = Sprite(self.get_pos(),overhead.SPRITE_CACHE["one_nonet.png"])
        self.sprite.kill()
        self.sprite = nonet
        overhead.sprites.add(nonet)
        
        return

    def move(self,player,level, monsters, overhead):
        #Movement code, usually should run a collission check
        #Recommend running attack before moving, this will give the player the opportunity
        #To make the outplays against the moving monsters

        
        ppos = player.get_pos()
        mypos = list(self.get_pos()) #shitty pathfinding
        if ppos[0] > mypos[0] and not level.is_wall(mypos[0]+1,mypos[1]):
            mypos[0] = mypos[0] + 1
        elif ppos[0] < mypos[0] and not level.is_wall(mypos[0]-1,mypos[1]):
            mypos[0] = mypos[0] - 1
        elif ppos[1] > mypos[1] and not level.is_wall(mypos[0],mypos[1]+1):
            mypos[1] = mypos[1] + 1
        elif ppos[1] < mypos[1] and not level.is_wall(mypos[0],mypos[1]-1):
            mypos[1] = mypos[1] - 1

        for x in monsters: #dont share square with other monsters
            if tuple(mypos) == x.get_pos():
                if self == x:
                    continue
                return

        if not player.get_pos() == (mypos[0],mypos[1]): #dont go inside the player
            self.sprite.rect.x = mypos[0]*24-4
            self.sprite.rect.y = mypos[1]*16-16

        self.attack(player,overhead)
        return

class Food_Bad:
    def __init__(self,sprite): #Most of this will remain the same, unless monster has
        #A special variable to keep track of
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self, sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        overhead.sound = pygame.mixer.Sound('seriously.wav')
        overhead.sound.play()
        player.hurt()
        return #If monster does something on death, make it happen here
    
    def attack(self,player):
        return

    def move(self,player,level,monsters, overhead):
        return

class Food_Good:
    def __init__(self,sprite): #Most of this will remain the same, unless monster has
        #A special variable to keep track of
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self, sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        for x in monsters:
            if x.name == "gordon":
                x.stage += 1
                break
        return #If monster does something on death, make it happen here
    
    def attack(self,player):
        return

    def move(self,player,level,monsters, overhead):
        return

class Illuminati:
    def __init__(self,sprite,overhead): #Most of this will remain the same, unless monster has
        #A special variable to keep track of
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite
        self.bounce = True
        self.tl = Sprite((self.get_pos()[0],self.get_pos()[1]-2),overhead.SPRITE_CACHE["ill_tl.png"])
        self.tr = Sprite((self.get_pos()[0]+1,self.get_pos()[1]-2),overhead.SPRITE_CACHE["ill_tr.png"])
        self.br = Sprite((self.get_pos()[0]+1,self.get_pos()[1]),overhead.SPRITE_CACHE["ill_br.png"])
        overhead.sprites.add(self.tl)
        overhead.sprites.add(self.tr)
        overhead.sprites.add(self.br)

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self, sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        drop = Sprite(self.get_pos(),SPRITE_CACHE["money.png"])
        tile = {"name":"item","type":"money","sprite":"money.png"}
        sprites.add(drop)
        items.append((drop,tile))
        return #If monster does something on death, make it happen here
    
    def attack(self,player, overhead, monsters):
        #run appropriate space checks, hurt the player if its appropriate
        pos = self.get_pos()
        if (pos[0]+1,pos[1]) == player.get_pos():
            for i in range(0,20):
                player.hurt()
        if (pos[0]-1,pos[1]) == player.get_pos():
            for i in range(0,20):
                player.hurt()

        chickity = Sprite(self.get_pos(),overhead.SPRITE_CACHE["dorito.png"])
        chick = Dorito(chickity)
        chick.name = "dorito"
        chick.health = 99
        chick.speed = 1
        chick.power = 1
        overhead.sprites.add(chickity)
        monsters.append(chick)
        
        
        return

    def move(self,player,level,monsters, overhead):
        #Movement code, usually should run a collission check
        #Recommend running attack before moving, this will give the player the opportunity
        #To make the outplays against the moving monsters
        self.attack(player, overhead, monsters)
        
        mypos = list(self.get_pos()) #shitty pathfinding
        if self.bounce:
            if not level.is_wall(mypos[0]+1,mypos[1]):
                mypos[0] = mypos[0] + 1
            else:
                self.bounce = False
        elif not self.bounce:
            if not level.is_wall(mypos[0]-1,mypos[1]):
                mypos[0] = mypos[0] - 1
            else:
                self.bounce = True

        if not player.get_pos() == (mypos[0],mypos[1]): #dont go inside the player
            self.sprite.rect.x = mypos[0]*24-4
            self.sprite.rect.y = mypos[1]*16-16

            self.tl.rect.x = mypos[0]*24-4
            self.tl.rect.y = (mypos[1]-2)*16-16

            self.tr.rect.x = (mypos[0]+1)*24-4
            self.tr.rect.y = (mypos[1]-2)*16-16

            self.br.rect.x = (mypos[0]+1)*24-4
            self.br.rect.y = mypos[1]*16-16
        return
    

class Dorito:
    def __init__(self,sprite): #Most of this will remain the same, unless monster has
        #A special variable to keep track of
        self.name = "Dummy"
        self.health = 0
        self.speed = 0
        self.power = 0
        self.alerted = False
        self.sprite = sprite

    def get_pos(self):
        return self.sprite._get_pos()

    def death(self, sprites, monsters, items, doors, player, overhead, SPRITE_CACHE):
        #monsters.pop(monsters.index(self))
        self.sprite.kill()
        return #If monster does something on death, make it happen here
    
    def attack(self,player, overhead):
        #run appropriate space checks, hurt the player if its appropriate
        pos = self.get_pos()
        blast = False
        for x in overhead.monsters:
            if x.get_pos() == (pos[0],pos[1]+1):
                blast = True
        if (pos[0],pos[1]+1) == player.get_pos():
            blast = True
        if blast:
            blast = []
            for i in range(-2,3):
                for j in range(-2,3):
                    blast.append([pos[0] + i, pos[1] + j])
                    attack = Sprite((pos[0]+i,pos[1]+j), overhead.SPRITE_CACHE["attack2.png"])
                    attack.expire = 10 #battle animation
                    overhead.sprites.add(attack)
            for x in blast:
                for y in overhead.monsters:
                    if y.get_pos() == tuple(x):
                        if y.name == "illuminati":
                            continue
                        y.death(overhead.sprites, overhead.monsters, None, overhead.doors, player, overhead, overhead.SPRITE_CACHE)
                        y.sprite.kill()
                        overhead.monsters.pop(overhead.monsters.index(y))
                if tuple(x) == player.get_pos():
                    player.health -= 420
            overhead.sound = pygame.mixer.Sound('quickscope.wav')
            overhead.sound.play()
            self.death(overhead.sprites, overhead.monsters, None, overhead.doors, player, overhead, overhead.SPRITE_CACHE)
      
        return

    def move(self,player,level,monsters, overhead):
        #Movement code, usually should run a collission check
        #Recommend running attack before moving, this will give the player the opportunity
        #To make the outplays against the moving monsters
        self.attack(player, overhead)
        
        ppos = player.get_pos()
        mypos = list(self.get_pos()) #shitty pathfinding
        if not level.is_wall(mypos[0],mypos[1]+1):
            mypos[1] = mypos[1] + 1


        for x in monsters: #dont share square with other monsters
            if tuple(mypos) == x.get_pos():
                if self == x:
                    continue
                return
            
        if not player.get_pos() == (mypos[0],mypos[1]): #dont go inside the player
            self.sprite.rect.x = mypos[0]*24-4
            self.sprite.rect.y = mypos[1]*16-16
        return
