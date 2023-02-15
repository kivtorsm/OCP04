# coding: utf-8

from models.json_file import ProgramData


class ControlTournament:
    """
    Controller for Tournament object
    """
    MINIMUM_PLAYERS = 8

    @staticmethod
    def player_already_signed_in_tournament(
            program_file: ProgramData,
            national_chess_identifier: str) -> bool:
        """
        Checks if a player has already been signed in a tournament
        :param program_file: program file in which the program data is saved
        :type program_file: ProgramData
        :param national_chess_identifier: player's chess ID to be checked
        :type national_chess_identifier: str
        :return: evaluation of the presence of player in the tournament
        :rtype: bool
        """
        tournament = program_file.get_last_tournament()
        player_list = tournament.player_list
        return national_chess_identifier in player_list

    @staticmethod
    def count_number_of_players(program_file: ProgramData) -> int:
        """
        Counts number of players signed in a tournament
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return: number of players signed-in the tournament
        :rtype: int
        """
        tournament = program_file.get_last_tournament()
        player_list = tournament.player_list
        number_of_players = len(player_list)
        return number_of_players

    def is_player_count_even(self, program_file) -> bool:
        """
        Checks if the number of players signed-in the tournament is even
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return: evaluation of the rest of the division of the number of
        players by 2
        :rtype: bool
        """
        # even = pair (fr)
        number_of_players = self.count_number_of_players(program_file)
        return (number_of_players % 2) == 0

    def does_tournament_has_minimum_number_of_players(
            self,
            program_file: ProgramData) -> bool:
        """
        Checks if the tournament has enough players signed-in
        :param program_file: program file in which the program data is saved
        :type program_file: ProgramData
        :return: evaluation of players signed in > minimum players
        :rtype: bool
        """
        total_players = self.count_number_of_players(program_file)
        return total_players >= self.MINIMUM_PLAYERS

    @staticmethod
    def sign_in_player(
            program_file: ProgramData,
            national_chess_identifier: str):
        """
        Signs a player in the tournament
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :param national_chess_identifier: ID of player to be signed in
        tournament
        :type national_chess_identifier: str
        :return: nothing
        :rtype:
        """
        tournament = program_file.get_last_tournament()
        tournament.sign_in_player(national_chess_identifier)
        program_file.update_ongoing_tournament(tournament)
