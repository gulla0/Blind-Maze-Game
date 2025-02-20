import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
FLASH_DURATION = 1.0  # seconds
FPS = 60
MOVE_DELAY = 0.15  # seconds between moves

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (240, 245, 255)  # Soft gradient start
SLATE_GRAY = (130, 135, 144)  # For grid outlines
SUBTLE_GRAY = (230, 230, 230, 50)  # For flash (with alpha)
DARK_GRAY = (150, 150, 150)  # For permanent border
BLUE = (0, 120, 255)  # Deeper blue for player
BLACK = (0, 0, 0)

# Level configurations (dynamic, no cap, constant 30s timer)
BASE_GRID = 5  # Starting grid size
GRID_INCREMENT = 2  # Increase grid size by 2 per level
TIME_LIMIT = 30  # Constant 30 seconds for all levels

# Maze generation
def generate_maze(width, height):
    grid = [[1 for _ in range(width)] for _ in range(height)]
    grid[0][0] = 0  # Start
    grid[height-1][width-1] = 0  # Goal
    x, y = 0, 0
    while x < width-1 or y < height-1:
        if random.choice([True, False]) and x < width-1:
            x += 1
        elif y < height-1:
            y += 1
        grid[y][x] = 0
    for y in range(height):
        for x in range(width):
            if random.random() < 0.5 and not (x == 0 and y == 0) and not (x == width-1 and y == height-1):
                grid[y][x] = 0
    return grid

