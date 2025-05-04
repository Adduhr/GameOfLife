import pygame
import random

from config import *
from colors import *


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def draw_context_plane(game_speed: int) -> None:
    """Zeichnet den Steuerungsbereich des Spiels."""
    text_margin = 10
    context_x = GAME_WIDTH + text_margin
    pygame.draw.rect(screen, BLACK, (GAME_WIDTH, 0, CONTEXT_PLANE_WIDTH, HEIGHT))

    # Draw the control plane
    font = pygame.font.Font(None, 16)

    if game_speed == MAX_UPDATE_FREQ - 1:
        game_speed = "Max."

    elif game_speed == 0:
        game_speed = "Min."

    controls_texts = [
        "Space: Pause/Play",
        "C: Clear",
        "R: Reset",
        "G: Generate Random",
        "",
        "UP: Faster",
        "DOWN: Slower",
        f"Game Speed: {game_speed}",
    ]
    controls = [(control_text, (context_x, (i + 1) * text_margin + i * 16))
                 for i, control_text in enumerate(controls_texts)]

    for control in controls:
        text = font.render(control[0], True, WHITE)
        screen.blit(text, control[1])


def gen(num: int) -> set[tuple[int, int]]:
    """Generiert eine zufällige Menge von Zellen für das Spiel abhängig von `num`."""
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(num)])


def draw_grid(positions: tuple[int, int]) -> None:
    """Zeichnet das Gitter und die Zellen des Spiels auf dem Bildschirm."""

    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, WHITE, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (GAME_WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


def next_generation(positions: tuple[int, int]) -> set[tuple[int, int]]:
    """Berechne die nächste Generation der Zellen basiert auf den Regels des Game of Life."""
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        # filtere lebendige Nachbarzellen
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)
    
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)
    
    return new_positions


def get_neighbors(pos: tuple[int, int]) -> list[tuple[int, int]]:
    """Gibt die 8er Nachbarn einer Zelle zurück."""

    x, y = pos
    neighbors = []
    for shift_x in [-1, 0, 1]:
        if x + shift_x < 0 or x + shift_x > GRID_WIDTH:
            continue
        for shift_y in [-1, 0, 1]:
            if y + shift_y < 0 or y + shift_y > GRID_HEIGHT:
                continue
            if shift_x == 0 and shift_y == 0:
                continue

            neighbors.append((x + shift_x, y + shift_y))
    
    return neighbors


def main():
    running = True
    playing = False
    update_freq = INITIAL_UPDATE_FREQ
    count = 0

    positions = set()
    initial_positions = set()

    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        
        # Steuere die Geschwindigkeit des Spiels
        if count >= update_freq:
            count = 0
            positions = next_generation(positions)

        pygame.display.set_caption("Game of Life - Playing" if playing else "Game of Life - Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos[0] < GRID_WIDTH:  # or pos[1] >= GRID_HEIGHT
                    if pos in positions:
                        positions.remove(pos)
                    else:
                        positions.add(pos)
            
            if event.type == pygame.KEYDOWN:

                # To pause or run press space
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                # To clear the grid press c
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                
                # To reset the grid to a saved state press r
                if event.key == pygame.K_r:
                    positions = initial_positions.copy()
                    playing = False
                    count = 0
                
                # To generate a random grid press g
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, GEN_RANDOM_QUANTIFIER) * GRID_WIDTH)
                    initial_positions = positions.copy()
                    playing = False
                    count = 0
                
                if event.key == pygame.K_UP:
                    if update_freq > 20:
                        update_freq -= 20
                    else:
                        # max speed = update every FPS
                        update_freq = 1
                
                if event.key == pygame.K_DOWN and update_freq < MAX_UPDATE_FREQ:
                    if update_freq >= 20:
                        update_freq += 20
                    else:
                        update_freq = 20
    
        screen.fill(GREY)
        draw_grid(positions)
        draw_context_plane(MAX_UPDATE_FREQ - update_freq)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
