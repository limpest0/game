import pygame.time
import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Задаем размеры окна
width, height = 900, 500
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("shyter")

# Загрузка изображения фона
background_image = pygame.image.load('Background.png')

# Загрузка изображения, которое будет поверх фона
foreground_image = pygame.image.load('boww.png')

arrow_image = pygame.image.load('arrow.png')

# Установка границ угла (в градусах)
min_angle = -45
max_angle = 90


class Arrow:
    def __init__(self, x, y, angle):
        self.image = pygame.transform.scale(arrow_image, (50, 10))
        self.angle = math.radians(angle)  # Угол в радианах
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3 # Скорость стрелы
        self.x_velocity = self.speed * math.cos(self.angle)
        # Учитываем, что ось y направлена вниз
        self.y_velocity = -self.speed * math.sin(self.angle)

    def update(self):
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


# Список стрел
arrows = []

# Координаты для изображения, которое будет поверх фона
foreground_x, foreground_y = 155, 330

# Новые размеры для изображения
new_width, new_height = 85, 85  # Укажите нужные размеры

# Масштабирование изображения до новых размеров
foreground_image = pygame.transform.scale(
    foreground_image, (new_width, new_height))
image_rect = foreground_image.get_rect(center=(foreground_x, foreground_y))


# Задержка между выстрелами (в миллисекундах)
shoot_delay = 500  # Например, задержка в полсекунды

# Переменная для отслеживания времени последнего выстрела
last_shot_time = 0

# Основной цикл игры
# Основной цикл игры
running = True
while running:
    # Получаем текущее время в миллисекундах
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Завершаем игру

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверяем прошла ли достаточная задержка с момента предыдущего выстрела
            if current_time - last_shot_time > shoot_delay:
                # Получение позиции мыши
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Вычисление угла между центром изображения и позицией мыши
                rel_x, rel_y = mouse_x - image_rect.centerx, mouse_y - image_rect.centery
                # Угол между центром и курсором мыши
                angle = math.degrees(math.atan2(-rel_y, rel_x))

                # Создание новой стрелы с вычисленным углом направления
                new_arrow = Arrow(image_rect.centerx,
                                  image_rect.centery, angle)
                arrows.append(new_arrow)

                # Обновляем время последнего выстрела
                last_shot_time = current_time

    # Отрисовка изображения фона
    screen.blit(background_image, (0, 0))

    # Получение позиции мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Вычисление угла между центром изображения и позицией мыши
    rel_x, rel_y = mouse_x - image_rect.centerx, mouse_y - image_rect.centery
    angle = math.degrees(math.atan2(-rel_y, rel_x)) - \
        -45  # Корректируем угол на 90 градусов

    # Ограничиваем угол в пределах заданных границ
    angle = max(min(angle, max_angle), min_angle)

    # Поворот изображения
    rotated_image = pygame.transform.rotate(foreground_image, angle)
    rotated_rect = rotated_image.get_rect(center=image_rect.center)

    # Отрисовка вращенного изображения поверх фона
    screen.blit(rotated_image, rotated_rect.topleft)

    for arrow in arrows:
        arrow.update()
        arrow.draw(screen)

    # Обновляем экран
    pygame.display.flip()

# После выхода из цикла игры закрываем Pygame
pygame.quit()
