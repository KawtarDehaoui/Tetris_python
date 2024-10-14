import pygame
import random
import constantes as c

# Définir la taille de la fenêtre
screen = pygame.display.set_mode(c.WINDOW_SIZE)

# Créer une grille vide
grid = [[0 for _ in range(c.GRID_WIDTH)] for _ in range(c.GRID_HEIGHT)]

# Fonction pour dessiner la grille
def draw_grid():
    for y in range(c.GRID_HEIGHT):
        for x in range(c.GRID_WIDTH):
            if grid[y][x] != 0:
                pygame.draw.rect(screen, c.PIECE_COLOR, (x * c.TILE_SIZE, y * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE))

    for y in range(c.GRID_HEIGHT):
        for x in range(c.GRID_WIDTH):
            pygame.draw.rect(screen, c.GRID_COLOR, (x * c.TILE_SIZE, y * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE), 1)

class Tetromino:
    def __init__(self):
        self.shape = random.choice(c.TETROMINOS)
        self.x = c.GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def check_collision(self, grid):
        for y, row in enumerate(self.shape):
            for x, value in enumerate(row):
                if value:
                    if (x + self.x < 0 or x + self.x >= c.GRID_WIDTH or
                            y + self.y >= c.GRID_HEIGHT or grid[y + self.y][x + self.x]):
                        return True
        return False
    
# Fixer la pièce dans la grille
def fix_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, value in enumerate(row):
            if value:
                grid[y + tetromino.y][x + tetromino.x] = 1

# Supprimer les lignes complètes
def clear_lines():
    global grid, score
    new_grid = [row for row in grid if any(value == 0 for value in row)]
    cleared_lines = c.GRID_HEIGHT - len(new_grid)
    new_grid = [[0 for _ in range(c.GRID_WIDTH)] for _ in range(cleared_lines)] + new_grid
    grid = new_grid
    score += cleared_lines * 100
    
# Fonction pour dessiner le score
def draw_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, c.TEXT_COLOR)
    screen.blit(text, (10, 10))


# Gestion des événements
def handle_input(current_tetromino):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino.x -= 1
                if current_tetromino.check_collision(grid):
                    current_tetromino.x += 1
            elif event.key == pygame.K_RIGHT:
                current_tetromino.x += 1
                if current_tetromino.check_collision(grid):
                    current_tetromino.x -= 1
            elif event.key == pygame.K_DOWN:
                current_tetromino.y += 1
                if current_tetromino.check_collision(grid):
                    current_tetromino.y -= 1
            elif event.key == pygame.K_UP:
                current_tetromino.rotate()
                if current_tetromino.check_collision(grid):
                    current_tetromino.rotate()

    return True

# Dessiner un bouton
def draw_button(text, position, size):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, c.TEXT_COLOR)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, c.PIECE_COLOR, button_rect)
    screen.blit(text_surface, (position[0] + (size[0] - text_surface.get_width()) // 2, 
                               position[1] + (size[1] - text_surface.get_height()) // 2))
    return button_rect

# Game over avec menu Retry / Quit
def show_game_over_menu():
    font = pygame.font.Font(None, 48)
    game_over_text = font.render('Game Over', True, c.TEXT_COLOR)
    screen.fill(c.BG_COLOR)
    screen.blit(game_over_text, (c.WINDOW_SIZE[0] // 2 - game_over_text.get_width() // 2, 
                                 c.WINDOW_SIZE[1] // 2 - game_over_text.get_height() // 2 - 50))
    
    retry_button = draw_button("Retry", (c.WINDOW_SIZE[0] // 2 - 75, c.WINDOW_SIZE[1] // 2 + 20), (150, 50))
    quit_button = draw_button("Quit", (c.WINDOW_SIZE[0] // 2 - 75, c.WINDOW_SIZE[1] // 2 + 90), (150, 50))
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                if retry_button.collidepoint(event.pos):
                    return True  
                elif quit_button.collidepoint(event.pos):
                    return False  

        pygame.time.wait(10)

# Boucle principale avec gestion du Game Over
def game_loop():
    global score, grid
    score = 0 
    running = True
    clock = pygame.time.Clock()
    current_tetromino = Tetromino()

    while running:
        running = handle_input(current_tetromino)
        current_tetromino.y += 1
        if current_tetromino.check_collision(grid):
            current_tetromino.y -= 1
            fix_tetromino(current_tetromino)
            clear_lines()
            current_tetromino = Tetromino()
            if current_tetromino.check_collision(grid):
                running = show_game_over_menu()  
                if running:
                    grid = [[0 for _ in range(c.GRID_WIDTH)] for _ in range(c.GRID_HEIGHT)]  # Réinitialiser la grille
                    score = 0  # Réinitialiser le score
                else:
                    return  # Quitter le jeu si l'utilisateur choisit Quit

        screen.fill(c.BG_COLOR)
        draw_grid()

        for y, row in enumerate(current_tetromino.shape):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, c.PIECE_COLOR, ((current_tetromino.x + x) * c.TILE_SIZE, 
                                                            (current_tetromino.y + y) * c.TILE_SIZE, 
                                                            c.TILE_SIZE, c.TILE_SIZE))

        draw_score(score)
        pygame.display.flip()
        clock.tick(10)
