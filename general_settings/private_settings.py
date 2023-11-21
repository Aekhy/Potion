DEBUG = False

# General settings constants
FRAMERATE = 60

# Shared
COLORS = {
    'black' : (0, 0, 0),
    'darkgrey' : (50, 50, 50),
    'grey' : (127, 127, 127),
    'white' : (255, 255, 255),
    'red' : (255, 0, 0),
    'darkred' : (139, 0, 0)
}

LAYERS = {
    'cauldron': 1,
    'inventory': 2,     # Inventory takes 4 layers  -- for slots it's from 2 and 3
    'tools': 2,
    'max': 20
}

# Game
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
GAME_FONT_PATH = ''
DEFAULT_FONT_SIZE = 25

# Font
TEXT_FONT_COLOR_DEFAULT = "White"
TEXT_OUTLINE_FONT_COLOR_DEFAULT = "Black"
TEXT_FONT_SIZE_DEFAULT = 16
TEXT_FONT_PATH_DEFAULT = "style/CinzelDecorative-Black.ttf"