import pygame, sys, random
def draw_floor():
    screen.blit(floor,(floor_x_pos,650)) 
    screen.blit(floor,(floor_x_pos + 450,650)) 
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-700))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes: 
        if pipe.bottom >= 600 : 
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3  ,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center= (100,bird_rect.centery))
    return new_bird, new_bird_rect 
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255)) # mã màu
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255)) # mã màu
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255)) # mã màu
        high_score_rect = high_score_surface.get_rect(center = (216,630))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency = 44110, size = -16, channels = 2, buffer = 512) # chỉnh âm thanh cho thích hợp 
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()    
game_font = pygame.font.Font('Project/FlappyBird/04B_19.TTF',40)
#Tạo biến      
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0 
# chen background
bg = pygame.image.load('Project/FlappyBird/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg) # full man hinh 
# chen san
floor = pygame.image.load('Project/FlappyBird/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# tao chim 
bird_down = pygame.transform.scale2x(pygame.image.load('Project/FlappyBird/assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('Project/FlappyBird/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('Project/FlappyBird/assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down,bird_mid,bird_up] # 0 1 2 
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load('FlappyBird/assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))
# tạo timer cho chim
birdflap = pygame.USEREVENT +1 
pygame.time.set_timer(birdflap,200)
# tạo ống 
pipe_surface = pygame.image.load('Project/FlappyBird/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# tạo timer
spawnpipe = pygame.USEREVENT # xuất hiện liên tục 
pygame.time.set_timer(spawnpipe,1200)
pipe_height = [200,300,400]
# Tạo màn hình kết thúc 
game_over_surface = pygame.transform.scale2x(pygame.image.load('Project/FlappyBird/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))
# Chèn âm thanh 
flap_sound = pygame.mixer.Sound('Project/FlappyBird/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('Project/FlappyBird/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('Project/FlappyBird/sound/sfx_point.wav')
score_sound_countdown = 100 
# while loop cua game
while True:
    for event in pygame.event.get(): # lấy sự kiện trong pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: # chon phim bay 
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -8.5  # cho chim di len 
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0 
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index <2:
                bird_index +=1
            else:
                bird_index =0
            bird, bird_rect = bird_animation()   
    screen.blit(bg,(0,0))   
    if game_active:
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)  
        game_active = check_collision(pipe_list)
        #ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game over')
    #sàn
    floor_x_pos -= 1 # di chuyen ve phia ben trai   
    draw_floor()
    if floor_x_pos <= -432: # chay lien tuc 
        floor_x_pos = 0   
    pygame.display.update()
    clock.tick(120)
