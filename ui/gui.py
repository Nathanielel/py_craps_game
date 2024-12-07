import tkinter as tk
from tkinter import messagebox
from game.core import CrapsGame
from game.player import HumanPlayer
from game.bets import *
class CrapsGUI:
    def __init__(self, master):
        self.master = master
        master.title("Craps Game")

        # Initialize game
        self.players = [HumanPlayer("Player 1", 1000), HumanPlayer("Player 2", 1000)]
        self.game = CrapsGame(self.players)

        # Bet amount label and entry (initialized but not displayed until needed)
        self.bet_amount_label = tk.Label(self.master, text="Bet Amount:")
        self.bet_amount_entry = tk.Entry(self.master)
        # Setup GUI elements
        self.setup_player_info()
        self.setup_main_controls()
        self.update_display()

        # # Entry for bet amount
        # tk.Label(self.master, text="Bet Amount:").grid(row=4, column=0)
        # self.bet_amount_entry = tk.Entry(self.master)

    def setup_player_info(self):
        """Display each player's bankroll and current bets."""
        self.player_info_frames = []
        for i, player in enumerate(self.players):
            frame = tk.Frame(self.master)
            frame.grid(row=i, column=0, sticky="W")
            tk.Label(frame, text=f"{player.name}: ${player.balance}").pack()
            self.player_info_frames.append(frame)

    def setup_main_controls(self):
        """Set up initial Place Bet and Roll buttons."""
        # Main controls frame to hold "Place Bet" and "Roll" buttons
        self.main_controls_frame = tk.Frame(self.master)
        self.main_controls_frame.grid(row=3, column=0, columnspan=2)

        # "Place Bet" button
        self.place_bet_button = tk.Button(self.main_controls_frame, text="Place Bet", command=self.show_bet_options)
        self.place_bet_button.grid(row=0, column=0, padx=5, pady=5)

        # "Roll" button
        self.roll_button = tk.Button(self.main_controls_frame, text="Roll", command=self.roll_dice)
        self.roll_button.grid(row=0, column=1, padx=5, pady=5)


        # Frame to hold dynamic bet buttons
        self.bet_controls_frame = tk.Frame(self.master)
        self.bet_controls_frame.grid(row=5, column=0, columnspan=2)

    def show_bet_options(self):
        """Show specific bet options and hide Place Bet and Roll buttons."""
        # Hide main controls by removing them from the grid
        self.main_controls_frame.grid_remove()

        # Display dynamic bet buttons for the first player (or selected player)
        self.create_dynamic_bet_buttons(self.players[0])

        # Show the bet amount entry field and label
        self.bet_amount_label.grid(row=4, column=0, padx=5, pady=5)
        self.bet_amount_entry.grid(row=4, column=1, padx=5, pady=5)


    def create_dynamic_bet_buttons(self, player):
        """Clear existing buttons and create new ones based on available bets."""
        # Clear any existing widgets in the bet controls frame
        for widget in self.bet_controls_frame.winfo_children():
            widget.destroy()

        # Create a button for each available bet
        available_bets = player._available_bets(self.game.point)
        for i, bet_type in enumerate(available_bets):
            button = tk.Button(self.bet_controls_frame, text=bet_type, command=lambda bt=bet_type: self.place_bet(bt, player))
            button.grid(row=0, column=i, padx=5, pady=5)


        # self.bet_amount_entry.grid(row=4, column=1)
        # Back button to return to Place Bet and Roll options
        back_button = tk.Button(self.bet_controls_frame, text="Back", command=self.show_main_controls)
        back_button.grid(row=1, column=0, columnspan=len(available_bets), pady=5)

    def place_bet(self, bet_type, player):
        """Handle bet placement for the selected bet type."""
        try:
            bet_amount = int(self.bet_amount_entry.get())
            if bet_amount > player.balance:
                raise ValueError("Insufficient balance.")

            # Place the bet based on bet type
            if bet_type == "Pass Line":
                self.game.bet_manager.place_bet(player.place_bet(bet_amount))
            elif bet_type == "Come":
                self.game.bet_manager.place_bet(player.place_bet(bet_amount))
            elif bet_type == "Field":
                self.game.bet_manager.place_bet(player.place_bet(bet_amount))
            # Add other bet types similarly...

            # Update display after placing bet
            self.update_display()

        except ValueError as e:
            tk.messagebox.showerror("Invalid Bet", str(e))

    def show_main_controls(self):
        """Return to main controls with Place Bet and Roll buttons."""
        # Clear dynamic bet buttons
        for widget in self.bet_controls_frame.winfo_children():
            widget.destroy()
        # Hide the bet amount entry field and label
        self.bet_amount_label.grid_remove()
        self.bet_amount_entry.grid_remove()
        # Show main controls by putting them back in the grid
        self.main_controls_frame.grid()

    def roll_dice(self):
        """Roll dice and update the game state."""
        self.game._shoot()  # Assume Player 1 for simplicity
        self.update_display()

    def update_display(self):
        """Update GUI with current game state."""
        for frame, player in zip(self.player_info_frames, self.players):
            for widget in frame.winfo_children():
                widget.destroy()
            tk.Label(frame, text=f"{player.name}: ${player.balance}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = CrapsGUI(root)
    root.mainloop()