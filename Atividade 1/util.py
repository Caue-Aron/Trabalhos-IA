FREE = "_"
WALL = "#"
WIN = "@"
VISITED = "!"
OUT_OF_BOUNDS = "OOB"

def build_map(n):
    return [[FREE for _ in range(n)] for _ in range (n)]

def draw_map(my_map, my_pos={"x":-1,"y":-1}):
    map_drawing = ""
    for idx_y, y in enumerate(my_map):
        for idx_x, x in enumerate(y):
            map_drawing += " | "
            if my_pos["x"] == idx_x and my_pos["y"] == idx_y:
                map_drawing += "x"
            else:
                map_drawing += x
        map_drawing += " |\n"
    
    return map_drawing + "\n"

def check_map_inbounds(my_map, my_pos):
    return not ((my_pos["x"] >= len(my_map) or my_pos["y"] >= len(my_map)) or (my_pos["x"] < 0 or my_pos["y"] < 0))

def check_map_not_wall(my_map, my_pos):
    return not (my_map[my_pos["y"]][my_pos["x"]] == WALL)

def check_map_not_visited(my_map, my_pos):
    return not (my_map[my_pos["y"]][my_pos["x"]] == VISITED)

def check_map_collision(my_map, my_pos, next_x, next_y):
    new_x = 0
    new_y = 0
    if next_x != 0:
        new_x = next_x + my_pos["x"]
        new_y = my_pos["y"]
    else:
        new_x = my_pos["x"]
        new_y = next_y + my_pos["y"]

    if not check_map_inbounds(my_map, {"x": new_x, "y": new_y}):
        return OUT_OF_BOUNDS
    
    elif not check_map_not_wall(my_map, {"x": new_x, "y": new_y}):
        return WALL
    
    elif not check_map_not_visited(my_map, {"x": new_x, "y": new_y}):
        return VISITED
    
    return FREE
    
def log_map(file_name, my_map_str):
    with open(file_name, mode="w", encoding="UTF-8") as file:
        file.write(my_map_str)