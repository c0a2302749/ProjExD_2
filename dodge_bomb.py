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
bombs = []
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
    '''
    ゲームオーバー時にだんだん画面を暗くし、最終的にゲームを終了する
    引数: pg.display
    戻り値: なし
    '''
    bg_img = pg.surface.Surface((WIDTH, HEIGHT))
    for alpha in range(0, 129, 5):
        bg_img.set_alpha(alpha)
        pg.draw.rect(bg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))
        pg.display.update()
        time.sleep(0.09)
    bgc_img = pg.image.load("fig/8.png")
    for _ in range(10):
        screen.blit(bgc_img, [random.randint(
            0, WIDTH), random.randint(0, HEIGHT)])
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, [WIDTH // 2 - 200, HEIGHT // 2 - 50])

    pg.display.update()
    time.sleep(5)


def add_bomb():
    '''
    爆弾を追加する,最大20個まで
    bombsのリストに追加する
    引数: なし
    戻り値: なし
    '''
    if len(bombs) > 20:
        return
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    # ランダムな速度を設定
    vx = random.choice([-5, -4, -3, 3, 4, 5])
    vy = random.choice([-5, -4, -3, 3, 4, 5])

    bombs.append((bd_img, bd_rct, vx, vy))

def create_rotated_images(kk_img):
    # 押下キーに対する移動量の合計値タプルをキーとし、rotozoomしたSurfaceを値とする辞書を準備
    r_pg = {
        (0, -5): pg.transform.rotozoom(kk_img, -90, 0.9),   # 上
        (5, -5): pg.transform.rotozoom(kk_img, -135, 0.9),  # 右上
        (5, 0): pg.transform.rotozoom(kk_img, -180, 0.9),   # 右
        (5, 5): pg.transform.rotozoom(kk_img, -225, 0.9),  # 右下
        (0, 5): pg.transform.rotozoom(kk_img, 45, 0.9),  # 下
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 0.9), # 左下
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 0.9), # 左
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 0.9) # 左上
    }
    return r_pg
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.image.load("fig/3.png")
    rotated_images = create_rotated_images(kk_img)
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
        if tmr % 50 == 0:
            add_bomb()

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[5] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[5] += 5
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
        if (tuple(sum_mv)) != (0, 0):
            kk_img = rotated_images[tuple(sum_mv)]

            
        
        screen.blit(kk_img, kk_rct)

        for i, (bd_img, bd_rct, vx, vy) in enumerate(bombs):
            bd_rct.move_ip(vx, vy)
            yoko, tate = check_bound(bd_rct)
            if not yoko:
                bombs[i] = (bd_img, bd_rct, -vx, vy)
            if not tate:
                bombs[i] = (bd_img, bd_rct, vx, -vy)

            screen.blit(bd_img, bd_rct)

            if kk_rct.colliderect(bd_rct):
                print("Game Over")
                return game_over(screen)
        pg.display.update()
        tmr += 5
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
