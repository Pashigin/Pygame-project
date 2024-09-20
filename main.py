from random import randint
import pygame


class CoinsGame:
    def __init__(self):
        pygame.init()

        # set the width and height of the game window
        self.window_height = 600
        self.window_width = 600

        # set the window properties
        self.window_color = (255, 255, 255)
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Rain of Coins")

        self.clock = pygame.time.Clock()

        # start the game with the following functions
        self.load_images()
        self.new_game()
        self.main_loop()

    # load images into the program, get the size of the images
    def load_images(self):
        self.images = []
        for name in ["robot", "monster", "coin"]:
            self.images.append(pygame.image.load(name + ".png"))

        self.robot_width = self.images[0].get_width()
        self.robot_height = self.images[0].get_height()

        self.monster_width = self.images[1].get_width()
        self.monster_height = self.images[1].get_height()

        self.coin_width = self.images[2].get_width()
        self.coin_height = self.images[2].get_height()

    # set properties for the new game
    def new_game(self):
        self.game_over = False
        self.points = 0
        self.monster_numbers = 2
        self.coin_numbers = 5

        # list of coins and monsters with their postitions
        self.monster_positions = []
        self.coins_positions = []

        # starting coordinates and speed of the robot
        self.x = self.window_width / 2 - self.robot_width / 2
        self.y = self.window_height - self.robot_height
        self.velocity = 3

        self.to_right = False
        self.to_left = False

        self.set_positions()

    # set the starting positions of the monsters and coins (random each time the game starts)
    def set_positions(self):
        for i in range(self.coin_numbers):
            self.coins_positions.append(
                [randint(0, self.window_width - self.coin_width), randint(-800, 0)]
            )

        for j in range(self.monster_numbers):
            self.monster_positions.append(
                [randint(0, self.window_width - self.monster_width), randint(-800, 0)]
            )

    # main loop of the game
    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            self.game_action()

    # main logic how the monsters and coins are dropping down and action with the robot (player)
    def game_action(self):
        # coins
        for i in range(self.coin_numbers):
            self.coins_positions[i][1] += 1
            if (
                self.coins_positions[i][1] + self.coin_height >= self.y
                and self.coins_positions[i][1] + self.coin_height / 2
                <= self.window_height
            ):
                robot_middle = self.x + self.robot_width / 2
                coin_middle = self.coins_positions[i][0] + self.coin_width / 2

                if (
                    abs(robot_middle - coin_middle)
                    <= (self.robot_width + self.coin_width) / 2
                ):
                    #   the robot caught a coin
                    self.coins_positions[i][0] = randint(
                        0, self.window_width - self.coin_width
                    )
                    self.coins_positions[i][1] = randint(-800, 0)
                    self.points += 1
            elif self.coins_positions[i][1] - self.coin_height > self.window_height:
                self.coins_positions[i][0] = randint(
                    0, self.window_width - self.coin_width
                )
                self.coins_positions[i][1] = randint(-800, 0)

        # monsters
        for j in range(self.monster_numbers):
            self.monster_positions[j][1] += 1
            if (
                self.monster_positions[j][1] + self.monster_height >= self.y
                and self.monster_positions[j][1] + self.monster_height / 2
                <= self.window_height
            ):
                robot_middle = self.x + self.robot_width / 2
                monster_middle = self.monster_positions[j][0] + self.monster_width / 2

                if (
                    abs(robot_middle - monster_middle)
                    <= (self.robot_width + self.monster_width) / 2
                ):
                    #   the robot caught a monster
                    self.game_over = True
            elif (
                self.monster_positions[j][1] + self.monster_height >= self.window_height
            ):
                self.monster_positions[j][0] = randint(
                    0, self.window_width - self.monster_width
                )
                self.monster_positions[j][1] = randint(-800, 0)

    # keyboard events
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_RETURN:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False

            if event.type == pygame.QUIT:
                exit()

        if self.to_right:
            if self.x + self.robot_width < self.window_width:
                self.x += self.velocity
        if self.to_left:
            if self.x > 0:
                self.x -= self.velocity

    # draw the game window and its content
    def draw_window(self):
        self.window.fill(self.window_color)

        if self.game_over is False:
            self.window.blit(self.images[0], (self.x, self.y))

            for i in range(self.coin_numbers):
                self.window.blit(
                    self.images[2],
                    (self.coins_positions[i][0], self.coins_positions[i][1]),
                )
            for j in range(self.monster_numbers):
                self.window.blit(
                    self.images[1],
                    (self.monster_positions[j][0], self.monster_positions[j][1]),
                )
        else:
            game_over_text = self.game_font.render("Game Over", True, (0, 0, 0))
            self.window.fill((255, 255, 255))
            self.window.blit(
                game_over_text,
                (
                    (self.window_width - game_over_text.get_width()) // 2,
                    (self.window_height - game_over_text.get_height()) // 2,
                ),
            )

        score_text = self.game_font.render(
            "Points: " + str(self.points), True, (255, 0, 0)
        )
        self.window.blit(score_text, (10, 10))

        exit_text = self.game_font.render("Exit: Esc", True, (255, 0, 0))
        self.window.blit(exit_text, (self.window_width - 100, 50))

        new_text = self.game_font.render("NG: Enter", True, (255, 0, 0))
        self.window.blit(new_text, (self.window_width - 110, 10))

        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    CoinsGame()
