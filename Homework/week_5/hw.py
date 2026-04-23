import csv
import os

def create_board():
    return [[' ']*3 for _ in range(3)]

def print_board(board, scores, players):
    print(f"\n {players['X']} (X): {scores['X']} | {players['O']} (O): {scores['O']}\n")
    print("  1  2  3")
    for i, row in enumerate(board):
        print(f" {i+1} {row[0]} | {row[1]} | {row[2]}")
        if i < 2:
            print("  ---+---+---")
    print()

def check_winner(board, mark):
    for row in board:
        if all(c == mark for c in row):
            return True
    for col in range(3):
        if all(board[row][col] == mark for row in range(3)):
            return True
    if all(board[i][i] == mark for i in range(3)):
        return True
    if all(board[i][2-i] == mark for i in range(3)):
        return True
    return False

def is_tie(board):
    return all(board[r][c] != ' ' for r in range(3) for c in range(3))

def get_move(board, player_name, mark):
    while True:
        try:
            move = input(f" {player_name} ({mark}) - enter row and column (e.g. 1 2): ")
            row, col = map(int, move.split())
            if row < 1 or row > 3 or col <1 or col > 3:
                print(" Please enter numbers between 1 and 3.")
                continue
            if board[row-1][col-1] != ' ':
                print(" That cell is already taken, try again.")
                continue
            return row-1, col-1
        except (ValueError, IndexError):
            print(" Invalid input. Enter two numbers like: 1 2")

def save_scores(players, scores, filename="scores.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Player", "Mark", "Score"])
        writer.writerow([players['X'], 'X', scores['X']])
        writer.writerow([players['O'], 'O', scores['O']])
    print(f"\n Scores saved to {filename}")

def play_game():
    print("\n === TIC TAC TOE ===\n")
    players = {
        'X': input(" Enter name for X player: ").strip(),
        'O': input(" Enter name for O player: ").strip()
    }
    scores = {'X': 0, 'O': 0}
    current = 'X'

    while True:
        board = create_board()

        while True:
            print_board(board, scores, players)
            row, col = get_move(board, players[current], current)
            board[row][col] = current

            if check_winner(board, current):
                print_board(board, scores, players)
                scores[current] += 1
                print(f" *** {players[current]} wins! ***\n")
                break

            if is_tie(board):
                print_board(board, scores, players)
                print(" *** It's a tie! ***\n")
                break

            current = 'O' if current == 'X' else 'X'

        print(f" Scores - {players['X']}: {scores['X']} | {players['O']}: {scores['O']}\n")
        again = input(" Play again? (yes / no): ").strip().lower()
        if again != 'yes':
            save_scores(players, scores)
            print("\n Thanks for playing! Goodbye.\n")
            break
        current = 'X'

play_game()