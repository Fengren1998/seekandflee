import pygame
import random as rng
import math

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Heavy Object by Mikhail Joseph Agudo')

black = (0,0,0)
white = (0,255,0)

clock = pygame.time.Clock()
crashed = False


class Object:
    def __init__(self, img, target=None, hunter=False):
        self.pos_x = rng.randint(0, display_width)
        self.pos_y = rng.randint(0, display_height)
        self.v_x = rng.randint(-5,5)
        self.v_y = rng.randint(-5,5)
        self.a_x = 0
        self.a_y = 0

        self.target_x, self.target_y = 0, 0

        self.weight = 1000
        self.f_x = 0
        self.f_y = 0

        self.max_v = 5
        self.facing = rng.uniform(0, 6.28319)

        self.steerer_dist = 50
        self.steerer_x = 0
        self.steerer_y = 0
        self.steer_x = 0
        self.steer_y = 0

        self.hunter = hunter
        self.target = target

        self.img = img
        #pygame.image.load('heavy_object.png')

    def deg_2_rad(self, degree):
        return degree * (math.pi/180)

    def angle_2_front(self):
        future_y = self.v_y - self.pos_y
        future_x = self.v_x - self.pos_x
        return math.atan2(future_y - self.pos_y, future_x - self.pos_x)

    def angle_2_target(self):
        return math.atan2(self.target.pos_y - self.steerer_y, self.target.pos_x - self.steerer_x)

    def steerer_pos(self):
        self.steerer_x = self.pos_x + self.steerer_dist * math.cos(self.facing)
        self.steerer_y = self.pos_y + self.steerer_dist * math.sin(self.facing)

    def steer_pos(self):
        self.steer_x = self.steerer_x + self.steerer_dist * math.cos(self.angle_2_target())
        self.steer_y = self.steerer_y + self.steerer_dist * math.cos(self.angle_2_target())

    def update(self):
        # Resolve the angles
        self.facing = self.angle_2_front()
        self.steerer_pos()
        self.steer_pos()

        self.target_x, self.target_y = self.target.pos_x, self.target.pos_y
        if self.hunter == True:
            self.f_x = (self.target_x - self.pos_x)/self.weight
            self.f_y = (self.target_y - self.pos_y)/self.weight
        elif self.hunter == False:
            self.f_x = -(self.target_x - self.pos_x)/self.weight
            self.f_y = -(self.target_y - self.pos_y)/self.weight

        if self.hunter == True:
            raw_x = [self.target_x, self.pos_x]
            norm_x = [float(i)/sum(raw_x) for i in raw_x]
            raw_y = [self.target_y, self.pos_y]
            norm_y = [float(i)/sum(raw_y) for i in raw_y]
        elif self.hunter == False:
            raw_x = [-self.target_x, -self.pos_x]
            norm_x = [float(i)/sum(raw_x) for i in raw_x]
            raw_y = [-self.target_y, -self.pos_y]
            norm_y = [float(i)/sum(raw_y) for i in raw_y]

        desired_v_x = (raw_x[0] - raw_x[1]) * self.max_v
        desired_v_y = (raw_y[0] - raw_y[1]) * self.max_v

        self.a_x = desired_v_x - self.v_x
        self.a_y = desired_v_y - self.v_y

        self.v_x = self.v_x + self.a_x
        self.v_y = self.v_y + self.a_y
        negative = self.max_v - (2 * self.max_v)
        if self.v_x > self.max_v:
            self.v_x = self.max_v
        elif self.v_x < negative:
            self.v_x = negative
        if self.v_y > self.max_v:
            self.v_y = self.max_v
        elif self.v_y < negative:
            self.v_y = negative

        self.pos_x = self.pos_x + self.v_x
        self.pos_y = self.pos_y + self.v_y

        if self.pos_x > display_width:
            self.pos_x = 0
        elif self.pos_x < 0:
            self.pos_x = display_width
        if self.pos_y > display_height:
            self.pos_y = 0
        elif self.pos_y < 0:
            self.pos_y = display_height

    def get_position(self):
        return (self.pos_x, self.pos_y)

    def display(self):
        gameDisplay.blit(self.img, (self.pos_x - 55, self.pos_y - 100))

good = pygame.image.load('heavy_object.png')
evil = pygame.image.load('heavy_object_evil.png')

Princess = Object(good)
Evility = Object(evil, Princess, True)
Princess.target = Evility

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    Princess.update()
    Evility.update()
    Princess.display()
    Evility.display()


    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
