import pygame, sys
from pygame.locals import QUIT
import random
import math
from boat import Boat

pygame.init()
#room
screen = pygame.display.set_mode((600, 550))

#player
player_x = 200
player_z = 0
player_z_spd = 0
player_y = 500
player_y_spd = 0
player_size = 50
player_spd = 4
player_PE = 0
player_jumpDur = 1
jump_start = 0
jumping = False
points = 0
touching_boat = True


#enemy
boats = []
for i in range(10):
    boats.append(Boat(random.randint(0,600),i * 50,pygame.image.load("boat.png"),random.choice([-1,1]),1,screen))
enemy_x = 2005
enemy_y = 500

#arrays
enemys_x = [200,-100,-100,-100,-100]
enemys_spd = [1,2,3,4,5]
random_r = [0,0,0,0,0]
moving = [True,False,False,False,False]
time = 0

for i in range(-5,5):
    random_r[i] = random.randint(0,500)
    enemys_spd[i] = random.randint(0,5)
    
#player visual
player_up = pygame.transform.scale(pygame.image.load("player_up.png"),(player_size,player_size))
player_down = pygame.transform.scale(pygame.image.load("player_down.png"),(player_size,player_size))
player_right = pygame.transform.scale(pygame.image.load("player_right.png"),(player_size,player_size))
player_left = pygame.transform.scale(pygame.image.load("player_left.png"),(player_size,player_size))
player_shadow = pygame.transform.scale(pygame.image.load("player_shadow.png"),(player_size,(player_size / 3 )))
player_direction = player_up
player_alive = True

#backround
dock = pygame.transform.scale(pygame.image.load("pole.png"),(player_size * 4,player_size * 4))
backround = pygame.transform.scale(pygame.image.load("backround.png"),(600,550))
backround_y = 0
death_img = pygame.transform.scale(pygame.image.load("death.png"),(600,550))
font  = pygame.font.Font("Font.ttf",30)
#rect
enemy = pygame.transform.scale(pygame.image.load("boat.png"),(200,100))
obj_enemy = enemy.get_rect(center = (enemys_x[0],enemy_y))
obj_shadow = player_shadow.get_rect(center = (0,0))
obj_player = player_direction.get_rect(center = (player_x,player_y))
obj_jumpman = player_direction.get_rect(center = (player_x,player_y))
obj_dock = dock.get_rect(center = (200,615))
#fps
clock = pygame.time.Clock()


def event_handler():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

def keyboard_input():
    keys = pygame.key.get_pressed()
    global player_x,player_y,player_direction,player_PE,player_y_spd,player_x_spd,jumping,jump_start,player_z_spd
    if keys[pygame.K_LEFT] == True:
        if not player_x <= 0:
            player_x -= player_spd
            player_direction = player_left
    if keys[pygame.K_RIGHT] == True:
        if not player_x >= 600:      
            player_x += player_spd
            player_direction = player_right
    if keys[pygame.K_UP] == True:
        if not player_y <= 0:
            #player_y -= player_spd
            update_camera(-player_spd)
            player_direction = player_up
    if keys[pygame.K_DOWN] == True:
        if not player_y >= 550:
            #player_y += player_spd
            update_camera(player_spd)
            player_direction = player_down
    if keys[pygame.K_SPACE] == True:
        if player_PE < 200:
            player_PE += 5
    else:
        if abs(player_PE) > 0 and not jumping:
            jumping = True
            jump_start = pygame.time.get_ticks()
            player_z_spd = player_PE * 0.1
            player_y_spd = -abs(player_PE * 0.11)
        player_PE = 0

def update_camera(boat_y_spd):
    global boats,dock,backround_y,points
    boat_height = 0
    for boat in boats:
        boat.y -= boat_y_spd
        boat_height = boat.size[1]
    obj_dock.y -= boat_y_spd
    backround_y -= boat_y_spd * 0.2
    if backround_y > screen.get_height():
        backround_y = 0
    points += boat_y_spd 
    #print(abs(points//boat_height))

            


def update():
    global enemy_x,enemy_y,obj_player,obj_enemy,player_x,player_y,player_y_spd,time,obj_shadow,jumping,player_jumpDur,player_PE,jump_start,player_z,player_z_spd,boats,backround_y,touching_boat,player_alive
    touching_boat = False
    for boat in boats:
        boat.update() 
        if obj_player.colliderect(boat.get_hitbox()) or obj_player.colliderect(obj_dock) and not jumping:
            touching_boat = True
    enemy_x += 1
    backround_y += -math.cos(pygame.time.get_ticks() * 0.01) * 0.4
    for i in range(5):
        if moving[i]:
            enemys_x[i] += enemys_spd[i]
    for boat in boats:
        pass
    
    time += 1
    
    if abs(player_y_spd) < 0.05:
        player_y_spd = 0
    else:
        obj_jumpman.y = obj_player.y
    for boat in boats:
        if not obj_shadow.colliderect(obj_dock):
            if obj_shadow.colliderect(boat.get_hitbox()):
                player_x += boat.speed * boat.direction
            
            #print("You Died")    
    if jumping:
        #player_y += player_y_spd
        update_camera(player_y_spd)
        player_z += player_z_spd
        player_y_spd *= 0.85
        # z jump
        if player_z_spd > 5:
            player_z_spd *= 0.88
        else:
            player_z_spd -= 1
            if player_z < 2:
                jumping = False
                player_z = 0
    elif not player_alive:
        death()     
 
            
            # y jump
    
    #     player_y -= jump((pygame.time.get_ticks() - jump_start)/1000,player_jumpDur,player_PE)
   

def draw():
    global obj_player,obj_enemy,obj_shadow,player_z,boats,backround_y,touching_boat,player_alive
    screen.fill((198, 245, 240))
    screen.blit(backround,(0,backround_y))
    screen.blit(backround,(0,backround_y - screen.get_height()))
    screen.blit(dock,obj_dock)
    obj_player = player_direction.get_rect(center = (player_x,player_y - player_z))
    obj_shadow = player_shadow.get_rect(center = (player_x,player_y + player_size * 0.5))
    for boat in boats:
        boat.render()
    screen.blit(player_shadow,obj_shadow)
    screen.blit(player_direction,obj_player)
    
    if player_y_spd > 0:
        screen.blit(player_direction,obj_jumpman) 
    if not touching_boat and player_z == 0:
        player_alive = False
        print("Debug")
    if not player_alive:
        death()
    pygame.display.update()
        
def death():
    global points
    #fade
    screen.blit(death_img,(0,0))
    death_point = font.render("Points",False,(255,255,255))
    death_font = font.render(f"{round(-points)}",False,(255,255,255))
    screen.blit(death_point,(215,220))
    screen.blit(death_font,(260,255))

while True:
    clock.tick(60) 
    event_handler()
    if player_alive:
        keyboard_input()
    update()
    draw()
    
    
    
   