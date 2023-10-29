from general_settings.private_settings import SCREEN_WIDTH
from utils.texts import TextOutlined
import pygame



class Nav():
    def __init__(self, x, y, tab_height, group, current_tab_index: int, options: list):
        self.current_tab_index = current_tab_index
        self.options = options
        self._tabs = []
        self.sprites = group
        self._x = x
        self._y = y
        self.tab_width = SCREEN_WIDTH/len(self.options)
        self.tab_height = tab_height
        self.space_color = 200
        self.fill_tabs()
        self.reset_colors()

    def get_tabs(self):
        return self._tabs
    
    tabs = property(get_tabs)

    def fill_tabs(self):

        for i in range(0,len(self.options)):
            # space
            # this value is used to darken the color of the current option

            space = pygame.sprite.Sprite(self.sprites)
            space.image = pygame.Surface((self.tab_width,self.tab_height))
            space.image.fill((self.space_color, self.space_color, self.space_color))
            space._layer = 1
            space.rect = space.image.get_rect()
            space.rect.topleft = (self._x * self.tab_width, self._y )

            # text
            text = TextOutlined(self._x * self.tab_width  + self.tab_width/2 , self._y + self.tab_height/2, self.options[i], 1.5)
            text.add_to_group(self.sprites)
            
            # state
            state = None
            
            tab = {
                 "space":space,
                 "text":text,
                 "state":state,
            }
    
            self._tabs.append(tab)
            self._x += 1


    def color_tab(self, index, diff):
        # select indicated tab
        c = self.space_color - diff
        self.tabs[index]["space"].image.fill((c, c, c))

    def reset_colors(self):
        for i in range(0, len(self.tabs)):
            c = self.space_color
            if i == self.current_tab_index:
                c -= 50
            self.tabs[i]["space"].image.fill((c,c,c))
        
    def hover_tab(self, index):
        self.reset_colors()
        self.color_tab(index, 20)

