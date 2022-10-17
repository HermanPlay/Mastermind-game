import pygame
from game import Game
import os


def main():
    g = Game()
    path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'results.txt') 
    try:
        file = open(path, 'x')
        file.close()
    except FileExistsError:
        pass
    while g.running:
        g.display = pygame.Surface((g.DISPLAY_W, g.DISPLAY_H))
        g.window = pygame.display.set_mode(((g.DISPLAY_W, g.DISPLAY_H)))
        g.curr_menu.display_menu()
        print('skonczylem wyswietlac menu')
        g.game_loop()
    
    
if __name__ == "__main__":
    main()
