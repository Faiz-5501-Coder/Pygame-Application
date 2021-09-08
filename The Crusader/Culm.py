#This program was written and continued to be updated from May 12 2018 to June 12 2018 by Mahir Faisal.
#The purpose of this program is to create a custom video game using Python's pygame Graphics module
#The name of the game is called The Crusader!
import pygame, os, random
from pygame.locals import *
from Vec2D import *
#from spritesheet import *
# set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
AQUA = (0, 255, 255)
WOOD = (255, 211, 155)
GREY = (169,169,169)

# set up the frame rate
FRAMERATE = 60

#Friction Constant
PLAYER_FRIC = -0.12

#Platform List 
PLATFORM_LIST = [[(0, WINDOWHEIGHT - 40, WINDOWWIDTH, 40), (10, 300, 200, 40), (400, 300, 200, 40), (400, WINDOWHEIGHT - 150, 105, 40)],
                 [(0, WINDOWHEIGHT - 40, WINDOWWIDTH, 40),(553,458,100,40),(360,448,111,40),(181,354,156,40),(14,315,100,40),(400,126,125,40)],
                 [(620, 562, 135, 40),(3, 581,145,40),(379,409,135,40),(39,409,135,40),(379,573,135,40),(379,200,135,40),(39,291,135,40)]]
#Enemy List
ENEMY_LIST = [[(80, 250, 60, 60), (102, 510,60, 60)],
              [(49,508,60,60),(57,264,60,60),(256,302,60,60)],
              [(49,530,60,60),(73, 358, 60, 60),(87,240,60,60),(441,358,60,60)]]

#PLAYER IMAGES
DIRECTION = []
JUMPING = []

#BACKGROUND IMAGE
BG = pygame.image.load('background.png')
BG = pygame.transform.scale(BG,(WINDOWWIDTH,WINDOWHEIGHT))




def terminate():
    """ This function is called when the user closes the window or presses ESC """
    pygame.quit()
    os._exit(1)

def drawText(text, font, surface, x, y, textcolour): #Takes the text font,text location, surface type, and text colour as input
    """ Draws the text on the surface at the location specified """
    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



    

def display_menu(windowSurface):
    """Displays the menu onto the screen"""
    windowSurface.fill(GREY)
    basicFont = pygame.font.SysFont("Calibri", 20)
    start_text = ['The Crusader!', '1. Play', '2. Instructions','For anyone who is playing this game for the first time,',' view the instructions FIRST before pressing 1 to play']
    height = 120
    titleimage,title_rect = load_image("gametitle.png")
    title_rect.x = 150
    title_rect.y = 50
    windowSurface.blit(titleimage,title_rect) #blits the title image on to screen
    for x in range(len(start_text)):
        drawText(start_text[x], basicFont, windowSurface, 50, height, BLACK)
        height += 30
    pygame.display.update()
