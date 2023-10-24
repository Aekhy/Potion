from config import *
from Cauldron import *
from Inventory.Inventory import Inventory
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
        # The game_sprites group will be updated at every tick
        self.game_sprites = pyg.sprite.LayeredUpdates()
        self.slots_sprites = pyg.sprite.LayeredUpdates()

        self.holding_item = {'bool':False}
        
        # Game objects
        self.cauldron = Cauldron(self)
        self.inventory = Inventory(self, 0, SCREEN_WIDTH - 100, [])

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
                    if event.type == pyg.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3) :
                        self.on_click(event)

    def on_click(self, event):
        pos = event.pos

        if not self.holding_item['bool'] and (self.inventory.rect.collidepoint(pos)):
            for slot in self.inventory.slot_list:
                if not slot.is_empty and slot.rect.collidepoint(event.pos):

                    # DEBUG : A decomposer
                    self.slot_source = slot
                    self.holding_item['item'] = slot.item
                    self.holding_item['quantity'] = slot.quantity if event.button == 3 else 1
                    slot.take_item(holding_item_quantity)
                    self.holding_item['bool'] = True

                    #Graphisme

                    self.holding_item['image'] = pygame.sprite.Sprite()
                    self.holding_item['image'].image = slot.item_image_sprite.image.copy()
                    self.holding_item['image'].rect = slot.item_image_sprite.rect.copy()
                    self.holding_item['image']._layer = LAYERS['inventory'] + 1

                    self.holding_item['name'] = TextOutlined(slot.x+slot.size/2,
                                                        slot.y+slot.size/2,
                                                        slot.item.get_name(),
                                                        LAYERS['inventory'] + 2,
                                                        "center",
                                                        slot.item_name_font_size,
                                                        slot.item_name_font_color)

                    self.holding_item['quantity'] = TextOutlined(slot.x+slot.size,
                                                        slot.y+slot.size,
                                                        str(holding_item_quantity),
                                                        LAYERS['inventory'] + 2,
                                                        "bottomright",
                                                        slot.quantity_font_size,
                                                        slot.quantity_font_color)
                    self.game_sprites.add(holding_item_image_sprite)
                    holding_item_name_sprite.add_to_group(self.game_sprites)
                    holding_item_quantity_sprite.add_to_group(self.game_sprites)


    def on_release(self, event):
        pass

    def update(self):
        # Async game updates
        self.game_sprites.update()

    def draw(self):
        # Game sprite drawing loop
        # Fill the screen with solid color
        self.screen.fill(COLORS['white'])

        # Print our sprites
        self.game_sprites.draw(self.screen)
        self.slots_sprites.draw(self.screen)

        if self.holding_item['bool']:
            pos = pyg.mouse.get_pos()
            rel = pyg.mouse.get_rel()
            holding_item['image'].rect.move_ip(rel)
            holding_item['name'].move_ip(rel)
            holding_item['quantity'].move_ip(rel)

        # Show the final screen
        pyg.display.update()

g = Game()
g.start()
while g.running:
    g.main()

pyg.quit()