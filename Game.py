
#------------------------------------------------------------
#           Santiago Rivera
#               CSIT 104
#            FINAL PROJECT
#------------------------------------------------------------

import pygame
import random
import os
import time

WIDTH = 700
HEIGHT = 600
FPS = 30 # how fast my game runs
pygame.init() # Iniciar pygame / Initialize pygame
pygame.mixer.init() # para el sonido / Initialize pygame sound


#--------------------------------------
#     Para Cargar Imagenes al programa / To Load Images to the Program
#--------------------------------------

game_folder = os.path.dirname(__file__) # the file itself where we saving the program
img_folder = os.path.join(game_folder, "Voy a usar") # Loading the folder where the images are located

#--------------------------------------
#     Para Cargar Sonido al programa / To load the sounds to the program
#--------------------------------------

music_dir = os.path.dirname(__file__) # the file itself where we saving the program
snd_folder = os.path.join(music_dir, 'musica') # Loading te folder where the sounds are located

#-------------------------------------------
#           To use the Game Over sound
#               (Game_Over.play())
#-------------------------------------------
Game_Over = pygame.mixer.Sound(os.path.join(snd_folder, 'Explosion.wav')) # When a box is dropped

#--------------------------------------
#       Colors that i will use
#--------------------------------------
BLACK = (0,0,0) # color to be ignored for the background images
RED = (255,0,0) # the color of the letters

#---------------------------------------------------------------------------------------
#                           Functions to Display:
#                              - Score
#                              - Game Over Message
#---------------------------------------------------------------------------------------
def Score_count(Score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+ str(Score), True, RED)
    screen.blit(text,(610,60)) # location of where it is going to appear

def text_objects(text, font) : #para tener el rectangulo donde vamos a posicionar
                               # el texto
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def message_display(text): # puedo colocar otro message_display con mas parametros
                           # para asi colocar un mensaje mas pequeno
                           # con letras mas pequena como ' Score = '

    font = pygame.font.SysFont('arial',50)
    TextSurf, TextRect = text_objects(text, font)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))

    screen.blit(TextSurf, TextRect) # para q este en el background

    pygame.display.update()#update the whole window if it has no parameters

    time.sleep(2)

    game_loop()# para empezar el juego otra vez / to restart the game


def box_drop(): #funcion q va a aparacer cuando se caiga una caja
    message_display(' GAME OVER!!! ')


#----------------------------------------------------------------------------------------
#     Para Crear un sprite(una imagen)
#               player
#---------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "1.png")).convert() # imagen del Sprite
        self.image.set_colorkey(BLACK) # para colocar el fondo negro
        self.rect = self.image.get_rect()# para mover y saber en q cordenadas esta
        self.rect.centerx = WIDTH/2 #posicion de Santi sobre X-azis
        self.rect.bottom = HEIGHT - 10 # un poquito elevado Y-azis
        self.speedx = 0 # only moves left to right
        self.current_frame = 0
        self.last_update = 0




        #--------------------------------------
        #    Images for Walking
        #--------------------------------------
        self.walk_L = [pygame.image.load(os.path.join(img_folder, "L1.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "L2.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "L3.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "L4.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "L5.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "L6.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "L7.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "L8.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "L9.png")).convert()]
        for frame in self.walk_L:
            frame.set_colorkey(BLACK)
        self.walk_R = [pygame.image.load(os.path.join(img_folder, "1.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "2.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "3.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "4.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "5.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "6.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "7.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "8.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "9.png")).convert()]
        for frame in self.walk_R:
            frame.set_colorkey(BLACK)

    def update(self): # en la seccion update esto se vera
        self.speedx = 0 # Para q el Pj no siga Caminando
        now = pygame.time.get_ticks() # El tiempo q ha pasado

        #----------------------------------------------------
        #               get Events
        #----------------------------------------------------
        keystate = pygame.key.get_pressed()# lista de eventos

        #------------------------------------------------------
        #           Aca puedo Colocar las 2 Imagenes
        #              Moviendosen a la izquierda
        #------------------------------------------------------
        if keystate[pygame.K_LEFT]:
            self.speedx = -7 # to move to the LEFT
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1 ) % len(self.walk_L)
                self.image = self.walk_L[self.current_frame]

        #------------------------------------------------------
        #           Aca puedo Colocar las 2 Imagenes
        #              Moviendosen a la Derecha
        #------------------------------------------------------
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7# to move to the right
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1 ) % len(self.walk_R)
                self.image = self.walk_R[self.current_frame]

        self.rect.x += self.speedx

        #------------------------------------------------------
        #               When Player hits the end
        #                   of the Screen
        #------------------------------------------------------
        if self.rect.left < 0 :
            self.rect.right = WIDTH
        if self.rect.right > WIDTH:
            self.rect.left = 0

#------------------------------------------------------------------------
#                   Class for the Boxes
#------------------------------------------------------------------------

class Box(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "cajanegra.png")).convert() # imagen del Sprite
        self.image = pygame.transform.scale(self.image,(50,50)) # The Image was too big, so i scale the image so it can fit the machine
        #pygame.transform.scale()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(127,550,200) # Three Machines - Three positions only
        self.rect.y = 108
        self.speedy = 3 # la velocidad de las cajas

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            Game_Over.play() # Play Game Over sound
            box_drop() # Display Game Over Message, and has the function to restart the game
            pygame.quit() # Quit pygame
            quit()





