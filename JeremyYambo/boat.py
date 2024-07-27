import pygame
import math
import random
class Boat:
    def __init__(self,x,y,img,direction,speed,screen):
        self.x = x
        self.y = y
        self.img = img
        self.direction = direction
        self.speed = speed
        self.screen = screen
        self.scale = 2.5
        self.size = [self.img.get_width() * self.scale,self.img.get_height() * self.scale]
        self.hitbox = pygame.Rect(self.x,self.y,self.size[0],self.size[1])
    
    def render(self):
        img = pygame.transform.scale(self.img,(self.size[0],self.size[1]))
        self.screen.blit(img,(self.x,self.y))
        hitbox = pygame.Rect(self.x + 20,self.y + 10,self.size[0] * 0.75,self.size[1] * 0.7)
    
    def update(self):
        self.y += math.cos(pygame.time.get_ticks() * 0.01) * 0.5
        if self.direction < 0:
            self.x -= self.speed
            if self.x < 0 - self.size[0]:
                self.x = self.screen.get_width()
        else: 
            self.x += self.speed
            if self.x > self.screen.get_width():
                self.x = 0 - self.size[0]
        if self.y > self.screen.get_height():
            self.y = -65
            self.x = random.randint(0,self.screen.get_width())
    def get_hitbox(self):
        return pygame.Rect(self.x + 20,self.y + 10,self.size[0] * 0.75,self.size[1] * 0.7)
        