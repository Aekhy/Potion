from items.settings import *
from utils.json_functions import Write

def MakeId():
    id = {
        "base":"base",
        "active":"active",
        "neutre":"neutre",
        "origine":"origine",
        "rien":"rien",
    }

    # DEV
    # I don't know if it's really important to have id of potion & ingredient & alchemical property
    data_list = [CHARACTERISTIC_DATA,INGREDIENT_DATA,ACTIVE_DATA,BASE_DATA,EFFECT_DATA,ALCHEMICAL_PROPERTY_DATA,POTION_DATA]

    for data in data_list:
        for key in data.keys():
            id[key] = key

    Write("items/primary_data/id.json", id)


