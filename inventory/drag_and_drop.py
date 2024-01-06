import pygame
from inventory.settings import QUANTITY_FONT_COLOR_DEFAULT, QUANTITY_FONT_SIZE_DEFAULT
from general_settings.private_settings import LAYERS
from utils.texts import TextOutlined

class DragAndDrop:
    def __init__(self, group, update_function, state=None) -> None:
        self._group = group
        self.update_function = update_function
        # if you give state in draganddrop, state need to have a _id attribute
        self._state = state
        self._holding = False
        self._item = None
        self._image = None
        self._name = None
        self._quantity = None
        self._slot_source = None
        self._drop_allowed = False


    def is_holding(self):
        return self._holding
    
    @property
    def item(self):
        return self._item
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, qtt):
        self._quantity = qtt
        if self.quantity == 0:
            self.reinit()
        else:
            self.update_sprites()
    
    def take(self, slots_take, slots_iterable, event):
        taken = False
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
                    taken = True
        return taken

    def move(self, event):
        if self._holding:
            self.move_sprites(event)

    def drop(self, slots_add, slots_iterable, event, cauldron_reset=None):
        if self._holding:
            self._drop_allowed = False
            interact_with_tool = False
            if self._state is not None and self._state.id == "ToolsScreen":
                if self._state._heater.rect.collidepoint(event.pos):
                    interact_with_tool = True
                    self._drop_allowed, self._item, self._quantity = self._state._heater.add_mixture(self._item, self._quantity)
                elif self._state._freezer.rect.collidepoint(event.pos):
                    interact_with_tool = True
                    self._drop_allowed, self._item, self._quantity = self._state._freezer.add_mixture(self._item, self._quantity)
                elif self._state._mortar.rect.collidepoint(event.pos):
                    interact_with_tool = True
                    self._drop_allowed, self._item, self._quantity = self._state._mortar.add_mixture(self._item, self._quantity)
                elif self._state._alembic.rect.collidepoint(event.pos):
                    interact_with_tool = True
                    self._drop_allowed, self._item, self._quantity = self._state._alembic.add_mixture(self._item, self._quantity)
                elif self._state._sublime.rect.collidepoint(event.pos):
                    interact_with_tool = True
                    self._drop_allowed, self._item, self._quantity = self._state._sublime.add_mixture(self._item, self._quantity)
                elif self._state._ferment.rect.collidepoint(event.pos):
                    interact_with_tool = True
                    self._drop_allowed, self._item, self._quantity = self._state._ferment.add_mixture(self._item, self._quantity)
            if not interact_with_tool:
                for slot in slots_iterable:
                    if slot.rect.collidepoint(event.pos) and (slot.has_room(self._item)) and (slot in slots_add):
                        self._drop_allowed = True
                        item, quantity = slot.add_item(self._item, self._quantity)
                        if quantity == self._quantity:
                            self._drop_allowed = False
                        self._item, self._quantity = item, quantity
                        self.update_function()
                        break

            if self._quantity == 0:
                self._holding = False
                if cauldron_reset is not None:
                    cauldron_reset()
                if self._state is not None and self._state.id == "ToolsScreen":
                    if self._state._heater.verify_slot(self._slot_source):
                        self._state._heater.reset()
                    elif self._state._freezer.verify_slot(self._slot_source):
                        self._state._freezer.reset()
                    elif self._state._mortar.verify_slot(self._slot_source):
                        self._state._mortar.reset()
                    elif self._state._alembic.verify_slot(self._slot_source):
                        self._state._alembic.reset() 
                    elif self._state._sublime.verify_slot(self._slot_source):
                        self._state._sublime.reset() 
                    elif self._state._ferment.verify_slot(self._slot_source):
                        self._state._ferment.reset() 

            if self._drop_allowed and self._holding:
                self.update_sprites()
            else:
                if not self._drop_allowed:
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
        
        self._quantity_sprite = TextOutlined(self._slot_source.x+self._slot_source.size,
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
        dx = self._item_sprite.rect.x - self._slot_source.item_image_sprite.rect.x
        dy = self._item_sprite.rect.y - self._slot_source.item_image_sprite.rect.y
        x = self._slot_source.rect.x + self._slot_source.size + dx
        y = self._slot_source.rect.y + self._slot_source.size + dy

        self._quantity_sprite.kill()
        self._quantity_sprite = TextOutlined(x, y,
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
        
    def reinit(self):
        self.kill_sprites()
        self = self.__init__(self._group, self.update_function)