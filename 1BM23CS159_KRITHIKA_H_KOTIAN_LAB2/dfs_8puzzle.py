from collections import deque
moves = {
    "up": -3,
    "down": 3,
    "left": -1,
    "right": 1
}
def is_valid(pos, move):
    if move == "left" and pos % 3 == 0:
        return False
    if move == "right" and pos % 3 == 2:
        return False
    if move == "up" and pos < 3:
        return False
    if move == "down" and pos > 5:
        return False
    return True

def get_neighbors(state):
    neighbors = []
    zero_pos = state.index(0)

    for move, delta in moves.items():
        if is_valid(zero_pos, move):
            new_pos = zero_pos + delta
            new_state = list(state)
            new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
            neighbors.append(tuple(new_state))
    return neighbors

def dfs(start, goal):
    stack = [(start, [start])] 
    visited = set()
    while stack:
        state, path = stack.pop()
        if state == goal:
            return path 
        if state in visited:
            continue
        visited.add(state)
        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return None 


if __name__ == "__main__":
    start = (1, 2, 3,
             4, 0, 6,
             7, 5, 8)
    goal = (1, 2, 3,
            4, 5, 6,
            7, 8, 0)
    solution = dfs(start, goal)
    if solution:
        print("Solution found in", len(solution) - 1, "moves:")
        print(goal[0:3])
        print(goal[3:6])
        print(goal[6:9])
        '''for step in solution:
            print(step[0:3])
            print(step[3:6])
            print(step[6:9])
            print()'''
    else:
        print("No solution found.")


