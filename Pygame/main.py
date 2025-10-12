import pygame
import random

# 顏色定義
BLACK = (0, 0, 0)

# 隕石尺寸清單
ROCK_SIZES = [
    (20, 20), (30, 30), (40, 40),
    (50, 50), (60, 60), (65, 65), (75, 75)
]

# 遊戲設定
FPS = 60
WIDTH, HEIGHT = 600, 600

# 飛船類別
class Player(pygame.sprite.Sprite):
    def __init__(self, shoot_sound):
        super().__init__()
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 30
        self.speedx = 8
        self.shoot_sound = shoot_sound

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        self.shoot_sound.play()

# 子彈類別
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.radius = 5
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# 隕石類別
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = random.choice(ROCK_SIZES)
        self.image_ori = pygame.image.load("images/rock.png").convert_alpha()
        self.image_ori = pygame.transform.scale(self.image_ori, self.size)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 4)
        self.total_degree = 0
        self.rot_degree = random.choice([2, 3, 4])

    def rotate(self):
        self.total_degree = (self.total_degree + self.rot_degree) % 360
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.reset()

    def reset(self):
        self.__init__()

# 顯示遊戲結束畫面（使用中文字型）
def show_game_over_screen(screen, font, score):
    game_over_text = font.render("遊戲結束！", True, BLACK)
    score_text = font.render(f"你的分數：{score}", True, BLACK)
    restart_text = font.render("按 R 鍵重新開始", True, BLACK)
    quit_text = font.render("按 ESC 鍵退出", True, BLACK)

    screen.fill((255, 255, 255))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# 主程式
def main():
    global all_sprites, bullets, rocks

    score = 0
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("飛船射擊遊戲")
    clock = pygame.time.Clock()

    # 使用支援中文的字型檔案
    font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 15)

    pygame.mixer.music.load("sound/background.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
    explosion_sound = pygame.mixer.Sound("sound/explosion.wav")

    background = pygame.image.load("images/background.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    rocks = pygame.sprite.Group()

    player = Player(shoot_sound)
    all_sprites.add(player)

    for i in range(7):
        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    player.shoot()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(rocks, bullets, True, True, pygame.sprite.collide_circle)
        for hit in hits:
            explosion_sound.play()
            score += 10
            new_rock = Rock()
            all_sprites.add(new_rock)
            rocks.add(new_rock)

        player_hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
        if player_hits:
            print("飛船被撞到！遊戲結束")
            show_game_over_screen(screen, font, score)
            main()
            return

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        score_text = font.render(f"分數：{score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("發生錯誤：", e)
    finally:
        pygame.quit()