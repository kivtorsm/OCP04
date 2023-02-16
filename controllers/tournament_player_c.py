
from models.json_file import ProgramData


class ControlTournamentPlayer:
    """
    Controller for tournament in player object
    """
    @staticmethod
    def has_already_played(
            program_file: ProgramData,
            player1_national_chess_identifier: str,
            player2_national_chess_identifier: str
    ) -> bool:
        """
        Checks if a player has already played against another
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :param player1_national_chess_identifier: player ID for which
        program checks if it has played player 2
        :type player1_national_chess_identifier: str
        :param player2_national_chess_identifier: player ID for which
        program checks if it has played player 1
        :type player2_national_chess_identifier: str
        :return: evaluation if player 1 has already played player 2
        :rtype: bool
        """
        current_tournament = program_file.get_last_tournament()
        player_in_tournament = current_tournament.get_player_in_tournament(player1_national_chess_identifier)
        print("has already played")
        print(player2_national_chess_identifier)
        print(player_in_tournament.has_played)
        print(player2_national_chess_identifier in player_in_tournament.has_played)
        return player2_national_chess_identifier in player_in_tournament.has_played
