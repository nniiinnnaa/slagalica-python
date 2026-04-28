import template
import template2
import start
import pygame as pg
import globala
import importlib
import sys
from network import NetworkClient

radi = globala.radi
clock = pg.time.Clock()
broj_poena = 0
odigrano = 0
NAMES = globala.NAMES

net = NetworkClient(sys.argv[1], int(sys.argv[2])) 

while odigrano < len(NAMES) and radi:
    idx = start.Start() 
    if idx < 0:
        continue
    game_name = NAMES[idx]
    module = importlib.import_module(game_name)
    func = getattr(module, game_name)
    score = func()
    broj_poena += score
    net.send_score(score)
    other_score = net.try_receive_score()  # This will NOT block
    print(f"Your score: {score}, Opponent's score: {other_score}")
    odigrano += 1
    radi = globala.radi

net.close()
