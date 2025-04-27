
import pygame
import sys
import random

# Initialize Pygame and set up display
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Initialize sound if available
try:
    pygame.mixer.init()
    eat_sound = pygame.mixer.Sound('eat.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
except (pygame.error, FileNotFoundError):
    pygame.mixer.quit()  # Clean up if initialization failed
    eat_sound = None
    game_over_sound = None

# Colors
BACKGROUND = (40, 44, 52)  # Dark modern background
GRID_COLOR = (58, 64, 74)  # Slightly lighter for grid
SNAKE_HEAD = (102, 217, 239)  # Cyan-ish
SNAKE_BODY = (85, 181, 199)  # Lighter cyan
FOOD_NORMAL = (249, 38, 114)  # Pink
FOOD_BONUS = (253, 151, 31)  # Orange
TEXT_COLOR = (248, 248, 242)  # Off-white
GAME_OVER_COLOR = (249, 38, 114)  # Pink

# Game settings
SNAKE_SIZE = 20  # Larger size for better visibility
MIN_SPEED = 5
MAX_SPEED = 25
SPEED_STEP = 1
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
        self.difficulty = 'normal'  # 'easy', 'normal', 'hard'
        self.paused = False
        self.selecting_speed = True
        self.reset_game()

    def get_difficulty_speed(self):
        speeds = {'easy': 8, 'normal': 12, 'hard': 16}
        return speeds[self.difficulty]

    def reset_game(self):
        self.snake_pos = [[100, 50], [90, 50], [80, 50]]
        self.snake_direction = 'RIGHT'
        self.score = 0
        self.high_score = self.load_high_score()
        self.food = self.generate_food()
        self.game_over = False
        self.bonus_food_timer = 0
        self.speed = 12  # Initial speed
        
    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        with open('highscore.txt', 'w') as f:
            f.write(str(max(self.score, self.high_score)))

    def generate_food(self):
        food_type = 'bonus' if random.random() < 0.2 else 'normal'  # 20% chance for bonus food
        pos = [random.randrange(1, (width//10)) * 10, 
               random.randrange(1, (height//10)) * 10]
        while pos in self.snake_pos:
            pos = [random.randrange(1, (width//10)) * 10, 
                   random.randrange(1, (height//10)) * 10]
        return {'pos': pos, 'type': food_type}

    def update(self):
        if not self.game_over:
            # Update snake position
            new_head = self.get_new_head()
            self.snake_pos.insert(0, new_head)

            # Check collisions
            if self.check_collision():
                self.game_over = True
                self.save_high_score()
                if game_over_sound:
                    game_over_sound.play()
                return

            # Check food collision
            if self.snake_pos[0] == self.food['pos']:
                points = FOOD_TYPES[self.food['type']]['points']
                if self.difficulty == 'hard':
                    points *= 2  # Double points on hard mode
                self.score += points
                self.food = self.generate_food()
                if eat_sound:
                    eat_sound.play()
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

    def draw(self):
        screen.fill(BACKGROUND)
        
        if self.selecting_speed:
            title_text = self.large_font.render("Select Speed", True, TEXT_COLOR)
            speed_text = self.large_font.render(str(self.speed), True, TEXT_COLOR)
            instruction_text = self.font.render("Use +/- to adjust speed, ENTER to start", True, TEXT_COLOR)
            
            screen.blit(title_text, [width/2 - 100, height/2 - 100])
            screen.blit(speed_text, [width/2 - 20, height/2 - 20])
            screen.blit(instruction_text, [width/2 - 150, height/2 + 50])
            pygame.display.update()
            return
        
        # Draw grid
        for x in range(0, width, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, height))
        for y in range(0, height, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (width, y))
        
        # Draw snake with rounded corners
        for i, pos in enumerate(self.snake_pos):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(screen, color,
                           pygame.Rect(pos[0], pos[1], SNAKE_SIZE-2, SNAKE_SIZE-2),
                           border_radius=8)

        # Draw food with glow effect
        food_color = FOOD_TYPES[self.food['type']]['color']
        food_pos = self.food['pos']
        # Glow effect
        for size in range(4, 0, -1):
            alpha_surface = pygame.Surface((SNAKE_SIZE+8, SNAKE_SIZE+8), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surface, (*food_color, 50),
                             (SNAKE_SIZE//2+4, SNAKE_SIZE//2+4), SNAKE_SIZE//2 + size)
            screen.blit(alpha_surface, (food_pos[0]-4, food_pos[1]-4))
        # Main food
        pygame.draw.circle(screen, food_color,
                         (food_pos[0]+SNAKE_SIZE//2, food_pos[1]+SNAKE_SIZE//2),
                         SNAKE_SIZE//2-1)

        # Draw scores with modern style
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, TEXT_COLOR)
        speed_text = self.font.render(f"Speed: {self.speed}", True, TEXT_COLOR)
        screen.blit(score_text, [20, 20])
        screen.blit(high_score_text, [width - 170, 20])
        screen.blit(speed_text, [width//2 - 50, 20])

        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((width, height))
            overlay.fill(BACKGROUND)
            overlay.set_alpha(180)
            screen.blit(overlay, (0,0))
            
            game_over_text = self.large_font.render("Game Over!", True, GAME_OVER_COLOR)
            restart_text = self.font.render("Press R to Restart or Q to Quit", True, TEXT_COLOR)
            screen.blit(game_over_text, [width/2 - 100, height/2 - 50])
            screen.blit(restart_text, [width/2 - 150, height/2 + 10])

        pygame.display.update()

def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        game.reset_game()
                else:
                    if event.key == pygame.K_RIGHT and game.snake_direction != 'LEFT':
                        game.snake_direction = 'RIGHT'
                    elif event.key == pygame.K_LEFT and game.snake_direction != 'RIGHT':
                        game.snake_direction = 'LEFT'
                    elif event.key == pygame.K_UP and game.snake_direction != 'DOWN':
                        game.snake_direction = 'UP'
                    elif event.key == pygame.K_DOWN and game.snake_direction != 'UP':
                        game.snake_direction = 'DOWN'
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        game.speed = min(MAX_SPEED, game.speed + SPEED_STEP)
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        game.speed = max(MIN_SPEED, game.speed - SPEED_STEP)
                    elif event.key == pygame.K_p:
                        game.paused = not game.paused
                    elif event.key == pygame.K_1:
                        game.difficulty = 'easy'
                        game.speed = game.get_difficulty_speed()
                    elif event.key == pygame.K_2:
                        game.difficulty = 'normal'
                        game.speed = game.get_difficulty_speed()
                    elif event.key == pygame.K_3:
                        game.difficulty = 'hard'
                        game.speed = game.get_difficulty_speed()
                    elif event.key == pygame.K_RETURN and game.selecting_speed:
                        game.selecting_speed = False

        if game.selecting_speed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
                game.speed = min(MAX_SPEED, game.speed + SPEED_STEP)
            elif keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
                game.speed = max(MIN_SPEED, game.speed - SPEED_STEP)
            game.draw()
        else:
            game.update()
            game.draw()
        game.clock.tick(game.speed)

if __name__ == "__main__":
    main()
