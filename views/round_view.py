
from models.match import Match

class RoundView:

    @staticmethod
    def prompt_for_start_round(round_number):
        input(f"\nAppuie sur entrée pour démarrer le Round {round_number}")

    @staticmethod
    def prompt_for_score_input(current_match: Match):
        print(current_match)
        print(type(current_match))
        score_list = current_match.match_data
        # FIXME : ça bugge
        player1_score_list = score_list[0]
        player1_national_chess_identifier = player1_score_list[0]
        player2_score_list = score_list[1]
        player2_national_chess_identifier = player2_score_list[0]
        score_player1 = input(f"\nEntrez le score du joueur {player1_national_chess_identifier}\n")
        score_player2 = input(f"Entrez le score du joueur {player2_national_chess_identifier}\n")
        match_score = [[player1_national_chess_identifier, score_player1], [player2_national_chess_identifier, score_player2]]
        return match_score
