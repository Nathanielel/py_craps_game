# from .game_state import GameState
from math import floor

class BetManager:
    """
    Tracks bets. Knows rules, how to pay them out.
    """


    def __init__(self):
        self.bets = []

    def place_bet(self, bet):
        self.bets.append(bet)

    def current_bets(self, player):
        print(f"{player}'s current bets:")
        for bet in self.bets:
            if bet.player == player:
                print(bet)
        

    def resolve_bets(self, point: int | None, roll: tuple[int, tuple[int, int]]):
        """
        Resolves all bets based on the current roll & game state (come-out or point round)
        
        Args:
        - point: current point
        - roll: (SUM , (die1, die2))
        """
        res = []
        print("Active bets:")
        for bet in self.bets: print( f"{bet}")

        for bet in self.bets:
            res = bet.resolve(roll, point)
            print(f"Resolution of {bet}: {('continued', 'WON', 'LOST')[res]}")
        self.bets = [b for b in self.bets if not b.resolved]


WIN = 1
BAR = -1
LOSE = -1

class Bet:
    def __init__(self, player, amount):
        self.player = player  # The player placing the bet
        self.amount = amount  # The amount of the bet
        self.resolved = False

    def __str__(self) -> str:
        return f"{self.player.name} wagers {self.amount}"

    def _award_winnings(self, payout_ratio):
        bet = self.amount
        won = floor(payout_ratio * bet) + bet
        print(f"Awarding {self.player.name} with ${won}")
        self.player.award_winnings(won)

    def would_resolve(self, rollsum: int = 1, point: int = 1) -> bool:
        raise NotImplementedError

    def resolve(self, dice_sum, point):
        """ Resolve the bet based on the dice roll and the game state.
        This should be overridden by subclasses for specific bets. """
        raise NotImplementedError
    
class PassLineBet(Bet):
    def __str__(self) -> str:
        return super().__str__() + " -- @ PASS"

    def would_resolve(self, rollsum: int = 1, point: int = 1) -> bool:
        return point is not None and rollsum not in {2, 3, 7, 11, 12}
    
    def resolve(self, roll, point) -> int:
        """Resolve a Pass Line bet based on dice roll and game state."""
        dice_sum = roll[0]
        if not point:
            # Come-out roll rules
            if dice_sum in {7, 11}:  # Win on 7 or 11
                self.resolved = True
                self._award_winnings(1/1)
                return WIN
            elif dice_sum in {2, 3, 12}:  # Lose on 2, 3, 12
                self.resolved = True
                return LOSE
        else:
            # Point phase rules
            if dice_sum == point:  # Win if point is hit
                self.resolved = True
                self._award_winnings(1/1)
                return WIN
            elif dice_sum == 7:  # Lose if 7 is rolled
                self.resolved = True
                return LOSE
        return 0

class DontPassBet(Bet):
    def __str__(self) -> str:
        return super().__str__() + " -- @ NO-PASS"
    
    def would_resolve(self, rollsum: int = 1, point: int = 1) -> bool:
        return point is not None and rollsum not in {2, 3, 7, 11, 12}

    def resolve(self, roll, point):
        """Resolve a Don't Pass bet based on dice roll and game state."""
        dice_sum = roll[0]
        if not point:
            if dice_sum in {2, 3}:  # Win on 2 or 3
                self._award_winnings(1/1)
                return WIN
            elif dice_sum == 7 or dice_sum == 11:  # Lose on 7 or 11
                return LOSE
            elif dice_sum == 12:  # Push on 12
                return "push"
        else:
            if dice_sum == 7:  # Win if 7 is rolled
                self._award_winnings(1/1)
                return WIN
            elif dice_sum == point:  # Lose if point is hit
                return LOSE
        self._award_winnings(0)
        return "push"

class ComeBet(Bet):
    def __init__(self, player, amount):
        super().__init__(player, amount)
        self.point = None  # The Come bet's own point
    
    def __str__(self) -> str:
        return super().__str__() + f" -- @ COME -- Come-Point: {self.point}"
    
    def would_resolve(self, rollsum: int = 1, point: int = 1) -> bool:
        return True

    def resolve(self, roll, point):
        """Resolve a Come bet. Works like a Pass Line bet after the come-out roll."""
        dice_sum = roll[0]
        if self.point is None:
            # Come-out roll for the Come bet
            if dice_sum in {7, 11}:  # Win on 7 or 11
                self.resolved = True
                self._award_winnings(1/1)
                return WIN
            elif dice_sum in {2, 3, 12}:  # Lose on 2, 3, 12
                self.resolved = True
                return LOSE
            else:
                # Set the point for the Come bet
                self.point = dice_sum
                return "continue"
        else:
            # Point phase for the Come bet
            if dice_sum == self.point:  # Win if point is hit
                self.resolved = True
                self._award_winnings(1/1)
                return WIN
            elif dice_sum == 7:  # Lose on 7
                self.resolved = True
                return LOSE
        return "continue"

class FieldBet(Bet):
    def would_resolve(self, rollsum: int = 1, point: int = 1) -> bool:
        return True

    def resolve(self, roll, point):
        """Resolve a Field bet. Wins or loses on a single roll."""
        dice_sum = roll[0]
        if dice_sum in {2, 3, 4, 9, 10, 11, 12}:  # Winning numbers
            return WIN
        else:  # Losing numbers
            return LOSE