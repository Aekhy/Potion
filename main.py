from Inventory import Inventory
from Case import Case
from settings.ClasseSetting import *
from Utils import *
from group import draw_grp

# initalise pygame module, pygame.display.init() is also automatically run.
pygame.init()

# create a display surface, with a ratio of (width,height)
# screen = pygame.display.set_mode((800,450))
screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT))


# set the name of the window
pygame.display.set_caption("L2-S1-Pygame")

# get a clock
clock = pygame.time.Clock()

slots_take_allowed = []
slots_drop_allowed = []
# inventory
inventory = Inventory((1920-5*INVENTORY_SLOT_SIZE)/2,1080-2*INVENTORY_SLOT_SIZE,DEFAULT_INVENTORY_LAYOUT)
inventory_rect = inventory.get_rect()
inventory_slot_list = inventory.get_slot_list()

for slot in inventory_slot_list:
    slots_take_allowed.append(slot)
    slots_drop_allowed.append(slot)



holding_item = False
is_game_running = True

while is_game_running:

    screen.fill("black")

    for event in pygame.event.get():
        # pygame.QUIT is an event which happend when we click
        # on the x of the window to close it
        if event.type == pygame.QUIT:
            is_game_running = False

        #------------- DRAG AND DROP -------------
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3) :
            
            if not holding_item and (inventory_rect.collidepoint(event.pos)):
                for slot in slots_take_allowed:
                    if not slot.is_empty() and slot.get_rect().collidepoint(event.pos) :
                        slot_source = slot
                        holding_item_item = slot.get_item()
                        holding_item_quantity = 1
                        if event.button == 3:
                            holding_item_quantity = slot.quantity
                        slot.take_item(holding_item_quantity)
                        holding_item = True

                        #Graphisme

                        holding_item_image_sprite = pygame.sprite.Sprite()
                        holding_item_image_sprite.image = slot.item_image_sprite.image.copy()
                        holding_item_image_sprite.rect = slot.item_image_sprite.rect.copy()
                        holding_item_image_sprite._layer = 2

                        holding_item_name_sprite = TextOutlined(slot.x+slot.size/2,
                                                                slot.y+slot.size/2,
                                                                holding_item_item.get_name(),
                                                                3,
                                                                "center",
                                                                slot.item_name_font_size,
                                                                slot.item_name_font_color)

                        holding_item_quantity_sprite = TextOutlined(slot.x+slot.size,
                                                                    slot.y+slot.size,
                                                                    str(holding_item_quantity),
                                                                    3,
                                                                    "bottomright",
                                                                    slot.quantity_font_size,
                                                                    slot.quantity_font_color)
                        draw_grp.add(holding_item_image_sprite)
                        holding_item_name_sprite.add_to_group(draw_grp)
                        holding_item_quantity_sprite.add_to_group(draw_grp)

        if event.type == pygame.MOUSEMOTION:
            if holding_item:
                #Graphisme
                holding_item_image_sprite.rect.move_ip(event.rel)
                holding_item_name_sprite.move_ip(event.rel)
                holding_item_quantity_sprite.move_ip(event.rel)
                
        if event.type == pygame.MOUSEBUTTONUP:
            if holding_item:
                # if we released over the inventory zone
                drop_allowed = False
                if inventory_rect.collidepoint(event.pos):
                    for slot in slots_drop_allowed:
                        # if we released over a slot
                        if slot.get_rect().collidepoint(event.pos) and slot.has_room(holding_item_item):
                        
                            # if that slot had room for our item
                            drop_allowed = True
                            holding_item_item, holding_item_quantity = slot.add_item(holding_item_item, holding_item_quantity)
                            # update graphisme quantity
                            # we want the quantity sprite rightly positionned in term of 
                            # distance from the center of the image
                            # important to get the right place to place the quantity
                            dx = holding_item_image_sprite.rect.x - slot_source.item_image_sprite.rect.x  
                            dy = holding_item_image_sprite.rect.y - slot_source.item_image_sprite.rect.y 
                            x = slot_source.get_rect().x + slot_source.size + dx
                            y = slot_source.get_rect().y + slot_source.size + dy

                            holding_item_quantity_sprite.kill()
                            holding_item_quantity_sprite = TextOutlined(x,
                                                                        y,
                                                                        str(holding_item_quantity),
                                                                        3,
                                                                        "bottomright",
                                                                        slot.quantity_font_size,
                                                                        slot.quantity_font_color)
                            holding_item_quantity_sprite.add_to_group(draw_grp)

                            if holding_item_quantity == 0:
                                holding_item = False

                if not drop_allowed:
                    slot_source.add_item(holding_item_item, holding_item_quantity)
                    holding_item = False
                
                if not holding_item:
                    holding_item_image_sprite.kill()
                    holding_item_name_sprite.kill()
                    holding_item_quantity_sprite.kill()
        
        #------------- END DRAG AND DROP -------------

    draw_grp.draw(screen)
    pygame.display.update()
    # set to 60 fps, can be confirmed with clock.get_fps()
    clock.tick(DEFAULT_FPS)
# opposite of pygame.init()
pygame.quit()


