# ETAPA 4(A) – Ambiente totalmente observável (Dijkstra)
import util as ut
from util import FREE, WALL, WIN, OUT_OF_BOUNDS, VISITED
import heapq

ROWS, COLS = 8, 15
cx, cy = COLS // 2, ROWS // 2

def build_picture_map():
    grid = [["1" for _ in range(COLS)] for __ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLS):
            if abs(x - cx) + abs(y - cy) <= 2:
                grid[y][x] = "3"
    for y in range(ROWS):
        for x in range(COLS):
            if abs(x - cx) + abs(y - cy) == 3:
                grid[y][x] = "2"
    start = (cx, 0)          # primeira linha
    goal  = (cx, ROWS - 1)   # última linha
    grid[start[1]][start[0]] = "i"
    grid[goal[1]][goal[0]]   = "f"
    return grid, start, goal

my_map, start_xy, goal_xy = build_picture_map()

def enter_cost(cell):
    if cell == WALL or cell == OUT_OF_BOUNDS:
        return None
    if cell in (FREE, VISITED, "x", WIN, "i", "f"):
        return 1
    if isinstance(cell, str) and cell.isdigit():
        return int(cell)
    return 1

def neighbors(grid, x, y):
    for dx, dy in [(1,0), (0,-1), (-1,0), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            if grid[ny][nx] != WALL:
                yield (nx, ny)

def dijkstra(grid, start, goal):
    sx, sy = start
    gx, gy = goal
    INF = 10**9
    g = [[INF for _ in range(len(grid[0]))] for __ in range(len(grid))]
    parent = {}
    g[sy][sx] = 0
    heap = [(0, sx, sy)]
    while heap:
        cost_u, x, y = heapq.heappop(heap)
        if (x, y) == (gx, gy):
            break
        if cost_u > g[y][x]:
            continue
        for nx, ny in neighbors(grid, x, y):
            step = enter_cost(grid[ny][nx])
            if step is None:
                continue
            new_cost = cost_u + step
            if new_cost < g[ny][nx]:
                g[ny][nx] = new_cost
                parent[(nx, ny)] = (x, y)
                heapq.heappush(heap, (new_cost, nx, ny))
    if g[gy][gx] == INF:
        return None, INF
    path = []
    cur = (gx, gy)
    while cur != (sx, sy):
        path.append(cur)
        cur = parent[cur]
    path.append((sx, sy))
    path.reverse()
    return path, g[gy][gx]

def force_marks(grid, start, goal):
    sx, sy = start
    gx, gy = goal
    grid[sy][sx] = "i"
    grid[gy][gx] = "f"

my_pos = {"x": start_xy[0], "y": start_xy[1]}
path, total_cost = dijkstra(my_map, start_xy, goal_xy)

moves = 0
force_marks(my_map, start_xy, goal_xy)
out = ""
out += f"Movimentos: {moves}\n"
out += ut.draw_map(my_map, my_pos)

if path is None:
    out += "Sem caminho viável.\n"
else:
    for (x, y) in path[1:]:
        prev_x, prev_y = my_pos["x"], my_pos["y"]
        if (prev_x, prev_y) != start_xy and (prev_x, prev_y) != goal_xy:
            my_map[prev_y][prev_x] = VISITED
        my_pos["x"], my_pos["y"] = x, y
        force_marks(my_map, start_xy, goal_xy)
        if (x, y) == goal_xy:
            moves += 1
            out += f"Movimentos: {moves}\n"
            out += ut.draw_map(my_map, my_pos)
            out += f"Custo total (planejado): {total_cost}\n"
            break
        if (x, y) != start_xy and (x, y) != goal_xy:
            my_map[y][x] = "x"
        moves += 1
        force_marks(my_map, start_xy, goal_xy)
        out += f"Movimentos: {moves}\n"
        out += ut.draw_map(my_map, my_pos)

ut.log_map("etapa4A.txt", out)
print(out)