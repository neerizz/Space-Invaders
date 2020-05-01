import pygame 
import random
import math
from pygame import mixer

pygame.init()  #initializing pyagme

screen = pygame.display.set_mode((800,600))  #setting up the display console
 
pygame.display.set_caption("Space Invaders") #Title of the game  

#Game Icon in titlebar
icon = pygame.image.load("alien.png")       
pygame.display.set_icon(icon)   

#Player avatar,initial_position,sensitivity_variable
player_img=pygame.image.load("space-invaders.png")
playerX=368
playerY=480
playerX_change=0


#enemy avatar, position, speed
enemy_img= []
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)




#bullet avatar, position, speed
bullet_img=pygame.image.load("bullet.png")
bulletX=375
bulletY=492
bulletX_change=0
bulletY_change=8
bulletstate="ready"

#score
score_value=0
font=pygame.font.Font("freesansbold.ttf",32)

textX=10
textY=10


over_font = pygame.font.Font("freesansbold.ttf",70)
def show_Score(x,y):
    score=font.render('Score:'+str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True, (255,255,255))
    screen.blit(over_text,(190,250))

#background image
background = pygame.image.load("space.png")

mixer.music.load("background.wav")
mixer.music.play(-1)

#function to call player avatar 
def player(x,y):
    screen.blit(player_img,(x,y))

#function to call enemy avatar
def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

#function to call BULLET avatar 
def fire_bullet(x,y):
    global bulletstate
    bulletstate="fire"
    screen.blit(bullet_img,(x+17,y+16))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

#infinite while loop to hold the console and control events
running = True
while running:
    screen.blit(background,(0,0))           #Background image
   # screen.fill((0,0,0))
    for event in pygame.event.get():        #iterating through all events
        if event.type == pygame.QUIT:       #to close window when cross is pressed
            running = False
        if event.type == pygame.KEYDOWN:    #when key is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -3         #when left key is pressed
            if event.key == pygame.K_RIGHT:
                playerX_change = 3          #when right key is pressed
            if event.key == pygame.K_SPACE:
                if bulletstate is "ready":
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:      #when key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:     #only when left or right arrow key is released  
                playerX_change=0                                              #stop when key is released          
            #if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:   #To make the enemy move
             #   enemyX_change=1.5                                               
    playerX += playerX_change   #player position update
    if playerX<=0:              #player boundary conditions
        playerX=0  
    elif playerX>=736:
        playerX=736
    
    for i in range(num_of_enemies):

        if enemyY[i]>452:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]     #enemy position update     
        if enemyX[i]<=0:               #enemy boundary conditions
            enemyX_change[i]=4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-4    
            enemyY[i] += enemyY_change[i]
        

        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_sound=mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY=492
            bulletstate="ready"
            score_value +=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)    
    if bulletY<=0: 
        bulletY=480
        bulletstate="ready"
    if bulletstate=="fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    show_Score(textX,textY)
    player(playerX,playerY)    #calling player avatar  
    pygame.display.update()    #display update--must be added at end    