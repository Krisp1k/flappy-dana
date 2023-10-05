import pygame
import os
import random
import urllib.parse
import urllib.request
import webbrowser

pygame.init()

# Set up the display
WIDTH, HEIGHT = 500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy DANA")

# Load resources
PEPE_IMAGE = pygame.image.load("src/xddddddddd.png")
PEPE_WIDTH, PEPE_HEIGHT = 64, 64
PEPE_IMAGE = pygame.transform.scale(PEPE_IMAGE, (PEPE_WIDTH, PEPE_HEIGHT))
PIPE_IMAGE = pygame.image.load("src/xddddddddd.png")
PIPE_WIDTH, PIPE_HEIGHT = 80, 500
PIPE_IMAGE = pygame.transform.scale(PIPE_IMAGE, (PIPE_WIDTH, PIPE_HEIGHT))
FONT = pygame.font.SysFont("comicsans", 50)
LABEL_FONT = pygame.font.SysFont("comicsans", 24)
TEXT_FONT = pygame.font.SysFont("comicsans", 16)
PE_SOUND = pygame.mixer.Sound("src/pe.mp3")
DEBUGER_SOUND = pygame.mixer.Sound('src/debuger.mp3')
DANA_SOUND = pygame.mixer.Sound('src/dana.mp3')

# Set up game variables
GRAVITY = 0.25
JUMP_VELOCITY = -8
PIPE_VELOCITY = -5
PIPE_GAP = 200
PIPE_SPACING = 300
PIPE_FREQUENCY = 120

pepe_x = WIDTH/2 - PEPE_WIDTH/2
pepe_y = HEIGHT/2 - PEPE_HEIGHT/2
pepe_vel = 0
pipes = []
score = 0
game_over = False

def reset_game():
    global pepe_x, pepe_y, pepe_vel, pipes, score, game_over
    pepe_x = WIDTH/2 - PEPE_WIDTH/2
    pepe_y = HEIGHT/2 - PEPE_HEIGHT/2
    pepe_vel = 0
    pipes = []
    score = 0
    game_over = False

# Define helper functions
def draw_window():
    global game_over
    # Load background image
    BACKGROUND_IMAGE = pygame.image.load("src/xddddddddd.png")
    #BACKGROUND_IMAGE = pygame.image.load("src/kitty_smol.png")
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
    
    # Draw background image
    WIN.blit(BACKGROUND_IMAGE, (0, 0))
    
    # Draw game elements
    for pipe in pipes:
        WIN.blit(PIPE_IMAGE, (pipe["x"], pipe["top_y"] - PIPE_HEIGHT))
        WIN.blit(PIPE_IMAGE, (pipe["x"], pipe["bottom_y"]))

    WIN.blit(PEPE_IMAGE, (pepe_x, pepe_y))
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    WIN.blit(score_text, (10, 10))

    if game_over:
        game_over_text = FONT.render("Game Over", True, (255, 0, 0))
        WIN.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()*2))
        
        # Add an input field for "name"
        input_rect = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 - 50, 200, 32)
        input_text = ""
        
        # Add a button for "submit" with the label "save to leaderboard"
        button_rect = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 + 10, 200, 50)
        button_text = LABEL_FONT.render("Save", True, (0, 0, 0))

        restart_rect = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 + 70, 200, 50)
        restart_text = LABEL_FONT.render("Restart", True, (255, 255, 255))

        leaderboards_rect = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 + 130, 200, 50)
        leaderboards_text = LABEL_FONT.render("Leaderboards", True, (255, 255, 255))
        
        # Game loop
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if len(input_text) < 25:
                        
                        if event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            input_text += event.unicode
                        
                        input_surface = TEXT_FONT.render(input_text, False, (255, 255, 255))

                        print(input_text)
                                
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if restart_rect.collidepoint(event.pos):
                        reset_game()
                        return

                    if button_rect.collidepoint(event.pos) and input_text != "" and len(input_text) > 0 and len(input_text) <= 25:
                        name = input_text
                        url = "https://api.krisp1k.eu/flappy-dana/add-to-leaderboard-dana.php"
                        data = urllib.parse.urlencode({"name": name, "score": score}).encode()
                        urllib.request.urlopen(url, data)
                        reset_game()
                        return
                    
                    if leaderboards_rect.collidepoint(event.pos):
                        # write a function that opens a specific url in the browser
                        url = "https://api.krisp1k.eu/flappy-dana/index-dana.php"
                        webbrowser.open(url)
                        return

            # Draw the input field
            pygame.draw.rect(WIN, (255, 255, 255), input_rect, 2)
            input_surface = TEXT_FONT.render(input_text, False, (255, 255, 255)) 
            WIN.blit(input_surface, (input_rect.x + 2, input_rect.y + 2))

            # Draw the button
            pygame.draw.rect(WIN, (0, 255, 0), button_rect)
            WIN.blit(button_text, (button_rect.x + button_rect.width/2.75, button_rect.y + 7))

            # make this rect slightly under the upper rect
            pygame.draw.rect(WIN, (255, 0, 0), restart_rect)
            WIN.blit(restart_text, (restart_rect.x + restart_rect.width/3.5, restart_rect.y + 10))

            pygame.draw.rect(WIN, (0, 0, 255), leaderboards_rect)
            WIN.blit(leaderboards_text, (leaderboards_rect.x + leaderboards_rect.width/10, leaderboards_rect.y + 10))


            pygame.display.update()

  

    # Update the display


    pygame.display.update()

def add_pipe():
    top_y = random.randint(50, HEIGHT/2 - PIPE_GAP) 
    bottom_y = top_y + PIPE_GAP
    pipes.append({"x": WIDTH, "top_y": top_y, "bottom_y": bottom_y, "scored": False})

def move_pipes():
    for pipe in pipes:
        pipe["x"] += PIPE_VELOCITY

def remove_pipes():
    for pipe in pipes:
        if pipe["x"] < -PIPE_WIDTH:
            pipes.remove(pipe)

def check_collision():
    global game_over
    for pipe in pipes:
        top_rect = pygame.Rect(pipe["x"], pipe["top_y"] - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)
        bottom_rect = pygame.Rect(pipe["x"], pipe["bottom_y"], PIPE_WIDTH, PIPE_HEIGHT)
        if top_rect.colliderect(pepe_rect) or bottom_rect.colliderect(pepe_rect):
            DEBUGER_SOUND.play()
            game_over = True

def check_score():
    global score
    for pipe in pipes:
        if pipe["x"] + PIPE_WIDTH < pepe_x and not pipe["scored"]:
            score += 1
            pipe["scored"] = True
            DANA_SOUND.play()

# Main game loop
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                pepe_vel = JUMP_VELOCITY
                PE_SOUND.play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                game_over = False
                pepe_x = WIDTH/2 - PEPE_WIDTH/2
                pepe_y = HEIGHT/2 - PEPE_HEIGHT/2
                pepe_vel = 0
                pipes = []
                score = 0

    # Update game state
    pepe_vel += GRAVITY
    pepe_y += pepe_vel
    pepe_rect = pygame.Rect(pepe_x, pepe_y, PEPE_WIDTH, PEPE_HEIGHT)
    if not game_over:
        if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - PIPE_SPACING:
            add_pipe()

        move_pipes()
        remove_pipes()
        check_collision()
        check_score()

    # Draw the window
    draw_window()

pygame.quit()