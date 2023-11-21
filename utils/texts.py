import pygame
from inventory.settings import *
from general_settings.private_settings import *
from general_settings.public_settings import outline

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, font_size=TEXT_FONT_SIZE_DEFAULT, font_color=TEXT_FONT_COLOR_DEFAULT, font_path=TEXT_FONT_PATH_DEFAULT):
        super().__init__()
        self.font = pygame.font.Font(font_path, font_size)
        self.image = self.font.render(str(text), False, font_color)
        self.rect = self.image.get_rect()


class TextOutlined():
    def __init__(self, x, y, text, layer, rect_position="center", font_size=TEXT_FONT_SIZE_DEFAULT, font_color=TEXT_FONT_COLOR_DEFAULT, outline_font_color=TEXT_OUTLINE_FONT_COLOR_DEFAULT, font_path=TEXT_FONT_PATH_DEFAULT):
        self.sprites = []
        # if the "step" is 1 render 9 sprites, if 2 render 4 + 1 added by hand sprites
        if outline:
            self.pas = 2
            for i in range(0, 3, self.pas):
                for j in range(0, 3, self.pas):
                    tmp_color = outline_font_color
                    tmp_layer = layer-0.01

                    # middle sprite text is above and different color from others
                    # if self.pas != 1 we need to add it by hand, not in loop
                    if self.pas == 1 and (i==1 and j==1):
                        tmp_color = font_color
                        tmp_layer = layer

                    tmp = TextSprite(text, font_size, tmp_color, font_path)
                    if self.pas == 1 and (i==1 and j==1):
                        self.rect = tmp.rect
                    self.place_rect(tmp, x-1+i, y-1+j, rect_position)
                    tmp._layer = tmp_layer # type: ignore
                    self.sprites.append(tmp)

        if not outline or self.pas == 2 :
            tmp = TextSprite(text, font_size, font_color, font_path)

            self.rect = tmp.rect

            self.place_rect(tmp, x, y, rect_position)
            tmp._layer = layer # type: ignore
            self.sprites.append(tmp)

    def place_rect(self, sprite, x, y, rect_position="center"):
        match rect_position:
                    case "topleft":
                        sprite.rect.topleft = (x,y)
                    case "topright":
                        sprite.rect.topright = (x,y)
                    case "bottomleft":
                        sprite.rect.bottomleft = (x,y)
                    case "bottomright":
                        sprite.rect.bottomright = (x,y)
                    case "midtop":
                        sprite.rect.midtop = (x,y)
                    case "midleft":
                        sprite.rect.midleft = (x,y)
                    case "midbottom":
                        sprite.rect.midbottom = (x,y)
                    case "midright":
                        sprite.rect.midright = (x,y)
                    case _:
                        sprite.rect.center = (x,y)
                        
    def add_to_group(self, group):
        for sprite in self.sprites:
            group.add(sprite)

    def remove_from_group(self, group):
        for sprite in self.sprites:
            group.remove(sprite)

    def kill(self):
        for sprite in self.sprites:
            sprite.kill()

    def update_x_y(self, x, y, rect_position="center"):
        if outline:
            k = 0
            for i in range(0, 3, self.pas):
                for j in range(0, 3, self.pas):
                    tmp = self.sprites[k]
                    self.place_rect(tmp, x-1+i, y-1+j, rect_position)
                    k+=1
        if not outline or self.pas == 2:
            tmp = self.sprites[len(self.sprites)-1]
            self.place_rect(tmp, x, y, rect_position)

    def move_ip(self, event_rel):
        for sprite in self.sprites:
            sprite.rect.move_ip(event_rel)

