
from models.json_file import ProgramData


class ControlTournamentPlayer:
    @staticmethod
    def has_already_played(
            program_file: ProgramData,
            player1_national_chess_identifier: str,
            player2_national_chess_identifier: str
    ):
        current_tournament = program_file.get_last_tournament()
        player_in_tournament = current_tournament.get_player_in_tournament(player1_national_chess_identifier)
        return player2_national_chess_identifier in player_in_tournament.has_played
