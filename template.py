import globala
import pygame as pg

screen = globala.screen
BACKGROUND = globala.BACKGROUND
WIDTH = globala.WIDTH
HEIGTH = globala.HEIGTH
dt = 0
clock = pg.time.Clock()

def draw():
    global screen
    screen.fill(BACKGROUND)
    #Komande koje vam crtaj sve na ekranu idu ovde
    #Uvek crtate ceo ekran, ako crtate deo ekrana (sto nikako ne preporucujem) sklonite screen.fill(BACKGROUND)
    pass


def template():
    #Ako nesto menjate od globalnih promenljivih, samo ih "deklarisite" ovako na pocetku fje
    global dt, clock, screen
    brojpoena = 2
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
                running = False
                globala.stop()
                pg.quit()
                break
            if event.type == pg.MOUSEBUTTONUP:
                x = mouse['x']
                y = mouse['y']
                if mouse['left']:
                    #Ove komande se dese na levi klik misa, kordinate na kojima je pokazivac misa su x,y
                    pass
                elif mouse['right']:
                    #Ove komande se dese na desni klik
                    pass
        
        dt += clock.tick(60) / 1000
        if running:
            pg.display.flip()
    return brojpoena

#ovde ne pisite nista, treba mi gotova funkcija koja ce da vraca broj poena
if __name__ == '__main__':
    brojpoena = template()
    print(brojpoena)