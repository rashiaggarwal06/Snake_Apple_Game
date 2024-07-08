import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (0, 0, 0)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("./Resources/apple.jpg").convert()
        self.x = 160
        self.y = 160

    def draw_apple(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        max_x = self.parent_screen.get_width() // SIZE
        max_y = self.parent_screen.get_height() // SIZE
        self.x = random.randint(0, max_x - 1) * SIZE
        self.y = random.randint(0, max_y - 1) * SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("./Resources/block.jpg").convert()
        self.block_dimension_x = [SIZE] * length
        self.block_dimension_y = [SIZE] * length
        self.direction = 'DOWN'

    def move_up(self):
        if self.direction != 'DOWN':
            self.direction = 'UP'

    def move_down(self):
        if self.direction != 'UP':
            self.direction = 'DOWN'

    def move_left(self):
        if self.direction != 'RIGHT':
            self.direction = 'LEFT'

    def move_right(self):
        if self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def increase_length(self):
        self.length += 1
        self.block_dimension_x.append(-1)
        self.block_dimension_y.append(-1)

    def draw_snake(self):
        self.parent_screen.fill((52, 162, 235))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_dimension_x[i], self.block_dimension_y[i]))
        pygame.display.flip()

    def walk(self):
        # Update body position
        for i in range(self.length - 1, 0, -1):
            self.block_dimension_x[i] = self.block_dimension_x[i - 1]
            self.block_dimension_y[i] = self.block_dimension_y[i - 1]

        # Update head position
        if self.direction == 'UP':
            self.block_dimension_y[0] -= SIZE
        if self.direction == 'DOWN':
            self.block_dimension_y[0] += SIZE
        if self.direction == 'LEFT':
            self.block_dimension_x[0] -= SIZE
        if self.direction == 'RIGHT':
            self.block_dimension_x[0] += SIZE

        self.draw_snake()

class Game:
    def __init__(self):  
        pygame.init()     
        self.surface = pygame.display.set_mode((1000, 500))

        pygame.mixer.init()
        self.play_background_sound()

        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 2)
        self.snake.draw_snake()
        self.apple = Apple(self.surface)
        self.apple.draw_apple()

        self.show_intro()
        self.play_background_sound()

    def show_intro(self):
        self.stop_all_sounds()
        intro_image = pygame.image.load("./Resources/background.jpg").convert()
        intro_image = pygame.transform.scale(intro_image, (1000, 500))  # Scale image to match window size

        # Calculate center coordinates
        intro_x = (self.surface.get_width() - intro_image.get_width()) // 2
        intro_y = (self.surface.get_height() - intro_image.get_height()) // 2

        self.surface.blit(intro_image, (intro_x, intro_y))
        pygame.display.flip()
        pygame.time.delay(3000)  # Display the image for 3 seconds

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
        
    def stop_all_sounds(self):
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        
    def play_background_sound(self):
        pygame.mixer.music.load('./Resources/bg_music_1.mp3')
        pygame.mixer.music.play()
        
    def play_sound(self, sound):
        sound_effect = pygame.mixer.Sound(f'./Resources/{sound}.mp3')
        pygame.mixer.Sound.play(sound_effect)

    def play(self):
        self.snake.walk()

        # Snake colliding with apple
        if self.is_collision(self.snake.block_dimension_x[0], self.snake.block_dimension_y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.block_dimension_x[0], self.snake.block_dimension_y[0], self.snake.block_dimension_x[i], self.snake.block_dimension_y[i]):
                self.play_sound("crash")
                raise Exception("GAME OVER")

        # Snake colliding with boundaries
        if (self.snake.block_dimension_x[0] < 0 or
            self.snake.block_dimension_x[0] >= self.surface.get_width() or
            self.snake.block_dimension_y[0] < 0 or
            self.snake.block_dimension_y[0] >= self.surface.get_height()):
            self.play_sound("crash")
            raise Exception("GAME OVER")

        self.apple.draw_apple()
        self.display_score()
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30, bold=True)
        score = font.render(f"SCORE: {self.snake.length - 2}", True, (255, 255, 255))
        self.surface.blit(score, (850, 15))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30, bold=True)
        line1 = font.render(f"GAME IS OVER!! YOUR SCORE IS {self.snake.length - 2}", True, (66, 245, 78))
        self.surface.blit(line1, (300, 150))
        line2 = font.render("To PLAY Again Press ENTER or To EXIT Press ESCAPE!", True, (52, 143, 235))
        self.surface.blit(line2, (200, 200))
        pygame.display.flip()

    def reset(self):
        self.stop_all_sounds()
        self.snake = Snake(self.surface, 2)
        self.snake.draw_snake()
        self.apple = Apple(self.surface)
        self.play_background_sound()

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        if pause:
                            pause = False  
                            self.reset()
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True

            pygame.display.flip()

            time.sleep(0.3)

if __name__ == "__main__":
    game = Game()
    game.run()