import pygame
import sys
import math
import random

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

enemy_speed = 1  # Начальная скорость врагов

# Инициализация шрифта и создание объекта шрифта
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

# Переменная для отслеживания количества убитых врагов
kill_count = 0
previous_kill_count = 0  # Переменная для хранения предыдущего количества убитых врагов

# Координата вертикальной линии (например, линия находится на координате 100 по x)
vertical_line_x = 170

# Переменная для отслеживания состояния игры
game_over = False
show_title = True

# Переменные для кнопки Play
global play_button_visible, play_button_alpha
play_button_visible = True
play_button_alpha = 255  # Начальное значение альфа-канала кнопки Play
play_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 100, 200, 50)  # Объявляем play_button_rect

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
    global running, game_over, show_title, show_title_end_time, previous_kill_count
    game_over = True
    previous_kill_count = kill_count  # Сохраняем текущий счет как предыдущий результат
    show_title_end_time = current_time + 1000  # Показываем заставку на 1 секунду
    show_title = True
    global play_button_visible, play_button_alpha
    play_button_visible = True
    play_button_alpha = 255  # Восстанавливаем альфа-канал кнопки Play
    show_title_screen()

def show_title_screen():
    screen.blit(background_image, (0, 0))  # Замените на ваше изображение заставки
    title_text = font.render("Нажмите кнопку Play для запуска игры", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(title_text, title_rect)

    previous_result_text = font.render(f'Прошлый результат: Kills - {previous_kill_count}', True, (255, 255, 255))
    previous_result_rect = previous_result_text.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(previous_result_text, previous_result_rect)

    global play_button_visible, play_button_alpha
    if play_button_visible:
        play_button_surface = pygame.Surface((play_button_rect.width, play_button_rect.height))
        play_button_surface.set_alpha(play_button_alpha)  # Устанавливаем альфа-канал поверхности кнопки Play
        play_button_surface.fill((0, 255, 0))
        screen.blit(play_button_surface, play_button_rect)
        play_text = font.render("Play", True, (0, 0, 0))
        play_text_rect = play_text.get_rect(center=play_button_rect.center)
        screen.blit(play_text, play_text_rect)

    pygame.display.update()

def reset_game():
    global enemy_speed, kill_count, last_spawn_time, arrows, enemies, game_over, show_title, previous_kill_count
    enemy_speed = 1
    kill_count = 0
    previous_kill_count = 0
    last_spawn_time = 0
    arrows.empty()
    enemies.empty()
    game_over = False
    show_title = True
    show_title_screen()

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

# Инициализация заставки перед началом игры
show_title_screen()

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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and show_title:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse_x, mouse_y):  # Проверка на нажатие кнопки Play
                show_title = False
                play_button_visible = False  # Скрываем кнопку Play
                play_button_alpha = 0  # Устанавливаем альфа-канал кнопки Play на минимальное значение

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse_x, mouse_y):  # Проверка на нажатие кнопки Play
                reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            if current_time - last_shot_time > shoot_delay:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rel_x, rel_y = mouse_x - image_rect.centerx, mouse_y - image_rect.centery
                angle = math.degrees(math.atan2(-rel_y, rel_x))

                new_arrow = Arrow(image_rect.centerx, image_rect.centery, angle)
                arrows.add(new_arrow)
                last_shot_time = current_time


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
        if current_time < show_title_end_time:
            pygame.draw.rect(screen, (0, 0, 0), play_button_rect)  # Перерисовываем кнопку, чтобы она была чёрной
            game_over_text = font.render(f'Проиграш', True, (255, 0, 0))
            screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
        else:
            show_title_screen()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
