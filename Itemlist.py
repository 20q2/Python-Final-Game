import pygame
from Game_Sprite import *

def Add_Item(name,inventory):
    item = pygame.sprite.Sprite()
    if name == "food":
        item.image = pygame.image.load("food_small.png")
        item.name = "food"
    if name == "potion-health":
        item.image = pygame.image.load("doge_small.png")
        item.name = "potion-health"
    if name == "potion-death":
        item.image = pygame.image.load("doge_small.png")
        item.name = name
    if name == "food2":
        item.image = pygame.image.load("food2_small.png")
        item.name = name
    if name == "airhorn":
        item.image = pygame.image.load("airhorn_small.png")
        item.name = name
    if name == "bee":
        item.image = pygame.image.load("bee_small.png")
        item.name = name
        

    item.rect = item.image.get_rect()
    inventory.append(item)
        
        

def Use_Item(name, player, sprites, monsters, items, doors, SPRITE_CACHE, overhead):
    if name == "food":
        player.health += 1
    elif name == "potion-health":
        player.power += 1
        overhead.sound = pygame.mixer.Sound('bork.wav')
        overhead.sound.play()
    elif name == "potion-death":
        player.health -= 1
        overhead.sound = pygame.mixer.Sound('bork.wav')
        overhead.sound.play()
    elif name == "food2":
        player.health += 2
    elif name == "bee":
        overhead.player = player
        overhead.prog_level = True
        overhead.sound = pygame.mixer.Sound('beemovie.wav')
        overhead.sound.play()
    elif name == "airhorn":
        blast = []
        for i in range(-2,3):
            for j in range(-2,3):
                pos = player.get_pos()
                blast.append([pos[0] + i, pos[1] + j])
                attack = Sprite((pos[0]+i,pos[1]+j), SPRITE_CACHE["attack2.png"])
                attack.expire = 10 #battle animation
                sprites.add(attack)
        for x in blast:
            for monster in monsters:
                if monster.get_pos() == (x[0],x[1]):
                    monster.health -= 3
                    if monster.health <= 0:
                        monster.death(sprites, monsters, items, doors, player, overhead, SPRITE_CACHE)
                        monster.sprite.kill()
                        monsters.pop(monsters.index(monster))
                        overhead.fog_redraw = 1
        overhead.sound = pygame.mixer.Sound('airhorn.wav')
        overhead.sound.play()
                            
    
