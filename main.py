import pygame
import random
pygame.init()
monster_image = pygame.image.load("monster.png")
monster_image = pygame.transform.scale(monster_image,(50,50))

player_image = pygame.image.load("player.gif")
player_image = pygame.transform.scale(player_image,(50,50))
from level1 import level1

screen = pygame.display.set_mode((800,500))
clock = pygame.time.Clock()

square = pygame.surface.Surface((50,50))
square.fill("white")

class Monster(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = monster_image
        #self.image.fill("brown")  # You can choose a different color for the monster
        self.rect = self.image.get_rect()
        self.rect.topleft=(random.randint(1,300) ,random.randint(1,300))
        self.player = player
        self.speed = 3
    
    def move(self):
        if pygame.sprite.spritecollide(self, map.blocks , False):
            self.speed = 1
        else:
            self.speed = 2
        if self.player.rect.left > self.rect.left:
            self.right(self.speed)
        if self.player.rect.left < self.rect.left:
            self.left(self.speed)
        if self.player.rect.top > self.rect.top:
            self.down(self.speed)
        if self.player.rect.top < self.rect.top:
            self.up(self.speed)

    def up(self , speed):
        self.rect.top -= speed
    def down(self , speed):
        self.rect.top += speed
    def left(self , speed):
        self.rect.left -= speed
    def right(self , speed):
        self.rect.left += speed

    

        
    
    def display(self):
        screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        #self.image.fill("yellow")
        self.rect = self.image.get_rect()
        self.rect.topleft=(400 , 300)
        self.speed = 6
        self.direction = "up"
        self.alive = True

    def collision(self , map ):
        for block in map.blocks:
            print(str(type(block))) 
            if str(type(block)) == "<class '__main__.Block'>":
                if pygame.sprite.collide_rect(self , block):
                    screen.fill("red")
                    self.alive = False
            if str(type(block)) == "<class '__main__.Gem'>":
                if pygame.sprite.collide_rect(self , block):
                    screen.fill("white")
                    self.alive = True
                    pygame.sprite.spritecollide(self, map.blocks, True, collided=None)
     
    
    def move(self , map):
        keys =  pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.rect.left > 650:
                map.shift(x = -self.speed)
                return ["left" , self.speed]
                
            else:
                self.rect.right += self.speed
            self.direction = "right"
            
            self.collision(map)
        if keys[pygame.K_LEFT]:
            if self.rect.left < 50:
                map.shift(x= self.speed)
                return  ["right" , self.speed]
            
            else:
                self.rect.left -= self.speed
            self.direction = "left"

            self.collision(map)

        if keys[pygame.K_UP]:
            if self.rect.top < 50:
                map.shift(y=self.speed)
                return ["down" , self.speed]
            
            else:
                self.rect.top -= self.speed
            self.direction = "up"
            
            self.collision(map)

       
        if keys[pygame.K_DOWN]:
            if self.rect.top > 400:
                map.shift(y=-self.speed)
                return ["up" , self.speed]
            
            else:
                self.rect.top += self.speed
            self.direction = "down"

            self.collision(map)

    def display(self):
        screen.blit(self.image , self.rect)


class Block(pygame.sprite.Sprite):
    def __init__(self , x , y , color = "gray" , width=50 , height=50 ):
        super().__init__()
        self.image = pygame.Surface((width , height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.width = width
        self.height = height
        self.color = color

class Gem(pygame.sprite.Sprite):
    def __init__(self , x , y , color = "yellow" , width=50 , height=50 ):
        super().__init__()
        self.image = pygame.Surface((width , height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.width = width
        self.height = height
        self.color = color

class Floor(pygame.sprite.Sprite):
    def __init__(self , x , y , color = "gray" , width=50 , height=50 ):
        super().__init__()
        self.image = pygame.Surface((width , height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.width = width
        self.height = height
        self.color = color



class Map():
    def __init__(self):
        self.shift_x = 0
        self.shift_y = 0
        self.blocks = pygame.sprite.Group()

    def createLevel(self):
        for i in range(len(level1)):
            for j in range(len(level1[0])):
                col = j*50
                row = i*50

                if level1[i][j] == 2:
                    gem = Gem(col , row , "white" )
                    self.blocks.add(gem)
                
                elif level1[i][j] == 1:
                    block = Block(col , row , "red")
                    self.blocks.add(block)

                elif level1[i][j] == 0 : 
                    floor = Floor(col , row , (67,70,75))
                    self.blocks.add(floor)
                    

    def shift(self , x=0 , y=0) :
        for block in self.blocks:
            block.rect.left += x
            block.rect.top += y

player = Player()
map = Map()
monster = Monster(player)


players = pygame.sprite.Group()

map.createLevel()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.fill("black")
    # map.blocks.draw(screen)

    for block in map.blocks.sprites() : 
        # block.draw(screen)
        if abs(player.rect.center[0] - block.rect.center[0] ) < 200 and abs(player.rect.center[1] - block.rect.center[1] ) < 200 :
            screen.blit(block.image , block.rect)
    
    mapMovement = player.move(map)

    if mapMovement : 
        if mapMovement[0] == "up" : 
            monster.up(mapMovement[1])
            
        if mapMovement[0] == "down" : 
            monster.down(mapMovement[1])
        
        if mapMovement[0] == "left" : 
            monster.left(mapMovement[1])
            
        if mapMovement[0] == "right" : 
            monster.right(mapMovement[1])
    else: 
        pass

    
   
    monster.move()

    player.display()
    monster.display()
 
    if pygame.sprite.collide_rect(player, monster):
        print("Player collided with the monster!")
        player.alive = False

    if not player.alive : 
        screen.fill("red")
        print("Game over")
        font = pygame.font.Font(None,40)
        textSurface = font.render("GAME OVER",False,"black")
        screen.blit(textSurface,(300,250))

    

    pygame.display.flip()
    clock.tick(25)
