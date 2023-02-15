

class PlayerInTournament:
    def __init__(
            self,
            national_chess_identifier,
            score=float(0),
            has_played=None
    ):
        self.national_chess_identifier = national_chess_identifier
        self.score = score
        self.has_played = has_played if has_played else []

    def __str__(self):
        return f"{self.national_chess_identifier} " \
               f"- {self.score} " \
               f"- {self.has_played}"

    def add_score(self, score: float):
        """
        Adds score to the player's score in a tournament
        :param score: score to be added to the player's score
        :type score: float
        :return: nothing
        :rtype:
        """
        self.score += score

    def add_has_played(self, national_chess_identifier: str):
        """
        Updates the list of opponents that the player has already played
        in the tournament
        :param national_chess_identifier: for the player that is to be added
        to the opponents list
        :type national_chess_identifier: str
        :return: nothing
        :rtype:
        """
        self.has_played.append(national_chess_identifier)