def Display_Inst(windowSurface): #Function blits images of the player, enemy and control options
    """Display Instructions"""
    windowSurface.fill(GREY)
    basicFont = pygame.font.SysFont("Calibri", 20,True)
    inst = ['Your objective is to fend off or avoid enemy robots in each level in an attempt to',
            'receive the golden key which is then used to access the next level.','Once you get the key, a door will spawn on the bottom left corner of the screen.',
            'Simply pass through the door in order to gain access to the next level.',
            'Press x to jump from platform to platform and press c to use your energy blaster', 'against incoming enemies. If you are able to push through all 3 levels without being',
            'killed, you win! There are 3 different difficulties to choose from so be careful, as the',
            'harder the difficulty setting the more damage that enemies will impose on to you.','Good luck on your journey! Use the arrow keys to move the player']
    height = 120
    for x in range(len(inst)):
        drawText(inst[x], basicFont, windowSurface, 50, height, BLACK)
        height += 30
    arrow_img,arrow_rect = load_image("arrows_game.png")
    arrow_img = pygame.transform.scale(arrow_img,(200,200))
    arrow_rect.y +=400 
    windowSurface.blit(arrow_img,arrow_rect)
    x_image,x_rect =load_image("X_key.png")
    x_image = pygame.transform.scale(x_image,(300,300))
    x_rect.x+=150
    x_rect.y +=400
    drawText('Jump',basicFont,windowSurface,255,480,BLACK)
    drawText('Shoot',basicFont,windowSurface,400,480,BLACK)
    drawText('You (The Player)',basicFont,windowSurface,480,480,BLACK)
    drawText('Enemy Robot',basicFont,windowSurface,620,450,BLACK)
    windowSurface.blit(x_image,x_rect)
    c_image,c_rect = load_image("C_key.png")
    c_image = pygame.transform.scale(c_image,(90,80))
    c_rect.x+=380
    c_rect.y+=511
    windowSurface.blit(c_image,c_rect)
    MGM, MGM_rect = load_image("Megaman Frames/Running Images/Standing.png")
    MGM = pygame.transform.scale(MGM,(60,60))
    MGM_rect.x+=500
    MGM_rect.y+=512
    windowSurface.blit(MGM,MGM_rect)
    inst_title,inst_rect = load_image("Instructions.png")
    inst_rect.x = 180
    inst_rect.y = 59
    windowSurface.blit(inst_title,inst_rect)
    rob,rob_rect = load_image("Enemy.png")
    rob = pygame.transform.scale(rob,(100,100))
    rob_rect.x += 620
    rob_rect.y += 480
    windowSurface.blit(rob,rob_rect)
    pygame.display.update()
    backscreen = False
    while not backscreen:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    display_menu(windowSurface)
                    backscreen = True
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
def Display_Diff(windowSurface):
    """Displays Difficulty Option"""
    windowSurface.fill(GREY)
    basicFont = pygame.font.SysFont("Calibri", 20)
    diff_text = ['Choose your Difficulty Preference:', '1. Easy', '2. Hard', '3. insane difficulty (You cannot win)']
    height = 120
    for x in range(len(diff_text)):
        drawText(diff_text[x], basicFont, windowSurface, 50, height, BLACK)
        height += 30
    pygame.display.update()
    choose_diff = False
    while choose_diff == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == ord('1'):
                    movespeed = 10
                    lives = 20
                    enemy_damage = 2
                    bulletspeed = 10
                    choose_diff = True
                elif event.key == ord('2'):
                    movespeed = 15
                    lives = 15
                    enemy_damage = 4
                    bulletspeed = 15
                    choose_diff = True
                elif event.key == ord('3'):
                    movespeed = 20
                    lives = 10
                    enemy_damage = 6
                    bulletspeed = 20
                    choose_diff = True
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

    stats = [movespeed,lives, enemy_damage,bulletspeed] 
    return stats               
def show_start(windowSurface):
    """ Allows the user to choose the level.  Based on the choice, 3 variables are
    set: speed of the player, initial health amount, enemy damage, and bullet speed
    is generated.  These 3 stats are returned as a list. """
    windowSurface.fill(GREY)
    basicFont = pygame.font.SysFont("Calibri", 20)
    start_text = ['1. Play', '2. Instructions','For anyone who is playing this game for the first time,','view the instructions FIRST before pressing 1 to play']
    height = 120
    titleimage,title_rect = load_image("gametitle.png") #Blits title image to the screen
    title_rect.x = 150
    title_rect.y = 50
    windowSurface.blit(titleimage,title_rect)
    for x in range(len(start_text)):
        drawText(start_text[x], basicFont, windowSurface, 50, height, BLACK)
        height += 30
    pygame.display.update()
    chosen = False
    while not chosen:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type== KEYDOWN:
                if event.key == ord('1'):
                    stats = Display_Diff(windowSurface)
                    chosen = True
                elif event.key == ord('2'):
                    Display_Inst(windowSurface)
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
    return stats 

