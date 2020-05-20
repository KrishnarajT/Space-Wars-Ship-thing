import pygame
import os
import random
import pyautogui
from Ky_Game import color
from pygame import mixer

pygame.font.init()
pygame.mixer.init()
# GENERAL CONSTANTS
WIDTH, HEIGHT = pyautogui.size()
FPS = 90
ORIGIN = (0, 0)

# adding music
pygame.mixer.music.load( "assets/bgm.wav" )
laser_Sound = pygame.mixer.Sound( "assets/laser.wav" )
explosion_Sound = pygame.mixer.Sound( "assets/explosion.wav" )
pygame.mixer.music.play( -1 )

# WINDOW CONSTANTS
WIN = pygame.display.set_mode( (WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.RESIZABLE )
pygame.display.set_caption( "Ship Shooter" )

# CONSTANT DEFITNIONS
# ENEMY SHIPS
RED_SPACE_SHIP = pygame.transform.scale( pygame.image.load(
    os.path.join( "assets", "pixel_ship_red_small.png" ) ), (140, 100) )

BLUE_SPACE_SHIP = pygame.transform.scale( pygame.image.load(
    os.path.join( "assets", "pixel_ship_blue_small.png" ) ), (100, 100) )

GREEN_SPACE_SHIP = pygame.transform.scale( pygame.image.load(
    os.path.join( "assets", "pixel_ship_green_small.png" ) ), (140, 100) )

# PLAYER'S SHIP
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join( "assets", "pixel_ship_yellow.png" ) )

# LASERS
RED_LASER = pygame.image.load(
    os.path.join( "assets", "pixel_laser_red.png" ) )

BLUE_LASER = pygame.image.load(
    os.path.join( "assets", "pixel_laser_blue.png" ) )

GREEN_LASER = pygame.image.load(
    os.path.join( "assets", "pixel_laser_green.png" ) )

YELLOW_LASER = pygame.image.load(
    os.path.join( "assets", "bullet.png" ) )

# BACKGROUND IMAGE - SCALED TO FIT THE SCREEN
BG_IMAGE = pygame.transform.scale( pygame.image.load( os.path.join( "assets", "SPACE WARS BGI.png" ) ),
                                   (WIDTH, HEIGHT) )
BG_IMAGE_LOST = pygame.transform.scale( pygame.image.load( os.path.join( "assets", "SPACE WARS BG LOST.png" ) ),
                                        (WIDTH, HEIGHT) )

# class for all the laser activity in the game.
class Laser:
    def __init__( self, x, y, img ):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface( self.img )
    
    def DrawLaser_( self, Window ):
        Window.blit( self.img, (self.x, self.y) )
    
    def MoveLaser_( self, Laser_Vel ):
        self.y += Laser_Vel
    
    def OffScreenLaser_( self, Height ):
        if self.y >= Height or (self.y + self.img.get_height()) < 0:
            return True
        else:
            return False
    
    def LaserCollision_( self, Collided_Obj ):
        return collide( self, Collided_Obj )

# Defining the ship class to later inherit others from it.
class GenShip:
    COOLDOWN = 30
    
    def __init__( self, x, y, Health = 100 ):
        self.x = x
        self.y = y
        self.Health = Health  # HEALTH REMAINING
        self.Ship_Image = None  # SPRITE THAT WILL HAVE THE SHIP IMAGE
        self.Laser_Image = None  # SPRITE THAT WILL HAVE THE SHIP'S LASER'S IMAGE
        self.Lasers = []  # ARRAY FOR SOME REASON
        self.Cool_Down_Counter = 0  # TIME BETWEEN 2 LASERS THAT GET SHOT
    
    # returns the image width, that got assigned to Ship_Image
    def GetWidth_( self ):
        return self.Ship_Image.get_width()
    
    # returns the image height, that got assigned to Ship_Image
    def GetHeight_( self ):
        return self.Ship_Image.get_height()
    
    def LaserCoolDown_( self ):
        if self.Cool_Down_Counter >= self.COOLDOWN:
            self.Cool_Down_Counter = 0
        elif self.Cool_Down_Counter > 0:
            self.Cool_Down_Counter += 1
    
    def ShootLaser_( self ):
        if self.Cool_Down_Counter == 0:
            Laser_Obj = Laser( self.x, self.y, self.Laser_Image )
            self.Lasers.append( Laser_Obj )
            self.Cool_Down_Counter = 1

