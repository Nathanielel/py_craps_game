from .dice import Dice
from .bets.bet_manager import BetManager
from .player import Player

class CrapsGame:
    """
    Essentially the dealer. Moves the point on & off.
    Gives each player the oppurtunity to bet / join
    Cycles shooters after the current one 'sevens out'
    """
    def __init__(self, players: list[Player]) -> None:
        self.type = "human" # TODO: implement bot, mixed
        self.players = players
        self.bet_manager = BetManager()
        self.point = None
        # self.roller = players[0]
        # self.state = GameState()


    def play_turn(self):
        """
        For the current shooter:
        - roll the dice once
        - resolve bets
        - update the table
        """
        roll = next(Dice.roll())
        # if (4 <= roll[0] <= 6) or (8 <= roll[0] <= 10):
        #     self.point = roll[0]
        print(f"Rolled {roll[0]}!  ( as {roll[1][0]} & {roll[1][1]} )")

        self.bet_manager.resolve_bets(self.point, roll)
        
        if self.point and roll[0] == 7:
            if self.type != 'bot':
                want_add = input("New round, want to add more human players? (y/n) ") == 'y'
                while want_add:
                    name = input("Enter your name: ")
                    bal = input("Enter your starting bankroll (default 1000): ")
                    self.players.append(Player(name, bal))
                    want_add = input("Want to add more human players? (y/n) ") == 'y'
            self._next_roller()

        self.update_point(roll[0])
        

    def run(self):
        """
        Keep the game running while there are players with money to bet (or the point is ON)
        
        """
        # Game doesnt end until all players are bankrupt & the last point resolves
        while all([p.balance > 0 for p in self.players]) or self.point:
            for player in self.players:
                player.place_bets(self.point, self.bet_manager)
            self.play_turn()

    def update_point(self, rollsum):
        """
        Move the point between off and on as appropriate
        """
        if self.point:
            if rollsum in {7, self.point}:
                self.point = None
            return
        if rollsum in {4, 5, 6, 8 ,9, 10}:
            print(f"Point of {rollsum} established")
            self.point = rollsum

    def _next_roller(self):
        """
        When a roller 'sevens-out' with an established point, we shift rolling player
        """
        self.players = self.players[1:] + self.players[0:1]                