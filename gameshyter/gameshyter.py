import pygame
import sys
import math

pygame.init()

width, height = 900, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("shyter")

background_image = pygame.image.load('Background.png')

foreground_image = pygame.image.load('boww.png')
new_boww_width = 75
new_boww_height = 75
foreground_image = pygame.transform.scale(foreground_image, (new_boww_width, new_boww_height))

arrow_image = pygame.image.load('yyy.png')

clock = pygame.time.Clock()

min_angle = -45
max_angle = 90

class Arrow:
    def __init__(self, x, y, angle):
        self.image = pygame.transform.scale(arrow_image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 15  # Скорость стрелы
        self.angle = math.radians(angle)  # Угол в радианах
        # Расчет компонент скорости по осям x и y с учетом угла
        self.x_velocity = self.speed * math.cos(self.angle)
        self.y_velocity = -self.speed * math.sin(self.angle)


    def update(self):
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Enemy:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def move(self):
        self.x -= 1  
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

arrows = []
enemies = []  
enemy_image_path = "enemy.png"
enemy = Enemy(800, 200, enemy_image_path)
enemies.append(enemy)  

running = True
last_shot_time = 0
shoot_delay = 500
initial_character_x = 155
initial_character_y = 330
image_rect = foreground_image.get_rect(center=(initial_character_x, initial_character_y))

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_time - last_shot_time > shoot_delay:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rel_x, rel_y = mouse_x - image_rect.centerx, mouse_y - image_rect.centery
                angle = math.degrees(math.atan2(-rel_y, rel_x))

                new_arrow = Arrow(image_rect.centerx, image_rect.centery, angle)
                arrows.append(new_arrow)
                last_shot_time = current_time

    screen.blit(background_image, (0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_x - image_rect.centerx, mouse_y - image_rect.centery
    angle = math.degrees(math.atan2(-rel_y, rel_x)) - -45
    angle = max(min(angle, max_angle), min_angle)
    rotated_image = pygame.transform.rotate(foreground_image, angle)
    rotated_rect = rotated_image.get_rect(center=image_rect.center)
    screen.blit(rotated_image, rotated_rect.topleft)

    for arrow in arrows:
        arrow.update()
        arrow.draw(screen)

    for enemy in enemies:
        enemy.move()
        enemy.draw(screen)
    clock.tick(60)
    pygame.display.update()