class Player( GenShip ):

    Fin = open("Assets/Highscore.txt", "r")
    StuffInFile = Fin.read()
    HighScore = int( StuffInFile )
    Fin.close()
    CurHighScore = 0
    
    if CurHighScore < 20:
        PLAYER_COOLDOWN = 30
    elif CurHighScore >= 20:
        PLAYER_COOLDOWN = 22
    elif CurHighScore >= 30:
        PLAYER_COOLDOWN = 17
    elif CurHighScore >= 40:
        PLAYER_COOLDOWN = 15
        
    def __init__( self, x, y, Health = 100 ):
        super().__init__( x, y, Health )
        self.Ship_Image = YELLOW_SPACE_SHIP
        self.Laser_Image = YELLOW_LASER
        self.mask = pygame.mask.from_surface( self.Ship_Image )  # mask for collision
        self.Max_Health = Health  # coz the max health is going to be the health that we give it,
    
    def LaserCoolDown_( self ):
      if self.Cool_Down_Counter >= self.PLAYER_COOLDOWN:
            self.Cool_Down_Counter = 0
      elif self.Cool_Down_Counter > 0:
            self.Cool_Down_Counter += 1
            
    def PlayerMoveLasers_( self, Laser_Vel, Enemies ):
        self.LaserCoolDown_()
        for laser in self.Lasers:
            laser.MoveLaser_( Laser_Vel )
            if laser.OffScreenLaser_( HEIGHT ):
                self.Lasers.remove( laser )
            else:
                for Maybe_Dead_Enemy in Enemies:
                    if laser.LaserCollision_( Maybe_Dead_Enemy ):
                        Enemies.remove( Maybe_Dead_Enemy )
                        self.CurHighScore += 1
                        self.Lasers.remove( laser )
    
    def PlayerHealthBar_( self, Window ):
        pygame.draw.rect( Window, (255, 0, 0),
                          (self.x, self.y + self.Ship_Image.get_height() + 10, self.Ship_Image.get_width(), 10) )
        pygame.draw.rect( Window, (0, 255, 0), (self.x, self.y + self.Ship_Image.get_height() + 10,
                                                self.Ship_Image.get_width() * (self.Health / self.Max_Health),
                                                10) )
    
    def PlayerDraw_( self, Window ):
        Window.blit( self.Ship_Image, (int( self.x ), int( self.y )) )
        for laser in self.Lasers:
            laser.DrawLaser_( Window )
        self.PlayerHealthBar_( Window )
    
    def ShootLaser_( self ):
        if self.Cool_Down_Counter == 0:
            Laser_Obj = Laser( self.x + 32, self.y, self.Laser_Image )
            laser_Sound.play()
            self.Lasers.append( Laser_Obj )
            self.Cool_Down_Counter = 1

class Enemy( GenShip ):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    
    def __init__( self, x, y, Ship_Color, Health = 100 ):
        super().__init__( x, y, Health )
        self.Ship_Image, self.Laser_Image = self.COLOR_MAP.get( Ship_Color )
        self.mask = pygame.mask.from_surface( self.Ship_Image )
    
    def MoveEnemyShip_( self, Enemy_Ship_Vel ):
        self.y += Enemy_Ship_Vel
    
    def MoveEnemyLasers_( self, Laser_Vel, Player_Obj ):
        self.LaserCoolDown_()
        for laser in self.Lasers[:]:
            laser.MoveLaser_( Laser_Vel )
            if laser.OffScreenLaser_( HEIGHT ):
                self.Lasers.remove( laser )
            elif laser.LaserCollision_( Player_Obj ):
                if laser in self.Lasers:
                    self.Lasers.remove( laser )
                Player_Obj.Health -= 10
    
    def ShootLaser_( self ):
        if self.Cool_Down_Counter == 0:
            if self.Ship_Image == BLUE_SPACE_SHIP:
                Laser_Obj = Laser( self.x, self.y, self.Laser_Image )
                self.Lasers.append( Laser_Obj )
            else:
                Laser_Obj = Laser( self.x + 20, self.y, self.Laser_Image )
                self.Lasers.append( Laser_Obj )
            self.Cool_Down_Counter = 1
    
    # draws the image that belongs to self on the screen on the coordinates that belong to self.
    def DrawEnemy_( self, Window ):
        Window.blit( self.Ship_Image, (int( self.x ), int( self.y )) )
        for laser in self.Lasers[:]:
            laser.DrawLaser_( Window )

