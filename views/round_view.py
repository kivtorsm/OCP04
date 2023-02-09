
from models.match import Match

class RoundView:

    @staticmethod
    def prompt_for_start_round(round_number):
        input(f"\nAppuie sur entrée pour démarrer le Round {round_number}")

    @staticmethod
    def prompt_for_score_input(player1_national_chess_identifier: str):
        score_player1 = input(f"\nEntrez le score du joueur {player1_national_chess_identifier}\n")
        return score_player1

    def show_score_value_error(self):
        print("Oups. Le score doit être 1, 0.5 ou 0\nEssayez de nouveau")
