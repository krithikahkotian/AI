import sys
import io
import math

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# --------------------------------------------
# Define the game tree structure
# --------------------------------------------
game_tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['L1', 'L2'],
    'E': ['L3', 'L4'],
    'F': ['L5', 'L6'],
    'G': ['L7', 'L8'],
    'L1': 10,
    'L2': 9,
    'L3': 14,
    'L4': 18,
    'L5': 5,
    'L6': 4,
    'L7': 50,
    'L8': 3
}

# --------------------------------------------
# Pretty print the game tree as ASCII art
# --------------------------------------------
def print_tree():
    print("\nGame Tree Structure:\n")
    print("                A (MAX)")
    print("              /        \\")
    print("           B (MIN)       C (MIN)")
    print("          /     \\        /     \\")
    print("       D (MAX)  E (MAX)  F (MAX)  G (MAX)")
    print("      /   \\     /   \\     /   \\     /   \\")
    print("    10    9   14   18   5    4   50    3")
    print("\n" + "="*80 + "\n")


# --------------------------------------------
# Alpha-Beta Pruning Implementation (with detailed trace)
# --------------------------------------------
def alphabeta(node, depth, alpha, beta, maximizing_player):
    indent = "  " * depth  # indentation for better readability

    # If leaf node
    if isinstance(game_tree[node], int):
        print(f"{indent}Reached leaf {node} with value {game_tree[node]}")
        return game_tree[node]

    # MAX node
    if maximizing_player:
        print(f"{indent}Exploring MAX node {node} (depth={depth}), alpha={alpha}, beta={beta}")
        max_eval = -math.inf
        for child in game_tree[node]:
            print(f"{indent}--> Exploring child {child} of {node}")
            eval = alphabeta(child, depth + 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            print(f"{indent}Updated MAX node {node}: value={max_eval}, alpha={alpha}, beta={beta}")
            if beta <= alpha:
                print(f"{indent}!!! PRUNING at MAX node {node} (beta={beta} <= alpha={alpha})")
                break
        return max_eval

    # MIN node
    else:
        print(f"{indent}Exploring MIN node {node} (depth={depth}), alpha={alpha}, beta={beta}")
        min_eval = math.inf
        for child in game_tree[node]:
            print(f"{indent}--> Exploring child {child} of {node}")
            eval = alphabeta(child, depth + 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            print(f"{indent}Updated MIN node {node}: value={min_eval}, alpha={alpha}, beta={beta}")
            if beta <= alpha:
                print(f"{indent}!!! PRUNING at MIN node {node} (beta={beta} <= alpha={alpha})")
                break
        return min_eval


# --------------------------------------------
# Run the algorithm
# --------------------------------------------
if __name__ == "__main__":
    print_tree()
    print("Starting Alpha-Beta Pruning...\n")
    print("="*80 + "\n")

    best_value = alphabeta('A', 0, -math.inf, math.inf, True)

    print("\n" + "="*80)
    print(f"RESULT: Best achievable value at root (A): {best_value}")
    print("="*80)