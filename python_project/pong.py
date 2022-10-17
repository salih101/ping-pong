from ast import Import
from pygame import mixer
from random import randint
import pygame
pygame.init()
mixer.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
gameOn = True
size = (700,500)
scoreA = 0
scoreB = 0


screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Ping Pong Game")
mixer.music.load("python_project/ping.mp3")

class Paddle(pygame.sprite.Sprite):

    def __init__(self,color,width,height):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image,color,[0,0,width,height])

        self.rect = self.image.get_rect()

    def moveUp(self,pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0
    
    def moveDown(self,pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y = 400

class Ball(pygame.sprite.Sprite):
    def __init__(self,color,width,height):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image,color,[0,0,width,height])
        self.velocity = [randint(4,8),randint(-8,8)]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)
paddleA = Paddle(WHITE,10,100)
paddleA.rect.x = 20
paddleA.rect.y = 200

paddleB = Paddle(WHITE,10,100)
paddleB.rect.x = 670
paddleB.rect.y = 200

ball = Ball(WHITE,10,10)
ball.rect.x =345
ball.rect.y =195

all_sprites = pygame.sprite.Group()

all_sprites.add(paddleA)
all_sprites.add(paddleB)
all_sprites.add(ball)

while gameOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                gameOn = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    if keys[pygame.K_UP]:
        paddleB.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(5)
    #game logic

    all_sprites.update()

    if pygame.sprite.collide_mask(ball,paddleA):
        scoreA += 1
        ball.bounce()
        mixer.music.play()
    if pygame.sprite.collide_mask(ball,paddleB):
        scoreB += 1
        ball.bounce()
        mixer.music.play()

    if ball.rect.x>=690:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1] 

    screen.fill(BLACK)
    pygame.draw.line(screen,WHITE,[349,0],[349,500],5)
    all_sprites.draw(screen)

    font = pygame.font.Font(None,74)
    text = font.render(str(scoreA),1,WHITE)
    screen.blit(text,(250,10))
    text = font.render(str(scoreB),1,WHITE)
    screen.blit(text,(420,10))
    pygame.display.flip()
    clock.tick(75)

pygame.quit()