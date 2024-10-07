from math import inf
from game.bets.bet_manager import *


class Player:
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

    def __str__(self) -> str:
        return self.name

    def place_bets(self, point: int | None, manager: BetManager):
        while True:
            choice = input(f"care to place another bet, {self.name}? ")
            if choice != 'y':
                return
            can_bet = self._available_bets(point)
            choice = input("what kind of bet would you like to place,"
                        f" {self.name}?\n  {can_bet}: ")
            while choice not in can_bet:
                print("Enter a Valid option")
                choice = input(f"what kind of bet would you like to place?\n\t{can_bet}: ")
            # TODO: handle single-roll bets (nested)
            wager = self._validated_bet("How much would you like to wager?")
            bet = Player.bet_types[choice](self, wager)
            manager.place_bet(bet)
            choice = input(f"care to place another bet, {self.name}? ")
            if choice != 'y':
                return

        # bet = self._validated_bet(f"{self}, enter your pass-line bet: ")
        # print(f"Bet placed: {bet}")
        # self.balance -= bet
        # return bets

    def award_winnings(self, won: int):
        print(f"YYAAAAYYY RECEIVING $$ {won} $$ !!!!")
        self.balance += won

    def _available_bets(self, point: int | None) -> set[str]:
        names = set(Player.bet_types.keys())
        if not point:
            return names - {"come", "dont-come"}
        return names - {"pass-line", "dont-pass"}

    def _validated_bet(self, prompt: str) -> int:
        """
        Get an integer bet from the user such that 0 <= bet <= self.balance
        """
        bet = inf
        if not prompt.endswith(' '):
            prompt += ' '
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
