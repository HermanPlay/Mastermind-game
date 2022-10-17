import pygame
import os
import random
from menu import MainMenu, OptionsMenu, VolumeMenu, ResultsMenu
import tkinter
import collections


class Game:
    def __init__(self):

        root = tkinter.Tk()
        self.MONITOR_W = root.winfo_screenwidth()
        self.MONITOR_H = root.winfo_screenheight()
        self.DISPLAY_W = 1280
        self.DISPLAY_H = 720

        self.x = (self.MONITOR_W - self.DISPLAY_W) / 2
        self.y = 35
        self.running = True
        self.playing = False

        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.ESC_KEY = False

        self.GAME_W = 500
        self.GAME_H = 900

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.x, self.y)

        pygame.init()
        pygame.display.set_caption('Mastermind')
        self.ROOT = os.path.dirname(__file__)
        self.PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'results.txt') 

        self.font = os.path.join(self.ROOT, 'assets', 'fonts', 'TamanKanak.otf')

        # Init images

        self.BG = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'bg.jpg'))
        self.BG = pygame.transform.scale(self.BG, (self.DISPLAY_W, self.DISPLAY_H))

        self.BG_GAME = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'bg.jpg'))
        self.BG_GAME = pygame.transform.scale(self.BG_GAME, (self.GAME_W, self.GAME_H))

        self.RED_BALL = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'red_ball.png')), (60, 60))
        self.BLUE_BALL = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'blue_ball.png')), (60, 60))
        self.PINK_BALL = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'pink_ball.png')), (60, 60))
        self.ORANGE_BALL = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'orange_ball.png')), (60, 60))
        self.YELLOW_BALL = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'yellow_ball.png')), (60, 60))
        self.GREY_BALL = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'grey_ball.png')), (60, 60))
        self.BLACK_BALL = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'black_ball.png')),(60, 60))
        self.GREEN_BALL = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'green_ball.png')), (60, 60))
        self.WHITE_CORRECT = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'white_correct.png'))
        self.BLACK_CORRECT = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'black_correct.png'))

        self.TRY_IMAGE = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'try_button.png'))
        self.BOARD_IMAGE = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'board.png'))
        self.INPUT_IMAGE = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'input_box.png'))
        self.HINT_IMAGE = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'hint.png'))
        self.MENU_IMAGE = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'menu.png'))
        self.ICON = pygame.image.load(os.path.join(self.ROOT, 'assets', 'images', 'logo.png'))
        pygame.display.set_icon(self.ICON)

        # Music

        self.MUSIC = pygame.mixer.Sound(os.path.join(self.ROOT, 'assets', 'music', 'amogus.wav'))

        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))

        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))

        self.WHITE = (255, 255, 255)

        self.balls_y_1 = self.GAME_H * 0.85
        self.balls_y_2 = self.GAME_H * 0.85 + 65
        self.balls_x = 50

        self.coords = {0: (self.balls_x, self.balls_y_1), 1: (self.balls_x+65, self.balls_y_1), 2: (self.balls_x+130, self.balls_y_1), 3: (self.balls_x+195, self.balls_y_1), 
        4: (self.balls_x, self.balls_y_2), 5: (self.balls_x+65, self.balls_y_2), 6: (self.balls_x+130, self.balls_y_2), 7: (self.balls_x+195, self.balls_y_2)}

        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.volume_menu = VolumeMenu(self)
        self.results_menu = ResultsMenu(self)
        self.curr_menu = self.main_menu

        self.clock = pygame.time.Clock()

        self.try_buttonx = 335
        self.try_buttony = self.GAME_H * 0.75
        self.inputx = 149
        self.boardy = self.GAME_H * 0.355
        temp = self.GAME_H*0.66
        self.board_places_y = [temp, temp-61, temp-122, temp-183, temp-244, temp-305, temp-366, temp-427, temp-488, temp-549]
        self.wonx = 149
        self.wony = self.GAME_H * 0.76
        self.losey = self.GAME_H * 0.92
        self.lose_coords = (self.balls_x, self.balls_x+65, self.balls_x+130, self.balls_x+195)
        self.hintx = 439
        temp = 310
        self.correctx = [temp, temp+55, temp+110, temp+165]
        temp = self.GAME_H * 0.66
        self.correcty = [temp, temp-61, temp-122, temp-183, temp-244, temp-305, temp-366, temp-427, temp-488, temp-549]

        self.input_board_coords = (self.balls_x, self.try_buttony)
        self.win = False

    def game_loop(self):
        self.code = []

        while len(self.code) != 4:
            choice = random.choice([self.RED_BALL, self.BLUE_BALL, self.PINK_BALL, self.ORANGE_BALL, self.YELLOW_BALL, self.GREY_BALL, self.BLACK_BALL, self.GREEN_BALL])
            if choice in self.code:
                continue
            else:
                self.code.append(choice)
        self.hint = random.choice(self.code)
        self.hint_index = self.code.index(self.hint)

        self.display = pygame.Surface((self.GAME_W, self.GAME_H))
        self.window = pygame.display.set_mode(((self.GAME_W, self.GAME_H)))
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        self.score = 1000
        self.start_time = pygame.time.get_ticks()
        self.limit = 300000
        self.input_box = {}
        self.correct = {}
        self.input_place = 0
        self.board_place = 0
        self.board = {}
        self.win = False
        self.lose = False
        self.tries = 0
        self.MUSIC.play()
        self.MUSIC.set_volume(0.0)
        self.miliseconds = 1
        
        while self.playing:
            self.check_events()
            self.sprites = []
            self.input_sprites = []

            if self.ESC_KEY:
                self.playing = False

            if not self.options_menu.time_limit:
                if not self.win:
                    try:
                        self.minutes = self.miliseconds // 60000
                        if self.minutes < 60:
                            self.miliseconds = pygame.time.get_ticks() - self.start_time
                    except AttributeError:
                        self.miliseconds = pygame.time.get_ticks() - self.start_time
            else:
                if not self.win:
                    self.miliseconds = self.limit - (pygame.time.get_ticks() - self.start_time)
            
            if self.miliseconds > 0:
                self.seconds = self.miliseconds // 1000
                self.minutes = self.seconds // 60
                if self.seconds > 59:
                    self.seconds -= self.minutes * 60
                if self.minutes < 10:
                    self.minutes = '0' + str(self.minutes)
                if self.seconds < 10:
                    self.seconds = '0' + str(self.seconds)
                self.time = f'{self.minutes}:{self.seconds}'
                self.minutes = int(self.minutes)
                self.seconds = int(self.seconds)
            elif self.options_menu.time_limit:
                self.win = True
                self.lose = True
            
            # Displaying images 
            
            self.display.blit(self.BG_GAME, (0, 0))
            if not self.win:
                self.add = True
                for index, image in enumerate([self.RED_BALL, self.BLUE_BALL, self.PINK_BALL, self.ORANGE_BALL, self.YELLOW_BALL, self.GREY_BALL, self.BLACK_BALL, self.GREEN_BALL]):
                    self.draw_sprites(image, self.coords[index][0], self.coords[index][1])
                self.draw_sprites(self.TRY_IMAGE, self.try_buttonx, self.try_buttony)
                self.draw_sprites(self.HINT_IMAGE, self.hintx, self.try_buttony)
                self.add = False
                for place, image in self.input_box.items():
                    self.draw_in_input(image, place)
                self.draw_sprites(self.INPUT_IMAGE, 149, self.try_buttony)

            elif self.lose:
                for index, image in enumerate(self.code):
                    self.draw_sprites(image, self.lose_coords[index], self.losey)
                self.draw_text('You lost!', 40, self.wonx, self.wony)
                self.draw_sprites(self.MENU_IMAGE, self.wonx, self.wony+75)

            else:
                self.draw_text('You won!', 40, self.wonx, self.wony)
                self.draw_sprites(self.MENU_IMAGE, self.wonx, self.wony+75)
            if self.options_menu.time_limit:
                self.time_text = self.draw_text('Time: ', 40, self.balls_x+300, self.balls_y_1)
                self.passed_time_text = self.draw_text(self.time, 40, self.balls_x+400, self.balls_y_1+5)
                self.score_text = self.draw_text('Score: ', 40, self.balls_x+300, self.balls_y_2)
                self.curr_score_text = self.draw_text(str(self.score), 40, self.balls_x+400, self.balls_y_2+5)
            self.draw_sprites(self.BOARD_IMAGE, self.inputx, self.boardy)
            for place in self.board:
               for index, image in enumerate(self.board[place]):
                   self.draw_sprites(image, self.input_board_coords[0]+(index*65), self.board_places_y[place])

            for place in self.correct:
                for index, image in enumerate(self.correct[place]):
                    self.draw_sprites(image, self.correctx[index], self.correcty[place])

            self.window.blit(self.display,(0, 0))

            pygame.display.update()
            self.reset_keys()
            self.MUSIC.set_volume(float(self.volume_menu.volume/10))

        if self.win and not self.lose:
            with open(self.PATH, 'r') as file:
                self.content = file.readlines()
                if len(self.content) > 0:
                    if self.score > int(self.content[0]):
                        del self.content[0]
                        self.content.insert(0, str(self.score)+'\n') 
                self.content.insert(1, str(self.score)+'\n')
                
            with open(self.PATH, 'w') as file:
                file.writelines(self.content)
        self.MUSIC.fadeout(1000)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.win:
                    if self.menu[0].collidepoint(pos):
                            self.playing = False
                for sprite in self.sprites:
                    if sprite[0].collidepoint(pos) and sprite[1] == self.TRY_IMAGE and len(self.input_box) == 4:
                        list_of_images = list(collections.OrderedDict(sorted(self.input_box.items())).values())
                        self.draw_on_board(list_of_images)
                        self.check_for_win()
                        self.input_box = {}
                        self.input_place = 0
                    elif sprite[0].collidepoint(pos) and sprite[1] == self.HINT_IMAGE:
                        if self.hint in self.input_box.values():
                            for item in self.input_box.items():
                                if self.hint in item:
                                    del self.input_box[item[0]]
                                    self.input_place = item[0]
                                    break
                        try:
                            del self.input_box[self.hint_index]
                        except KeyError:
                            pass
                        self.input_box[self.hint_index] = self.hint
                    elif sprite[0].collidepoint(pos) and sprite[1] != self.TRY_IMAGE and sprite[1] not in self.input_box.values() and len(self.input_box) != 4:
                        if self.input_place in self.input_box:
                            if self.input_place == 3:
                                self.input_place = 0
                            else:
                                self.input_place += 1
                        self.input_box[self.input_place] = sprite[1]
                        self.input_place += 1
                for sprite in self.input_sprites:
                    if sprite[0].collidepoint(pos):
                        if self.input_place > list(self.input_box.keys())[list(self.input_box.values()).index(sprite[1])]:
                            self.input_place = list(self.input_box.keys())[list(self.input_box.values()).index(sprite[1])]
                        del self.input_box[list(self.input_box.keys())[list(self.input_box.values()).index(sprite[1])]]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
    
    def reset_keys(self):
        self.START_KEY = False
        self.BACK_KEY = False
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.ESC_KEY = False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_sprites(self, image, x, y):
        image_rect = image.get_rect()
        image_rect.center = (x, y)
        if self.add:
            self.sprites.append((image_rect, image))
        elif image == self.MENU_IMAGE:
            self.menu = (image_rect, image)
        self.display.blit(image, image_rect)       

    def draw_in_input(self, image, place):
        coords = (self.input_board_coords[0]+(place*65), self.input_board_coords[1])
        image_rect = image.get_rect()
        image_rect.center = coords
        self.input_sprites.append((image_rect, image))
        self.display.blit(image, image_rect) 

    def draw_on_board(self, image):
        images = []
        for i in range(4):
            images.append(image[i])
        self.board[self.board_place] = images
        self.board_place += 1

    def check_for_win(self):
        answer = []
        values  = list(collections.OrderedDict(sorted(self.input_box.items())).values())
        self.score -= 100
        for image in values:
            if image in self.code:
                answer.append('white')
                if values.index(image) == self.code.index(image):
                    answer.pop()
                    answer.append('black')
        if 'white' not in answer and len(answer) == 4:
            if self.options_menu.time_limit:
                self.score = round(self.score * (self.miliseconds / 60000))
            self.win = True
        sorted_answer = sorted(answer)
        for i in sorted_answer:
            if i == 'white':
                index = sorted_answer.index(i)
                del sorted_answer[index]
                sorted_answer.insert(index, self.WHITE_CORRECT)
            else:
                index = sorted_answer.index(i)
                del sorted_answer[index]
                sorted_answer.insert(index, self.BLACK_CORRECT)
        self.correct[self.tries] = sorted_answer
        self.tries += 1
        if self.tries == 10:
            self.win = True
            self.lose = True
            
        