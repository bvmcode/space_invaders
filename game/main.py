import pygame
import random
import math

pygame.init()
pygame.display.set_caption('Space Invaders')
screen = pygame.display.set_mode((800, 800)) # w/h
icon = pygame.image.load('./images/icon.png')
pygame.display.set_icon(icon)
player_img = pygame.image.load('./images/player.png')
bg_img = pygame.image.load('./images/background.png')
enemy_img = pygame.image.load('./images/enemy.png')
bullet_img = pygame.image.load('./images/bullet.png')
font = pygame.font.Font('freesansbold.ttf', 32)
player_x_initial = 365
player_y_initial = 650


def player_position(x, y, movement_type= None):
    if movement_type:
        movement_clip = 2.5
        min_position_x = 5
        max_position_x = 730
        min_position_y = 570
        max_position_y = 740
        if movement_type == 'LEFT' and x > min_position_x:
            x -= movement_clip
        if movement_type == 'RIGHT' and x < max_position_x:
            x += movement_clip
        if movement_type == 'UP' and y > min_position_y:
            y -= movement_clip
        if movement_type == 'DOWN' and y < max_position_y:
            y += movement_clip
    screen.blit(player_img, (x, y))
    return x, y


def enemy_position(ex, ey, horiz_movement_type, player_x, player_y):
    enemy_displacement_x = 2.2
    enemy_displacement_y = 40

    if ex >= 740:
        horiz_movement_type = 'LEFT'
        ey += enemy_displacement_y
    if ex <= 2:
        horiz_movement_type = 'RIGHT'
        ey += enemy_displacement_y

    if horiz_movement_type == 'RIGHT':
        ex += enemy_displacement_x
    if horiz_movement_type == 'LEFT':
        ex -= enemy_displacement_x

    distance_to_player_x = abs(player_x - ex)
    distance_to_player_y = abs(player_y - ey)
    if ey >= 700 or (distance_to_player_x<=50 and distance_to_player_y<=50):
        print('game over')
    screen.blit(enemy_img, (ex, ey))        
    return ex, ey, horiz_movement_type


def fire_bullet(bullet_x, bullet_y):
    bullet_displacement = 20
    bullet_y = bullet_y - bullet_displacement
    if bullet_y < 30:
        return bullet_y, 'ready'
    screen.blit(bullet_img, (bullet_x, bullet_y))
    return bullet_y, 'fired'

def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x-bullet_x,2) + math.pow(enemy_y-bullet_y,2))
    if distance < 25:
        return True
    return False

def show_score(score):
    text_x = 10
    text_y = 10
    rendering = font.render(f'Score : {score}', True, (255,255,255))
    screen.blit(rendering, (text_x, text_y))

def main():
    running = True
    player_x = player_x_initial
    player_y = player_y_initial
    enemy_x = random.randint(50,750)
    enemy_y = random.randint(50,150)
    next_bullet = 'ready'
    bullet_x = 0
    bullet_y = 0
    score = 0

    num_of_enemies = 10
    enemies = []
    for i in range(num_of_enemies):
        enemies.append( (random.randint(50,750), random.randint(50,150), 'RIGHT' ))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if next_bullet == 'ready':
                        bullet_x = player_x + 10
                        bullet_y = player_y + 16
                        bullet_y, next_bullet = fire_bullet(bullet_x, bullet_y)
        
        screen.blit(bg_img, (0,0))
        player_x, player_y = player_position(player_x, player_y)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x, player_y = player_position(player_x, player_y, 'LEFT')
        if keys[pygame.K_RIGHT]:
            player_x, player_y = player_position(player_x, player_y, 'RIGHT')
        if keys[pygame.K_UP]:
            player_x, player_y = player_position(player_x, player_y, 'UP')
        if keys[pygame.K_DOWN]:
            player_x, player_y = player_position(player_x, player_y, 'DOWN')

        if next_bullet == 'fired':
            bullet_y, next_bullet = fire_bullet(bullet_x, bullet_y)
        for i in range(num_of_enemies):

            enemy_x, enemy_y, horiz_movement_type = enemy_position(enemies[i][0], enemies[i][1], enemies[i][2], player_x, player_y)

            destroyed = collision(enemy_x, enemy_y, bullet_x, bullet_y)
            
            if destroyed:
                score += 1
                enemies[i] = None
            else:
                enemies[i] = (enemy_x, enemy_y, horiz_movement_type )

        enemies = [i for i in enemies if i]
        num_of_enemies = len(enemies)

        show_score(score)
        pygame.display.update()
    

if __name__ == '__main__':
    main()