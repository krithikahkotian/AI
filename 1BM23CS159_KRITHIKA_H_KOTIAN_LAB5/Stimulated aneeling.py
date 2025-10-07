import math
import random

# Function to calculate number of attacking pairs
def compute_attacking_pairs(state):
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i+1, n):
            # same column
            if state[i] == state[j]:
                attacks += 1
            # same diagonal
            elif abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

# Generate a random neighbor by moving one queen
def random_neighbor(state):
    n = len(state)
    neighbor = state[:]
    col = random.randint(0, n-1)  # choose a random column
    row = random.randint(0, n-1)  # choose a random row
    neighbor[col] = row
    return neighbor

# Simulated Annealing algorithm
def simulated_annealing(initial_state, T=1000, cooling_rate=0.99):
    current = initial_state
    while T > 0.1:
        next_state = random_neighbor(current)
       
        deltaE = compute_attacking_pairs(current) - compute_attacking_pairs(next_state)
       
        if deltaE > 0:  # better solution
            current = next_state
        else:
            # accept worse solution with probability
            prob = math.exp(deltaE / T)
            if random.random() < prob:
                current = next_state
       
        # decrease temperature
        T = T * cooling_rate
   
    return current

# Print board
def print_board(state):
    n = len(state)
    for row in range(n):
        line = "|"
        for col in range(n):
            if state[col] == row:
                line += " Q |"
            else:
                line += " - |"
        print(line)
    print("\n")

# Example usage
if __name__ == "__main__":
    n = 8
    initial_state = [random.randint(0, n-1) for _ in range(n)]
    print("Initial State:", initial_state, "with", compute_attacking_pairs(initial_state), "attacks")
    print_board(initial_state)

    solution = simulated_annealing(initial_state)

    print("Final State:", solution, "with", compute_attacking_pairs(solution), "attacks")
    print_board(solution)
