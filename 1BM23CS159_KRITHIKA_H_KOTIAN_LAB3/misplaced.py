import heapq

goal_state = [1,2,3,8,0,4,7,6,5]

def h_misplaced(state):
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal_state[i])

def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]  

    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_index = r*3 + c
            new_state = state[:]
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            neighbors.append(new_state)
    return neighbors

def a_star(start_state):
    open_list = []
    visited = set()

    h = h_misplaced(start_state)
    heapq.heappush(open_list, (h, 0, start_state, [start_state]))

    while open_list:
        f, g, state, path = heapq.heappop(open_list)

        if state == goal_state:
            return path

        state_key = tuple(state)
        if state_key in visited:
            continue
        visited.add(state_key)

        for neighbor in get_neighbors(state):
            if tuple(neighbor) in visited:
                continue
            g_new = g + 1
            h_new = h_misplaced(neighbor)
            f_new = g_new + h_new
            heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))

    return None

if __name__ == "__main__":
    start_state = [2,8,3,1,6,4,7,0,5]

    path = a_star(start_state)
    print("\n--- Misplaced Tiles Heuristic ---")
    for step in path:
        for i in range(0, 9, 3):
            print(step[i:i+3])
        print()
