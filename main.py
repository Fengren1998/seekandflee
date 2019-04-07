import pygame
import random as rng
import math

pygame.init()
vec = pygame.math.Vector2

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pursuit and Evasion by Mikhail Joseph Agudo')

black = (0,0,0)
white = (0,255,0)

clock = pygame.time.Clock()
crashed = False


class Object:
    def __init__(self, img, target=None, hunter=False):
        self.p = vec(rng.randint(0, display_width), rng.randint(0, display_height))
        self.v = vec(0, 0)
        self.a = vec(0, 0)
        self.t = vec(0, 0)

        self.weight = 1000
        self.f = vec(0, 0)

        self.max_v = 5
        self.max_a = 0.1

        self.p_count = 0
        self.just_tp = False
        self.past_p = self.p

        self.steerer_dist = 55
        self.steerer = vec(0, 0)
        self.steer = vec(0, 0)

        self.hunter = hunter
        self.target = target

        self.img = img
        self.collision = self.img.get_rect()

    def rand_pos(self):
        self.p = vec(rng.randint(0, display_width), rng.randint(0, display_height))

    def steerer_pos(self):
        self.steerer = ((self.v * 10) + self.p)

    def steer_pos(self):
        if self.hunter == True:
            if self.target.just_tp == True:
                temp = (self.target.past_p + self.target.v) - self.steerer
            else:
                temp = (self.target.steer + self.target.v) - self.steerer
        else:
            temp = self.target.p - self.steerer

        if temp.length() > float(self.steerer_dist):
            temp.scale_to_length(self.steerer_dist)


        if self.hunter == True:
            self.steer = self.steerer + temp
        else:
            self.steer = self.steerer - temp

    def update(self):
        # Update collision rect
        self.collision.center = (self.p.x, self.p.y)

        # Resolve the steering
        self.steerer_pos()
        self.steer_pos()
        print(self.steerer)

        self.t = self.steer

        self.f = self.t - self.p

        self.a = self.f
        self.a.scale_to_length(self.max_a)

        self.v = self.v + self.a
        if self.v.length() > self.max_v:
            self.v.scale_to_length(self.max_v)
        print('V: ' + str(self.v))

        self.p = self.p + self.v

        ADD_SPEED = 10
        if self.p.x > display_width:
            self.p.x = 0
            self.v.x += ADD_SPEED
            self.just_tp = True
            self.past_p = self.p
        elif self.p.x < 0:
            self.p.x = display_width
            self.v.x -= ADD_SPEED
            self.just_tp = True
            self.past_p = self.p
        if self.p.y > display_height:
            self.p.y = 0
            self.v.y += ADD_SPEED
            self.just_tp = True
            self.past_p = self.p
        elif self.p.y < 0:
            self.p.y = display_height
            self.v.y -= ADD_SPEED
            self.just_tp = True
            self.past_p = self.p

        if self.p_count >= 500:
            self.just_tp = False

        if self.just_tp == True:
            self.p_count += 1

    def display(self):
        gameDisplay.blit(self.img, (self.p.x - 32, self.p.y - 50))
        pygame.draw.line(gameDisplay, (255,0,255), self.p, self.steerer, 5)
        pygame.draw.line(gameDisplay, (255,0,0), self.steerer, self.steer, 5)

good = pygame.image.load('data/heavy_object.png')
evil = pygame.image.load('data/heavy_object_evil.png')
catch = pygame.image.load('data/catch.png')

Evility = Object(evil)
Princess = Object(good, Evility, True)
Evility.target = Princess

catch_linger = 200
catch_count = 200

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    Princess.update()
    Evility.update()
    Princess.display()
    Evility.display()

    if Princess.collision.colliderect(Evility.collision) == True:
        print('COLLIDE')

        if Princess.hunter == True:
            Princess.hunter = False
            Evility.hunter = True
        else:
            Princess.hunter = True
            Evility.hunter = False
        Princess.rand_pos()
        Evility.rand_pos()

        catch_count = 0

    if catch_count < catch_linger:
        gameDisplay.blit(catch, (display_width/4 + 50, display_height/4 - 50))
        catch_count += 1

    print('X: ' + str(Princess.p.x) + ' Y: ' + str(Princess.p.y) + ' Steerx: ' + str(Princess.steer.x) + ' Steery: ' + str(Princess.steer.y))


    pygame.display.update()
    clock.tick(120)

pygame.quit()
quit()
