import pygame
import sys
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bullet Hell Game")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

def reset_game():
    player_x, player_y = 400, 300
    bullets = []
    last_spawn = pygame.time.get_ticks()
    score = 0
    spawn_count = 1  # 🔥 한 번에 생성되는 탄 수
    return player_x, player_y, bullets, last_spawn, score, spawn_count, False

player_x, player_y, bullets, last_spawn, score, spawn_count, game_over = reset_game()

player_speed = 7
bullet_speed = 4

player_radius = 10
bullet_radius = 8

running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_x, player_y, bullets, last_spawn, score, spawn_count, game_over = reset_game()

    if not game_over:
        # 🔵 플레이어 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed

        # 🟡 점수 증가 (틱마다 +1)
        score += 1

        # 🔥 10점마다 탄막 증가
        if score % 10 == 0:
            spawn_count += 1

        # 🔴 탄 생성
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn > 1000:
            last_spawn = current_time

            for _ in range(spawn_count):
                side = random.choice(["top", "bottom", "left", "right"])

                if side == "top":
                    x = random.randint(0, 800)
                    y = 0
                elif side == "bottom":
                    x = random.randint(0, 800)
                    y = 600
                elif side == "left":
                    x = 0
                    y = random.randint(0, 600)
                else:
                    x = 800
                    y = random.randint(0, 600)

                dx = player_x - x
                dy = player_y - y
                dist = math.hypot(dx, dy)

                dx /= dist
                dy /= dist

                bullets.append([x, y, dx, dy])

        # 🔴 탄 이동
        new_bullets = []
        for x, y, dx, dy in bullets:
            x += dx * bullet_speed
            y += dy * bullet_speed

            # 💥 충돌
            dist = math.hypot(player_x - x, player_y - y)
            if dist < player_radius + bullet_radius:
                game_over = True

            new_bullets.append([x, y, dx, dy])

        bullets = new_bullets

    # 🔵 플레이어
    pygame.draw.circle(screen, BLUE, (int(player_x), int(player_y)), player_radius)

    # 🔴 탄
    for x, y, _, _ in bullets:
        pygame.draw.circle(screen, RED, (int(x), int(y)), bullet_radius)

    # 🟡 점수 표시
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # 💥 게임오버
    if game_over:
        text = big_font.render("GAME OVER", True, (0, 0, 0))
        screen.blit(text, (250, 250))

        text2 = font.render("Press ENTER", True, (0, 0, 0))
        screen.blit(text2, (260, 320))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()