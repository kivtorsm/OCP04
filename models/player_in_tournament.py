

class PlayerInTournament:
    def __init__(self, national_chess_identifier, score=float(0), has_played=[]):
        self.national_chess_identifier = national_chess_identifier
        self.score = score
        self.has_played = has_played

    def __str__(self):
        return f"{self.national_chess_identifier} - {self.score} - {self.has_played}"

    def add_score(self, score: float):
        self.score += score

    def add_has_played(self, national_chess_identifier: str):
        self.has_played.append(national_chess_identifier)
