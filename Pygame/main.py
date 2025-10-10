import pygame
import random

# 遊戲設定
FPS = 60
WIDTH, HEIGHT = 600, 600

# 分數
score = 0

# 飛船類別
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect()
        self.radius = 25  # 圓形碰撞半徑
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 30
        self.speedx = 8

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

# 子彈類別
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect()
        self.radius = 5  # 圓形碰撞半徑
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# 石頭類別
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/rock.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.radius = 15  # 圓形碰撞半徑
        self.reset()

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.reset()

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(2, 5)
        self.speedx = random.randint(-2, 2)

# 主程式
def main():
    global all_sprites, bullets, rocks, score

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("飛船射擊遊戲")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    # 載入背景圖
    background = pygame.image.load("images/background.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # 建立群組
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    rocks = pygame.sprite.Group()

    # 建立玩家
    player = Player()
    all_sprites.add(player)

    # 建立石頭
    for i in range(5):
        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)

    # 主迴圈
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # Z 鍵發射
                    player.shoot()

        # 更新
        all_sprites.update()

        # 子彈打中石頭（圓形碰撞）
        hits = pygame.sprite.groupcollide(rocks, bullets, True, True, pygame.sprite.collide_circle)
        for hit in hits:
            score += 10
            new_rock = Rock()
            all_sprites.add(new_rock)
            rocks.add(new_rock)

        # 飛船撞到石頭 → 結束遊戲（圓形碰撞）
        player_hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
        if player_hits:
            print("飛船被撞到！遊戲結束")
            running = False

        # 畫面顯示
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    pygame.quit()

# 執行主程式
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("發生錯誤：", e)
    finally:
        pygame.quit()