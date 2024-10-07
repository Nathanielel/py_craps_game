from ui.human_interface import start_human_game, join_human_game


import inspect
import builtins
pyprint = builtins.print
def custom_print(*args, **kwargs):
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    pyprint(f"[{filename}:{lineno}]\t", *args, **kwargs)

# Override the default print
builtins.print = custom_print

# Example usage:
print("This is a test message.")

if __name__ == "__main__":
    players = []
    print("Welcome to the game of Craps!")
    print(f"players at the table: {players}")
    start_human_game()
    # else:
    #     join_human_game(game_in_progress, name, bal)

