import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 640, 480
SNAKE_SIZE = 10
SNAKE_SPEED = 15

# Updated colors for a modern look
MODERN_BACKGROUND = (30, 30, 30)  # Dark gray
MODERN_SNAKE_COLOR = (0, 255, 0)  # Bright green
MODERN_FOOD_COLOR = (255, 165, 0)  # Orange
MODERN_TEXT_COLOR = (255, 255, 255)  # White


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake_pos = [[100, 50], [90, 50], [80, 50]]
        self.snake_direction = 'RIGHT'
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        self.score = 0

    def spawn_food(self):
        return [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]

    # Updated draw_snake to use circles
    def draw_snake(self):
        for pos in self.snake_pos:
            pygame.draw.circle(self.screen, MODERN_SNAKE_COLOR, (
                pos[0] + SNAKE_SIZE // 2, pos[1] + SNAKE_SIZE // 2), SNAKE_SIZE // 2)

    # Updated draw_food to use a circle
    def draw_food(self):
        pygame.draw.circle(self.screen, MODERN_FOOD_COLOR, (
            self.food_pos[0] + SNAKE_SIZE // 2, self.food_pos[1] + SNAKE_SIZE // 2), SNAKE_SIZE // 2)

    def update_snake(self):
        if self.snake_direction == 'RIGHT':
            head_pos = [self.snake_pos[0][0] +
                        SNAKE_SIZE, self.snake_pos[0][1]]
        elif self.snake_direction == 'LEFT':
            head_pos = [self.snake_pos[0][0] -
                        SNAKE_SIZE, self.snake_pos[0][1]]
        elif self.snake_direction == 'UP':
            head_pos = [self.snake_pos[0][0],
                        self.snake_pos[0][1] - SNAKE_SIZE]
        elif self.snake_direction == 'DOWN':
            head_pos = [self.snake_pos[0][0],
                        self.snake_pos[0][1] + SNAKE_SIZE]
        self.snake_pos.insert(0, head_pos)

    def check_collisions(self):
        # Wall collision
        if (self.snake_pos[0][0] >= WIDTH or self.snake_pos[0][0] < 0 or
                self.snake_pos[0][1] >= HEIGHT or self.snake_pos[0][1] < 0):
            self.game_over()

        # Self collision
        if self.snake_pos[0] in self.snake_pos[1:]:
            self.game_over()

    def check_food_collision(self):
        if self.snake_pos[0] == self.food_pos:
            self.food_spawn = False
            self.score += 1
        else:
            self.snake_pos.pop()

        if not self.food_spawn:
            self.food_pos = self.spawn_food()
            self.food_spawn = True

    # Updated display_score to use modern text color
    def display_score(self):
        font = pygame.font.SysFont('arial', 25)
        score_surface = font.render(
            f'Score: {self.score}', True, MODERN_TEXT_COLOR)
        self.screen.blit(score_surface, (10, 10))

    # Updated game_over to use modern text color and background
    def game_over(self):
        font = pygame.font.SysFont('arial', 50)
        game_over_surface = font.render('Game Over', True, MODERN_TEXT_COLOR)
        self.screen.fill(MODERN_BACKGROUND)
        self.screen.blit(game_over_surface, (WIDTH // 4, HEIGHT // 3))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.snake_direction != 'LEFT':
                        self.snake_direction = 'RIGHT'
                    elif event.key == pygame.K_LEFT and self.snake_direction != 'RIGHT':
                        self.snake_direction = 'LEFT'
                    elif event.key == pygame.K_UP and self.snake_direction != 'DOWN':
                        self.snake_direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.snake_direction != 'UP':
                        self.snake_direction = 'DOWN'

            self.update_snake()
            self.check_collisions()
            self.check_food_collision()

            # Updated the main loop to use the modern background color
            self.screen.fill(MODERN_BACKGROUND)
            self.draw_snake()
            self.draw_food()
            self.display_score()

            pygame.display.update()
            self.clock.tick(SNAKE_SPEED)


if __name__ == '__main__':
    game = SnakeGame()
    game.run()
