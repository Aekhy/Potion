from states.tab_menu import TabMenu
import pygame

class PotionsMenu(TabMenu):
    def __init__(self, game):
        super().__init__(game, 2)

    def reset(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.inGame = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.exit_state()
                elif event.key == pygame.K_ESCAPE:
                    new_event = self._game.states("Options")
                    new_event.enter_state()
           
            # For hovering the navs
            elif event.type == pygame.MOUSEMOTION:
                self.hover_nav_menu = [False, -1]
                for i in range(0,len(self.nav_menu.tabs)):
                    if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.hover_nav_menu = [True, i]
                        break

            # To select the next state we want to go in
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0,len(self.nav_menu.tabs)):
                    if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.choice = i
                        break

    def update(self):
        self.tab_menu_update(self.reset)
        self.sprites.update()

    def draw(self,screen):
        self.sprites.draw(screen)