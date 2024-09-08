from tabnanny import check
from wsgiref.util import request_uri

import pygame, sys, random
from pygame.transform import rotate


# Create game function
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos- 650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
    return pipes
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        hit_sound.play()
        return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'play':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (216, 630))
        screen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
# Draw Floor
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))
# Game Pre Init
pygame.mixer.pre_init(44100, -16, 2, 2048)
# Game Init
pygame.init()
screen = pygame.display.set_mode((432, 768))
gravity = 0.25
bird_movement = 0
game_avtice = True
game_font = pygame.font.Font('04B_19.TTF', 40)
score = 0
high_score = 0
# Insert BG
bg = pygame.image.load("assests/background-night.png").convert()
bg = pygame.transform.scale(bg, (432, 768))
#Insert Floor
floor = pygame.image.load("assests/floor.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# Create Bird
bird_down = pygame.image.load("assests/yellowbird-downflap.png").convert_alpha()
bird_mid = pygame.image.load("assests/yellowbird-midflap.png").convert_alpha()
bird_up = pygame.image.load("assests/yellowbird-upflap.png").convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 384))
# Create timer for bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 1200)
# Create Pipe
pipe_surface = pygame.image.load("assests/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# Create Timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]
# Create game over display
game_over_surface = pygame.transform.scale2x(pygame.image.load("assests/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216, 384))
#Insert sound when flap
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_avtice:
                bird_movement = 0
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_avtice == False:
                game_avtice = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    # Draw BG
    screen.blit(bg, (0, 0))
    if game_avtice:
        # Draw Bird and add rectange arround
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_avtice = check_collision(pipe_list)
        # Draw Pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('play')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    # Draw floor
    floor_x_pos -= 1
    draw_floor()

    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    pygame.time.Clock().tick(120)

