import pygame as pg
import random
import time
import globala
import sys

pg.init()

WIDTH = 1280
HEIGHT = 720
BACKGROUND = (100, 160, 240)

screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(BACKGROUND)
clock = pg.time.Clock()
dt = 0

font = pg.font.SysFont(None, 30)

leva_kolona = []
desna_kolona = []
stanja_levih = {}
stanja_desnih = {}
levi_rects = []
desni_rects = []
povezani_parovi = []
poeni = 0
prvi_klik = None
spojnice = {}
start_time = 0
trajanje = 60

def draw():
    global screen
    screen.fill(BACKGROUND)

    vreme_proslo = int(time.time() - start_time)
    vreme_preostalo = max(0, trajanje - vreme_proslo)
    tajmer_tekst = font.render(f"Vreme: {vreme_preostalo}s", True, (255, 0, 0))
    screen.blit(tajmer_tekst, (WIDTH - 150, 20))

    naslov = font.render("Spojnice", True, (0, 0, 0))
    screen.blit(naslov, (WIDTH // 2 - naslov.get_width() // 2, 20))

    for rect, pojam in levi_rects:
        stanje = stanja_levih[pojam]
        boja = (200, 200, 255)
        if stanje == "zeleno":
            boja = (144, 238, 144)
        elif stanje == "crveno":
            boja = (255, 99, 71)
        pg.draw.rect(screen, boja, rect)
        pg.draw.rect(screen, (0, 0, 0), rect, 2)
        text = font.render(pojam, True, (0, 0, 0))
        screen.blit(text, (rect.x + 10, rect.y + 5))

    for rect, pojam in desni_rects:
        stanje = stanja_desnih[pojam]
        boja = (200, 255, 200)
        if stanje == "zeleno":
            boja = (144, 238, 144)
        pg.draw.rect(screen, boja, rect)
        pg.draw.rect(screen, (0, 0, 0), rect, 2)
        text = font.render(pojam, True, (0, 0, 0))
        screen.blit(text, (rect.x + 10, rect.y + 5))

    for p_levo, p_desno in povezani_parovi:
        r1 = next(r for r, p in levi_rects if p == p_levo)
        r2 = next(r for r, p in desni_rects if p == p_desno)
        pg.draw.line(screen, (0, 0, 0), r1.midright, r2.midleft, 2)

def Spojnice():
    global dt, clock, screen
    global leva_kolona, desna_kolona, stanja_levih, stanja_desnih
    global levi_rects, desni_rects, povezani_parovi, poeni, prvi_klik
    global spojnice, start_time

    svi_setovi = [
        {"Adis Abeba": "Etiopija", "Aman": "Jordan", "Akra": "Gana", "Adana": "Turska", "Antananarivo" : "Madagaskar", "Adelajd" : "Australija"},
        {"C2H2": "Acetilen", "C6H12": "Cikloheksan", "C6H12O6": "Fruktoza", "CH3OH": "Metanol", "C10H22" : "Dekan", "C2H5OH" : "Etanol"},
        {"Ivana Španović": "Atletika", "Ivan Lenđer": "Plivanje", "Neven Subotić": "Fudbal", "Marko Vujin": "Rukomet", "Milena Rašić" : "Odbojka", "Miloš Teodosić" : "Košarka"},
        {"Plazma": "Bambi", "Cica Maca": "Pionir", "Najlepše želje": "Štark", "Domaćica": "Banini", "Banat čokolada" : "Swisslion", "Munchmallow" : "Jaffa"},
        {"Srna": "Lane", "Koza": "Jare", "Ovca": "Jagnje", "Kobila": "Ždrebe", "Košuta" : "Tele", "Ćurka" : "Ćurče"},
        {"Gain": "Eager", "Mike": "Oxlong", "Nick": "Gurh", "Dixie": "Normus", "Gabe" : "Itch", "Hugh" : "Jass"}
    ]

    spojnice = random.choice(svi_setovi)
    leva_kolona = list(spojnice.keys())
    desna_kolona = list(spojnice.values())
    random.shuffle(desna_kolona)

    spacing = 80
    start_y = 150
    levi_rects = []
    desni_rects = []
    stanja_levih = {}
    stanja_desnih = {}
    povezani_parovi = []
    poeni = 0
    prvi_klik = None

    for i, pojam in enumerate(leva_kolona):
        rect = pg.Rect(100, start_y + i * spacing, 300, 50)
        levi_rects.append((rect, pojam))
        stanja_levih[pojam] = "nekliknuto"

    for i, pojam in enumerate(desna_kolona):
        rect = pg.Rect(WIDTH - 400, start_y + i * spacing, 300, 50)
        desni_rects.append((rect, pojam))
        stanja_desnih[pojam] = "nekliknuto"

    start_time = time.time()
    running = True
    prikazi_rezultate = False

    while running:
        draw()
        mouse = {
            "x": pg.mouse.get_pos()[0],
            "y": pg.mouse.get_pos()[1],
            "left": pg.mouse.get_pressed()[0],
            "right": pg.mouse.get_pressed()[2]
        }

        vreme_proslo = int(time.time() - start_time)
        if vreme_proslo >= trajanje or all(stanja_levih[p] != "nekliknuto" for p in leva_kolona):
            prikazi_rezultate = True
            running = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                globala.stop()
                pg.quit()   
                sys.exit()
                return poeni
            if event.type == pg.MOUSEBUTTONUP:
                x, y = mouse['x'], mouse['y']
                if mouse['left']:
                    if not prvi_klik:
                        for rect, pojam in levi_rects:
                            if rect.collidepoint((x, y)) and stanja_levih[pojam] == "nekliknuto":
                                prvi_klik = pojam
                                break
                    else:
                        for rect, pojam_d in desni_rects:
                            if rect.collidepoint((x, y)) and stanja_desnih[pojam_d] != "zeleno":
                                pojam_l = prvi_klik
                                tacan = spojnice.get(pojam_l) == pojam_d
                                if tacan:
                                    stanja_levih[pojam_l] = "zeleno"
                                    stanja_desnih[pojam_d] = "zeleno"
                                    povezani_parovi.append((pojam_l, pojam_d))
                                    poeni += 2
                                else:
                                    stanja_levih[pojam_l] = "crveno"
                                prvi_klik = None
                                break

        dt += clock.tick(60) / 1000
        pg.display.flip()

    prikaz = True
    while prikaz:
        screen.fill(BACKGROUND)
        kraj = font.render("Klikni bilo gde da nastaviš", True, (0, 0, 0))
        screen.blit(kraj, (WIDTH // 2 - kraj.get_width() // 2, 40))
        for i, (levo, desno) in enumerate(spojnice.items()):
            tekst = font.render(f"{levo} - {desno}", True, (0, 0, 0))
            screen.blit(tekst, (WIDTH // 2 - 150, 100 + i * 50))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                globala.stop()
                pg.quit()   
                return poeni
            if event.type == pg.MOUSEBUTTONDOWN:
                prikaz = False

    return poeni

if __name__ == '__main__':
    brojpoena = Spojnice()
    print(brojpoena)
