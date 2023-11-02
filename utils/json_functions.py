import json

def Read(path:str):
    with open(path) as file :
        data = json.load(file) 
    return data

def Write(path:str, data:dict, indent_number:int=4):
    
    black_list = [
        "items/primary_data/characteristic.json",
        "items/primary_data/effect",
        "items/primary_data/alchemical_property.json",
        "items/primary_data/active.json",
        "items/primary_data/base.json",
        "items/primary_data/ingredient.json",
        "items/primary_data/potions.json",
        "items/primary_data/id.json",
        "items/secondary_data/base_active_compatibility_matrix.json",
        "items/secondary_data/base_graph.json",
        "items/secondary_data/active_graph.json",
        "items/secondary_data/alchemical_property_matrix.json",
        "items/secondary_data/potion_tree.json"
    ]
    lucky_to_be_alive = None
    safe = True
    for p in black_list:
        if path == p:
            safe = False
            lucky_to_be_alive = p
            break

    if safe:
        j = json.dumps(data, indent=indent_number)
        with open(path, 'w') as file:
            file.write(j)
    else:
        print(f"You tried to overwrite an important json file {lucky_to_be_alive}")