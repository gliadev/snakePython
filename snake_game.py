import pygame
import random
import time

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tamaño de las celdas
CELL_SIZE = 20

# fuente de los contenedores
FONT = None


class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -1)
        self.grow = False

    def move(self):
        head = (
            self.body[0][0] + self.direction[0] * CELL_SIZE,
            self.body[0][1] + self.direction[1] * CELL_SIZE,
        )
        self.body = [head] + self.body
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(
                surface, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            )

    def handle_keys(self, key):
        if key == pygame.K_UP and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == pygame.K_DOWN and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == pygame.K_LEFT and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == pygame.K_RIGHT and self.direction != (-1, 0):
            self.direction = (1, 0)

    def collides_with_food(self, food):
        return (
            self.body[0][0] == food.position[0] and self.body[0][1] == food.position[1]
        )

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

    def grow_snake(self):
        self.grow = True


class Food:
    def __init__(self):
        self.position = (
            random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
            random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE,
        )
        self.grow = False

    def draw(self, surface):
        pygame.draw.rect(
            surface, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        )

    def grow_snake(self):
        self.grow = True


def game_over_screen(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()


def main():
    global FONT
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    FONT = pygame.font.Font(None, 36)

    snake = Snake()
    food = Food()

    clock = pygame.time.Clock()

    start_time = time.time()
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                snake.handle_keys(event.key)

        snake.move()

        if snake.collides_with_food(food):
            snake.grow_snake()
            food = Food()
            score += 1

        if (
            snake.body[0][0] < 0
            or snake.body[0][0] >= WIDTH
            or snake.body[0][1] < 0
            or snake.body[0][1] >= HEIGHT
        ):
            game_over_screen(screen)
            pygame.time.wait(2000)
            running = False

        if snake.collides_with_self():
            game_over_screen(screen)
            pygame.time.wait(2000)
            running = False

        # Llenar pantalla con color negro antes de dibujar los elementos
        screen.fill(BLACK)

        # Dibujar marcadores de tiempo y puntos
        elapsed_time = int(time.time() - start_time)
        time_text = FONT.render(f"Time: {elapsed_time} s", True, WHITE)
        screen.blit(time_text, (10, 10))

        score_text = FONT.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(score_text, score_rect)

        snake.draw(screen)
        food.draw(screen)
        pygame.display.flip()

        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