def load_image(filename):
    """ Load an image from a file.  Return the image and corresponding rectangle """
    image = pygame.image.load(filename)
    #image = image.convert()        #For faster screen updating
    image = image.convert_alpha()   #Not as fast as .convert(), but works with transparent backgrounds
    return image, image.get_rect()




class Player(pygame.sprite.Sprite):
    """ The player controlled by the user """
    def __init__(self, game,movespeed,lives,enemy_damage):  
        pygame.sprite.Sprite.__init__(self)
        self.game = game #Makes a reference to the game class for jump function
        self.imageright, self.rect = load_image("Megaman Frames/Running Images/Standing.png")
        self.imageright = pygame.transform.scale(self.imageright,(60,60))
        DIRECTION.append(self.imageright)
        self.imageleft = pygame.transform.flip(self.imageright, True, False)
        DIRECTION.append(self.imageleft)
        DIRECTION.append(self.rect)
        self.jumpimageright,self.jumprect = load_image("Megaman Frames/Running Images/JumpR5.png")
        self.jumpimageright = pygame.transform.scale(self.jumpimageright,(60,60))
        JUMPING.append(self.jumpimageright)
        self.jumpimageleft = pygame.transform.flip(self.jumpimageright, True, False)
        JUMPING.append(self.jumpimageleft)
        self.image = DIRECTION[0] #0 position indicates the right and position 1 indicates the left. the player starts off facing right.
       

        #Defines the player's central x and y values 
        self.rect.centerx = 755
        self.rect.centery = 300
        
        # set up movement variables
        self.DirectRight = True
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.movespeed = movespeed
        self.lives = lives
        self.enemy_damage = enemy_damage
        self.position = Vec2d(755,300)
        self.velocity = Vec2d(0,0)
        self.acceleration = Vec2d(0,0)

    def imageDetection(self,imagelist): #Used for jumping and direction images
        if self.DirectRight:
            self.image = imagelist[0]
        if not self.DirectRight:
            self.image = imagelist[1]
        return self.image
        
    def jump(self): #Jump Function - Lets the player jump
        self.rect.y += 0.5
        hit_plat = pygame.sprite.spritecollide(self, self.game.platforms, False) 
        self.rect.y -= 0.5
        if hit_plat:
            if self.rect.top > 0 and self.rect.top < WINDOWHEIGHT:
                self.velocity.y = -23

                
    def update(self): # update the player's position
        """ Change the position of the player's rectangle """
        self.acceleration =  Vec2d(0,1)
        if self.moveDown and self.rect.bottom < WINDOWHEIGHT:
            self.rect.top += self.movespeed
        elif self.moveUp and self.rect.top > 0:
            self.rect.top -= self.movespeed
        elif self.moveLeft and self.rect.left > 0:
            self.rect.left -= self.movespeed
            self.acceleration.x = -0.5 
        elif self.moveRight and self.rect.right < WINDOWWIDTH:
            self.rect.right += self.movespeed
            self.acceleration.x = 0.5 
        if self.rect.bottom < WINDOWHEIGHT:
            self.rect.bottom = self.rect.bottom + self.movespeed
        #accounts for friction - provides smmoth movement
        self.acceleration.x += self.velocity.x * PLAYER_FRIC
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        if self.position.x > WINDOWWIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position = WINDOWWIDTH
        self.rect.bottom = self.position.y
