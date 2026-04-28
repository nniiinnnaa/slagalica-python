import pygame as pg
import random
import sys
pg.init()

WIDTH = 1280
HEIGTH = 720

BACKGROUND = (100, 160, 240)

screen = pg.display.set_mode((WIDTH, HEIGTH))
screen.fill(BACKGROUND)
clock = pg.time.Clock()
dt = 0

with open("pitanja.txt", "r", encoding="utf-8") as f:
    content = f.readlines()

def draw():
    global screen, pitanje, odgovori, tacan, content, boje
    screen.fill(BACKGROUND)
    fontTitle = pg.font.SysFont("Arial", 32)
    pg.draw.rect(screen, "white", (0, 100, WIDTH, 50))
    textTitle = fontTitle.render(content[pitanje * 6].strip(), True, "black")
    screen.blit(textTitle, (100, 110))
    pg.draw.rect(screen, "white", (0, 200, WIDTH, 50))
    textTitle = fontTitle.render(odgovori[0], True, "black")
    screen.blit(textTitle, (100, 210))
    pg.draw.rect(screen, "white", (0, 300, WIDTH, 50))
    textTitle = fontTitle.render(odgovori[1], True, "black")
    screen.blit(textTitle, (100, 310))
    pg.draw.rect(screen, "white", (0, 400, WIDTH, 50))
    textTitle = fontTitle.render(odgovori[2], True, "black")
    screen.blit(textTitle, (100, 410))
    pg.draw.rect(screen, "white", (0, 500, WIDTH, 50))
    textTitle = fontTitle.render(odgovori[3], True, "black")
    screen.blit(textTitle, (100, 510))
    pg.draw.rect(screen, "white", (0, 600, WIDTH, 50))
    textTitle = fontTitle.render("Preskoci pitanje", True, "black")
    screen.blit(textTitle, (100, 610))


def koznazna():
    global dt, clock, screen, pitanje, odgovori, tacan, content, boje
    pitanje = random.randint(0, 99)
    iskoriscena = {pitanje}
    odgovori = [content[pitanje * 6 + i].strip() for i in range(1, 5)]
    tacan = random.randint(0, 3)
    if (tacan != 0):
        odgovori[0], odgovori[tacan] = odgovori[tacan], odgovori[0]
    brojpoena = 0
    running = True
    while running:
        draw()
        mouse = {
            "x": pg.mouse.get_pos()[0],
            "y": pg.mouse.get_pos()[1],
            "left": pg.mouse.get_pressed()[0],
            "right": pg.mouse.get_pressed()[2]
        }
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                running = False
            if event.type == pg.MOUSEBUTTONUP:
                x = mouse['x']
                y = mouse['y']
                if mouse['left']:
                    if y <= 200 or 250 <= y <= 300 or 350 <= y <= 400 or 450 <= y <= 500 or 550 <= y <= 600 or y >= 650:
                        continue
                    fontTitle = pg.font.SysFont("Arial", 32)
                    if y < 250:
                        pg.draw.rect(screen, "red", (0, 200, WIDTH, 50))
                        textTitle = fontTitle.render(odgovori[0], True, "black")
                        screen.blit(textTitle, (100, 210))
                        if tacan == 0:
                            brojpoena += 1 #tacan odgovor, prilagoditi broj peona
                        else:
                            brojpoena -= 1 #netacan odgovor, prilagoditi broj poena
                    elif y < 350:
                        pg.draw.rect(screen, "red", (0, 300, WIDTH, 50))
                        textTitle = fontTitle.render(odgovori[1], True, "black")
                        screen.blit(textTitle, (100, 310))
                        if tacan == 1:
                            brojpoena += 1 #tacan odgovor, prilagoditi broj poena
                        else:
                            brojpoena -= 1 #netacan odgovor, prilagoditi broj poena
                    elif y < 450:
                        pg.draw.rect(screen, "red", (0, 400, WIDTH, 50))
                        textTitle = fontTitle.render(odgovori[2], True, "black")
                        screen.blit(textTitle, (100, 410))
                        if tacan == 2:
                            brojpoena += 1 #tacan odgovor, prilagoditi broj poena
                        else:
                            brojpoena -= 1 #netacan odgovor, prilagoditi broj poena
                    elif y < 550:
                        pg.draw.rect(screen, "red", (0, 500, WIDTH, 50))
                        textTitle = fontTitle.render(odgovori[3], True, "black")
                        screen.blit(textTitle, (100, 510))
                        if tacan == 3:
                            brojpoena += 1 #tacan odgovor, prilagoditi broj poena
                        else:
                            brojpoena -= 1 #netacan odgovor, prilagoditi broj poena
                    if tacan == 0:
                        pg.draw.rect(screen, "green", (0, 200, WIDTH, 50))
                        textTitle = fontTitle.render(odgovori[0], True, "black")
                        screen.blit(textTitle, (100, 210))
                    elif tacan == 1:
                        pg.draw.rect(screen, "green", (0, 300, WIDTH, 50))
                        textTitle = fontTitle.render(odgovori[1], True, "black")
                        screen.blit(textTitle, (100, 310))
                    elif tacan == 2:
                        pg.draw.rect(screen, "green", (0, 400, WIDTH, 50))
                        textTitle = fontTitle.render(odgovori[2], True, "black")
                        screen.blit(textTitle, (100, 410))
                    else:
                        pg.draw.rect(screen, "green", (0, 500, WIDTH, 50))
                        textTitle = fontTitle.render(odgovori[3], True, "black")
                        screen.blit(textTitle, (100, 510))
                    pg.display.flip()
                    pg.time.delay(1500)
                    if (len(iskoriscena) >= 10):
                        running = False
                        break
                    while (pitanje in iskoriscena):
                        pitanje = random.randint(0, 99)
                    iskoriscena.add(pitanje)
                    odgovori = [content[pitanje * 6 + i].strip() for i in range(1, 5)]
                    tacan = random.randint(0, 3)
                    if (tacan != 0):
                        odgovori[0], odgovori[tacan] = odgovori[tacan], odgovori[0]
                    
        dt += clock.tick(60) / 1000
        pg.display.flip()
    return brojpoena

if __name__ == '__main__':
    brojpoena = koznazna()
    print(brojpoena)