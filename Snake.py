import pygame
import random
import time

# Initializin pygame
pygame.init()

# Screen dimensions
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake AI Game with Pathfinding')

# Colors
background_color = (0, 0, 0)
snake_color = (0, 255, 0)
food_color = (255, 255, 255)

# Snake settings
snake_block = 10
snake_speed = 30

# The clock for controlling game speed
clock = pygame.time.Clock()

# Pathfinding Algorithm classes and functions
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        # Cost from start to current node
        self.g = 0
        # Estimated cost 
        self.h = 0
        # Total cost
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(grid, start, end):
    # Both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    start_node = Node(None, start)
    end_node = Node(None, end)
    open_list.append(start_node)

    # Loop until you find the end
    while open_list:
        current_node = min(open_list, key=lambda x: x.f)
        open_list.remove(current_node)
        closed_list.append(current_node)
        
        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            # Return the path in reverse
            return path[::-1]  
        
        # Generate children
        (x, y) = current_node.position
        # Possible movements
        neighbors = [(x-10, y), (x+10, y), (x, y-10), (x, y+10)]
        for next in neighbors:
            # Check if in bounds
            if next[0] < 0 or next[0] >= width or next[1] < 0 or next[1] >= height:
                continue
            if grid[next[0] // 10][next[1] // 10] != 0:
                continue
            node = Node(current_node, next)
            if node in closed_list:
                continue
            node.g = current_node.g + 10
            node.h = (end_node.position[0] - node.position[0]) ** 2 + (end_node.position[1] - node.position[1]) ** 2
            node.f = node.g + node.h

            if add_to_open(open_list, node):
                open_list.append(node)

# Check if a neighbor should be added to open list
def add_to_open(open_list, neighbor):
    for node in open_list:
        if neighbor == node and neighbor.f >= node.f:
            return False
    return True

# Function to draw snake on the screen
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, snake_color, [x[0], x[1], snake_block, snake_block])

# Game statistics
def draw_text(surface, text, color, font_size, x, y):
    font = pygame.font.SysFont("arial", font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))
    
# Main game working
def gameLoop():
    game_over = False
    game_close = False 
    # Initial snake position
    snake_list = [[width // 2, height // 2]]
    # Initial snake length
    snake_length = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            screen.fill(background_color)
            draw_text(screen, "Game Over! Press C-Play Again or Q-Quit", food_color, 20, width // 4, height // 3)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()  # Restart the game

        screen.fill(background_color)

        grid = [[0 for _ in range(height // 10)] for _ in range(width // 10)]
        for block in snake_list[:-1]:
            if 0 <= block[0] < width and 0 <= block[1] < height:
                grid[block[0] // 10][block[1] // 10] = 1

        start = (snake_list[-1][0], snake_list[-1][1])
        end = (foodx, foody)
        path = astar(grid, start, end)

        if path and len(path) > 1:
            # Visualization of the path
            for step in path[1:]:  
                pygame.draw.rect(screen, (64, 224, 208), [step[0], step[1], snake_block, snake_block], 1)

            next_step = path[1]
            snake_list.append(list(next_step))
            if len(snake_list) > snake_length:
                del snake_list[0]
        else:
            game_close = True

        if snake_list[-1][0] == foodx and snake_list[-1][1] == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake_length += 1

        # Collision detection
        head = snake_list[-1]
        if head[0] >= width or head[0] < 0 or head[1] >= height or head[1] < 0:
            game_close = True
        for block in snake_list[:-1]:
            if block == head:
                game_close = True

        # Display score and path length
        draw_text(screen, f"Score: {snake_length - 1}", food_color, 20, 5, 5)
        if path:
            draw_text(screen, f"Path Length: {len(path)}", food_color, 20, 5, 25)

        pygame.draw.rect(screen, food_color, [foodx, foody, snake_block, snake_block])
        draw_snake(snake_list)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()