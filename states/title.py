from states.state import State
from utils.texts import TextOutlined
from general_settings.private_settings import *
import pygame

class Title(State):
    def __init__(self, game):
        super().__init__(game)
        self.sprites = pygame.sprite.LayeredUpdates()

        self.space_between_choice = 50

        self.game_title = TextOutlined(SCREEN_WIDTH/2, SCREEN_HEIGHT/4, "Potion", 1)
        self.game_title.add_to_group(self.sprites)

        self.play_button = TextOutlined(SCREEN_WIDTH/2, SCREEN_HEIGHT/4+self.space_between_choice*2, "Jouer", 1)
        self.play_button.add_to_group(self.sprites)

        self.exit_button = TextOutlined(SCREEN_WIDTH/2, SCREEN_HEIGHT/4+self.space_between_choice * 3, "Quitter", 1)
        self.exit_button.add_to_group(self.sprites)

        self.preselected_choice = 0
        self.chose = False
        self.choices = {
            0:{"rect":self.play_button.rect},
            1:{"rect":self.exit_button.rect}
        }

        self.len_choice = len(self.choices)

        self.preselection_sprite = pygame.sprite.Sprite(self.sprites)
        self.preselection_sprite.image = pygame.Surface((100,DEFAULT_FONT_SIZE))
        self.preselection_sprite.image.fill((200,200,200))
        self.preselection_sprite.rect = self.preselection_sprite.image.get_rect()
        self.preselection_sprite.rect.center = (SCREEN_WIDTH/2 , SCREEN_HEIGHT/4+self.space_between_choice * (self.preselected_choice+2))
    
    def update_preselection_sprite(self):
        self.preselection_sprite.rect.center = (SCREEN_WIDTH/2 , SCREEN_HEIGHT/4+self.space_between_choice * (self.preselected_choice+2))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.inGame = False
            elif event.type == pygame.MOUSEMOTION:
                for key, value in self.choices.items():
                    if value["rect"].collidepoint(event.pos):
                        self.preselected_choice = key
                        
                       
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for key, value in self.choices.items():
                        if value["rect"].collidepoint(event.pos):
                            self.preselected_choice = key
                            self.chose = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.chose = True
                elif event.key == pygame.K_UP:
                    self.preselected_choice = (self.preselected_choice - 1) % self.len_choice
                elif event.key == pygame.K_DOWN:
                    self.preselected_choice = (self.preselected_choice + 1) % self.len_choice
                elif event.key == pygame.K_q:
                    self._game.states("PopUp").enter_state()

    def update(self):
        # DEV
        # go see comments in states.py
        if not self._in_state:
            self._in_state = True
            
        self.preselection_sprite.rect.center = (SCREEN_WIDTH/2 , SCREEN_HEIGHT/4+self.space_between_choice * (self.preselected_choice+2))
        
        if self.chose:
            self.chose = False
            
            if self.preselected_choice == self.len_choice - 1: # quit
                self.preselected_choice = 0
                self._game.inGame = False
            elif self.preselected_choice == 0: # play

                # Loading the informations about the dirname
                self._game.save_manager.LoadSave("saves/save_one")

                new_state = self._game.states("CauldronScreen")
                new_state.enter_state()
            # elif self.preselected_choice == 1:
            #     self.preselected_choice = 0
            #     new_state = self._game.states("")
            #     new_state.enter_state()

        self.sprites.update()

    def draw(self, surface):
        self.sprites.draw(surface)