#------------------------------------------------------------------------
#                           Create window
#------------------------------------------------------------------------

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creando la ventana / Create the window
pygame.display.set_caption("BOX PICKING") # Game Title
clock = pygame.time.Clock() # para el tiempo / Keep track of the clock ... this helps when using images

def game_loop():
    #---------------------------------------------------------
    #               Loading sounds
    #---------------------------------------------------------
    pickUp_Box = pygame.mixer.Sound(os.path.join(snd_folder, 'caja.wav'))
    pygame.mixer.music.load(os.path.join(snd_folder, "sample gamble.ogg"))
    pygame.mixer.music.set_volume(0.4)# para q no suene tan duro ... Volume
    #------------------------------------------------------------------------
    all_sprites = pygame.sprite.Group() # Group where we putting the objects
    #------------------------------------------------------------------------
    boxes = pygame.sprite.Group()
    caja = Box()
    all_sprites.add(caja) # adding a Box to the group of all sprites
    boxes.add(caja) # adding a Box to the Box Group - to Collide w/ Player

    #------------------------------------------------------------------------
    santi = Player() # instance of Player
    all_sprites.add(santi) # agregandolo al grupo para q aparesca en pantalla

    Score = 0 # To Keep track of the Score
    nivel = 0 # To know when to Increase the speed of the boxes

    #------------------------------------------------------------------------
    #               Game Loop
    #------------------------------------------------------------------------

    pygame.mixer.music.play(loops = -1) # to play it over n over again
    running = True
    # loop pasa a 30 FPS
    while running: # para salir del loop solo hay q hacer running -- False
        #keep loop running at the right speed
        clock.tick(FPS)

        #--------------------------------------
        #      Process input (events)
        #--------------------------------------
        for event in pygame.event.get():
            # mirando si cierran la ventana dandole a la XX
            # to close the program when you click the X
                if event.type == pygame.QUIT:
                    running = False
        #--------------------------------------
        #               Update
        #--------------------------------------
        all_sprites.update()
        #--------------------------------------
        #       Checking to see if Player
        #           pick up the box
        #--------------------------------------
        picks = pygame.sprite.spritecollide(santi,boxes,True) # True means delete the object that collide ... meaning the package
        if picks:
            Score += 1
            pickUp_Box.set_volume(0.2)
            pickUp_Box.play()
            if Score % 5 == 0: # if Score is a multiple of 5 -> Increase level
                nivel += 1
            '''
            - Create a new package
            - add it to all sprites group so it can be draw
            - add it to box group to check collide function
            - Check score to see the dropping speed it should have
            '''
            caja = Box()
            all_sprites.add(caja)
            boxes.add(caja)
            # If Score is Greater or equal to 5, 10, 15 ... Then Increase The Speed of  the New Dropping Boxes
            if Score >= 5*nivel : #New Boxes from 1-5, 5-10, 10-15 and so on ... so we can change the speed to them all not just one
                caja.speedy += nivel # Just Change the Speed. No need to Change where the Boxes Spawn cuz is already ramdon


        #     Para Cargar El background
        fondo = pygame.image.load(os.path.join(img_folder, "nuevo escenario.png")).convert()
        fondo_rect = fondo.get_rect()
        #     Para Cargar La garra
        garra = pygame.image.load(os.path.join(img_folder, "garrabuena.png")).convert()
        garra.set_colorkey(BLACK)
        garra_rect = garra.get_rect()
        garra_rect.centerx = 350 #Position over X-azis
        garra_rect.top = 55 # Position over Y-azis
        #--------------------------------------
        #           Drawing
        #--------------------------------------
        screen.fill(BLACK)
        screen.blit(fondo,fondo_rect)
        #-----------------------------------
        #              garra 2
        #-----------------------------------
        garra2 = pygame.image.load(os.path.join(img_folder, "garrabuena.png")).convert()
        garra2.set_colorkey(BLACK)
        garra_rect2 = garra2.get_rect()
        garra_rect2.centerx = 150 # Position over X-azis
        garra_rect2.top = 55 # Position over Y-azis
        #-----------------------------------
        #              garra 3
        #-----------------------------------
        garra3 = pygame.image.load(os.path.join(img_folder, "garrabuena.png")).convert()
        garra3.set_colorkey(BLACK)
        garra_rect3 = garra3.get_rect()
        garra_rect3.centerx = 550 #Position over X-azis
        garra_rect3.top = 55 # Position over Y-azis


        #------------------------------------
        all_sprites.draw(screen) # to draw all the objects in this Group
        screen.blit(garra,garra_rect)
        screen.blit(garra2,garra_rect2)
        screen.blit(garra3,garra_rect3)
        Score_count(Score)
        # AFTER drawing everything
        pygame.display.flip() # para cambiar lo q ya tenemos dibujado a la pantalla


game_loop()
pygame.quit() #para cerrar la ventana ... pygame todo
quit()
