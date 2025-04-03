import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600  # Window size
GRID_SIZE = 10  # Size of each cell
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Colors
TREE_COLOR = (34, 139, 34)  # Green
FIRE_COLOR = (255, 0, 0)  # Red
EMPTY_COLOR = (0, 0, 0)  # Black

# Default Probabilities (can be adjusted via user input)
INITIAL_TREE_DENSITY = 60  # 60% of the grid starts with trees
GROW_CHANCE = 1  # 1% chance for an empty space to grow a tree
FIRE_CHANCE = 0.1  # 0.1% chance for a tree to catch fire (lightning)
SPREAD_CHANCE = 40  # 40% probability of fire spreading to adjacent trees

def get_user_inputs():
    global INITIAL_TREE_DENSITY, GROW_CHANCE, FIRE_CHANCE, SPREAD_CHANCE
    try:
        INITIAL_TREE_DENSITY = int(input("Enter initial tree density (0 - 100): ")) / 100
        GROW_CHANCE = int(input("Enter tree regrowth rate (0 - 100): ")) / 100
        FIRE_CHANCE = int(input("Enter fire starting chance (0 - 100): ")) / 100
        SPREAD_CHANCE = int(input("Enter fire spread chance (0 - 100): ")) / 100
    except ValueError:
        print("Invalid input! Using default values.")

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Fire Simulation")

# Initialize grid
def create_forest():
    return [[random.choices(["TREE", "EMPTY"], [INITIAL_TREE_DENSITY, 1 - INITIAL_TREE_DENSITY])[0] for _ in range(COLS)] for _ in range(ROWS)]

def draw_forest(forest):
    screen.fill(EMPTY_COLOR)
    for y in range(ROWS):
        for x in range(COLS):
            color = EMPTY_COLOR
            if forest[y][x] == "TREE":
                color = TREE_COLOR
            elif forest[y][x] == "FIRE":
                color = FIRE_COLOR
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.display.flip()

def update_forest(forest):
    new_forest = [row[:] for row in forest]  # Copy grid
    for y in range(ROWS):
        for x in range(COLS):
            if forest[y][x] == "EMPTY" and random.random() < GROW_CHANCE:
                new_forest[y][x] = "TREE"
            elif forest[y][x] == "TREE":
                if random.random() < FIRE_CHANCE:
                    new_forest[y][x] = "FIRE"
            elif forest[y][x] == "FIRE":
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if 0 <= y + dy < ROWS and 0 <= x + dx < COLS and forest[y + dy][x + dx] == "TREE":
                            if random.random() < SPREAD_CHANCE:
                                new_forest[y + dy][x + dx] = "FIRE"
                new_forest[y][x] = "EMPTY"
    return new_forest

def main():
    get_user_inputs()  # Get user inputs for probabilities
    forest = create_forest()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_forest(forest)
        forest = update_forest(forest)
        time.sleep(0.1)  # Delay for smooth simulation
    pygame.quit()

if __name__ == "__main__":
    main()