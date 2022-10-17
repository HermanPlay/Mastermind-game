import pygame
import os


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w = self.game.DISPLAY_W / 2
        self.mid_h = self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -180
        self.height = 20
    
    def draw_cursor(self):
        self.game.draw_text('*', 50, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    
class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'Start'
        self.startx = self.mid_w
        self.starty = self.mid_h + 30
        self.resultsx = self.mid_w 
        self.resultsy = self.mid_h + 140
        self.optionsx = self.mid_w
        self.optionsy = self.mid_h + 85
        self.quitx = self.mid_w
        self.quity = self.mid_h + 195 
        self.cursor_rect.midtop = (self.startx+self.offset, self.starty+self.height)
    
    def display_menu(self):
        self.run_display = True
        
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.game.BG, (0, 0))
            self.game.draw_text('Mastermind', 80, self.game.DISPLAY_W/2, self.game.DISPLAY_H/4)
            self.game.draw_text('Start game', 50, self.startx, self.starty)
            self.game.draw_text('Options', 50, self.optionsx, self.optionsy)
            self.game.draw_text('Results', 50, self.resultsx, self.resultsy)
            self.game.draw_text('Quit', 50, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()
 
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx+self.offset, self.optionsy+self.height)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.resultsx+self.offset, self.resultsy+self.height)
                self.state = 'Results'
            elif self.state == 'Results':
                self.cursor_rect.midtop = (self.quitx+self.offset, self.quity+self.height)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx+self.offset, self.starty+self.height)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx+self.offset, self.quity+self.height)
                self.state = 'Quit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx+self.offset, self.starty+self.height)
                self.state = 'Start'
            elif self.state == 'Results':
                self.state = 'Options'
                self.cursor_rect.midtop = (self.optionsx+self.offset, self.optionsy+self.height)
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.resultsx+self.offset, self.resultsy+self.height)
                self.state = 'Results'
    
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.run_display = False
            elif self.state == 'Options':
                self.run_display = False
                self.game.curr_menu = self.game.options_menu
            elif self.state == 'Results':
                self.run_display = False
                self.game.curr_menu = self.game.results_menu
            elif self.state == 'Quit':
                self.game.running = False
                self.game.playing = False
                self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'Volume'
        self.time_limit = True

        self.volumex = self.mid_w
        self.volumey = self.mid_h + 30
        self.time_limitx = self.mid_w
        self.time_limity = self.mid_h + 90

        self.cursor_rect.midtop = (self.volumex+self.offset, self.volumey+self.height)

    def display_menu(self):
        self.run_display = True
        
        while self.run_display:
            self.game.check_events()
            self.check_input()
            if self.time_limit:
                fstring = 'On'
            else:
                fstring = 'Off'
            self.game.display.blit(self.game.BG, (0,0))
            self.game.draw_text('Volume', 50, self.volumex, self.volumey)
            self.game.draw_text(f'Time limit: {fstring}', 50, self.time_limitx, self.time_limity)
            self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == 'Volume':
                self.cursor_rect.midtop = (self.time_limitx+self.offset, self.time_limity+self.height)
                self.state = 'Time limit'
            elif self.state == 'Time limit':
                self.cursor_rect.midtop = (self.volumex+self.offset, self.volumey+self.height)
                self.state = 'Volume'
        elif self.game.BACK_KEY or self.game.ESC_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            if self.state == 'Time limit':
                if self.time_limit:
                    self.time_limit = False
                else:
                    self.time_limit = True
            elif self.state == 'Volume':
                self.run_display = False
                self.game.curr_menu = self.game.volume_menu
        

class VolumeMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.volume = 10
        self.volumex = self.game.DISPLAY_W / 2
        self.volumey = self.game.DISPLAY_H / 2

    def display_menu(self):
        self.run_display = True
        self.game.MUSIC.set_volume(0.0)
        
        while self.run_display:
            self.game.MUSIC.set_volume(float(self.volume/10))
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.game.BG, (0,0))
            self.game.draw_text(f'Volume: {self.volume}', 50, self.volumex, self.volumey)
            self.blit_screen()

    def check_input(self):
        if self.game.UP_KEY:
            if self.volume < 10:
                self.volume += 1
        elif self.game.DOWN_KEY:
            if self.volume > 0:
                self.volume -= 1
        elif self.game.BACK_KEY or self.game.ESC_KEY:
            self.game.curr_menu = self.game.options_menu
            self.run_display = False

class ResultsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.resultx = self.game.DISPLAY_W / 2
        temp = self.game.DISPLAY_H * 0.4
        self.coords = [temp, temp+50, temp+100, temp+150, temp+200, temp+250]

    def display_menu(self):
        self.run_display = True
        
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.game.BG, (0,0))
            path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'results.txt') 
            with open(path, 'r') as file:
                file = file.read().split('\n')
                for i in range(6):
                    if i == 0:
                        info = 'Best result: ' + file[i]
                    else:
                        try:
                            info = file[i]
                        except IndexError:
                            info = ''
                    self.game.draw_text(info, 40, self.resultx, self.coords[i])
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESC_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
