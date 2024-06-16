import pygame
import sys
import math
import random

pygame.init()

width, height = 900, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("shyter")

background_image = pygame.image.load('1233.png')

foreground_image = pygame.image.load('boww.png')
new_boww_width = 75
new_boww_height = 75
foreground_image = pygame.transform.scale(foreground_image, (new_boww_width, new_boww_height))

arrow_image = pygame.image.load('yyy.png')

clock = pygame.time.Clock()

min_angle = -45
max_angle = 90

enemy_speed = 1  # Начальная скорость врагов

# Инициализация шрифта и создание объекта шрифта
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

# Переменная для отслеживания количества убитых врагов
kill_count = 0

# Координата вертикальной линии (например, линия находится на координате 100 по x)
vertical_line_x = 170

# Переменная для отслеживания состояния игры
game_over = False

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.transform.scale(arrow_image, (50, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 20
        self.angle = math.radians(angle)
        self.x_velocity = self.speed * math.cos(self.angle)
        self.y_velocity = -self.speed * math.sin(self.angle)

    def update(self):
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        if self.rect.x > width:
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, hit_image_path):
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        self.hit_image = pygame.image.load(hit_image_path)
        self.image = pygame.transform.scale(self.original_image, (75, 75))
        self.hit_image = pygame.transform.scale(self.hit_image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit = False
        self.hit_time = 0

    def draw(self):
        if self.hit:
            screen.blit(self.hit_image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def handle_hit(self):
        self.hit = True
        self.hit_time = pygame.time.get_ticks()

    def update(self):
        global enemy_speed
        if not self.hit:
            self.rect.x -= enemy_speed
            if self.rect.x <= vertical_line_x:  # Проверка пересечения с вертикальной линией
                end_game()
        if self.hit and current_time - self.hit_time > 500:  # 0.5 секунды
            self.kill()
            enemy_speed += 0.5  # Увеличение скорости врагов после смерти
            global kill_count
            kill_count += 1  # Увеличение счетчика убитых врагов

def end_game():
    global running, game_over
    game_over = True
    game_over_text = font.render(f'Game Over! Kills: {kill_count}', True, (255, 0, 0))
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
    pygame.display.update()

def reset_game():
    global enemy_speed, kill_count, last_spawn_time, arrows, enemies, game_over
    enemy_speed = 1
    kill_count = 0
    last_spawn_time = 0
    arrows.empty()
    enemies.empty()
    game_over = False

arrows = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_image_path = "enemy.png"
hit_image_path = "enemy_hit.png"
spawn_delay = 2000  # Увеличение задержки между спавнами врагов до 2 секунд
last_spawn_time = 0

def spawn_enemy():
    y_position = random.randint(height - height // 3, height - 50)
    new_enemy = Enemy(width, y_position, enemy_image_path, hit_image_path)
    enemies.add(new_enemy)

running = True
last_shot_time = 0
shoot_delay = 1000
initial_character_x = 155
initial_character_y = 330
image_rect = foreground_image.get_rect(center=(initial_character_x, initial_character_y))

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            if current_time - last_shot_time > shoot_delay:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rel_x, rel_y = mouse_x - image_rect.centerx, mouse_y - image_rect.centery
                angle = math.degrees(math.atan2(-rel_y, rel_x))

                new_arrow = Arrow(image_rect.centerx, image_rect.centery, angle)
                arrows.add(new_arrow)
                last_shot_time = current_time

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_q:
                reset_game()

    screen.blit(background_image, (0, 0))

    if not game_over:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - image_rect.centerx, mouse_y - image_rect.centery
        angle = math.degrees(math.atan2(-rel_y, rel_x)) - -45
        angle = max(min(angle, max_angle), min_angle)
        rotated_image = pygame.transform.rotate(foreground_image, angle)
        rotated_rect = rotated_image.get_rect(center=image_rect.center)
        screen.blit(rotated_image, rotated_rect.topleft)

        arrows.update()
        enemies.update()

        # Спавн врагов
        if current_time - last_spawn_time > spawn_delay:
            spawn_enemy()
            last_spawn_time = current_time

        collision = pygame.sprite.groupcollide(arrows, enemies, True, False)
        if collision:
            for arrow in collision:  # each bullet
                for enemy in collision[arrow]:  # each alien that collides with that bullet
                    enemy.handle_hit()

        arrows.draw(screen)
        for enemy in enemies:
            enemy.draw()

    # Отрисовка счетчика убитых врагов
    kill_count_text = font.render(f'Kills: {kill_count}', True, (0, 0, 0))
    screen.blit(kill_count_text, (10, 10))

    if game_over:
        game_over_text = font.render(f'Game Over! Press Q to Restart', True, (255, 0, 0))
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

    clock.tick(60)
    pygame.display.update()
