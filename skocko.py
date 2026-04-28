import pygame as pg
import random
import sys

pg.init()

WIDTH, HEIGHT = 1280, 720
levad = 440 

# boje
pozlevo = (50, 120, 200)
pozdesno = (80, 180, 255)
bela = (255, 255, 255)
crna = (0, 0, 0)
crv = (220, 20, 60)
zuta = (255, 215, 0)

# const
fps = 60
vremel = 90
b = 6
znakv = 80
krugd = znakv // 2
timerd = 30
ivice = 10

# simboli
znakovi = [
    (200, 0, 0), (0, 200, 0), (0, 0, 200),
    (200, 200, 0), (200, 0, 200), (0, 200, 200)
]

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# za dugme mi reko ovo caskanje
bt_font = pg.font.SysFont(None, 48)
bt_txt = bt_font.render('PROVERI', True, crna)

def provera(a, r):
    R = sum(1 for i in range(4) if a[i] == r[i])
    p_r = {s: r.count(s) for s in set(r)}
    p_a = {g: a.count(g) for g in set(a)}
    Y = sum(min(p_r.get(k, 0), p_a.get(k, 0)) for k in p_a) - R
    return R, Y

def draw(prov_rects, p, fidbek, tr_string, s, proteklot, boolic, prikazi):
    screen.fill(pozdesno)
    # levi deo
    pg.draw.rect(screen, pozlevo, (0, 0, levad, HEIGHT))
    
    row_h = znakv + ivice
    
    # redovi
    for i in range(b + 3):
        y = i * row_h
        pg.draw.line(screen, crna, (0, y), (levad, y), 1)

    # userov string
    for r, guess in enumerate(p):
        y = r * row_h + ivice
        for c, idx in enumerate(guess):
            x = ivice + c * (znakv + ivice)
            rect = pg.Rect(x, y, znakv, znakv)
            pg.draw.rect(screen, znakovi[idx], rect)
            pg.draw.rect(screen, crna, rect, 1)

    # trenutni red
    if not boolic and len(p) < b:
        r = len(p)
        y = r * row_h + ivice
        for c, idx in enumerate(tr_string):
            x = ivice + c * (znakv + ivice)
            rect = pg.Rect(x, y, znakv, znakv)
            pg.draw.rect(screen, znakovi[idx], rect)
            pg.draw.rect(screen, crna, rect, 1)

    label = pg.font.SysFont(None, 36).render('Odgovor:', True, crna)
    label_y = b * row_h + ivice
    screen.blit(label, (ivice, label_y))

    # resenje ispod
    sol_y = (b + 1) * row_h + ivice
    for c, idx in enumerate(s):
        x = ivice + c * (znakv + ivice)
        rect = pg.Rect(x, sol_y, znakv, znakv)
        if boolic:
            pg.draw.rect(screen, znakovi[idx], rect)
        pg.draw.rect(screen, crna, rect, 1)

    # timer kutija
    timer_x = levad + ivice
    pg.draw.rect(screen, crna, (timer_x, ivice, timerd + 2, HEIGHT - 2*ivice), 1)
    fill_h = int((proteklot / vremel) * (HEIGHT - 2*ivice))
    pg.draw.rect(screen, bela, (timer_x + 1, HEIGHT - ivice - fill_h, timerd, fill_h))

    # fidbek kutija
    fb_x = timer_x + timerd + ivice + 2
    fb_y = WIDTH - fb_x - ivice
    pg.draw.rect(screen, crna, (fb_x, ivice, fb_y, HEIGHT - 2*ivice), 1)
    for r, fb in enumerate(fidbek):
        y = r * row_h + krugd + ivice
        novix = fb_x + ivice + krugd
        for i in range(fb[0]):
            cx = novix + i*(krugd*2 + ivice)
            pg.draw.circle(screen, crv, (cx, y), krugd)
        for i in range(fb[1]):
            cx = novix + (fb[0]+i)*(krugd*2 + ivice)
            pg.draw.circle(screen, zuta, (cx, y), krugd)

    # simboli dole
    noviy = HEIGHT - znakv - ivice
    prov_rects.clear()
    pg.draw.rect(screen, crna, (fb_x, noviy-ivice, fb_y, znakv + 2*ivice), 1)
    for i, color in enumerate(znakovi):
        x = fb_x + ivice + i*(znakv + ivice)
        rect = pg.Rect(x, noviy, znakv, znakv)
        prov_rects.append(rect)
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, crna, rect, 1)
        if rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(screen, bela, rect, 3)

    # proveri dugme
    px = bt_txt.get_width() + ivice*2
    py = bt_txt.get_height() + ivice
    prov_rect = pg.Rect(fb_x + fb_y - px - ivice, noviy, px, py)
    pg.draw.rect(screen, bela, prov_rect)
    pg.draw.rect(screen, crna, prov_rect, 2)
    screen.blit(bt_txt, bt_txt.get_rect(center=prov_rect.center))

    # poruka na kraju
    if boolic:
        por = pg.font.SysFont(None, 48).render(prikazi, True, crna)
        mx = fb_x + fb_y//2 - por.get_width()//2
        my = HEIGHT//2 - por.get_height()//2
        screen.blit(por, (mx, my))

    pg.display.flip()

def skocko():
    prov_rects = []
    p = []
    fidbek = []
    tr_string = []
    s = [random.randint(0,5) for _ in range(4)]
    proteklot = 0
    boolic = False
    prikazi = ''

    start_ticks = pg.time.get_ticks()
    running = True
    while running:
        dt = clock.tick(fps)/1000
        if not boolic:
            proteklot = (pg.time.get_ticks() - start_ticks)/1000
            if proteklot >= vremel:
                boolic = True
                prikazi = 'Kabum'

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                running = False
            if event.type == pg.KEYDOWN and not boolic and event.key == pg.K_BACKSPACE and tr_string:
                tr_string.pop()
            if event.type == pg.MOUSEBUTTONDOWN and not boolic:
                x,y = event.pos
                for i,rect in enumerate(prov_rects):
                    if rect.collidepoint(x,y) and len(tr_string) < 4:
                        tr_string.append(i)

                timer_x = levad + ivice
                fb_x = timer_x + timerd + ivice + 2
                fb_y = WIDTH - fb_x - ivice
                px = bt_txt.get_width() + ivice*2
                py = bt_txt.get_height() + ivice
                prov_rect = pg.Rect(fb_x + fb_y - px - ivice, HEIGHT - znakv - ivice, px, py)
                if prov_rect.collidepoint(x,y) and len(tr_string) == 4:
                    R,Y = provera(tr_string, s)
                    fidbek.append((R,Y))
                    p.append(tr_string.copy())
                    if R==4:
                        boolic = True
                        prikazi = 'pobeda'
                        pg.time.delay(1500)
                        running = False
                        break
                    elif len(p)>=b:
                        boolic = True
                        prikazi = 'STIDI SE'
                        pg.time.delay(1500)
                        running = False
                        break
                    tr_string.clear()
                    

        draw(prov_rects, p, fidbek, tr_string, s, proteklot, boolic, prikazi)

    return 100 if fidbek and fidbek[-1][0]==4 else 0

if __name__ == '__main__':
    score = skocko()
    print(score)
    pg.quit()
    sys.exit()