from general_settings.private_settings import *
from tools.tools import Cauldron, Freezer, Alembic
from inventory.inventory import Inventory
from utils.texts import TextOutlined
from inventory.settings import *
import pygame as pyg


class Game:
    def __init__(self):
        pyg.init()
        self.screen = pyg.display.set_mode(( SCREEN_WIDTH,SCREEN_HEIGHT ))
        self.clock = pyg.time.Clock()
        #self.font = pyg.font.Font(DEFAULT_FONT_PATH, DEFAULT_FONT_SIZE)
        self.running = True

    def start(self):
        # When we start the game at the beginning or after a pause for example
        self.inGame = True
        # The sprites group will be updated at every tick
        self.sprites = pyg.sprite.LayeredUpdates()

        self.slots = {"take":[],"add":[]}
        self.holding_item = {'bool':False}
        
        # Game objects
        self.cauldron = Cauldron(self, self.sprites, 100, 100)
        self.inventory = Inventory(self, self.sprites, (SCREEN_WIDTH-5*INVENTORY_SLOT_SIZE)/2,SCREEN_HEIGHT-2*INVENTORY_SLOT_SIZE, INVENTORY_LAYOUT)
        self.freezer = Freezer(self,400,50)
        self.alembic = Alembic(self,500,50) 

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
                    if (event.button == 1 or event.button == 3) :
                        if self.cauldron.finish_button.rect.collidepoint(event.pos):
                            self.cauldron.finish()
                        elif self.alembic.finish_button.rect.collidepoint(event.pos):
                            self.alembic.apply_effect()
                        elif self.freezer.finish_button.rect.collidepoint(event.pos):
                            self.freezer.apply_effect()
                        if not self.holding_item['bool']:
                            self.drag(event)
                            
                case pyg.MOUSEMOTION:
                    if self.holding_item['bool']:
                        self.holding_item['image'].rect.move_ip(event.rel)
                        self.holding_item['name'].move_ip(event.rel)
                        self.holding_item['quantity_sprite'].move_ip(event.rel)
                        
                case pyg.MOUSEBUTTONUP:
                    if self.holding_item['bool']:
                        self.drop(event)

    def drag(self, event):
        for slot in self.slots["take"]:
            if not slot.is_empty and slot.rect.collidepoint(event.pos):
                # DEBUG : A decomposer
                self.slot_source = slot
                self.holding_item['item'] = slot.item
                self.holding_item['quantity'] = slot.quantity if event.button == 3 else 1
                slot.take_item(self.holding_item['quantity'])
                self.holding_item['bool'] = True
                #Graphisme

                self.holding_item['image'] = pyg.sprite.Sprite()
                self.holding_item['image'].image = slot.item_image_sprite.image.copy()
                self.holding_item['image'].rect = slot.item_image_sprite.rect.copy()
                self.holding_item['image']._layer = LAYERS['inventory'] + 1
                
                self.holding_item['name'] = TextOutlined(slot.x+slot.size/2,
                                                        slot.y+slot.size/2,
                                                        self.holding_item['item'].name,
                                                        LAYERS['inventory'] + 2,
                                                        "center",
                                                        slot.item_name_font_size,
                                                        slot.item_name_font_color)

                self.holding_item['quantity_sprite'] = TextOutlined(slot.x+slot.size,
                                                            slot.y+slot.size,
                                                            str(self.holding_item['quantity']),
                                                            LAYERS['inventory'] + 2,
                                                            "bottomright",
                                                            slot.quantity_font_size,
                                                            slot.quantity_font_color)
                self.sprites.add(self.holding_item['image'])
                self.holding_item['name'].add_to_group(self.sprites)
                self.holding_item['quantity_sprite'].add_to_group(self.sprites)


    def drop(self, event):
        holding_item = self.holding_item
        if holding_item['bool']:
            drop_allowed = False
            # if we released over the inventory zone
            if self.inventory.rect.collidepoint(event.pos):
                for slot in self.slots["add"]:
                    # if we released over a slot
                    if slot.rect.collidepoint(event.pos) and slot.has_room(holding_item['item']):
                    
                        # if this slot has room for our item
                        drop_allowed = True
                        holding_item['item'], holding_item['quantity'] = slot.add_item(holding_item['item'], holding_item['quantity'])
            # if we released over the cauldron
            if self.cauldron.rect.collidepoint(event.pos):
                drop_allowed, holding_item['item'], holding_item['quantity'] = self.cauldron.add_thing(holding_item['item'],holding_item['quantity'])
                print(drop_allowed, holding_item['item'], holding_item['quantity'])
            
            if self.alembic.rect.collidepoint(event.pos):
                drop_allowed, holding_item['item'], holding_item['quantity'] = self.alembic.add_mixture(holding_item['item'],holding_item['quantity'])
                print(drop_allowed, holding_item['item'], holding_item['quantity'])

            if self.freezer.rect.collidepoint(event.pos):
                drop_allowed, holding_item['item'], holding_item['quantity'] = self.freezer.add_mixture(holding_item['item'],holding_item['quantity'])
                print(drop_allowed, holding_item['item'], holding_item['quantity'])

            if holding_item['quantity'] == 0:
                holding_item['bool'] = False
                if self.cauldron.verify_slot(self.slot_source):
                    self.cauldron.reset()
                elif self.alembic.verify_slot(self.slot_source):
                    self.alembic.reset()
                elif self.freezer.verify_slot(self.slot_source):
                    self.freezer.reset()

            if drop_allowed and holding_item['bool']:
                # update graphics quantity
                # we want the quantity sprite rightly positionned in term of 
                # distance from the center of the image
                # important to get the right place to place the quantity
                dx = holding_item['image'].rect.x - self.slot_source.item_image_sprite.rect.x
                dy = holding_item['image'].rect.y - self.slot_source.item_image_sprite.rect.y
                x = self.slot_source.rect.x + self.slot_source.size + dx
                y = self.slot_source.rect.y + self.slot_source.size + dy

                holding_item['quantity_sprite'].kill()
                holding_item['quantity_sprite'] = TextOutlined(x, y,
                                                            str(holding_item['quantity']),
                                                            LAYERS['inventory'] + 2,
                                                            "bottomright",
                                                            QUANTITY_FONT_SIZE_DEFAULT,
                                                            QUANTITY_FONT_COLOR_DEFAULT)
                holding_item['quantity_sprite'].add_to_group(self.sprites)               
            else:
                if not drop_allowed:
                    self.slot_source.add_item(holding_item['item'], holding_item['quantity'])
                    holding_item['bool'] = False
                
                if not holding_item['bool']:
                    holding_item['image'].kill()
                    holding_item['name'].kill()
                    holding_item['quantity_sprite'].kill()

            

    def update(self):
        # Async game updates
        self.sprites.update()

    def draw(self):
        # Game sprite drawing loop
        # Fill the screen with solid color
        self.screen.fill(COLORS['white'])

        # Print our sprites
        self.sprites.draw(self.screen)
        

        # Show the final screen
        pyg.display.update()

g = Game()
g.start()
while g.running:
    g.main()

pyg.quit()