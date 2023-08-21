import pygame
import random

from level1 import level1

screen = pygame.display.set_mode((800,500))
clock = pygame.time.Clock()

square = pygame.surface.Surface((50,50))
square.fill("white")

class Monster(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.surface.Surface((25, 25))
        self.image.fill("brown")  # You can choose a different color for the monster
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
        self.image = pygame.surface.Surface((25,25))
        self.image.fill("yellow")
        self.rect = self.image.get_rect()
        self.rect.topleft=(400 , 300)
        self.speed = 6
        self.direction = "up"

    def collision(self , map ):
        for block in map.blocks:
            if pygame.sprite.collide_rect(self , block):
                if self.direction == "up" :
                    self.rect.top = block.rect.bottom
                if self.direction == "down" :
                    self.rect.bottom = block.rect.top
                if self.direction == "left" :
                    self.rect.left = block.rect.right
                if self.direction == "right" :
                    self.rect.right = block.rect.left
                    
    
    def move(self , map):
        keys =  pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction = "right"
            if self.rect.left > 650:
                map.shift(x = -self.speed)
                return ["left" , self.speed]
                
            else:
                self.rect.right += self.speed
            
            self.collision(map)
        if keys[pygame.K_LEFT]:
            self.direction = "left"
            if self.rect.left < 50:
                map.shift(x= self.speed)
                return  ["right" , self.speed]
            
            else:
                self.rect.left -= self.speed

            self.collision(map)

        if keys[pygame.K_UP]:
            self.direction = "up"
            if self.rect.top < 50:
                map.shift(y=self.speed)
                return ["down" , self.speed]
            
            else:
                self.rect.top -= self.speed
            
            self.collision(map)

       
        if keys[pygame.K_DOWN]:
            self.direction = "down"
            if self.rect.top > 400:
                map.shift(y=-self.speed)
                return ["up" , self.speed]
            
            else:
                self.rect.top += self.speed

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
                    block = Block(col , row , random.choice(["brown" , "white" , "green"  "yellow"]))
                    self.blocks.add(block)
                
                elif level1[i][j] == 1:
                    block = Block(col , row , "lightblue")
                    self.blocks.add(block)

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

    screen.fill("green")
    map.blocks.draw(screen)
    
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

    

    pygame.display.flip()
    clock.tick(25)
