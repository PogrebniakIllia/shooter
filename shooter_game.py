from pygame import *
from random import randint


window = display.set_mode((700,500))
display.set_caption("Шутер")

background = transform.scale(image.load("galaxy.jpg"),(700,500))
clock = time.Clock()
FPS = 60
font.init()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, haight, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width,haight))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.darection = ""
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

lost = 0
score = 0

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 615:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.centery, 10, 40, 100)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        global score
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80,620)
            lost = lost + 1
            print (lost)
        if sprite.spritecollide(self,bullets, True):
            score += 1
            self.rect.y = 0
            self.rect.x = randint(80, 620)

class Label:
    def set_text(self, text, fsize = 12, text_color = (0, 0, 0)):
        self.image = font.SysFont("verdana", fsize).render(text, True, text_color)

    def draw(self, shift_x = 0, shift_y = 0):
        window.blit(self.image, (shift_x,shift_y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

sound_fire = mixer.Sound('fire.ogg')

player = Player("rocket.png", 300, 400, 65, 65, 8)
#enemy = Enemy("ufo.png", randint(80,620), 0, 80, 50, randint(1,7))
enemies = sprite.Group()
for i in range(1, 6):
    enemy = Enemy("ufo.png", randint(80,620), 0, 80, 50, randint(1,7))    
    enemies.add(enemy)

bullets = sprite.Group()
lost_text=Label()
win_text=Label()
# win = font.render("YOU WIN!", True, (255, 215, 0))

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False  
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                sound_fire.play()
    if finish!= True:
        window.blit(background, (0, 0))
        enemies.update()
        player.update()
        bullets.update()
        enemies.draw(window)
        player.reset()
        bullets.draw(window)
        lost_text.set_text("Пропущено: " + str(lost), 20, (255, 255, 255))
        lost_text.draw(10, 10)
        win_text.set_text("Збито: " + str(score), 20, (255, 255, 255))
        win_text.draw(10, 40)
        #sprite.groupcollide(enemies, bullets, False, True)
    
    
        if sprite.spritecollide(player, enemies, False) or lost >= 10:
            loss = Label()
            loss.set_text("YOU LOSE!", 60, (255, 0, 0))
            window.blit(background, (0, 0))
            loss.draw(200, 200)
            finish =True
        if score >= 10:
            win = Label()
            win.set_text("YOU WIN!", 60, (255, 255, 0))
            window.blit(background, (0, 0))
            win.draw(200, 200)
            finish = True

    clock.tick(FPS)
    display.update()
