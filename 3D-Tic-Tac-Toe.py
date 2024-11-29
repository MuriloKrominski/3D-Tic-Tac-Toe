import tkinter as tk
from tkinter import messagebox
import webbrowser


class TicTacToe3D:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("3D Tic-Tac-Toe by Murilo Krominski")
        self.tabuleiro = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.turn = "X"
        self.score = {"X": 0, "O": 0, "Ties": 0}
        self.moves = 0

        self.setup_ui()
        self.update_score()

    def setup_ui(self):
        """Sets up the graphical interface."""
        self.frame_score = tk.Frame(self.root)
        self.frame_score.pack()

        self.score_label = tk.Label(
            self.frame_score,
            text="Score: X 0 vs O 0 | Ties: 0",
            font=("Arial", 14)
        )
        self.score_label.pack()

        self.frames_board = []
        for layer in range(3):
            frame = tk.LabelFrame(self.root, text=f"Layer {layer + 1}", padx=5, pady=5)
            frame.pack(side="left", padx=10, pady=10)
            self.frames_board.append(frame)
            for row in range(3):
                for col in range(3):
                    button = tk.Button(
                        frame,
                        text="",
                        font=("Arial", 20),
                        width=4,
                        height=2,
                        command=lambda l=layer, r=row, c=col: self.play(l, r, c)
                    )
                    button.grid(row=row, column=col)
                    self.tabuleiro[layer][row][col] = button

        self.reset_button = tk.Button(
            self.root,
            text="Restart Game",
            command=self.restart_game,
            font=("Arial", 12)
        )
        self.reset_button.pack(pady=10)

        self.footer_label = tk.Label(
            self.root,
            text="Created by Murilo Krominski\nhttps://murilokrominski.github.io",
            font=("Arial", 10),
            fg="blue",
            cursor="hand2"
        )
        self.footer_label.pack(pady=5)
        self.footer_label.bind("<Button-1>", lambda e: webbrowser.open("https://murilokrominski.github.io"))

    def update_score(self):
        """Updates the score displayed in the interface."""
        self.score_label.config(
            text=f"Score: X {self.score['X']} vs O {self.score['O']} | Ties: {self.score['Ties']}"
        )

    def play(self, layer, row, col):
        """Executes a move on the board."""
        button = self.tabuleiro[layer][row][col]
        if button["text"] == "":
            button.config(text=self.turn)
            self.moves += 1

            if self.check_winner():
                self.score[self.turn] += 1
                self.end_game(f"Congratulations! Player ({self.turn}) wins!")
                return

            if self.moves == 27:  # Board is full
                self.score["Ties"] += 1
                self.end_game("It's a tie! No one wins.")
                return

            # Alternate turn
            self.turn = "O" if self.turn == "X" else "X"
        else:
            messagebox.showwarning("Invalid Move", "This cell is already occupied!")

    def check_winner(self):
        """Checks if the current player has won."""
        # Check rows, columns, and diagonals in each layer
        for layer in range(3):
            for row in range(3):
                if all(self.tabuleiro[layer][row][col].cget("text") == self.turn for col in range(3)):
                    return True
            for col in range(3):
                if all(self.tabuleiro[layer][row][col].cget("text") == self.turn for row in range(3)):
                    return True
            if all(self.tabuleiro[layer][i][i].cget("text") == self.turn for i in range(3)):
                return True
            if all(self.tabuleiro[layer][i][2 - i].cget("text") == self.turn for i in range(3)):
                return True

        # Check 3D columns (same position in different layers)
        for row in range(3):
            for col in range(3):
                if all(self.tabuleiro[layer][row][col].cget("text") == self.turn for layer in range(3)):
                    return True

        # Check 3D diagonals
        if all(self.tabuleiro[i][i][i].cget("text") == self.turn for i in range(3)):
            return True
        if all(self.tabuleiro[i][i][2 - i].cget("text") == self.turn for i in range(3)):
            return True
        if all(self.tabuleiro[i][2 - i][i].cget("text") == self.turn for i in range(3)):
            return True
        if all(self.tabuleiro[i][2 - i][2 - i].cget("text") == self.turn for i in range(3)):
            return True

        # Check diagonals crossing layers (example in uploaded image)
        if all(self.tabuleiro[i][i][0].cget("text") == self.turn for i in range(3)):
            return True
        if all(self.tabuleiro[i][2 - i][0].cget("text") == self.turn for i in range(3)):
            return True
        if all(self.tabuleiro[i][i][2].cget("text") == self.turn for i in range(3)):
            return True
        if all(self.tabuleiro[i][2 - i][2].cget("text") == self.turn for i in range(3)):
            return True

        return False

    def end_game(self, message):
        """Ends the game and displays the result."""
        self.update_score()
        for layer in range(3):
            for row in range(3):
                for col in range(3):
                    self.tabuleiro[layer][row][col].config(state="disabled")
        messagebox.showinfo("Game Over", message)

    def restart_game(self):
        """Restarts the game for a new round."""
        self.turn = "X"
        self.moves = 0
        for layer in range(3):
            for row in range(3):
                for col in range(3):
                    button = self.tabuleiro[layer][row][col]
                    button.config(text="", state="normal")

    def start(self):
        """Starts the main event loop for the graphical interface."""
        self.root.mainloop()


# Start the game
if __name__ == "__main__":
    game = TicTacToe3D()
    game.start()
