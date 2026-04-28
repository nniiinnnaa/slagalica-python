import pygame as pg
import globala
import sys
screen = globala.screen
BACKGROUND = globala.BACKGROUND
WIDTH = globala.WIDTH
HEIGTH = globala.HEIGTH
GAMES = globala.GAMES
dt = 0
clock = pg.time.Clock()


BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60
BUTTON_MARGIN = 20
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 180, 220)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_PLAYED = (180, 180, 180) 

font = pg.font.SysFont(None, 40)
played_games = [False] * len(GAMES)

def get_buttons():
    buttons = []
    total_height = len(GAMES) * BUTTON_HEIGHT + (len(GAMES) - 1) * BUTTON_MARGIN
    start_y = (HEIGTH - total_height) // 2
    for i, game in enumerate(GAMES):
        rect = pg.Rect(
            (WIDTH - BUTTON_WIDTH) // 2,
            start_y + i * (BUTTON_HEIGHT + BUTTON_MARGIN),
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        buttons.append((rect, game))
    return buttons

def draw(played_games):
    global screen
    screen.fill(BACKGROUND)
    mouse_pos = pg.mouse.get_pos()
    for idx, (rect, label) in enumerate(get_buttons()):
        if played_games[idx]:
            color = BUTTON_PLAYED
        else:
            color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pg.draw.rect(screen, color, rect, border_radius=10)
        text = font.render(label, True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def Start():
    global dt, clock, screen, played_games
    running = True
    
    while not all(played_games) and running:
        draw(played_games)
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
                sys.exit()
                break
            if event.type == pg.MOUSEBUTTONUP:
                if mouse['left']:
                    for idx, (rect, game) in enumerate(get_buttons()):
                        if rect.collidepoint(mouse["x"], mouse["y"]) and not played_games[idx]:
                            played_games[idx] = True  
                            return idx
        dt += clock.tick(60) / 1000
        if running:
            pg.display.flip()
    return -1 

#ovde ne pisite nista, treba mi gotova funkcija koja ce da vraca broj poena
if __name__ == '__main__':
    Start()