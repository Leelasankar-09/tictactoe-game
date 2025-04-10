import tkinter as tk
from tkinter import messagebox
import random

# Global variables
player1 = ""
player2 = ""
player = "X"
player1_score = 0
player2_score = 0
time_left = 10
board_size = 3
board = []
buttons = []

# Functions
def check_winner(board):
    size = len(board)
    for i in range(size):
        if all(board[i][j] == player for j in range(size)):
            return [(i, j) for j in range(size)]
        if all(board[j][i] == player for j in range(size)):
            return [(j, i) for j in range(size)]
    if all(board[i][i] == player for i in range(size)):
        return [(i, i) for i in range(size)]
    if all(board[i][size - 1 - i] == player for i in range(size)):
        return [(i, size - 1 - i) for i in range(size)]
    return None

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def update_turn_label():
    turn_label.config(text=f"Player {player1 if player == 'X' else player2}'s Turn ({player})")

def update_score(winner):
    global player1_score, player2_score
    if winner == "X":
        player1_score += 1
    elif winner == "O":
        player2_score += 1
    score_label.config(text=f"{player1}: {player1_score} | {player2}: {player2_score}")

def restart_game():
    global board, player, time_left
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
    player = "X"
    time_left = 10
    timer_label.config(text=f"Time left: {time_left}s")
    update_turn_label()
    for i in range(board_size):
        for j in range(board_size):
            buttons[i][j].config(text=' ', state=tk.NORMAL, bg="#ecf0f1")

def countdown():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time left: {time_left}s")
        root.after(1000, countdown)
    else:
        skip_turn()

def skip_turn():
    global player, time_left
    messagebox.showinfo("Time's Up!", f"Player {player} ran out of time! Turn skipped.")
    player = "O" if player == "X" else "X"
    update_turn_label()
    time_left = 10
    countdown()

def ai_move():
    empty_cells = [(i, j) for i in range(board_size) for j in range(board_size) if board[i][j] == ' ']
    if empty_cells:
        row, col = random.choice(empty_cells)
        on_click(row, col)

