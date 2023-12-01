import pygame
from pygame.locals import *
import random
import threading
import math
import time

pygame.display.init()
pygame.font.init()
global alexspeed
alexspeed = 0.2
Screenwidth = 800
screenheight = 600
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (2, 48, 32)
boxrn = (211,0,0)
gotopostempcolor = (255,0,255)
colorkey = (255,255,255)
pygame.display.set_mode((800, 600))
BulletGroup = pygame.sprite.Group()
AlexGroup = pygame.sprite.Group()
global HealthBar1
global swamphealth
swamphealth = 100
global PlayAgain
screen = pygame.display.set_mode([Screenwidth, screenheight])


g = pygame.image.load("H:/Desktop/Thonny/Thonny/Race car/satisfying stuff/shrek.png").convert_alpha()
#g = pygame.transform.scale(g,(5,5))

s = pygame.image.load("H:/Desktop/Thonny/Thonny/Race car/satisfying stuff/ALEX.png").convert_alpha()
#s = pygame.transform.scale(s,(5,5))

class HealthBar(pygame.sprite.Sprite):
    def __init__(self):  
        super().__init__()
        self.Health = 100
        self.Width = 25
        self.Text = "Swamp Health"

    def DrawHealthBar(self):
        global swamphealth
        swamphealth = self.Health
        sysfont = pygame.font.get_default_font()
        font = pygame.font.SysFont(None, 40)
        Healthimg = font.render(self.Text, True, BLUE)
        screen.blit(Healthimg, (275, 500))
        Bar = pygame.draw.rect(screen,GREEN,pygame.Rect(275, 550,(2 * self.Health),20))
        
    def TakeHealth(self):
        self.Health -= 10
        


class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 400
        self.y = 300
        self.xspeed = 0.2
        self.yspeed = 0.2
        
    def draw(self):
        global colorkey
        if self.x >= 670:
            self.xspeed = -0.2
            colorkey = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
        elif self.x <= 0:
            self.xspeed = 0.2
            colorkey = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
        
        if self.y >= 475:
            self.yspeed = -0.2
            colorkey = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
        elif self.y <= 0:
            self.yspeed = 0.2
            colorkey = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
        
        self.x += self.xspeed
        self.y += self.yspeed
        screen.blit(g, (self.x, self.y))
    
    def getpos(self):
        return(self.x , self.y)
    
    def Damage(self):
        global HealthBar1
        HealthBar1.TakeHealth()
        pass

        
class Bullet(pygame.sprite.Sprite):
    def __init__(self , x , y):
        super().__init__()
        self.targetx = x
        self.targety = y
        self.startposx , self.startposy = box.getpos()
        self.speed = 5
        self.angle = 0
        self.xspeed = 0
        self.yspeed = 0
        self.rect = pygame.Rect(self.startposx, self.startposy,20,20)
        
        def GetAngleBetween(point1, point2):
            width = point2[0] - point1[0]
            height = point2[1] - point1[1]
            angle = math.atan2(height, width)
            return angle
        
        self.angle = GetAngleBetween((self.targetx, self.targety) , (self.startposx, self.startposy))
    
    def update(self):
    
        
        
        #if self.angle < 1:
           #print("stopped")
        
        #if (self.startposx - self.targetx) < 5 and not (self.startposx - self.targetx) < 0:
            #self.kill()
            
        self.rect = pygame.Rect(self.startposx, self.startposy,20,20)
            
        

        self.startposx -= math.cos(self.angle) * self.speed
        self.startposy -= math.sin(self.angle) * self.speed
        pygame.draw.rect(screen,gotopostempcolor,self.rect)
        
        
class ALEX(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = random.randint(0 , 500)
        self.xspeed = alexspeed
        self.yspeed = alexspeed
        self.rect = pygame.Rect(self.x, self.y,50,50)
        
    def update(self):
        self.rect = pygame.Rect(self.x,self.y,150,150)
        if self.x >= 730:
            box.Damage()
            self.kill()
        self.x += self.xspeed
        # block = pygame.draw.rect(screen,gotopostempcolor,self.rect)
        screen.blit(s, (self.x, self.y))
        
        if pygame.sprite.spritecollide(self, BulletGroup, False):
            global alexspeed
            alexspeed = alexspeed * 1.10
            self.kill()
        if swamphealth == 0:
            self.kill()
            
class PlayAgainClass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 300
        self.y = 400
        self.sizex = 200
        self.sizey = 125
        print("ran")
        
    def Draw(self):
        pygame.draw.rect(screen,GREEN,pygame.Rect(self.x , self.y,self.sizex,self.sizey))
        sysfont1 = pygame.font.get_default_font()
        font1 = pygame.font.SysFont(None, 80)
        font2 = pygame.font.SysFont(None, 30)
        Healthimg1 = font1.render("Play again?", True, GREEN)
        Healthimg2 = font2.render("Click here", True, BLUE)
        screen.blit(Healthimg1, (250, 100))
        screen.blit(Healthimg2, (350, 450))
    
    def Clicked(self,x,y):
        if x >= 300 and x <= 500:
            if y >= 400 and y <= 525:
                global PlayAgain
                PlayAgain()
        
def addalex():
    while swamphealth != 0:
        AlexGroup.add(ALEX())
        time.sleep(1)
        
def shoot():
    while swamphealth != 0:
        x ,y = pygame.mouse.get_pos()
                
        BulletGroup.add(Bullet(x , y))
        time.sleep(0.5)
        

global box   
box = Vehicle()
global HealthBar1
HealthBar1 = HealthBar()

def PlayAgain():
    print("ran")
    global swamphealth
    global alexspeed
    alexspeed = 0.2
    swamphealth = 100
    
    t1 = threading.Thread(target = addalex)
    t1.start()
    
    #t2 = threading.Thread(target = shoot)
    #t2.start()

    global HealthBar1
    HealthBar1 = HealthBar()
    global box
    box = Vehicle()
 

t1 = threading.Thread(target = addalex)
t1.start()

#t2 = threading.Thread(target = shoot)
#t2.start()



Button = PlayAgainClass()

while True:
    if swamphealth != 0:
    
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x ,y = pygame.mouse.get_pos()
                
                BulletGroup.add(Bullet(x , y))
                
        
        
        BulletGroup.update()
        AlexGroup.update()
        HealthBar1.DrawHealthBar()
        
        pygame.draw.rect(screen,DARK_GREEN ,pygame.Rect(775,0 ,30 , 800))
        
        box.draw()
        pygame.display.update()
        screen.fill((colorkey))     
    else:
        print(swamphealth)
        if swamphealth == 0:
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        x,y = pygame.mouse.get_pos()
                        Button.Clicked(x,y)
                        
            
            Button.Draw() 
                    
            pygame.display.update()
            screen.fill((BLUE))
    
        
