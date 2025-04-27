import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'  # Suppress ALSA warnings

import pygame
import sys
import random

# Initialize Pygame and set up display
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
BACKGROUND = (40, 44, 52)
GRID_COLOR = (58, 64, 74)
SNAKE_HEAD = (102, 217, 239)
SNAKE_BODY = (85, 181, 199)
FOOD_NORMAL = (249, 38, 114)
FOOD_BONUS = (253, 151, 31)
TEXT_COLOR = (248, 248, 242)
GAME_OVER_COLOR = (249, 38, 114)

# Game settings
SNAKE_SIZE = 20
GRID_SIZE = 20
FOOD_TYPES = {
    'normal': {'color': FOOD_NORMAL, 'points': 1},
    'bonus': {'color': FOOD_BONUS, 'points': 3}
}

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 20)
        self.large_font = pygame.font.SysFont('arial', 40)
        self.reset_game()

    def reset_game(self):
        self.snake_pos = [[100, 50], [90, 50], [80, 50]]
        self.snake_direction = 'RIGHT'
        self.score = 0
        self.food = self.generate_food()
        self.game_over = False
        self.paused = False

    def generate_food(self):
        pos = [random.randrange(1, (width//GRID_SIZE)) * GRID_SIZE, 
               random.randrange(1, (height//GRID_SIZE)) * GRID_SIZE]
        while pos in self.snake_pos:
            pos = [random.randrange(1, (width//GRID_SIZE)) * GRID_SIZE, 
                   random.randrange(1, (height//GRID_SIZE)) * GRID_SIZE]
        return {'pos': pos, 'type': 'normal'}

    def update(self):
        if not self.game_over and not self.paused:
            new_head = self.get_new_head()
            self.snake_pos.insert(0, new_head)

            if self.check_collision():
                self.game_over = True
                return

            # Adjust collision detection for food
            head_x, head_y = self.snake_pos[0]
            food_x, food_y = self.food['pos']
            if abs(head_x - food_x) < SNAKE_SIZE and abs(head_y - food_y) < SNAKE_SIZE:
                self.score += FOOD_TYPES[self.food['type']]['points']
                self.food = self.generate_food()
            else:
                self.snake_pos.pop()

    def get_new_head(self):
        head = self.snake_pos[0].copy()
        if self.snake_direction == 'RIGHT':
            head[0] += SNAKE_SIZE
        elif self.snake_direction == 'LEFT':
            head[0] -= SNAKE_SIZE
        elif self.snake_direction == 'UP':
            head[1] -= SNAKE_SIZE
        elif self.snake_direction == 'DOWN':
            head[1] += SNAKE_SIZE
        return head

    def check_collision(self):
        head = self.snake_pos[0]
        return (head[0] >= width or head[0] < 0 or 
                head[1] >= height or head[1] < 0 or 
                head in self.snake_pos[1:])

    def handle_resize(self, event):
        global width, height, screen
        width, height = event.w, event.h
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def draw(self):
        screen.fill(BACKGROUND)

        # Draw grid lines
        for x in range(0, width, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, height))
        for y in range(0, height, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (width, y))

        for pos in self.snake_pos:
            pygame.draw.rect(screen, SNAKE_BODY, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

        food_pos = self.food['pos']
        pygame.draw.rect(screen, FOOD_TYPES[self.food['type']]['color'], pygame.Rect(food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE))

        # Dynamically adjust text size based on screen dimensions
        dynamic_font_size = max(20, min(width // 32, height // 24))
        dynamic_font = pygame.font.SysFont('arial', dynamic_font_size)

        score_text = dynamic_font.render(f"Score: {self.score}", True, TEXT_COLOR)
        screen.blit(score_text, [10, 10])

        if self.game_over:
            game_over_text = dynamic_font.render("Game Over!", True, GAME_OVER_COLOR)
            restart_text = dynamic_font.render("Press R to Restart or Q to Quit", True, TEXT_COLOR)
            screen.blit(game_over_text, [width//2 - 100, height//2 - 50])
            screen.blit(restart_text, [width//2 - 150, height//2])

        pygame.display.update()

def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                game.handle_resize(event)

            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_r:
                        game.reset_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_RIGHT and game.snake_direction != 'LEFT':
                        game.snake_direction = 'RIGHT'
                    elif event.key == pygame.K_LEFT and game.snake_direction != 'RIGHT':
                        game.snake_direction = 'LEFT'
                    elif event.key == pygame.K_UP and game.snake_direction != 'DOWN':
                        game.snake_direction = 'UP'
                    elif event.key == pygame.K_DOWN and game.snake_direction != 'UP':
                        game.snake_direction = 'DOWN'
                    elif event.key == pygame.K_p:
                        game.paused = not game.paused

        game.update()
        game.draw()
        game.clock.tick(10)

if __name__ == "__main__":
    main()