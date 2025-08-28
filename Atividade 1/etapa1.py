import util as ut
from util import FREE, WALL, WIN, OUT_OF_BOUNDS, VISITED

n = 6
my_map = ut.build_map(n)
my_pos = {"x": 2, "y": 2}

def attempt_move(x, y):
    if ut.check_map_collision(my_map, my_pos, x, y) != OUT_OF_BOUNDS:
        my_map[my_pos["y"]][my_pos["x"]] = VISITED
        my_pos["x"] += x
        my_pos["y"] += y
        return False
    else:
        return True

# has the agent reached the 4 edges?    
edges = 0
count = 0
my_map_str = ""
my_map_str += f'Move {count}\nEdges found: {edges}\n'
my_map_str += ut.draw_map(my_map, my_pos)
while edges < 4:
    # north
    if edges == 0:
        found_edge = attempt_move(0, -1)

    # east
    elif edges == 1:
        found_edge = attempt_move(+1, 0)

    # south
    elif edges == 2:
        found_edge = attempt_move(0, +1)

    # west
    elif edges == 3:
        found_edge = attempt_move(-1, 0)

    if found_edge:
        edges += 1

    count += 1

    my_map_str += f'Move {count}\nEdges found: {edges}\n'
    my_map_str += ut.draw_map(my_map, my_pos)

ut.log_map("etapa1.txt", my_map_str)
print("SUCCESS!")