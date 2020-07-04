# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:32:48 2018

@author: Surface-S
"""

import pygame
import sys
import platform
import os
import player
import enemy
import bullet
from pygame import K_w,K_s,K_a,K_d,K_UP,K_DOWN,K_LEFT,K_RIGHT,MOUSEBUTTONDOWN

screen_width = 1200
screen_height = 500
LIVES = 3 
SCORE = 0
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('sound/main_theme.ogg')
pygame.mixer.music.set_volume(0.2)

bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)

me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
me_down_sound.set_volume(0.2)

enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.2)

bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)

def main():
    global LIVES, SCORE
    global screen
    
    #initial level is 1
    level = 1
    
    pygame.mixer.music.play(-1)
    
    screen = pygame.display.set_mode((screen_width,screen_height))
    background = pygame.image.load("images/blackbroad.jpg").convert()
    
    # this is the player
    me = player.Player(screen_width,screen_height)
    enemies = pygame.sprite.Group()
    
    # this is the boss
    boss1 = enemy.Boss(screen_width,screen_height)
    enemies.add(boss1)
    
    smallenemy = pygame.sprite.Group()
    # create many small enemies
    create_smallenemy(enemies,smallenemy,10)
    
    largeenemy = pygame.sprite.Group()
    # create many small enemies
    create_largeenemy(enemies,largeenemy,1)
    
    # create the boss's bullet
    bossbullet = pygame.sprite.Group()
    # bullets fired from the midleft of the boss
    bossbullet.add(bullet.BossBullet(boss1.rect.midleft))
    
    # use list to contain each bullet 
    bullet1 = []
    bullet_index = 0
    bullet_num = 20
    # set the initial bullets frequence, if the "bullet_frequence" is smaller, then the player fires more bullet in per second
    bullet_frequence = 10
    
    for i in range(bullet_num):
        # bullets fired from the midright of the player
        bullet1.append(bullet.Bullet(me.rect.midright))
        
    pause = False
    
    #images of pause and resume
    pause_image = pygame.image.load("images/pause.png").convert_alpha()
    resume_image = pygame.image.load('images/resume.png').convert_alpha()
    pause_rect = pause_image.get_rect()
    pause_rect.left, pause_rect.top = screen_width - pause_rect.width - 10, 10
    
    # use this to show images longer and show many bullets on screen
    delay = 50
    
    # control the speed of loops
    timer = pygame.time.Clock()
    
    while True:
        # add the difficulties
        if SCORE >= 8000 and level == 1:
            create_smallenemy(enemies,smallenemy,10)
            create_largeenemy(enemies,largeenemy,5)
            bullet_frequence -= 2
            level += 1
            
        if SCORE >= 15000 and level == 2:
            create_smallenemy(enemies,smallenemy,10)
            create_largeenemy(enemies,largeenemy,5)
            bullet_frequence -= 2
            level += 1
            
        if SCORE >= 30000 and level == 3:
            
            create_largeenemy(enemies,largeenemy,5)
            bullet_frequence -= 2
            level += 1
        
        if SCORE >= 40000 and level == 4:
            
            create_largeenemy(enemies,largeenemy,10)
            level += 1
            
        show ("lives {}, score {}".format(LIVES, SCORE))
        
        # to check if quit
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break
        
        # to check if puased
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1 and pause_rect.collidepoint(e.pos):
                pause = not pause
                if pause:
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()
                else:
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()
        
        if LIVES:
            if not pause:
                screen.blit(pause_image,pause_rect)
                
                # whether the player collide with any enemy
                which_collide = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
                if which_collide: #at least one enemy collides with the player
                    me_down_sound.play(0)
                    me.live = False
                    for en in which_collide:
                        enemy1_down_sound.play(0)
                        en.live = False
                
                # fire 1 bullet every 12 loops
                if not (delay % bullet_frequence):
                    bullet_sound.play(0)
                    bullet1[bullet_index].reset(me.rect.midright)
                    bullet_index = (bullet_index + 1) % bullet_num
                
                # if the boss lives
                if boss1.live:
                    for bossbu in bossbullet:
                        #only if boss appear in the screen, boss fire bullets
                        if (bossbu.live) and (boss1.rect.left == screen_width//4 * 3):
                            bossbu.move()
                            screen.blit(bossbu.image,bossbu.rect)
                        else:
                            bossbu.reset(boss1.rect.midleft)
                    # level higher than or equal to 3, boss comes out
                    # boss moves left to 3/4 screen, then moves up and down
                    if boss1.rect.left > screen_width//4 * 3 and level >= 3:
                        boss1.moveleft()
                    # if the player is upper, boss moves up
                    elif (me.rect.top + me.rect.height//2)<(boss1.rect.top + boss1.rect.height//2)-1:
                        boss1.moveup()
                    # if the player is lower, boss moves down
                    elif (me.rect.top + me.rect.height//2)>(boss1.rect.top + boss1.rect.height//2)+1:
                        boss1.movedown()
                    screen.blit(boss1.image,boss1.rect)
                    
                    # darw the life bar
                    if boss1.life >= 5:
                        bar_color = GREEN
                    else:
                        bar_color = RED
                    pygame.draw.line(screen, bar_color,
                                             (boss1.rect.left, boss1.rect.top + 45),
                                             (boss1.rect.left + boss1.rect.width * boss1.life // enemy.Boss.life,
                                              boss1.rect.top + 45),
                                             2)
                if not (boss1.live): #boss destroied
                    screen.blit(boss1.boom_image,boss1.rect)
                    # use delay to show destroy image on screen longer
                    if not (delay % 7):
                        SCORE += 1000
                        boss1.reset()
                        
                for each in largeenemy:
                    if (each.live):    
                        each.move()
                        screen.blit(each.image,each.rect)
                        
                        # darw the life bar
                        if each.life >= 3:
                            bar_color = GREEN
                        else:
                            bar_color = RED
                        pygame.draw.line(screen, bar_color,
                                         (each.rect.left, each.rect.top),
                                         (each.rect.left + each.rect.width * each.life // enemy.LargeEnemy.life,
                                          each.rect.top ),
                                         2)
    
                    else: # enemy destroied
                        screen.blit(each.boom_image,each.rect)
                        # use delay to show destroy image on screen longer
                        if not (delay % 7):
                            SCORE += 500
                            each.reset() 
                
                for each in smallenemy:
                    if (each.live):    
                        each.move()
                        screen.blit(each.image,each.rect)
                    else: # enemy destroied
                        screen.blit(each.boom_image,each.rect)
                        # use delay to show destroy image on screen longer
                        if not (delay % 7):
                            SCORE += 100
                            each.reset()
                
                # to check if the boss's bullet hits the player
                bossbullet_collide = pygame.sprite.spritecollide(me,bossbullet,False,pygame.sprite.collide_mask)
                if bossbullet_collide: #at least one enemy collides with the player
                    me_down_sound.play(0)
                    me.live = False
                    for bossbu in bossbullet_collide:
                        bossbu.live = False
                
                # to check if any player's bullet hits any enemies
                for bul in bullet1:
                    if bul.live == True:
                        bul.move()
                        screen.blit(bul.image,bul.rect)
                        
                        bullet_collide = pygame.sprite.spritecollide(bul,enemies,False,pygame.sprite.collide_mask)
                        # if any collide happens
                        if bullet_collide: 
                            bul.live = False
                            for en in bullet_collide:
                                # each hits makes enemies' life minues one
                                en.life -= 1
                                # when the enemies's life is zero, they are destroied
                                if en.life == 0:
                                    enemy1_down_sound.play(0)
                                    en.live = False
                                    
                                
                pygame.display.flip()
                
                # to check the player's moving
                key_pressed = pygame.key.get_pressed()
                if key_pressed[K_w] or key_pressed[K_UP]:
                    me.Up()
                if key_pressed[K_s] or key_pressed[K_DOWN]:
                    me.Down()   
                if key_pressed[K_a] or key_pressed[K_LEFT]:
                    me.Left()
                if key_pressed[K_d] or key_pressed[K_RIGHT]:
                    me.Right()
                    
                # create the background
                screen.blit(background,(0,0))
                
                if (me.live):
                    screen.blit(me.playerimage,me.rect)  
                else: # the player destroied
                    screen.blit(me.boom_image,me.rect)
                    # use delay to show destroy image on screen longer
                    if not (delay % 7):
                        LIVES -= 1
                        me.reset()                   
                
                if platform.system() == "Windows":
                    timer.tick(30)
              
                delay -= 1
                # reset delay
                if delay == 0:
                    delay = 50
                    
            else:#if paused
                screen.blit(background,(0,0))
                # show resume image
                screen.blit(resume_image,pause_rect)
                # show text "PAUSED"
                pause_font = pygame.font.Font('font/rough.TTF', 48)
                pause_text1 = pause_font.render('PAUSED', False, WHITE)
                pause_text1_rect = pause_text1.get_rect()
                pause_text1_rect.left, pause_text1_rect.top = \
                    (screen_width - pause_text1_rect.width) // 2, screen_height // 3
                screen.blit(pause_text1, pause_text1_rect)
                pygame.display.flip()
                
        elif LIVES == 0:#live=0
            pygame.mixer.music.stop()
            pygame.mixer.stop()
                    
            screen.blit(background,(0,0))
            
            #show text "Your Score"
            gameover_font = pygame.font.Font('font/font.TTF', 48)
            gameover_text1 = gameover_font.render('Your Score', False, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                    (screen_width - gameover_text1_rect.width) // 2, screen_height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
                    
            
            #show the score
            gameover_text2 = gameover_font.render(str(SCORE), False, WHITE)
            gameover_text2_rect = gameover_text1.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                    (screen_width - gameover_text1_rect.width) // 2, gameover_text1_rect.bottom + 10                                 
            screen.blit(gameover_text2, gameover_text2_rect)
            
            #show text "Game Over"
            gameover_text0 = gameover_font.render("Game Over", False, WHITE)
            gameover_text0_rect = gameover_text0.get_rect()
            gameover_text0_rect.left, gameover_text0_rect.top = \
                                         (screen_width - gameover_text1_rect.width) // 2, gameover_text1_rect.top - 70
            screen.blit(gameover_text0, gameover_text0_rect)
            
            pygame.display.flip()
            
    pygame.quit()
    if platform.system() == "Windows":
        sys.exit()

    os._exit(0)

# this function is to create many small enemies
def create_smallenemy(group1,group2,num):
    for i in range(num):
        # create class element
        enemy1 = enemy.SmallEnemy(screen_width, screen_height)
        # add this element to group1 and group2
        group1.add(enemy1)
        group2.add(enemy1)

# this function is to create many large enemies
def create_largeenemy(group1,group2,num):
    for i in range(num):
        enemy1 = enemy.LargeEnemy(screen_width, screen_height)
        group1.add(enemy1)
        group2.add(enemy1)
        
        group2.add(enemy1)

def show(text):
    pygame.font.init()
    myFont = pygame.font.Font('font/font.ttf', 25)
    surf = myFont.render(text, False, pygame.Color("black"), pygame.Color("white"))
    screen.blit(surf, (0,0))        
        
        
# enjoy now        
main()



