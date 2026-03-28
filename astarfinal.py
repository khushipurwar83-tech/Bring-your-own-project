import pygame
from queue import PriorityQueue

# SETTINGS
WIDTH = 600
ROWS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding")

# NODE CLASS
class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = col * width   # ✅ FIXED
        self.y = row * width   # ✅ FIXED
        self.color = WHITE
        self.width = width

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


# GRID
def make_grid():
    grid = []
    gap = WIDTH // ROWS
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            grid[i].append(Node(i, j, gap))
    return grid


def draw(win, grid):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    gap = WIDTH // ROWS
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * gap), (WIDTH, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, WIDTH))

    pygame.display.update()


# HEURISTIC
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# NEIGHBORS
def get_neighbors(node, grid):
    neighbors = []
    r, c = node.row, node.col

    if r < ROWS - 1 and grid[r + 1][c].color != BLACK:
        neighbors.append(grid[r + 1][c])
    if r > 0 and grid[r - 1][c].color != BLACK:
        neighbors.append(grid[r - 1][c])
    if c < ROWS - 1 and grid[r][c + 1].color != BLACK:
        neighbors.append(grid[r][c + 1])
    if c > 0 and grid[r][c - 1].color != BLACK:
        neighbors.append(grid[r][c - 1])

    return neighbors


# A* ALGORITHM
def astar(draw_func, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h((start.row, start.col), (end.row, end.col))

    while not open_set.empty():
        current = open_set.get()[2]

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.color = BLUE
                draw_func()
            return True

        for neighbor in get_neighbors(current, grid):
            temp_g = g_score[current] + 1

            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + h(
                    (neighbor.row, neighbor.col),
                    (end.row, end.col)
                )

                count += 1
                open_set.put((f_score[neighbor], count, neighbor))
                neighbor.color = ORANGE

        if current != start:
            current.color = PURPLE

        draw_func()

    return False


# MAIN
def main():
    grid = make_grid()
    start = None
    end = None

    run = True
    while run:
        draw(WIN, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    astar(lambda: draw(WIN, grid), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid()

            # LEFT CLICK
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                gap = WIDTH // ROWS
                x, y = pos
                row = y // gap
                col = x // gap

                node = grid[row][col]

                if not start:
                    start = node
                    node.color = GREEN
                elif not end:
                    end = node
                    node.color = RED
                else:
                    node.color = BLACK

            # RIGHT CLICK
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                gap = WIDTH // ROWS
                x, y = pos
                row = y // gap
                col = x // gap

                node = grid[row][col]
                node.color = WHITE

                if node == start:
                    start = None
                elif node == end:
                    end = None

    pygame.quit()


main()