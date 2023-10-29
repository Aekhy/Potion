from general_settings.private_settings import *
import sys
import pygame as pyg


from states.title import Title
from states.ingredient_menu import IngredientMenu
class Game:
    def __init__(self):
        pyg.init()
        self.screen = pyg.display.set_mode(( SCREEN_WIDTH,SCREEN_HEIGHT ))
        self.clock = pyg.time.Clock()
        #self.font = pyg.font.Font(DEFAULT_FONT_PATH, DEFAULT_FONT_SIZE)
        self.running = True

        self.state_stack = []
        self._all_states = {}
        self.start()

    def states(self, state):
        if not state in self._all_states.keys():
            if state == "Title":
                self._all_states[state] = Title(self)
            elif state == "IngredientMenu":
                self._all_states[state] = IngredientMenu(self)
        return self._all_states[state]
               
    def start(self):
        # When we start the game at the beginning or after a pause for example
        new_state = self.states("Title")
        new_state.enter_state()
        self.inGame = True

    def main(self):
        # Game loop
        while self.inGame:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FRAMERATE)
        self.running = False

    # ////////// PRIVATE \\\\\\\\\\
    def reset_keys(self):
        self.actions = {}

    def events(self):
        # Game events management
        self.state_stack[-1].events()

    def update(self):
        # Async game updates
        self.state_stack[-1].update()

    def draw(self):
        # Game sprite drawing loop
        # Fill the screen with solid color
        self.screen.fill(COLORS['white'])

        # Print our sprites
        self.state_stack[-1].draw(self.screen)
        
        # Show the final screen
        pyg.display.update()

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.main()

pyg.quit()
sys.exit()