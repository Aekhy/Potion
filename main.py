from general_settings.private_settings import *
import sys
import pygame as pyg


from states.title import Title

class Game:
    def __init__(self):
        pyg.init()
        self.screen = pyg.display.set_mode(( SCREEN_WIDTH,SCREEN_HEIGHT ))
        self.clock = pyg.time.Clock()
        #self.font = pyg.font.Font(DEFAULT_FONT_PATH, DEFAULT_FONT_SIZE)
        self.running = True

        self.state_stack = []
        self.keybinds = {
            
        }
        self.actions = {
            
        }

        self.start()

    def start(self):
        # When we start the game at the beginning or after a pause for example
        self.title_screen = Title(self)
        self.title_screen.enter_state()
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

    def events(self):
        # Game events management
        for event in pyg.event.get():
            match event.type:
                case pyg.QUIT:
                    self.inGame = False
                    self.running = False
                case pyg.MOUSEBUTTONDOWN:
                    self.actions["primaryclick"] = event.button == 1
                    self.actions["middleclick"] = event.button == 2
                    self.actions["secondaryclick"] = event.button == 3
                    self.actions["mouse_pos"] = event.pos

                case pyg.MOUSEMOTION:
                    self.actions["mouse_motion"] = True
                    self.actions["mouse_rel"] = event.rel

                case pyg.MOUSEBUTTONUP:
                    self.actions["primaryclick"] = not event.button == 1
                    self.actions["middleclick"] = not event.button != 2
                    self.actions["secondaryclick"] = not event.button == 3

                case _:
                    pass

    def update(self):
        # Async game updates
        self.state_stack[-1].update(self.actions)

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