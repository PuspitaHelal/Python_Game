import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import sys

# ---------------- SOUND (NO FILES) ----------------
def play_sound(sound_type):
    if sys.platform == "win32":
        import winsound
        if sound_type == "win":
            winsound.Beep(1000, 200)
        elif sound_type == "lose":
            winsound.Beep(400, 300)
        elif sound_type == "tie":
            winsound.Beep(700, 200)
        elif sound_type == "click":
            winsound.Beep(900, 100)

# ---------------- GAME DATA ----------------
choices = ["Rock", "Paper", "Scissors"]
player_score = 0
computer_score = 0
rounds = 0
MAX_ROUNDS = 5

# ---------------- COLORS ----------------
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "white"
ROCK_COLOR = "#ff6b6b"
PAPER_COLOR = "#4dabf7"
SCISSORS_COLOR = "#51cf66"
HOVER_COLOR = "#333333"

# ---------------- DIFFICULTY ----------------
difficulty = "Easy"

def computer_pick(user_choice):
    if difficulty == "Easy":
        return random.choice(choices)

    if difficulty == "Medium":
        return random.choice(choices + [user_choice])

    # Hard = computer tries to win
    if user_choice == "Rock":
        return "Paper"
    if user_choice == "Paper":
        return "Scissors"
    return "Rock"

# ---------------- ANIMATION ----------------
def flash_button(btn, color):
    btn.config(bg="white")
    root.after(150, lambda: btn.config(bg=color))

# ---------------- GAME LOGIC ----------------
def play(user_choice):
    global player_score, computer_score, rounds

    if rounds >= MAX_ROUNDS:
        return

    play_sound("click")
    rounds += 1

    computer_choice = computer_pick(user_choice)

    if user_choice == computer_choice:
        result = "It's a Tie!"
        play_sound("tie")
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = "🎉 You Win!"
        player_score += 1
        play_sound("win")
    else:
        result = "😢 You Lose!"
        computer_score += 1
        play_sound("lose")

    score_label.config(
        text=f"{player_name}: {player_score}   Computer: {computer_score}"
    )
    round_label.config(text=f"Round: {rounds} / {MAX_ROUNDS}")

    messagebox.showinfo(
        "Result",
        f"Round {rounds}\n\n"
        f"{player_name} chose: {user_choice}\n"
        f"Computer chose: {computer_choice}\n\n{result}"
    )

    if rounds == MAX_ROUNDS:
        end_game()

def end_game():
    if player_score > computer_score:
        final = "🏆 You won the game!"
    elif player_score < computer_score:
        final = "😢 Computer won the game!"
    else:
        final = "🤝 Game Draw!"

    messagebox.showinfo(
        "Game Over",
        f"Final Score\n{player_name}: {player_score}\nComputer: {computer_score}\n\n{final}"
    )

    game_over_label.config(text=f"Game Over! {final}")
    disable_buttons()

def reset_game():
    global player_score, computer_score, rounds
    player_score = 0
    computer_score = 0
    rounds = 0
    score_label.config(text=f"{player_name}: 0   Computer: 0")
    round_label.config(text=f"Round: 0 / {MAX_ROUNDS}")
    game_over_label.config(text="")
    enable_buttons()

# ---------------- BUTTON STATES ----------------
def disable_buttons():
    rock_btn.config(state="disabled")
    paper_btn.config(state="disabled")
    scissors_btn.config(state="disabled")

def enable_buttons():
    rock_btn.config(state="normal")
    paper_btn.config(state="normal")
    scissors_btn.config(state="normal")

# ---------------- HOVER ----------------
def on_enter(e):
    e.widget.config(bg=HOVER_COLOR)

def on_leave(e, color):
    e.widget.config(bg=color)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("380x460")
root.configure(bg=BG_COLOR)

# Player Name
player_name = simpledialog.askstring("Player Name", "Enter your name:")
if not player_name:
    player_name = "Player"

# Difficulty
difficulty = simpledialog.askstring(
    "Difficulty",
    "Choose difficulty: Easy / Medium / Hard"
)
if difficulty not in ["Easy", "Medium", "Hard"]:
    difficulty = "Easy"

# Title
tk.Label(
    root,
    text="Rock Paper Scissors",
    font=("Arial", 16, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
).pack(pady=10)

# Score
score_label = tk.Label(
    root,
    text=f"{player_name}: 0   Computer: 0",
    font=("Arial", 11),
    fg="#ffd43b",
    bg=BG_COLOR
)
score_label.pack(pady=5)

round_label = tk.Label(
    root,
    text=f"Round: 0 / {MAX_ROUNDS}",
    font=("Arial", 10),
    fg="#adb5bd",
    bg=BG_COLOR
)
round_label.pack(pady=5)

# Buttons
rock_btn = tk.Button(
    root, text="Rock", width=15,
    font=("Arial", 11, "bold"),
    bg=ROCK_COLOR, fg="white", relief="flat",
    command=lambda: [flash_button(rock_btn, ROCK_COLOR), play("Rock")]
)
rock_btn.pack(pady=6)
rock_btn.bind("<Enter>", on_enter)
rock_btn.bind("<Leave>", lambda e: on_leave(e, ROCK_COLOR))

paper_btn = tk.Button(
    root, text="Paper", width=15,
    font=("Arial", 11, "bold"),
    bg=PAPER_COLOR, fg="white", relief="flat",
    command=lambda: [flash_button(paper_btn, PAPER_COLOR), play("Paper")]
)
paper_btn.pack(pady=6)
paper_btn.bind("<Enter>", on_enter)
paper_btn.bind("<Leave>", lambda e: on_leave(e, PAPER_COLOR))

scissors_btn = tk.Button(
    root, text="Scissors", width=15,
    font=("Arial", 11, "bold"),
    bg=SCISSORS_COLOR, fg="white", relief="flat",
    command=lambda: [flash_button(scissors_btn, SCISSORS_COLOR), play("Scissors")]
)
scissors_btn.pack(pady=6)
scissors_btn.bind("<Enter>", on_enter)
scissors_btn.bind("<Leave>", lambda e: on_leave(e, SCISSORS_COLOR))

# Game Over
game_over_label = tk.Label(
    root, text="", font=("Arial", 12, "bold"),
    fg="#ff8787", bg=BG_COLOR
)
game_over_label.pack(pady=10)

# Reset
tk.Button(
    root, text="Reset Game", width=15,
    font=("Arial", 10, "bold"),
    bg="#868e96", fg="white",
    relief="flat", command=reset_game
).pack(pady=5)

root.mainloop()
