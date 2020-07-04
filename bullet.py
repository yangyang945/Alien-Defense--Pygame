# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 10:26:53 2018

@author: Surface-S
"""

import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = position
        
        #use mask to check the collides
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 24
        self.live = True
        
    def reset(self,position):
        self.rect.left, self.rect.bottom = position
        self.live = True

    def move(self):
        if self.rect.left <= 1200:
            self.rect.left += self.velocity
        else:
            self.live = False
            
class BossBullet(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bossbullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = position
        
        #use mask to check the collides
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 10
        self.live = True
        
    def reset(self,position):
        self.rect.left, self.rect.bottom = position
        self.live = True

    def move(self):
        if self.rect.left >= 0:
            self.rect.left -= self.velocity
        else:
            self.live = False