# CHECK INPUT
def checkInput( player_Ship_Obj, player_Ship_Vel ):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_Ship_Obj.y >= 0:
        player_Ship_Obj.y -= player_Ship_Vel  # this changes the value of the self variable of the object
    if keys[pygame.K_a] and player_Ship_Obj.x >= 0:
        player_Ship_Obj.x -= player_Ship_Vel
    if keys[pygame.K_s] and player_Ship_Obj.y + player_Ship_Obj.GetHeight_() + 20 <= HEIGHT:
        player_Ship_Obj.y += player_Ship_Vel
    if keys[pygame.K_d] and player_Ship_Obj.x + player_Ship_Obj.GetWidth_() <= WIDTH:
        player_Ship_Obj.x += player_Ship_Vel
    if keys[pygame.K_SPACE]:
        player_Ship_Obj.ShootLaser_()

# DRAW STUFF
def drawText( level, life, player_Obj, won_Level = False):
    
    # FONTS
    main_Font = pygame.font.Font( 'Fonts\F-Roboto-Thin.ttf', 50 )
    level_Won_Font = pygame.font.Font( 'Fonts\CloisterBlack.ttf', 250 )
    
    # LABELS
    level_Label = main_Font.render( f"LEVEL : {level}", 1, color.get( "White" ) )
    lives_Label = main_Font.render( f"LIFE :  {life}", 1, color.get( "Green" ) )
    score_Label = main_Font.render( f"SCORE :  {player_Obj.CurHighScore}", 1, color.get( "Green" ) )
    high_Score_Label = main_Font.render( f"HIGH SCORE :  {player_Obj.HighScore}", 1, color.get( "Green" ) )
    
    #BLIT
    WIN.blit( lives_Label, (10, 10) )
    WIN.blit( level_Label, (WIDTH - level_Label.get_width() - 10, 10) )
    WIN.blit( score_Label, (WIDTH - score_Label.get_width() - 10, level_Label.get_height() + 10) )
    WIN.blit( high_Score_Label, (WIDTH - high_Score_Label.get_width() - 10, (level_Label.get_height() * 2) + 10) )
    
    # CHANGE LEVEL
    if won_Level:
        level_Won_Label = level_Won_Font.render( f"L :  {level} ", True, color.get( "White" ) )
        WIN.blit( level_Won_Label, (int( (WIDTH / 2 - level_Won_Label.get_width() / 2) ),
                                    int( HEIGHT / 2 - level_Won_Label.get_height() / 2 )) )

# UPDATE STUFF
def updateStuff( level, life, enemies, player_Obj, lost, won_Level, loop ):
    WIN.fill( color.get( "Black" ) )  # to not leave trails in the game
    
    for enemy in enemies:  # drawing the enemies.
        enemy.DrawEnemy_( WIN )
    player_Obj.PlayerDraw_( WIN )  # drawing the player ship.
    if lost:
        pygame.time.wait( 2000 )
        WIN.blit( BG_IMAGE_LOST, ORIGIN )
        pygame.display.update()
        fout = open( "Assets/Highscore.txt", "w" )
        fout.write( player_Obj.HighScore.__str__() )
        fout.close()
        pygame.time.wait( 3000 )
    drawText( level, life, player_Obj, won_Level )
    
    pygame.display.update()

