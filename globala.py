import pygame as pg
pg.init()

WIDTH = 1280
HEIGTH = 720
GAMES = ("Moj Broj", "Skočko", "Slagalica", "Asocijacije", "Spojnice", "Ko zna zna")
NAMES = ("mojbroj", "skocko", "slagalica", "asocijacije", "Spojnice", "koznazna")
BACKGROUND = (100, 160, 240)

screen = pg.display.set_mode((WIDTH, HEIGTH))
screen.fill(BACKGROUND)

radi = 1

def stop():
    global radi
    radi = 0
