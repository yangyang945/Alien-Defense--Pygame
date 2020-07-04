# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 12:02:45 2018

@author: Surface-S
"""

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        
        self.playerimage = pygame.image.load("images/tuya.png").convert_alpha()
        # get the position of the player
        self.rect = self.playerimage.get_rect()
        self.rect.left = self.width // 2 - self.rect.width // 2
        self.rect.top = self.height - self.rect.height
        
        # the destroy image
        self.boom_image = pygame.image.load("images/boom.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.playerimage)
        
        self.live = True
        
        self.velocity = 16
        
    def reset(self):
        self.live = True
        self.playerimage = pygame.image.load("images/tuya.png").convert_alpha()
        
    def Up(self):
        if self.rect.top < 0:
            self.rect.top = self.height - self.rect.height
        else: # if reach the upper bound, goes to the bottom of screen 
            self.rect.top -= self.velocity
            
    def Down(self):
        if self.rect.bottom > self.height:
            self.rect.bottom = self.rect.height
        else:# if reach the lower bound, goes to the top of screen
            self.rect.bottom += self.velocity   

    def Left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.velocity
            
    def Right(self):
        if self.rect.right >= self.width:
            self.rect.right = self.width
        else:
            self.rect.right += self.velocity