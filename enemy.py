# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 17:39:40 2018

@author: Surface-S
"""

import pygame
from random import randint

class SmallEnemy(pygame.sprite.Sprite):
    
    # 1 bullet hits it, then it is destroied
    life = 1
    
    def __init__(self,width,height):
        pygame.sprite.Sprite.__init__(self)
        
        self.width = width
        self.height = height
        self.image = pygame.image.load("images/smallenemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        # create enemy randomly
        self.rect.left = randint(self.width,self.width + 10*self.rect.width)
        self.rect.top = randint(0, self.height - self.rect.height)
        
        # the destroy image
        self.boom_image = pygame.image.load("images/boom.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.live = True
        self.life = SmallEnemy.life
        self.velocity = 4
        
    def move(self):
        if self.rect.right > 0:
            self.rect.right -= self.velocity
        else:
            self.reset()
    
    def reset(self):
        self.live = True
        self.life = SmallEnemy.life
        self.rect.left = randint(self.width,self.width + 10*self.rect.width)
        self.rect.top = randint(0, self.height - self.rect.height)
        
class LargeEnemy(pygame.sprite.Sprite):
    
    # 8 bullet hits it, then it is destroied
    life = 8
    
    def __init__(self,width,height):
        pygame.sprite.Sprite.__init__(self)
        
        self.width = width
        self.height = height
        self.image = pygame.image.load("images/largeenemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        # create enemy randomly
        self.rect.left = randint(self.width + 2*self.rect.width,self.width + 10*self.rect.width)
        self.rect.top = randint(0, self.height - self.rect.height)
        
        # the destroy image
        self.boom_image = pygame.image.load("images/boom.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.live = True
        self.moveup = True
        self.life = LargeEnemy.life
        self.velocity = 2
        
    def move(self):
        if self.rect.right > 0:
            self.rect.right -= self.velocity
        else:
            self.reset()
    
    def reset(self):
        self.live = True
        self.life = LargeEnemy.life
        self.rect.left = randint(self.width + 10*self.rect.width,self.width + 20*self.rect.width)
        self.rect.top = randint(0, self.height - self.rect.height)
        
class Boss(pygame.sprite.Sprite):
    
    # 20 bullet hits it, then it is destroied
    life = 20
    
    def __init__(self,width,height):
        pygame.sprite.Sprite.__init__(self)
        
        self.width = width
        self.height = height
        self.image = pygame.image.load("images/boss.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        # create enemy randomly
        self.rect.left = self.width + 5*self.rect.width
        self.rect.top = randint(0, self.height - self.rect.height)
        
        # the destroy image
        self.boom_image = pygame.image.load("images/boom.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.live = True
        self.life = Boss.life
        self.velocity = 2
        
    def moveleft(self):
            self.rect.right -= self.velocity

    def moveup(self):
            self.rect.top -= 3*self.velocity
        
    def movedown(self):
            self.rect.bottom += 3*self.velocity

    def reset(self):
        self.live = True
        self.life = Boss.life
        self.rect.left = self.width + 5*self.rect.width
        self.rect.top = randint(0, self.height - self.rect.height)            
