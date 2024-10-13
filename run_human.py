from ui.human_interface import start_human_game, join_human_game

###
# Comment this out to remove filenames & line-numbers from log output
import builtins, inspect, os

pyprint = builtins.print


def custom_print(*args, **kwargs):
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    pyprint(f"[{os.path.relpath(filename)}:{lineno}]\t", *args, **kwargs)


# Override the default print
builtins.print = custom_print
###


# Example usage:
print("This is a test message.")

if __name__ == "__main__":
    players = []
    print("Welcome to the game of Craps!")
    start_human_game()
    # else:
    #     join_human_game(game_in_progress, name, bal)
