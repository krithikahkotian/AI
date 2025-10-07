import random

# ----------------------------------------------------------
# Function to calculate number of attacking pairs
# ----------------------------------------------------------
def compute_attacking_pairs(state):
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            # same column
            if state[i] == state[j]:
                attacks += 1
            # same diagonal
            elif abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks


# ----------------------------------------------------------
# Generate all neighbors by moving one queen in its column
# ----------------------------------------------------------
def get_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if state[col] != row:
                new_state = state[:]
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors


# ----------------------------------------------------------
# Basic Hill Climbing search
# ----------------------------------------------------------
def hill_climbing(initial_state):
    current = initial_state
    while True:
        neighbors = get_neighbors(current)
        neighbor = min(neighbors, key=lambda s: compute_attacking_pairs(s))
        if compute_attacking_pairs(neighbor) >= compute_attacking_pairs(current):
            return current
        current = neighbor


# ----------------------------------------------------------
# Hill Climbing with Random Restarts
# ----------------------------------------------------------
def hill_climbing_with_restarts(n=4, max_restarts=100):
    for restart in range(max_restarts):
        current = [random.randint(0, n - 1) for _ in range(n)]  # random start
        while True:
            neighbors = get_neighbors(current)
            neighbor = min(neighbors, key=lambda s: compute_attacking_pairs(s))
            if compute_attacking_pairs(neighbor) >= compute_attacking_pairs(current):
                break
            current = neighbor

        # Check if we found a solution
        if compute_attacking_pairs(current) == 0:
            print(f"Solution found after {restart + 1} restart(s)!")
            return current

    print("No solution found within restart limit.")
    return None


# ----------------------------------------------------------
# Print board nicely
# ----------------------------------------------------------
def print_board(state):
    n = len(state)
    print("-" * (5 * n + 1))
    for row in range(n):
        line = "|"
        for col in range(n):
            if state[col] == row:
                line += " Q  |"  # show queen
            else:
                line += " .. |"
        print(line)
        print("-" * (5 * n + 1))
    print("\n")


# ----------------------------------------------------------
# Example usage
# ----------------------------------------------------------
if __name__ == "__main__":
    # You can start from a fixed state
    initial_state = [3, 1, 2, 0]
    print("Initial State:", initial_state, "with", compute_attacking_pairs(initial_state), "attacks")
    print_board(initial_state)

    

    # Run hill climbing with random restarts
    print("=== Running Hill Climbing with Random Restarts ===")
    solution = hill_climbing_with_restarts(n=4, max_restarts=100)
    if solution:
        print("Final State:", solution, "with", compute_attacking_pairs(solution), "attacks")
        print_board(solution)