class Enemy(pygame.sprite.Sprite): #Creates an enemy for the game
    def __init__(self, x, y, width, height): 
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image("Enemy.png")
        self.image = pygame.transform.scale(self.image,(width,height))
        self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect()

        self.rect.x = x 
        self.rect.y = y
        self.enemyRight = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height): #init initializes the platform's position on the screen along with the width and height associated with the platform
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image("Platform Images/Plat1.png")
        self.image = pygame.transform.scale(self.image,(width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x #Defines the x,y position of the platform on the screen
        self.rect.y = y
        

class Artifact(pygame.sprite.Sprite): #Generates the gold key artifact
    def __init__(self, player_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image("Artifact Sprite/Gold Key.png")
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image,(80, 50))
        self.rect = self.image.get_rect()
        self.rect.top = random.randint(0,  player_rect.top - self.rect.height)
        self.rect.left = random.randint(0, WINDOWWIDTH - self.rect.width)
        
class Goal(pygame.sprite.Sprite): #Generates the goal door
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image("Door Sprite/Door.png")
        self.image = pygame.transform.scale(self.image,(60, 60))
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(15, 515, 20 ,WINDOWHEIGHT)
        
class Bullet(pygame.sprite.Sprite): #Creates enemy and player bullets
    def __init__(self, x, y, player_direction,bullet_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image("Megaman Frames/Running Images/Buster Bullet.png")
        self.image = pygame.transform.scale(self.image,(40,30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = y
        self.bull_speed = bullet_speed
        self.DirectRight = player_direction
    def update(self):
        if self.DirectRight:
            self.rect.x += self.bull_speed
            if self.rect.right > WINDOWWIDTH:
                self.kill()
        if not self.DirectRight:
            self.rect.x -= self.bull_speed
            if self.rect.left < 0:
                self.kill()

class Level(pygame.sprite.Sprite): #Used to make multiple levels for the game
    def __init__(self, levcount,stats):
        pygame.sprite.Sprite.__init__(self)
        self.Hit_Count = 0
        self.levelnum = levcount
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.goal_door = Goal()
        self.player = Player(self, stats[0], stats[1],stats[2])
        self.enemies = pygame.sprite.Group()
        self.victoryitem = Artifact(self.player.rect)
        self.all_sprites.add(self.victoryitem)
        self.all_sprites.add(self.player)
        

        enemy = ENEMY_LIST[self.levelnum]
        for e in enemy:
            enem = Enemy(*e)
            self.all_sprites.add(enem)
            self.enemies.add(enem)

        platform = PLATFORM_LIST[self.levelnum]
        for plat in platform:
            plats = Platform(*plat)
            self.all_sprites.add(plats)
            self.platforms.add(plats)   
class Game():
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self,stats):
        """ Constructor. Create all our attributes and initialize
        the game. The stats provided customize the game. """

        self.GamePlayedOnce = False
        self.LevelPlayedOnce = False
        self.LosePlayedOnce = False
        self.level_win = False
        self.game_lose = False
        self.game_win = False
        #Set to True when game or level has been won or lost
        self.levelCount = 0 #Keeps a counter for the number of levels in the game
        self.stats = stats
        self.level = Level(self.levelCount,self.stats)
        # set up music
        pygame.mixer.music.load('GHZ.ogg')
        self.levelWinAudio = pygame.mixer.Sound('levelvic.ogg')
        self.gameWinAudio = pygame.mixer.Sound('gamewin.ogg')
        self.gameLoseAudio = pygame.mixer.Sound('gameover.ogg')
        self.MU_Music = pygame.mixer.Sound('Prelude.ogg')
        self.PlayerDamagedEffect = pygame.mixer.Sound('roblox.ogg')

        # Play the background music
        pygame.mixer.music.play(-1, 0.0)
        self.musicPlaying = True
        
    def process_events(self, windowSurface):
        """ Process all of the keyboard and mouse events.  """

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    self.level.player.moveRight = False
                    self.level.player.moveLeft = True
                    self.level.player.image = DIRECTION[1]
                    self.level.player.DirectRight = False
                elif event.key == K_RIGHT or event.key == ord('d'):
                    self.level.player.moveLeft = False
                    self.level.player.moveRight = True
                    self.level.player.image = DIRECTION[0]
                    self.level.player.DirectRight = True
                elif event.key == K_UP or event.key == ord('w'):
                    self.level.player.moveDown = False
                    self.level.player.moveUp = True
                elif event.key == K_DOWN or event.key == ord('s'):
                    self.level.player.moveUp = False
                    self.level.player.moveDown = True
                elif event.key == ord('x'):
                    self.level.player.jump() #Player Jumps
                elif event.key == ord('c'): #Player shoots a bullet
                    bullet = Bullet(self.level.player.rect.x, self.level.player.rect.centery,self.level.player.DirectRight,self.stats[3])
                    self.level.all_sprites.add(bullet)
                    self.level.player_bullets.add(bullet)

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_LEFT or event.key == ord('a'):
                    self.level.player.moveLeft = False
                elif event.key == K_RIGHT or event.key == ord('d'):
                    self.level.player.moveRight = False
                elif event.key == K_UP or event.key == ord('w'):
                    self.level.player.moveUp = False
                elif event.key == K_DOWN or event.key == ord('s'):
                    self.level.player.moveDown = False
                elif event.key == ord('m'):
                    # toggles the background music
                    if self.musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    self.musicPlaying = not self.musicPlaying                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #The user clicks to restart the game when it is over
                #Elif event continues to execute until user wins or loses the game
                if self.game_lose or self.game_win:
                    #Display the menu, choose a level and start a new game
                    self.gameWinAudio.stop()
                    self.gameLoseAudio.stop()
                    self.levelWinAudio.stop()
                    self.MU_Music.play()
                    display_menu(windowSurface)
                    stats = show_start(windowSurface)
                    self.MU_Music.stop()
                    self.__init__(stats)
                elif self.level_win:
                    self.levelCount += 1
                    self.LevelPlayedOnce = False
                    self.levelWinAudio.stop()
                    pygame.mixer.music.play(-1,0.0)
                    if self.levelCount <3:
                        self.level = Level(self.levelCount, self.stats)
                        self.level_win = False
                else:
                    self.game_win = True

    
                      
    def run_logic(self):
        """ This method is run each time through the frame. It
        updates positions and checks for collisions. """
        if not self.game_win or not self.game_lose or not self.level_win:
            for enemy in self.level.enemies:
                if self.level.player.rect.centery < enemy.rect.bottom and self.level.player.rect.centery > enemy.rect.top:
                    if self.level.player.rect.right > enemy.rect.right:
                        if len(self.level.enemy_bullets) == 0: 
                            enemy_bullet = Bullet(enemy.rect.x, enemy.rect.centery, enemy.enemyRight,self.stats[3])
                            self.level.all_sprites.add(enemy_bullet)
                            self.level.enemy_bullets.add(enemy_bullet)
                        bullet_hits_player = pygame.sprite.spritecollide(self.level.player, self.level.enemy_bullets, True)
                        if len(bullet_hits_player) > 0:
                            self.level.player.lives -= self.level.player.enemy_damage
                            self.PlayerDamagedEffect.play()
                bullet_hits_enemy = pygame.sprite.spritecollide(enemy, self.level.player_bullets, True)
                        
                if len(bullet_hits_enemy) > 0:
                    self.level.Hit_Count += 1
                    if self.level.Hit_Count == 3: #Kills enemy after 3 hits
                        enemy.kill()
                        self.level.Hit_Count = 0
            for platform in self.level.platforms:
                bullet_hits_platform = pygame.sprite.spritecollide(platform, self.level.player_bullets, True)

                
                            
                                        
            # update the all_sprites group
            self.level.all_sprites.update()
            # check for collisions and remove the enemy if killed by the player. Also checks for player-platform collisions
            platform_hits = pygame.sprite.spritecollide(self.level.player, self.level.platforms, False)
            if len(platform_hits) > 0:
                if self.level.player.rect.top > platform_hits[0].rect.top:
                    self.level.player.rect.top = platform_hits[0].rect.bottom - 1
                    self.level.player.velocity.y = 3
                elif self.level.player.rect.top < platform_hits[0].rect.top:
                    self.level.player.position.y = platform_hits[0].rect.top + 1
                    self.level.player.velocity.y = 0
                    self.level.player.image = self.level.player.imageDetection(DIRECTION)
            else:
                self.level.player.image = self.level.player.imageDetection(JUMPING)

            if self.level.player.rect.colliderect(self.level.victoryitem.rect):
                self.level.all_sprites.add(self.level.goal_door)
                self.level.all_sprites.remove(self.level.victoryitem)
                
            #Checks if player won or lose the game
            if self.level.player.rect.colliderect(self.level.goal_door.rect) and self.level.goal_door in self.level.all_sprites and self.levelCount <3:
                self.level_win = True
            if self.level.player.lives <=0 or self.level.player.rect.y >WINDOWHEIGHT:
                self.PlayerDamagedEffect.stop() #Plays a sound effect whenever the player is damaged by the enemy
                self.game_lose = True
            if self.levelCount == 3:
                self.game_win = True
                
                

  
    def display_frame(self, windowSurface):
        """ Display everything to the screen for the game. """
        
        # draw the background image onto the surface
        windowSurface.blit(BG,(0,0))
        if self.game_win:
            if not self.GamePlayedOnce:
                pygame.mixer.music.stop()
                self.gameWinAudio.play()
                self.GamePlayedOnce = True
            
            # The user will click to restart the game
            windowSurface.fill(BLACK)
            x = WINDOWWIDTH / 2 - 120
            y = WINDOWHEIGHT / 2 - 20
            basicFont = pygame.font.SysFont("Comic Sans MS", 20)
            drawText("You Win! Click to return to the menu", basicFont, windowSurface, x ,y, GREEN)
                
        elif self.level_win:
            if not self.LevelPlayedOnce:
                pygame.mixer.music.stop()
                self.levelWinAudio.play()
                self.LevelPlayedOnce = True
            windowSurface.fill(BLACK)
            x = WINDOWWIDTH / 2 - 120
            y = WINDOWHEIGHT / 2 - 20
            basicFont = pygame.font.SysFont("Comic Sans MS", 20)
            drawText("Mission Success! Click to Proceed", basicFont, windowSurface, x ,y, GREEN)
            #The user will click to proceed to the next level
                
        
        elif self.game_lose:
            if not self.LosePlayedOnce:
                pygame.mixer.music.stop()
                self.gameLoseAudio.play()
                self.LosePlayedOnce = True
            windowSurface.fill(BLACK)
            x = WINDOWWIDTH / 2 - 120
            y = WINDOWHEIGHT / 2 - 20
            basicFont = pygame.font.SysFont("Comic Sans MS", 20)
            drawText("Mission Failed! Click to return to the main menu", basicFont, windowSurface, x ,y, GREEN)
            #The player clicks to restart game
            
        
        else:
            # draw the player and the level attributes onto the surface
            self.level.all_sprites.draw(windowSurface)
            basicFont = pygame.font.SysFont("Comic Sans MS",20)
            drawText("Health: "+str(self.level.player.lives), basicFont, windowSurface,0,0,YELLOW)
            drawText("Level: "+str(self.levelCount+1),basicFont,windowSurface,700,0,YELLOW)
 
        # draw and update the window onto the screen
        pygame.display.update()

def main():
    """ Mainline for the program """
    
    pygame.init()
    mainClock = pygame.time.Clock()

    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('The Crusader')
    #Display a menu, choose a level and instantiate a game
    #MENU MUSIC
    MU_Music = pygame.mixer.Sound('Prelude.ogg')
    MU_Music.play()
    stats = show_start(windowSurface)
    MU_Music.stop()
    game = Game(stats)
        
    # run the game loop until the user quits
    while True:
        # Process events (keystrokes, mouse clicks, etc)
        game.process_events(windowSurface)

        # Update object positions, check for collisions
        game.run_logic()
        
        # Draw the current frame
        game.display_frame(windowSurface)        
        
        mainClock.tick(FRAMERATE)
        
main()

    
