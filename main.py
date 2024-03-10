from pygame import *

# Initialize Pygame
init()
win_width , win_height = 700 , 500

# Create window
window = display.set_mode((win_width,win_height))
display.set_caption('labyrunth')
back = (230, 191, 76)
barriers = sprite.Group()
bullets = sprite.Group()
monster = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,size_x,size_y):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,pl_x_speed,pl_y_speed):
        GameSprite.__init__(self,player_image,player_x,player_y,size_x,size_y)
        self.x_speed = pl_x_speed
        self.y_speed = pl_y_speed

    def fire(self):
        bullet = Bullet('image/bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullet.add(bullets)


    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right,p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,
                                     p.rect.right)  # если коснулись нескольких стен, то левый край - максимальный
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # идем вниз
            for p in platforms_touched:
                self.y_speed = 0
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:  # идем вверх
            for p in platforms_touched:
                self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
                self.rect.top = max(self.rect.top,
                                    p.rect.bottom)
        def fire(self):
            bullet = Bullet('image/bullet.png',self.rect.right,self,rect.centery,15,20,15)
            bullet.add(bullets)

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed


    def update(self):
        self.rect.x +=self.speed
        if self.rect.x > win_width + 10:
            self.kill()

class Enemy(GameSprite):
    side = 'left'

    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        GameSprite.__init__(self,player_image,player_x,player_y,size_x,size_y)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed




w1 = GameSprite('image/wall.png',win_width/2-win_height/3,win_height/2,230,50)
w2 = GameSprite('image/wall.png',370,100,50,400)
#main charter
packman = Player('image/hero.png',5,win_height-80,80,80,0,0)

barriers.add(w1)
barriers.add(w2)
final_sprite = GameSprite('image/zalojnik.png',win_height-85,win_height-100,80,80)
monster1 = Enemy('image/zlodei.png',win_width-80,150,80,80,5)
monster2 = Enemy('image/zlodei.png',win_width-80,230,80,80,5)
monster.add(monster1)
monster.add(monster2)
finish = False
win = False
# Main game loop
running = True
game_over = False
win_condition_met = False

while running:
    if not win:
        time.delay(50)
        for e in event.get():
            if e.type == QUIT:
                running = False
            elif e.type == KEYDOWN:
                if e.key == K_LEFT:
                    packman.x_speed = -5
                elif e.key == K_RIGHT:
                    packman.x_speed = +5
                elif e.key == K_UP:
                    packman.y_speed = -5
                elif e.key == K_DOWN:
                    packman.y_speed = +5
                elif e.key == K_SPACE:
                    packman.fire()
            elif e.type == KEYUP:
                if e.key == K_LEFT:
                    packman.x_speed = 0
                elif e.key == K_RIGHT:
                    packman.x_speed = 0
                elif e.key == K_UP:
                    packman.y_speed = 0
                elif e.key == K_DOWN:
                    packman.y_speed = 0
        if not finish and not game_over and not win_condition_met:
            window.fill(back)
            packman.update()
            monster1.update()
            monster2.update()
            bullets.update()

            barriers.draw(window)
            bullets.draw(window)
            monster.draw(window)
            packman.reset()
            final_sprite.reset()
            collisions_wall = sprite.groupcollide(bullets, barriers, True, False)
            collisions = sprite.groupcollide(bullets, monster, True, True)

            if sprite.spritecollide(packman, monster, False):
                game_over = True
                img_game_over = image.load('image/game_over.png')
                window.fill((255, 255, 255))
                window.blit(transform.scale(img_game_over, (win_width, win_height)), (0, 0))
                monster1 = Enemy('image/zlodei.png', win_width - 80, 150, 80, 80, 0)
                monster2 = Enemy('image/zlodei.png', win_width - 80, 230, 80, 80, 0)

            if packman.rect.colliderect(final_sprite.rect):
                win_condition_met = True
                img_win = image.load('image/win.jpg')
                window.fill((255, 255, 255))
                window.blit(transform.scale(img_win, (win_width, win_height)), (0, 0))

        display.update()

quit()
