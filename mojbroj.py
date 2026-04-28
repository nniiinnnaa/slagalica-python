import pygame
import sys
import globala
from mojbrojlogic import GameLogic
from mojbrojui import GameUI
import time

def mojbroj():
    pygame.init()
    screen = pygame.display.set_mode((globala.WIDTH, globala.HEIGTH))
    pygame.display.set_caption("Moj Broj")
    
    clock = pygame.time.Clock()
    game_logic = GameLogic()
    game_ui = GameUI(globala.WIDTH, globala.HEIGTH)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_logic.pick_next_number()
            game_ui.handle_event(event, game_logic)

        game_logic.update()
        game_ui.render(game_logic)

        # Kada istekne drugi tajmer, prekini igru i vrati poene
        if game_logic.second_timer_active and game_logic.second_timer_start is not None:
            if time.time() - game_logic.second_timer_start >= game_logic.second_timer_duration:
                points = game_logic.calculate_points()
                return points

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    rezultat = mojbroj()
    print(rezultat)