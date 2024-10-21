import pygame  # type: ignore

save_file = "pong.txt"

# Pygame setup
pygame.init()

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Pong")

clock = pygame.time.Clock()
running = True

BALL_COLOR = (0, 0, 255)
PLAYER_COLOR = (255, 255, 255)

ball_x_velocity = 10    
ball_y_velocity = 10

player_width = 20
player_height = 120
player_speed = 10
bot_speed = 5

player_score = 0
bot_score = 0

class Ball:
    def __init__(self, x_position, y_position, radius, color) -> None:
        self.x = x_position
        self.y = y_position
        self.radius = radius
        self.color = color
        self.x_speed = ball_x_velocity
        self.y_speed = ball_y_velocity 
    

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    
    def start_mid(self):
        self.x = screen_width / 2
        self.y = screen_height / 2


    def calculate_current_pos(self):
        # Update position
        self.x += self.x_speed
        self.y += self.y_speed

        if (self.x - self.radius) <= 0:
            global bot_score
            bot_score += 1
            print(f"{bot_score=}")
    
            self.x_speed = -self.x_speed
            self.start_mid()
        
            
        if self.x + self.radius >= screen_width:        
            global player_score
            player_score += 1
            print(f"{player_score=}")
            
            self.x_speed = -self.x_speed
            self.start_mid()


        
        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.y_speed = -self.y_speed
            self.y = max(self.radius, min(self.y, screen_height - self.radius))


        #print(f"{self.x=}\t {screen_width=}\t {self.x_speed=}")

    
    def check_collisions(self, players):
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

        for player_rect in players:
            if ball_rect.colliderect(player_rect):
                self.x_speed = -self.x_speed
                # Use the aceleration of the player to make the ball make curves
                #print("Collision detected")


class Player():
    def __init__(self, width, height, x, y, color, speed) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = player_speed

    def draw(self, scren):
        pygame.draw.rect(screen, self.color, self.rect)


    def moveUp(self, times = 1):
        if self.rect.top > 0:
            self.rect.y = self.rect.y - (self.speed * times)

    def moveDown(self, times = 1):
        if self.rect.bottom < screen_height:
            self.rect.y = self.rect.y + (self.speed * times)


    def follow_ball(self, ball: Ball):
        if abs(self.rect.x - ball.x) < screen_width / 5:
            if ball.y < self.rect.y:
                self.moveUp()
            else:
                self.moveDown()



ball = Ball(500, 300, 20, BALL_COLOR)
player = Player(player_width, player_height, 10, 250, PLAYER_COLOR, player_speed)
bot = Player(player_width, player_height, (screen_width - (player_width * 2)), 250, PLAYER_COLOR, bot_speed)

while running:
    screen.fill("black")
    ball.draw(screen)
    player.draw(screen)
    bot.draw(screen)

    ball.calculate_current_pos()
    ball.check_collisions([player.rect, bot.rect])
    bot.follow_ball(ball)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Handle input for movement
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.moveUp()

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.moveDown()

    if keys[pygame.K_q]:
        running = False


    # Update display
    pygame.display.flip()
    clock.tick(60)
