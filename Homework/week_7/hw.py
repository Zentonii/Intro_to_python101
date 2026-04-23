import random

ROWS = 10
COLS = 20

def create_random_grid():
    return [[random.randint(0, 1) for _ in range(COLS)] for _ in range(ROWS)]

def display_grid(grid, generation):
    print(f"\n--- Generation {generation} ---")
    for row in grid:
        print(' '.join('[]' if cell == 1 else '.' for cell in row))
    alive = sum(cell for row in grid for cell in row)
    print(f"Alive cells: {alive}")

def count_neighbours(grid, r, c):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                count += grid[nr][nc]
    return count

def next_generation(grid):
    new_grid = []
    for r in range(ROWS):
        new_row = []
        for c in range(COLS):
            neighbours = count_neighbours(grid, r, c)
            cell = grid[r][c]          
            if cell == 1 and (neighbours < 2 or neighbours > 3):
                new_row.append(0)         
            elif cell == 1 and neighbours in [2, 3]:
                new_row.append(1)
            elif cell == 0 and neighbours == 3:
                new_row.append(1)
            else:
                new_row.append(0)
        new_grid.append(new_row)
    return new_grid

def play():
    grid = create_random_grid()
    generation = 1

    while True:
        display_grid(grid, generation)
        answer = input("\nContinue to next generation? (yes / no): ").strip().lower()
        if answer != 'yes':
            print("\nSimulation stopped. Goodbye!")
            break
        grid = next_generation(grid)
        generation += 1

play()