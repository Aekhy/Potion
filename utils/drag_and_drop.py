import pygame
from inventory.settings import QUANTITY_FONT_COLOR_DEFAULT, QUANTITY_FONT_SIZE_DEFAULT
from general_settings.private_settings import LAYERS
from utils.texts import TextOutlined


class DragAndDrop:
    def __init__(self, group, update_function) -> None:
        self._group = group
        self.update_function = update_function
        self._holding = False
        self._item = None
        self._image = None
        self._name = None
        self._quantity = None
        self._slot_source = None

    def is_holding(self):
        return self._holding
    
    def take(self, slots_take, slots_iterable, event):
        if not self._holding:
            for slot in slots_iterable:
                if slot.rect.collidepoint(event.pos) and (not slot.is_empty) and (slot in slots_take):
                    self._slot_source = slot
                    self._item = slot.item
                    self._quantity = slot.quantity if event.button == 3 else 1
                    slot.take_item(self._quantity)
                    self._holding = True
                    self.update_function()
                    self.make_sprites()

    def move(self, event):
        if self._holding:
            self.move_sprites(event)

    def drop(self, slots_add, slots_iterable, event):
        if self._holding:

            drop_allowed = False
            for slot in slots_iterable:
                if slot.rect.collidepoint(event.pos) and (slot.has_room(self._item)) and (slot in slots_add):
                    drop_allowed = True
                    self._item, self._quantity = slot.add_item(self._item, self._quantity)
                    self.update_function()
            if self._quantity == 0:
                self._holding = False

            if drop_allowed and self._holding:
                self.update_sprites()
            else:
                if not drop_allowed:
                    self._holding = False
                    self._slot_source.add_item(self._item, self._quantity)
                    self.update_function()
                if not self._holding:
                    self.kill_sprites()
    
    def make_sprites(self):
        self._item_sprite = pygame.sprite.Sprite()
        self._item_sprite.image = self._slot_source.item_image_sprite.image.copy()
        self._item_sprite.rect = self._slot_source.item_image_sprite.rect.copy()
        self._item_sprite.layer = LAYERS['inventory'] + 1

        self._name_sprite = TextOutlined(self._slot_source.x+self._slot_source.size/2,
                                        self._slot_source.y+self._slot_source.size/2,
                                        self._item.name,
                                        LAYERS['inventory'] + 2,
                                        "center",
                                        self._slot_source.item_name_font_size,
                                        self._slot_source.item_name_font_color)
        
        self._quantity_sprite = TextOutlined(self._slot_source.x+self._slot_source.size, # type: ignore
                                            self._slot_source.y+self._slot_source.size,
                                            str(self._quantity),
                                            LAYERS['inventory'] + 2,
                                            "bottomright",
                                            self._slot_source.quantity_font_size,
                                            self._slot_source.quantity_font_color)
        
        self._group.add(self._item_sprite)
        self._name_sprite.add_to_group(self._group)
        self._quantity_sprite.add_to_group(self._group)
   
    def move_sprites(self, event):
        if self._holding:
            self._item_sprite.rect.move_ip(event.rel)
            self._name_sprite.move_ip(event.rel)
            self._quantity_sprite.move_ip(event.rel)

    def update_sprites(self):
        dx = self._item_sprite.rect.x - self._slot_source.item_image_sprite.rect.x # type: ignore
        dy = self._item_sprite.rect.y - self._slot_source.item_image_sprite.rect.y # type: ignore
        x = self._slot_source.rect.x + self._slot_source.size + dx
        y = self._slot_source.rect.y + self._slot_source.size + dy

        self._quantity_sprite.kill() # type: ignore
        self._quantity_sprite = TextOutlined(x, y, # type: ignore
                                            str(self._quantity),
                                            LAYERS['inventory'] + 2,
                                            "bottomright",
                                            QUANTITY_FONT_SIZE_DEFAULT,
                                            QUANTITY_FONT_COLOR_DEFAULT)
        
        self._quantity_sprite.add_to_group(self._group)

    def kill_sprites(self):
        self._item_sprite.kill()
        self._name_sprite.kill()
        self._quantity_sprite.kill()