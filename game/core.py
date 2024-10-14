from .dice import Dice
from .bets.bet_manager import BetManager
from .player import HumanPlayer

DEBUG = False

class CrapsGame:
    """
    Essentially the dealer. Moves the point on & off.
    Gives each player the oppurtunity to bet / join
    Cycles shooters after the current one 'sevens out'
    """

    def __init__(self, players: list[HumanPlayer]) -> None:
        self.type = "human"  # TODO: implement bot, mixed
        self.players = players
        self.bet_manager = BetManager()
        self.point = None

    def _shoot(self):
        """
        For the current shooter:
        - roll the dice once
        - resolve bets
        - update the table
        """
        roll = next(Dice.roll())
        print(f"Rolled {roll[0]}!  ( as {roll[1][0]} & {roll[1][1]} )")

        self.bet_manager.resolve_bets(self.point, roll)


        if self.point and roll[0] == 7:
            self._next_roller()

        self._update_point(roll[0])

    def _cashout(self):
        """
        Currently only able to leave the table when the point is off
        """
        if not self.point:
            here = self.players[:]
            for p in here:
                if p.cashing_out:
                    print(f"{p} leaves the table with {p.balance}!")
                    self.players.remove(p)

    def _add_human_players(self):
        want_add = input("New round, want to add more human players? (y/n) ") == "y"
        while want_add:
            name = input("Enter your name: ")
            bal = input("Enter your starting bankroll (default 1000): ")
            self.players.append(HumanPlayer(name, bal))
            want_add = input("Want to add more human players? (y/n) ") == "y"

    def _update_point(self, rollsum):
        """
        Move the point between off and on as appropriate
        """
        if self.point:
            if rollsum in {7, self.point}:
                for p in self.players:
                    p.skip = False
                self.point = None
            return
        if rollsum in {4, 5, 6, 8, 9, 10}:
            print(f"Point of {rollsum} established")
            self.point = rollsum

    def _next_roller(self):
        """
        When a roller 'sevens-out' with an established point, we shift rolling player
        """
        self.players = self.players[1:] + self.players[0:1]


    def run(self):
        """
        Keep the game running while there are players with money to bet (or the point is ON)
        """
        # Game doesnt end until all players are bankrupt & the last point resolves
        while (all([p.balance > 0 for p in self.players])) or self.point:
            print(f"players at the table: {[str(p) for p in self.players ]}")

            if self.type != "bot" and not self.point:
                self._add_human_players()
            
            for player in self.players:
                player.play(self.point, self.bet_manager)
            
            self._cashout()
            if not self.players: return  # Everybody left

            self._shoot()
            print(f"Point is {self.point}!")