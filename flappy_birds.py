import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface,(floor_posX,435))
    screen.blit(floor_surface,(floor_posX + 287,435))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (300,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (300,random_pipe_pos - 150))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 2
	return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
        
    if bird_rect.top <= -50 or bird_rect.bottom >= 435:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 5 , 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird]
    new_bird_rect = new_bird.get_rect(center = (35,bird_rect.centery))
    return new_bird_rect,new_bird

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (138,50))
        screen.blit(score_surface,score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (138,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (138,400))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((276,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',20)

# Game varialble
gravity = 0.12
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/sprites/background-night.png').convert()
# bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/sprites/base.png').convert()
floor_posX = 0

bird_downflap = pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (35,256))

BIRDFLAP = pygame.USEREVENT + 1

# bird_surface = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
# # bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (35,256))

pipe_surface = pygame.image.load('assets/sprites/pipe-red.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [200,250,300,350,400]

game_over_surface = pygame.image.load('assets/sprites/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (138,230))

flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
death_sound = pygame.mixer.Sound('assets/audio/hit.wav')
# score_sound = pygame.mixer.Sound('assets/audio/point.wav')
# score_sound_count = 100

#mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (35,256)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_rect,bird_surface = bird_animation()

    screen.blit(bg_surface,(0,0))
 
    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,(bird_rect))
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        # score_sound_count -= 1
        # if score_sound_count <=0:
        #     score_sound.play()

    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_posX -= 0.5
    draw_floor()
    if floor_posX <= -287 :
        floor_posX = 0

    pygame.display.update()
    clock.tick(120)