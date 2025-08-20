import random
WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],[0, 3, 6], [1, 4, 7], [2, 5, 8],[0, 4, 8], [2, 4, 6]
]

def print_board(board):
    print()
    for i in range(3):
        row=board[i*3:(i+1)*3]
        print(" | ".join(row))
        if i < 2:
            print("-" * 9)
    print()

def check_winner(board, player):
    for combo in WINNING_COMBINATIONS:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_full(board):
    return all(cell != " " for cell in board)

def tic_tac_toe():
    board = [" "] * 9 
    human = "X"
    computer = "O"
    print("Welcome to Tic Tac Toe!")
    print("You are X, Computer is O.")
    print_board(board)
    while True:
        while True:
            try:
                move = int(input("Enter your move (1-9): ")) - 1
                if move < 0 or move > 8:
                    raise ValueError
                if board[move] == " ":
                    board[move]=human
                    break
                else:
                    print("Cell already taken. Try again.")
            except ValueError:
                print("Invalid input. Enter a number between 1-9.")
        print_board(board)
        if check_winner(board, human):
            print("You win!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        print("Computer's turn...")
        while True:
            move = random.randint(0, 8)
            if board[move] == " ":
                board[move] = computer
                break
        print_board(board)
        if check_winner(board, computer):
            print("Computer wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break


if __name__ == "__main__":
    tic_tac_toe()