# Button class for interactive buttons
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Arial", 36)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                 self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Game class
class BlindMazeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Blind Maze Explorer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 36)  # Modern font
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.state = "start"  # States: "start", "playing", "game_over"

    def reset_game(self, level=0):
        self.level = level
        grid_size = BASE_GRID + (level * GRID_INCREMENT)
        self.width = grid_size
        self.height = grid_size
        self.time_limit = TIME_LIMIT
        self.grid = generate_maze(self.width, self.height)
        self.player = [0, 0]
        self.goal = [self.width-1, self.height-1]
        self.game_timer = self.time_limit
        self.game_over = False
        self.hit_walls = {}  # (x, y) -> flash time remaining
        self.marked_walls = set()  # (x, y) for permanent borders
        self.cell_size = min(self.screen_width // (self.width + 2), self.screen_height // (self.height + 2))

    def run(self):
        while True:
            if self.state == "start":
                self.show_start_screen()
            elif self.state == "playing":
                self.play_game()
            elif self.state == "game_over":
                self.show_end_screen()

    def show_start_screen(self):
        self.screen.fill(WHITE)
        for y in range(self.screen_height):
            color = (LIGHT_BLUE[0], LIGHT_BLUE[1], LIGHT_BLUE[2], 255 - int(y/self.screen_height * 15))
            pygame.draw.line(self.screen, color, (0, y), (self.screen_width, y))
        title = self.font.render("Blind Maze Explorer", True, BLACK)
        rules = self.small_font.render("Rules: Use Arrow Keys to Move, Reach GOAL in 30 Seconds, Walls Flash When Hit", True, BLACK)
        play_button = Button(self.screen_width//2 - 100, self.screen_height//2, 200, 50, "Play", (100, 200, 100), (150, 250, 150))
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, self.screen_height//4))
        self.screen.blit(rules, (self.screen_width//2 - rules.get_width()//2, self.screen_height//2 - 50))
        play_button.draw(self.screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_clicked(event.pos):
                        self.state = "playing"
                        self.reset_game(0)  # Start at Level 0 (first level)
                        return
            self.clock.tick(FPS)

    def play_game(self):
        last_move_time = 0
        while True:
            if self.game_over:
                self.state = "game_over"
                return
            current_time = time.time()
            last_move_time = self.handle_events(current_time, last_move_time)
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self, current_time, last_move_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and current_time - last_move_time >= MOVE_DELAY:
                new_x, new_y = self.player[0], self.player[1]
                if event.key == pygame.K_UP:
                    new_y -= 1
                elif event.key == pygame.K_DOWN:
                    new_y += 1
                elif event.key == pygame.K_LEFT:
                    new_x -= 1
                elif event.key == pygame.K_RIGHT:
                    new_x += 1
                self.move_player(new_x, new_y)
                return current_time
        return last_move_time

    def move_player(self, new_x, new_y):
        if (0 <= new_x < self.width and 0 <= new_y < self.height):
            if self.grid[new_y][new_x] == 0:
                self.player = [new_x, new_y]
            else:
                self.hit_walls[(new_x, new_y)] = FLASH_DURATION
                self.marked_walls.add((new_x, new_y))

    def update(self):
        dt = self.clock.get_time() / 1000.0
        self.game_timer -= dt
        if self.game_timer <= 0:
            self.game_over = True
        for pos in list(self.hit_walls.keys()):
            self.hit_walls[pos] -= dt
            if self.hit_walls[pos] <= 0:
                del self.hit_walls[pos]
        if self.player == self.goal:
            self.level += 1
            self.reset_game(self.level)  # Continue to next level

    def draw(self):
        # Gradient background
        for y in range(self.screen_height):
            color = (LIGHT_BLUE[0], LIGHT_BLUE[1], LIGHT_BLUE[2], 255 - int(y/self.screen_height * 15))
            pygame.draw.line(self.screen, color, (0, y), (self.screen_width, y))
        # Draw grid outlines
        offset_x, offset_y = (self.screen_width - self.width * self.cell_size) // 2, (self.screen_height - self.height * self.cell_size) // 2
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(self.screen, SLATE_GRAY, 
                               (offset_x + x*self.cell_size, offset_y + y*self.cell_size, self.cell_size, self.cell_size), 1, border_radius=2)
        # Draw start (black star)
        start_surface = self.small_font.render("*", True, BLACK)
        self.screen.blit(start_surface, (offset_x + self.cell_size//2 - 5, offset_y + self.cell_size//2 - 10))
        # Draw goal (checkered flag)
        goal_surface = self.small_font.render("🏁", True, BLACK)
        self.screen.blit(goal_surface, (offset_x + self.goal[0]*self.cell_size + self.cell_size//2 - 10, 
                                      offset_y + self.goal[1]*self.cell_size + self.cell_size//2 - 10))
        # Draw player (blue triangle)
        pygame.draw.polygon(self.screen, BLUE, [
            (offset_x + self.player[0]*self.cell_size + self.cell_size//2, offset_y + self.player[1]*self.cell_size + self.cell_size//4),
            (offset_x + self.player[0]*self.cell_size + self.cell_size//4, offset_y + self.player[1]*self.cell_size + 3*self.cell_size//4),
            (offset_x + self.player[0]*self.cell_size + 3*self.cell_size//4, offset_y + self.player[1]*self.cell_size + 3*self.cell_size//4)
        ])
        # Draw hit walls (subtle flash)
        for (x, y), timer in self.hit_walls.items():
            if timer > 0:
                s = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                s.fill(SUBTLE_GRAY)
                self.screen.blit(s, (offset_x + x*self.cell_size, offset_y + y*self.cell_size))
        # Draw marked walls (clear permanent border)
        for (x, y) in self.marked_walls:
            pygame.draw.rect(self.screen, DARK_GRAY, 
                           (offset_x + x*self.cell_size, offset_y + y*self.cell_size, self.cell_size, self.cell_size), 2)
        # Draw UI (with semi-transparent panel, positioned to avoid clutter)
        ui_width, ui_height = 300, 120
        ui_x, ui_y = (self.screen_width - ui_width) // 2, 20
        ui_panel = pygame.Surface((ui_width, ui_height), pygame.SRCALPHA)
        ui_panel.fill((200, 200, 200, 50))  # Light gray, 50% opacity
        self.screen.blit(ui_panel, (ui_x, ui_y))
        timer_text = self.font.render(f"Time: {int(self.game_timer)}", True, BLACK)
        level_text = self.font.render(f"Level: {self.level + 1}", True, BLACK)
        instructions = self.small_font.render("Use Arrow Keys to Move", True, BLACK)
        self.screen.blit(timer_text, (ui_x + 20, ui_y + 20))
        self.screen.blit(level_text, (ui_x + 20, ui_y + 60))
        self.screen.blit(instructions, (ui_x + 20, ui_y + 90))
        pygame.display.flip()

    def show_end_screen(self):
        self.screen.fill(WHITE)
        for y in range(self.screen_height):
            color = (LIGHT_BLUE[0], LIGHT_BLUE[1], LIGHT_BLUE[2], 255 - int(y/self.screen_height * 15))
            pygame.draw.line(self.screen, color, (0, y), (self.screen_width, y))
        message = self.font.render("Game Over!", True, BLACK)
        score = self.level  # Final score = (final level played - 1), so level 1 gives score 0, level 2 gives score 1, etc.
        score_text = self.font.render(f"Score: {score}", True, BLACK)
        replay_button = Button(self.screen_width//2 - 150, self.screen_height//2, 140, 50, "Replay", (100, 200, 100), (150, 250, 150))
        end_button = Button(self.screen_width//2 + 10, self.screen_height//2, 140, 50, "End", (200, 100, 100), (250, 150, 150))
        self.screen.blit(message, (self.screen_width//2 - message.get_width()//2, self.screen_height//3))
        self.screen.blit(score_text, (self.screen_width//2 - score_text.get_width()//2, self.screen_height//3 + 50))
        replay_button.draw(self.screen)
        end_button.draw(self.screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_button.is_clicked(event.pos):
                        self.state = "playing"
                        self.reset_game(0)  # Restart at Level 0 (first level)
                        return
                    if end_button.is_clicked(event.pos):
                        pygame.quit()
                        exit()
            self.clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    game = BlindMazeGame()
    game.run()