import json

def Read(path:str):
    with open(path) as file :
        data = json.load(file) 
    return data

def Write(path:str, data:dict, indent_number:int=4):
    
    black_list = [
        "items/base_active_compatibility_matrix.json",
        "items/base_graph.json",
        "items/active_graph.json",
        "items/alchemical_property_matrix.json",
        "items/potion_tree.json"
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