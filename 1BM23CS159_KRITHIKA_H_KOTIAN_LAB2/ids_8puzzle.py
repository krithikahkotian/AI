from collections import deque
MOVE_SET = [("up", -3), ("left", -1), ("right", 1), ("down", 3)]
def is_valid(pos, move_name):
    if move_name == "left" and pos % 3 == 0:
        return False
    if move_name == "right" and pos % 3 == 2:
        return False
    if move_name == "up" and pos < 3:
        return False
    if move_name == "down" and pos > 5:
        return False
    return True

def get_neighbors(state):
    zero_pos = state.index(0)
    neighbors = []
    for name, delta in MOVE_SET:
        if is_valid(zero_pos, name):
            new_pos = zero_pos + delta
            ns = list(state)
            ns[zero_pos], ns[new_pos] = ns[new_pos], ns[zero_pos]
            neighbors.append((name, tuple(ns)))
    return neighbors

def is_solvable(state):
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2 == 0

def dls(node, goal, depth, path, visited):
    if node == goal:
        return path    
    if depth == 0:
        return None
    for move, nb in get_neighbors(node):
        if nb not in visited:
            visited.add(nb)
            result = dls(nb, goal, depth - 1, path + [(move, nb)], visited)
            if result is not None:
                return result
            visited.remove(nb) 
    return None

def ids(start, goal, max_depth=20):
    if not is_solvable(start):
        return None  
    for depth in range(max_depth + 1):
        visited = set([start])
        path = dls(start, goal, depth, [("start", start)], visited)
        if path is not None:
            return path
    return None


start = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)

goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

solution = ids(start, goal, max_depth=20)

if solution:
    for step, (move, state) in enumerate(solution):
        print(f"Step {step}: {move}")
        print(state[0:3])
        print(state[3:6])
        print(state[6:9])
        print()
else:
    print("No solution found (or exceeds max_depth).")
