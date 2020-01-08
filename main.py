"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
import numpy as np
import copy
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
 
# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell


def reset_grid():
    grid = []
    for row in range(10):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(10):
            grid[row].append(0)  # Append a cell

    return grid
 
grid[1][5] = 1
y = 1
x = 5
 
pygame.init()
 
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
pygame.display.set_caption("Array Backed Grid")
 
done = False
 
clock = pygame.time.Clock()

ACTIONS = {
    "UP": 0,
    "DOWN": 1,
    "LEFT": 2,
    "RIGHT":3
    }

def is_in_grid(x, y):
    if y < len(grid) and y >= 0:
        if x < len(grid[0]) and x >= 0:
            return True
    return False


def update_agent_pos(x, y):

    while(True):
        to_y, to_x = y, x
        action = np.random.randint(5)
        if action == ACTIONS["UP"]:
            to_y += -1
        elif action == ACTIONS["DOWN"]:
            to_y += 1
        elif action == ACTIONS["LEFT"]:
            to_x += -1
        elif action == ACTIONS["RIGHT"]:
            to_x += 1

        if is_in_grid(to_y, to_x) is True:
            return to_x, to_y

while not done:
    screen.fill(BLACK)
 
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
 
    # Limit to 60 frames per second
    clock.tick(1)
 
    pygame.display.flip()

    # エージェントの位置の更新
    to_x, to_y = update_agent_pos(x, y)

    # 位置の更新 
    grid[y][x] = 0
    grid[to_y][to_x] = 1
    x, y = to_x, to_y
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
