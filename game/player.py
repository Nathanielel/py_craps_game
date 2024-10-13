from math import inf
from game.bets.bet_manager import *

MENU_PROMPT = """\
Select an option, {}:
        (b) - Check [B]alance
        (c) - [C]urrent Bets
        (p) - [P]lace bet
        (r) - continue to [R]oll
        (s) - [S]tand / no more bets this round
        (q) - cash out / [Q]uit\n---> """


class HumanPlayer:
    """
    Human craps player class
    """
    bet_types = {
        "pass-line": PassLineBet,
        "dont-pass": DontPassBet,
        "single-roll": {
            "field": FieldBet,
            "any-craps": Bet,
            "seven": Bet,
            "eleven": Bet,
            "three": Bet,
            "doubles": {
                "boxcars": Bet,
                "snake-eyes": Bet,
            },
        },
        "lay": Bet,
        "buy": Bet,
        "come": ComeBet,
        "dont-come": Bet,
    }
    def __init__(self, name: int, balance: str | int):
        self.name = name
        if balance == "":
            self.balance = 1000
        else:
            self.balance = int(balance)
        self.active_bets = {}
        self.skip = False
        self.cashing_out = False

    def __str__(self) -> str:
        return self.name

    def play(self, point, manager):
        while True:
            action = self._menu()
            if action == "b":
                self.balance_chk()
            elif action == "p":
                self._place_bets(point, manager)
            elif action == "r":
                return
            elif action == "s":
                self.skip = True
                return
            elif action == "q":
                self.cashing_out = True
                self.skip = True
                return

    def balance_chk(self):
        print(f"You have ${self.balance} in your bankroll.")

    def award_winnings(self, won: int):
        print(f"YYAAAAYYY RECEIVING $$ {won} $$ !!!!")
        self.balance += won

    def _menu(self):
        choice = None
        if self.skip:
            return "r"
        while True:
            choice = input(MENU_PROMPT.format(self.name)
            ).lower()
            if choice not in ["p", "b", "c", "q", "r", "s"]:
                print("SELECT A VALID OPTION!")
                continue
            return choice

    def _place_bets(self, point: int | None, manager: BetManager):
        can_bet = self._available_bets(point)
        can_bet.add("cancel")
        choice = input(
            "what kind of bet would you like to place," f" {self.name}?\n  {can_bet}: "
        )
        while choice not in can_bet:
            print("Enter a Valid option")
            choice = input(f"what kind of bet would you like to place?\n\t{can_bet}: ")
        if choice == "cancel":
            return
        # TODO: handle single-roll bets (nested)
        wager = self._validated_bet("How much would you like to wager?")
        bet = HumanPlayer.bet_types[choice](self, wager)
        self.balance -= wager
        manager.place_bet(bet)


    def _available_bets(self, point: int | None) -> set[str]:
        names = set(HumanPlayer.bet_types.keys())
        if not point:
            return names - {"come", "dont-come"}
        return names - {"pass-line", "dont-pass"}

    def _validated_bet(self, prompt: str) -> int:
        """
        Get an integer bet from the user such that 0 <= bet <= self.balance
        """
        bet = inf
        if not prompt.endswith(" "):
            prompt += " "
        while True:
            try:
                bet = int(input(prompt))
            except ValueError:
                print("Must bet an integer value")
                continue

            if bet <= self.balance:
                break
            print(f"Only have {self.balance} to bet! Try again!")
        return bet
