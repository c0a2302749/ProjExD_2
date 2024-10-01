import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    '''
    引数:こうかとん, 爆弾のrect
    戻り値: 真理値タプル(横判定, 縦判定)
    画面内ならTrue, 画面外ならFalse
    '''
    yoko, tate = True, True
    if obj_rct.left < 0 or obj_rct.right > WIDTH:
        yoko = False
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
        tate = False
    return yoko, tate


def game_over(screen: pg.display) -> None:
    bg_img = pg.surface.Surface((WIDTH, HEIGHT))
    for alpha in range(0, 129, 5):
        bg_img.set_alpha(alpha)
        pg.draw.rect(bg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))
        pg.display.update()
        time.sleep(0.1)
    bgc_img = pg.image.load("fig/8.png")
    for _ in range(10):
        screen.blit(bgc_img, [random.randint(
            0, WIDTH), random.randint(0, HEIGHT)])
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, [WIDTH // 2 - 200, HEIGHT // 2 - 50])

    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bd_img = pg.surface.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5
    clock = pg.time.Clock()
    tmr = 0
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        # kk_rct.move_ip(sum_mv)
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bd_img, bd_rct)
        if kk_rct.colliderect(bd_rct):
            print("Game Over")
            return game_over(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
