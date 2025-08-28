import util as ut
from util import FREE, WALL, WIN, OUT_OF_BOUNDS, VISITED
from collections import deque

n = 10
my_map = ut.build_map(n)
my_map[0][4] = WALL
my_map[1][0] = WALL
my_map[1][3] = WALL
my_map[2][2] = WALL
my_map[3][2] = WALL
my_map[3][5] = WALL
my_map[4][1] = WALL
my_map[4][6] = WALL
my_map[5][3] = WALL
my_map[5][5] = WALL
my_map[5][6] = WALL
my_map[5][7] = WALL
my_map[5][8] = WALL
my_map[6][5] = WALL
my_map[6][8] = WALL
my_map[7][5] = WALL
my_map[7][7] = WIN
my_map[7][8] = WALL
my_map[8][5] = WALL
my_map[8][7] = WALL
my_map[8][8] = WALL
my_map[9][5] = WALL

my_pos = {"x": 0, "y": 0}

def neighbors(grid, cell):
    x, y = cell
    moves = [(1,0),(0,-1),(-1,0),(0,1)]
    for dx, dy in moves:
        nx, ny = x+dx, y+dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[ny][nx] != WALL:
                yield (nx, ny)

def BFS_spanning_tree(grid, start):
    tree = {}
    visited = set([start])
    queue = deque([start])
    tree[start] = []
    
    while queue:
        node = queue.popleft()
        for neigh in neighbors(grid, node):
            if neigh not in visited:
                visited.add(neigh)
                queue.append(neigh)
                
                tree.setdefault(node, []).append(neigh)
                tree.setdefault(neigh, []).append(node)
    
    return tree

def explore(grid, start):
    tree = BFS_spanning_tree(grid, start)
    visited = set()
    path = []

    def dfs(node):
        visited.add(node)
        path.append(node)
        for neigh in tree[node]:
            if neigh not in visited:
                dfs(neigh)
                path.append(node)
    
    dfs(start)
    return path

path = explore(my_map, (my_pos["x"], my_pos["y"]))

count = 0
my_map_str = ""
my_map_str += f'Moves: {count}\n'
my_map_str += ut.draw_map(my_map, my_pos)
for x, y in path:
    my_map[my_pos["y"]][my_pos["x"]] = VISITED
    my_pos["x"] = x
    my_pos["y"] = y

    if my_map[my_pos["y"]][my_pos["x"]] == WIN:
        my_map[my_pos["y"]][my_pos["x"]] = "x"

        count += 1
        my_map_str += f'Moves: {count}\n'
        my_map_str += ut.draw_map(my_map, my_pos)
        break

    my_map[my_pos["y"]][my_pos["x"]] = "x"

    count += 1
    my_map_str += f'Moves: {count}\n'
    my_map_str += ut.draw_map(my_map, my_pos)

ut.log_map("etapa3.txt", my_map_str)