def on_click(row, col):
    global player, time_left
    if board[row][col] == ' ':
        symbol = "❌" if theme_var.get() == "Emoji" and player == "X" else "⭕" if theme_var.get() == "Emoji" and player == "O" else player
        buttons[row][col].config(text=symbol, state=tk.DISABLED, bg="#34495e" if player == "X" else "#e74c3c", fg="white")
        board[row][col] = player

        winning_combination = check_winner(board)
        if winning_combination:
            for (i, j) in winning_combination:
                buttons[i][j].config(bg="lightgreen")
            messagebox.showinfo("Game Over", f"Player {player1 if player == 'X' else player2} wins!")
            update_score(player)
            restart_game()
            return

        elif is_board_full(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            restart_game()
            return

        player = "O" if player == "X" else "X"
        update_turn_label()

        if mode_var.get() == "Single Player" and player == "O":
            ai_move()

        time_left = 10
        countdown()

def start_game():
    global player1, player2, board_size, board, buttons
    player1 = entry1.get().strip() or "Player X"
    player2 = entry2.get().strip() or "Player O"
    
    label1.destroy()
    label2.destroy()
    entry1.destroy()
    entry2.destroy()
    start_button.destroy()
    title_label.destroy()
    mode_frame.destroy()
    size_frame.destroy()
    theme_frame.destroy()

    board_size = board_size_var.get()
    create_board()
    update_turn_label()
    update_score(None)
    countdown()

def create_board():
    global buttons, board
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
    buttons_frame = tk.Frame(root, bg="#2c3e50")
    buttons_frame.grid(row=3, column=0, columnspan=3, pady=10)

    buttons = [[tk.Button(buttons_frame, text=' ', font=('Arial', 24, 'bold'), width=4, height=2,
                          bg="#ecf0f1", fg="#2c3e50", activebackground="#bdc3c7",
                          command=lambda i=i, j=j: on_click(i, j))
                for j in range(board_size)] for i in range(board_size)]

    for i in range(board_size):
        for j in range(board_size):
            buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

    reset_button = tk.Button(root, text="Reset Game", font=('Arial', 12, 'bold'),
                            bg="#3498db", fg="white", command=restart_game)
    reset_button.grid(row=4, column=0, columnspan=3, pady=10)

# GUI Setup
root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(bg="#2c3e50")
root.geometry("500x600")

# Title
title_label = tk.Label(root, text="Tic Tac Toe", font=('Arial', 24, 'bold'), bg="#2c3e50", fg="#ecf0f1")
title_label.grid(row=0, column=0, columnspan=3, pady=20)

# Player name input fields
label1 = tk.Label(root, text="Player X Name:", font=('Arial', 14), bg="#2c3e50", fg="#ecf0f1")
label1.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry1 = tk.Entry(root, font=('Arial', 12), bg="#ecf0f1", fg="#2c3e50", width=15)
entry1.grid(row=1, column=1, padx=10, pady=5)

label2 = tk.Label(root, text="Player O Name:", font=('Arial', 14), bg="#2c3e50", fg="#ecf0f1")
label2.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry2 = tk.Entry(root, font=('Arial', 12), bg="#ecf0f1", fg="#2c3e50", width=15)
entry2.grid(row=2, column=1, padx=10, pady=5)

# Mode Selection
mode_frame = tk.Frame(root, bg="#2c3e50")
mode_frame.grid(row=3, column=0, columnspan=3, pady=10)
mode_var = tk.StringVar(value="Two Player")
mode_label = tk.Label(mode_frame, text="Select Mode:", font=('Arial', 12), bg="#2c3e50", fg="#ecf0f1")
mode_label.grid(row=0, column=0, padx=5)
tk.Radiobutton(mode_frame, text="Single Player", variable=mode_var, value="Single Player", bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e").grid(row=0, column=1)
tk.Radiobutton(mode_frame, text="Two Player", variable=mode_var, value="Two Player", bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e").grid(row=0, column=2)

# Board Size Selection
size_frame = tk.Frame(root, bg="#2c3e50")
size_frame.grid(row=4, column=0, columnspan=3, pady=10)
board_size_var = tk.IntVar(value=3)
size_label = tk.Label(size_frame, text="Select Board Size:", font=('Arial', 12), bg="#2c3e50", fg="#ecf0f1")
size_label.grid(row=0, column=0, padx=5)
size_dropdown = tk.OptionMenu(size_frame, board_size_var, 3, 4, 5)
size_dropdown.config(bg="#ecf0f1", fg="#2c3e50")
size_dropdown.grid(row=0, column=1)

# Theme Selection
theme_frame = tk.Frame(root, bg="#2c3e50")
theme_frame.grid(row=5, column=0, columnspan=3, pady=10)
theme_var = tk.StringVar(value="Text")
theme_label = tk.Label(theme_frame, text="Select Theme:", font=('Arial', 12), bg="#2c3e50", fg="#ecf0f1")
theme_label.grid(row=0, column=0, padx=5)
tk.Radiobutton(theme_frame, text="Text", variable=theme_var, value="Text", bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e").grid(row=0, column=1)
tk.Radiobutton(theme_frame, text="Emoji", variable=theme_var, value="Emoji", bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e").grid(row=0, column=2)

# Start Button
start_button = tk.Button(root, text="Start Game", font=('Arial', 14, 'bold'), bg="#e67e22", fg="white", command=start_game)
start_button.grid(row=6, column=0, columnspan=3, pady=20)

# Game Info Labels
score_label = tk.Label(root, text="", font=('Arial', 16), bg="#2c3e50", fg="#ecf0f1")
score_label.grid(row=1, column=0, columnspan=3)
turn_label = tk.Label(root, text="", font=('Arial', 16), bg="#2c3e50", fg="#ecf0f1")
turn_label.grid(row=2, column=0, columnspan=3)
timer_label = tk.Label(root, text=f"Time left: {time_left}s", font=('Arial', 16), bg="#2c3e50", fg="#ecf0f1")
timer_label.grid(row=5, column=0, columnspan=3)

root.mainloop()