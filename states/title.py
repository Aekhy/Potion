from states.state import State
from utils.texts import TextOutlined
from general_settings.private_settings import *
import pygame

class Title(State):
    def __init__(self, game):
        super().__init__(game)
        self.sprites = pygame.sprite.LayeredUpdates()

        self.space_between_choice = 50

        self.game_title = TextOutlined(SCREEN_WIDTH/2, SCREEN_HEIGHT/4, "Potion", 0)
        self.game_title.add_to_group(self.sprites)

        self.play_button = TextOutlined(SCREEN_WIDTH/2, SCREEN_HEIGHT/4+self.space_between_choice, "Jouer", 0)
        self.play_button.add_to_group(self.sprites)

        self.settings_button = TextOutlined(SCREEN_WIDTH/2, SCREEN_HEIGHT/4+self.space_between_choice * 2, "Paramètres", 0)
        self.settings_button.add_to_group(self.sprites)

    def update(self, actions):
        #self.game.reset_keys()
        pass

    def draw(self, surface):
        self.sprites.draw(surface)

        

