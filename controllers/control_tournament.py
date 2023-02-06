# coding: utf-8

from models.json_file import ProgramData


class ControlTournament:
    MINIMUM_PLAYERS = 8

    def player_already_signed_in_tournament(self, program_file: ProgramData, national_chess_identifier: str):
        tournament = program_file.get_last_tournament()
        player_list = tournament.player_list
        return national_chess_identifier in player_list

    def count_number_of_players(self, program_file):
        tournament = program_file.get_last_tournament()
        player_list = tournament.player_list
        number_of_players = len(player_list)
        return number_of_players

    def is_player_count_even(self, program_file):
        # even = pair (fr)
        number_of_players = self.count_number_of_players(program_file)
        return (number_of_players % 2) == 0

    def does_tournament_has_minimum_number_of_players(self, program_file: ProgramData):
        total_players = self.count_number_of_players(program_file)
        return total_players >= self.MINIMUM_PLAYERS

    def sign_in_player(self, program_file: ProgramData, national_chess_identifier: str):
        tournament = program_file.get_last_tournament()
        tournament.sign_in_player(national_chess_identifier)
        program_file.update_ongoing_tournament(tournament)
