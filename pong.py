import pygame 

# Initalize Pygame
pygame.init()

# Display Screen with Caption
WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

# Constant Variables
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans",50)
WINNING_SCORE = 7

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y 

def draw(win, paddles, ball, left_score, right_score):
    # Background
    win.fill(BLACK)

    # Score
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH*(3/4) - right_score_text.get_width()//2, 20))

    # Paddles
    for paddle in paddles:
        paddle.draw(win)

    # Center Line
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE,( WIDTH // 2 - 5, i, 10, HEIGHT//20))

    # Ball
    ball.draw(win)

    # Update Drawing
    pygame.display.update() # Performs drawing operation


class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    def __init__(self, x,y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def handle_collision(ball, left_paddle, right_paddle):
    #Ceiling collision
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    #Left Paddle
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x+ left_paddle.width:
                ball.x_vel *= -1

                #This code is math for solving for the velocity and angle of the y direction for the ball
                middle_y = left_paddle.y + left_paddle.height/2
                difference_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2)/ball.MAX_VEL  
                y_vel = difference_y / reduction_factor
                ball.y_vel = -1* y_vel
    else: 
         #Right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                #This code is math for solving for the velocity and angle of the y direction for the ball
                middle_y = right_paddle.y + right_paddle.height/2
                difference_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2)/ball.MAX_VEL  
                y_vel = difference_y / reduction_factor
                ball.y_vel = -1* y_vel
       

def handle_paddle_movement(keys, left_paddle, right_paddle):
    # Left Player key presses
    if keys[pygame.K_w]  and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up = True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    # Right player key Presses
    if keys[pygame.K_UP]  and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up = True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    # Creating the Paddles
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT )
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT )
    ball = Ball(WIDTH//2, HEIGHT // 2, BALL_RADIUS)

    #Scores
    left_score = 0
    right_score = 0

    # Win Condition
    won = False

    while run: 
        # Runs maximum at 60 frames per second
        clock.tick(FPS)

        # Draw entities
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)

        # If close button event is clicked
        for event in pygame.event.get():
            # If you click the close button
            if event.type == pygame.QUIT:
                run = False
                break
        
        # Get key presses and pass to paddle movement
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        
        #Move the Ball and check to see if there is collision
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Round Resets
        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        # Win Condition
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Wins!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Wins!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            won = False

    # Close
    pygame.quit()

if __name__ == '__main__':
    main()