# CHECK COLLISION
def collide( first_Obj, second_Obj ):
    offset_X = int( second_Obj.x - first_Obj.x )
    offset_Y = int( second_Obj.y - first_Obj.y )
    if first_Obj.mask.overlap( second_Obj.mask, (offset_X, offset_Y) ) is not None:
        explosion_Sound.play()
        return True
    else:
        return False

def main( ):
    # BASIC VARIABLES
    loop = True
    level = 0
    life = 5
    lost = False
    won = False
    won_Count = 0
    laser_Vel = 4
    player_Ship_Vel = 7
    enemies = []  # list that has objects of the enemy class.
    enemies_InWave = 5  # enemies that come in one level.
    enemy_Ship_Vel = 2
    clock = pygame.time.Clock()  # keeps track of the frame rate.
    player_Obj = Player( 0, 0, 100 )  # this is the player ship object.
    player_Obj.x = WIDTH / 2 - player_Obj.GetWidth_() / 2  # assigning the val of x to player obj
    player_Obj.y = (HEIGHT * 0.75 - player_Obj.GetHeight_() / 2)  # assigning the val of y to obj, so its in the center.
    
    while loop:
        clock.tick( FPS )
        if player_Obj.CurHighScore > player_Obj.HighScore:
            player_Obj.HighScore = player_Obj.CurHighScore
        if life <= 0 or player_Obj.Health <= 0:
            lost = True
        
        # draws the stuff u see on the screen.
        updateStuff( level, life, enemies, player_Obj, lost, won, loop )
        if lost:
            loop = False
            continue
        if len( enemies ) == 0:  # this happens when you defeat all the enemies
            if level is not 0:
                enemies_InWave += 2  # increase the enemies in the next level
            if enemies_InWave == 5 + level * 2:
                won = True
                for player_Laser in player_Obj.Lasers[:]:
                    if not player_Laser.OffScreenLaser_( HEIGHT ):
                        player_Obj.Lasers.remove( player_Laser )
            
            level += 1  # increase the level coz you won
            # appends enemy objects into the enemies list.
            for i in range( 0, enemies_InWave ):
                enemy_Ship_RandX = random.randrange( 50, WIDTH - 100 )
                enemy_Ship_RandY = random.randrange( -1500, -100 )
                enemy_Ship_Rand_Color = random.choice( ["red", "blue", "green"] )
                Enemy_Obj = Enemy( enemy_Ship_RandX, enemy_Ship_RandY, enemy_Ship_Rand_Color )
                enemies.append( Enemy_Obj )
        if won:
            won_Count += 1
            if won_Count > FPS * 2:
                won_Count = 0
                won = False
            else:
                continue
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fout = open( "Assets/Highscore.txt", "w" )
                fout.write( player_Obj.HighScore.__str__() )
                fout.close()
                loop = False
            elif event.type == pygame.KEYDOWN:  # press the esc key to exit fullscreen
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode( (WIDTH, HEIGHT) )  # this makes the x button appear
        
        checkInput( player_Obj, player_Ship_Vel )
        
        # moves the enemy ships
        for enemy in enemies[:]:
            enemy.MoveEnemyShip_( enemy_Ship_Vel )
            enemy.MoveEnemyLasers_( laser_Vel, player_Obj )
            
            if random.randrange( 0, 3 * 60 ) == 1:
                enemy.ShootLaser_()
            
            if collide( enemy, player_Obj ):
                player_Obj.Health -= 10
                player_Obj.CurHighScore += 1
                enemies.remove( enemy )
            elif enemy.y + enemy.GetHeight_() > HEIGHT:
                life -= 1
                enemies.remove( enemy )
        player_Obj.PlayerMoveLasers_( -laser_Vel, enemies )

def mainMenu( ):
    run = True
    while run:
        WIN.blit( BG_IMAGE, ORIGIN )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                main()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                    run = False
        
        pygame.display.update()
    pygame.quit()

mainMenu()
