import pygame
import math
import random

WIN_WIDTH = 800
WIN_HEIGHT = 800
BACKGROUND_COLOUR = (255, 255, 255)


class Particle:
    def __init__(self, x, y, size, speed, angle):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = speed
        self.angle = angle

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > WIN_WIDTH - self.size:
            self.x = 2 * (WIN_WIDTH - self.size) - self.x
            self.angle = -self.angle

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle

        if self.y > WIN_HEIGHT - self.size:
            self.y = 2 * (WIN_HEIGHT - self.size) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    distance = math.hypot(dx, dy)
    if distance < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        p1.angle = 2 * tangent - p1.angle
        p2.angle = 2 * tangent - p2.angle
        (p1.speed, p2.speed) = (p2.speed, p1.speed)
        angle = 0.5 * math.pi + tangent
        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Diffusion simulation")


number_of_particles = 100
my_particles = []
for n in range(number_of_particles):
    size = 10
    x = random.randint(size, WIN_WIDTH/2-size)
    y = random.randint(size, WIN_HEIGHT/2-size)
    speed = random.uniform(0, 3)
    angle = random.uniform(0, 2*math.pi)
    my_particles.append(Particle(x, y, size, speed, angle))

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()
    pygame.display.flip()
    screen.fill(BACKGROUND_COLOUR)