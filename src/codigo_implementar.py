import pygame
import sys
import random


# Inicializar Pygame
pygame.init()



# Configurar la pantalla
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WORLD OF TREES")

# Cargar las imágenes de fondo
background_image = pygame.image.load("Fondo seco f0.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

menu_background_image = pygame.image.load("fondo nuevo.jpg")
menu_background_image = pygame.transform.scale(menu_background_image, (WIDTH, HEIGHT))


# Cargar el GIF para el fondo
gif_frames = []
for i in range(1, 6):  # Suponiendo que tienes 5 imágenes del GIF
    gif_frame = pygame.image.load(f"Fondo seco f0.jpg")  # Cambia el nombre del archivo según corresponda
    gif_frame = pygame.transform.scale(gif_frame, (WIDTH, HEIGHT))
    gif_frames.append(gif_frame)

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Velocidad del jugador
player_speed = 3


# Configuraciones de aparición de llantas y gotas
TIRES_PER_LEVEL = {
    1: 1,
    2: 10,
    3: 15
}
TIRE_SPAWN_RATE = {  # Configuración de llantas por nivel
    1: 1,
    2: 10,
    3: 15
}
WATER_DROP_CHANCE = 1  # Mayor número significa menos frecuencia


# Coordenadas personalizables para el menú
title_position = (WIDTH // 2 - 200, HEIGHT // 4)  # Coordenadas del título
play_button_position = (WIDTH // 2 - 100, HEIGHT // 2)  # Coordenadas del botón de jugar
options_button_position = (WIDTH // 2 - 100, HEIGHT // 2 + 50)  # Coordenadas del botón de opciones
exit_button_position = (WIDTH // 2 - 100, HEIGHT // 2 + 100)  # Coordenadas del botón de salir


# Clase para el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {
            "front": pygame.image.load("personaje/personaje enfrente.png").convert_alpha(),
            "left": pygame.image.load("personaje/personaje izquierda.png").convert_alpha(),
            "right": pygame.image.load("personaje/personaje derecha.png").convert_alpha(),
        }
        self.image = self.images["front"]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2.5
        self.rect.y = HEIGHT - 200
        self.health = 100
        self.moving = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= player_speed
            self.image = self.images["left"]
            self.moving = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += player_speed
            self.image = self.images["right"]
            self.moving = True
        else:
            self.moving = False

        if not self.moving:
            self.image = self.images["front"]

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
# Clase para las llantas
class Tire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("llanta.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(-100, -30)

    def update(self):
        self.rect.y += 2
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-100, -30)
            self.rect.x = random.randint(0, WIDTH - 30)

# Clase para las gotas de agua
class WaterDrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("gota.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(-100, -30)

    def update(self):
        self.rect.y += 5
        if self.rect.y > HEIGHT:
            self.kill()

# Crear grupos de sprites
player = Player()
tires = pygame.sprite.Group()
water_drops = pygame.sprite.Group()

# Función para añadir llantas
def create_tires(level):
    tire_count = 5 if level == 'easy' else 10
    for _ in range(tire_count):
        tire = Tire()
        tires.add(tire)

# Temporizador
start_ticks = pygame.time.get_ticks()
time_limit = 60  # 60 segundos

# Función para dibujar la barra de vida
def draw_health_bar(screen, x, y, current_health, max_health):
    health_percentage = current_health / max_health
    bar_width = 200
    bar_height = 20
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, bar_width * health_percentage, bar_height))


# Cargar imágenes para el título y los botones
title_image = pygame.image.load("tutilo.png").convert_alpha()  # Cambia el nombre del archivo según sea necesario
play_button_image = pygame.image.load(
    "control.png").convert_alpha()  # Cambia el nombre del archivo según sea necesario
options_button_image = pygame.image.load(
    "tuerca.png").convert_alpha()  # Cambia el nombre del archivo según sea necesario
exit_button_image = pygame.image.load(
    "tuerca.png").convert_alpha()  # Cambia el nombre del archivo según sea necesario


# Actualizar la función para mostrar la pantalla inicial
def show_main_menu():
    screen.blit(menu_background_image, (0, 0))

    # Mostrar el título como imagen
    screen.blit(title_image, (WIDTH // 2 - title_image.get_width() // 2, HEIGHT // 4))

    # Mostrar botones como imágenes
    screen.blit(play_button_image, (WIDTH // 2 - play_button_image.get_width() // 2, HEIGHT // 2))
    screen.blit(options_button_image, (WIDTH // 2 - options_button_image.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(exit_button_image, (WIDTH // 2 - exit_button_image.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()
    return play_button_image.get_rect(topleft=(WIDTH // 2 - play_button_image.get_width() // 2, HEIGHT // 2)), \
        options_button_image.get_rect(topleft=(WIDTH // 2 - options_button_image.get_width() // 2, HEIGHT // 2 + 50)), \
        exit_button_image.get_rect(topleft=(WIDTH // 2 - exit_button_image.get_width() // 2, HEIGHT // 2 + 100))


# El resto del código permanece igual


# Cargar la imagen de fondo para la selección de dificultad
difficulty_background_image = pygame.image.load("fondo nuevo.jpg")
difficulty_background_image = pygame.transform.scale(difficulty_background_image, (WIDTH, HEIGHT))

# Función para mostrar la selección de dificultad
def show_difficulty_selection():
    screen.blit(difficulty_background_image, (0, 0))  # Dibuja el fondo de dificultad
    font = pygame.font.Font(None, 74)
    title_text = font.render("Selecciona Dificultad", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    easy_button = font.render("Principiante", True, WHITE)
    hard_button = font.render("Avanzado", True, WHITE)
    screen.blit(easy_button, (WIDTH // 2 - easy_button.get_width() // 2, HEIGHT // 2))
    screen.blit(hard_button, (WIDTH // 2 - hard_button.get_width() // 2, HEIGHT // 2 + 50))
    back_button = font.render("Volver", True, WHITE)
    screen.blit(back_button, (20, 20))  # Botón de volver en la esquina superior izquierda
    pygame.display.flip()
    return easy_button.get_rect(topleft=(WIDTH // 2 - easy_button.get_width() // 2, HEIGHT // 2)), \
           hard_button.get_rect(topleft=(WIDTH // 2 - hard_button.get_width() // 2, HEIGHT // 2 + 50)), \
           back_button.get_rect(topleft=(20, 20))  # Botón de volver


# Cargar la imagen de fondo para la selección de niveles
level_background_image = pygame.image.load("fondo nuevo.jpg")
level_background_image = pygame.transform.scale(level_background_image, (WIDTH, HEIGHT))

# Función para mostrar niveles
def show_level_selection():
    screen.blit(level_background_image, (0, 0))  # Dibuja el fondo de niveles
    font = pygame.font.Font(None, 74)
    title_text = font.render("Selecciona Nivel", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    level1_button = font.render("Nivel 1", True, WHITE)
    level2_button = font.render("Nivel 2", True, WHITE)
    level3_button = font.render("Nivel 3", True, WHITE)
    screen.blit(level1_button, (WIDTH // 2 - level1_button.get_width() // 2, HEIGHT // 2))
    screen.blit(level2_button, (WIDTH // 2 - level2_button.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(level3_button, (WIDTH // 2 - level3_button.get_width() // 2, HEIGHT // 2 + 100))
    back_button = font.render("Volver", True, WHITE)
    screen.blit(back_button, (20, 20))  # Botón de volver en la esquina superior izquierda
    pygame.display.flip()
    return level1_button.get_rect(topleft=(WIDTH // 2 - level1_button.get_width() // 2, HEIGHT // 2)), \
           level2_button.get_rect(topleft=(WIDTH // 2 - level2_button.get_width() // 2, HEIGHT // 2 + 50)), \
           level3_button.get_rect(topleft=(WIDTH // 2 - level3_button.get_width() // 2, HEIGHT // 2 + 100)), \
           back_button.get_rect(topleft=(20, 20))  # Botón de volver


# Función para mostrar la pantalla de controles
def show_controls():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    controls_text = font.render("Controles:", True, WHITE)
    screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 4))
    movement_text = font.render("Izquierda: ←   Derecha: →", True, WHITE)
    screen.blit(movement_text, (WIDTH // 2 - movement_text.get_width() // 2, HEIGHT // 2))
    back_button = font.render("Volver", True, WHITE)
    screen.blit(back_button, (WIDTH // 2 - back_button.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    return back_button.get_rect(topleft=(WIDTH // 2 - back_button.get_width() // 2, HEIGHT // 2 + 50))

# Función para mostrar la selección de idioma
def show_language_selection():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    lang_text = font.render("Selecciona Idioma:", True, WHITE)
    screen.blit(lang_text, (WIDTH // 2 - lang_text.get_width() // 2, HEIGHT // 4))
    spanish_button = font.render("Español", True, WHITE)
    english_button = font.render("Inglés", True, WHITE)
    screen.blit(spanish_button, (WIDTH // 2 - spanish_button.get_width() // 2, HEIGHT // 2))
    screen.blit(english_button, (WIDTH // 2 - english_button.get_width() // 2, HEIGHT // 2 + 50))
    back_button = font.render("Volver", True, WHITE)
    screen.blit(back_button, (WIDTH // 2 - back_button.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    return spanish_button.get_rect(topleft=(WIDTH // 2 - spanish_button.get_width() // 2, HEIGHT // 2)), \
           english_button.get_rect(topleft=(WIDTH // 2 - english_button.get_width() // 2, HEIGHT // 2 + 50)), \
           back_button.get_rect(topleft=(WIDTH // 2 - back_button.get_width() // 2, HEIGHT // 2 + 100))

# Función para mostrar la pantalla de ajustes
def show_options():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    options_text = font.render("Opciones:", True, WHITE)
    screen.blit(options_text, (WIDTH // 2 - options_text.get_width() // 2, HEIGHT // 4))
    controls_button = font.render("Controles", True, WHITE)
    language_button = font.render("Idioma", True, WHITE)
    back_button = font.render("Volver", True, WHITE)
    screen.blit(controls_button, (WIDTH // 2 - controls_button.get_width() // 2, HEIGHT // 2))
    screen.blit(language_button, (WIDTH // 2 - language_button.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(back_button, (WIDTH // 2 - back_button.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    return controls_button.get_rect(topleft=(WIDTH // 2 - controls_button.get_width() // 2, HEIGHT // 2)), \
           language_button.get_rect(topleft=(WIDTH // 2 - language_button.get_width() // 2, HEIGHT // 2 + 50)), \
           back_button.get_rect(topleft=(WIDTH // 2 - back_button.get_width() // 2, HEIGHT // 2 + 100))

# Función para mostrar la pantalla de Juego Terminado
def show_game_over():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("¡Game Over!", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    restart_button = font.render("Reiniciar", True, WHITE)
    menu_button = font.render("Menu", True, WHITE)
    screen.blit(restart_button, (WIDTH // 2 - restart_button.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(menu_button, (WIDTH // 2 - menu_button.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    return restart_button.get_rect(topleft=(WIDTH // 2 - restart_button.get_width() // 2, HEIGHT // 2 + 50)), \
           menu_button.get_rect(topleft=(WIDTH // 2 - menu_button.get_width() // 2, HEIGHT // 2 + 100))

# Función para mostrar la pantalla de Juego Terminado
def show_game_finished():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    finished_text = font.render("¡Juego Terminado!", True, GREEN)
    screen.blit(finished_text, (WIDTH // 2 - finished_text.get_width() // 2, HEIGHT // 2 - finished_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Bucle principal del juego
running = True
game_active = False
selected_language = "español"  # Idioma por defecto

while running:
    if not game_active:
        play_rect, options_rect, exit_rect = show_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_rect.collidepoint(mouse_pos):
                    easy_rect, hard_rect, back_rect_difficulty = show_difficulty_selection()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = event.pos
                                if easy_rect.collidepoint(mouse_pos):
                                    difficulty = 'easy'
                                    break
                                elif hard_rect.collidepoint(mouse_pos):
                                    difficulty = 'hard'
                                    break
                                elif back_rect_difficulty.collidepoint(mouse_pos):  # Volver
                                    break
                        else:
                            continue
                        break

                    if 'difficulty' in locals():
                        level1_rect, level2_rect, level3_rect, back_rect_level = show_level_selection()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_pos = event.pos
                                    if level1_rect.collidepoint(mouse_pos):
                                        level = 1
                                        break
                                    elif level2_rect.collidepoint(mouse_pos):
                                        level = 2
                                        break
                                    elif level3_rect.collidepoint(mouse_pos):
                                        level = 3
                                        break
                                    elif back_rect_level.collidepoint(mouse_pos):  # Volver
                                        break
                            else:
                                continue
                            break

                        if 'level' in locals():
                            game_active = True
                            player.health = 100
                            start_ticks = pygame.time.get_ticks()  # Reinicia el temporizador
                            tires.empty()
                            create_tires(difficulty)

                elif options_rect.collidepoint(mouse_pos):
                    controls_rect, language_rect, back_rect_options = show_options()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = event.pos
                                if controls_rect.collidepoint(mouse_pos):
                                    back_rect_controls = show_controls()
                                    while True:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                running = False
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                mouse_pos = event.pos
                                                if back_rect_controls.collidepoint(mouse_pos):
                                                    break
                                    break
                                elif language_rect.collidepoint(mouse_pos):
                                    spanish_rect, english_rect, back_rect_language = show_language_selection()
                                    while True:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                running = False
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                mouse_pos = event.pos
                                                if spanish_rect.collidepoint(mouse_pos):
                                                    selected_language = "español"
                                                    break
                                                elif english_rect.collidepoint(mouse_pos):
                                                    selected_language = "inglés"
                                                    break
                                                elif back_rect_language.collidepoint(mouse_pos):  # Volver
                                                    break
                                        else:
                                            continue
                                        break
                                    break
                                elif back_rect_options.collidepoint(mouse_pos):  # Volver
                                    break
                elif exit_rect.collidepoint(mouse_pos):
                    running = False

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar sprites
        player.update()
        tires.update()

        # Generar gotas de agua
        if random.randint(1, 30) == 1:
            water_drop = WaterDrop()
            water_drops.add(water_drop)

        water_drops.update()

        # Detectar colisiones con llantas
        tire_hits = pygame.sprite.spritecollide(player, tires, False)
        if tire_hits:
            player.health -= 10
            for tire in tire_hits:
                tire.rect.y = random.randint(-100, -30)

            if player.health <= 0:
                restart_rect, menu_rect = show_game_over()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos
                            if restart_rect.collidepoint(mouse_pos):
                                game_active = True
                                player.health = 100
                                start_ticks = pygame.time.get_ticks()
                                tires.empty()
                                create_tires(difficulty)
                                break
                            elif menu_rect.collidepoint(mouse_pos):
                                game_active = False
                                break
                    else:
                        continue
                    break

        # Detectar colisiones con gotas de agua
        water_hits = pygame.sprite.spritecollide(player, water_drops, True)
        if water_hits:
            player.health = min(player.health + 5, 100)

        # Controlar el tiempo
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > time_limit:
            show_game_finished()
            game_active = False

        # Dibujar todo
        if level == 1:
            screen.blit(background_image, (0, 0))
        tires.draw(screen)
        water_drops.draw(screen)
        screen.blit(player.image, player.rect)

        # Dibujar la barra de vida
        draw_health_bar(screen, 50, 50, player.health, 100)

        # Mostrar el tiempo restante
        timer_text = pygame.font.Font(None, 36).render(f'Tiempo: {int(time_limit - seconds)}', True, WHITE)
        screen.blit(timer_text, (WIDTH - 150, 50))

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(120)

pygame.quit()
sys.exit()