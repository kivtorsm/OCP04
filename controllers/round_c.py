# coding: utf-8

import random

from models.tournament import Tournament
from models.match import Match
from models.json_file import ProgramData
from models.player_in_tournament import PlayerInTournament

from controllers.tournament_player_c import ControlTournamentPlayer

from views.round_v import RoundView


class ControlRound:
    """
    Round object controller
    """
    def __init__(self, round_view: RoundView):
        # view
        self.round_view = round_view
        # controllers
        self.player_in_tournament_control = ControlTournamentPlayer()

    @staticmethod
    def is_current_round_initialised(program_file: ProgramData):
        """
        Checks if ongoing round has already been initialized
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return:
        :rtype:
        """
        try:
            current_round = program_file.get_current_round()
            return current_round.match_list != []
        except AttributeError:
            pass

    def initialise_round(self, program_file: ProgramData):
        """
        Initializes round1 in a given tournament by :
        - Listing pairs of participants that will confront each other
        - Updating the round with the list of pairs
        - Increasing the current round number
        :param program_file: program file with the tournament where to
        initialize round 1
        :type program_file: ProgramData
        :return: No return
        :rtype: None
        """
        current_tournament = program_file.get_last_tournament()
        current_round_number = current_tournament.current_round
        if current_round_number == 1:
            # Create random pair list
            pair_list = ControlRound.set_pair_list_random(current_tournament)
        else:
            pair_list = self.set_pair_list_based_on_scores(program_file)

        # Update the match list to the current_round of the tournament
        program_file.set_tournament_round_match_list(pair_list)

    @staticmethod
    def set_pair_list_random(tournament: Tournament) -> list:
        """
        Shuffles participant list and creates random pairs returned as a list
        of pairs to play each other
        :param tournament: a given tournament for which we want to create
        random pairs
        :type tournament: tournament class
        :return: list of pairs
        :rtype: list
        """
        player_list = tournament.get_player_list()
        # Shuffle player list
        random.shuffle(player_list)
        match_list = []
        # Get number of player per round
        number_of_matches_per_round = \
            tournament.get_number_of_matches_per_round()
        # For each match, create a pair of players to play each other
        # and add to list
        for match_number in range(0, int(len(player_list)/2)):
            # Each pair is a list formed by [player, score]
            player1 = [player_list[match_number], 0]
            player2 = [player_list[match_number + number_of_matches_per_round],
                       0]
            match = Match(player1, player2)
            # The pair (list type) is appended to the global pair list.
            match_list.append(match)
        return match_list

    def set_pair_list_based_on_scores(self, program_file: ProgramData) -> list:
        """
        Defines the paris of players to confront each other based on their
        previous scores
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return: lists of matches to be played in a round
        :rtype: list
        """
        # sort player list
        player_list_sorted = self.sort_player_list_by_score(program_file)
        # create a copy list for resetting purposes
        copy_list = player_list_sorted.copy()
        # Initialize pairings list
        pairings = []
        trouble_maker_dict = {}
        for player in player_list_sorted:
            trouble_maker_dict[player.national_chess_identifier] = 0

            # we empty the sorted player list and check for pairs until the list is empty
        while len(player_list_sorted) > 0:
            is_solution_possible = self.is_solution_possible(player_list_sorted)
            # Check if a solution is possible, if not, change player positions in list till a solution works
            if not is_solution_possible:
                # identifiy the trouble maker and increase the number of positions to change in the list
                trouble_maker = self.look_for_trouble_maker(player_list_sorted)
                trouble_maker_dict[trouble_maker.national_chess_identifier] += 1

                # reset the player list from the copy
                player_list_sorted = copy_list.copy()

                # modify position of all players in the trouble maker dict
                for player in player_list_sorted:
                    new_position = player_list_sorted.index(player) \
                                   - trouble_maker_dict[player.national_chess_identifier]
                    player_list_sorted.remove(player)
                    player_list_sorted.insert(new_position, player)

                # reset the pairings list
                pairings = []

            # if a solution can be found
            else:
                # for each 1st player in the list we will select the first player that has never been an opponent
                player1 = player_list_sorted[0]

                # Check if there is at least one remaining player that has not played the current player for which
                # we are performing the check. For that we take out position 0 from the list
                if not self.are_remaining_players_in_player_has_played(
                        program_file, player_list_sorted[1:], player1.national_chess_identifier
                ):

                    # parsing all players in the list looking for a proper fit
                    for count in range(1, len(player_list_sorted)):
                        # check list of players until we find one that the first player in tbe list has not
                        # played against
                        player2 = player_list_sorted[count]

                        # Check if both players have already confronted each other
                        if not self.player_in_tournament_control.has_already_played(
                                program_file,
                                player1.national_chess_identifier,
                                player2.national_chess_identifier):
                            print("fonctionnement normal")
                            print(" - avant modif")
                            print("restants")
                            for player in player_list_sorted:
                                print(player)
                            print("pairings")
                            for player in pairings:
                                print(player)
                            # append both players to pairings
                            pairings.append(player_list_sorted[0])
                            pairings.append(player_list_sorted[count])

                            # remove both players from the initial sorted player list
                            player_list_sorted.pop(count)
                            player_list_sorted.pop(0)

                            # break the for loop
                            break

        # create match list
        match_list = []

        # each match entry will contain a group of 2 players taken in  order it's provided in the pairings list
        for count in range(0, len(pairings), 2):
            player1 = [pairings[count].national_chess_identifier, 0]
            player2 = [pairings[count + 1].national_chess_identifier, 0]
            match = Match(player1, player2)
            match_list.append(match)

        return match_list

    @staticmethod
    def are_remaining_players_in_player_has_played(
            program_file: ProgramData, player_list: list, national_chess_identifier: str) -> bool:
        """
        Checks if a list of players is contained in the has_played list of a player in a tournament
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :param player_list: player list that we want to check
        :type player_list: list
        :param national_chess_identifier: chess ID of a player for which we want to check the has-played list
        :type national_chess_identifier:
        :return: true or false, is the list of players inside the has_played list of the player for which we
        have provided a chess ID
        :rtype: bool
        """
        player_id_list = []
        player_has_played_list = program_file.get_player_in_tournament(national_chess_identifier).has_played
        for player in player_list:
            player_id_list.append(player.national_chess_identifier)
        check = all(item in player_has_played_list for item in player_id_list)
        return check

    def set_match_score(self, program_file: ProgramData):
        """
        Runs match score input for user to input all matches scores
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return: nothing
        :rtype:
        """
        # Get current round
        current_round = program_file.get_current_round()
        # get current match number
        current_match_number = current_round.next_match
        # get current match
        current_match = current_round.match_list[current_match_number - 1]
        # get match score list
        score_list = current_match.match_data
        # get player 1 score list
        player1_score_list = score_list[0]
        # get player 1 national chess identifier
        player1_national_chess_identifier = player1_score_list[0]
        # get player 2 score list
        player2_score_list = score_list[1]
        # get player 2 national chess identifier
        player2_national_chess_identifier = player2_score_list[0]
        # set outbound score player
        score_player1 = 2
        score_player2 = 2

        # ask for input until user types right value
        while score_player1 != [0, 0.5, 1]:
            # control view : prompt for player 1 score
            user_input = self.round_view.prompt_for_score_input(
                player1_national_chess_identifier)
            score_player1 = float(user_input)
            if score_player1 in [float(0), float(0.5), float(1)]:
                break
            else:
                self.round_view.show_score_value_error()
        # guess player 2 score based on player 1's
        if score_player1 == 0:
            score_player2 = 1
        elif score_player1 == 0.5:
            score_player2 = 0.5
        elif score_player1 == 1:
            score_player2 = 0

        # build match score list
        player1_score_list = [player1_national_chess_identifier, score_player1]
        player2_score_list = [player2_national_chess_identifier, score_player2]
        match = Match(player1_score_list, player2_score_list)
        # update match_list in current round with match score
        current_round.match_list[current_round.next_match - 1] = match
        # get ongoing tournament
        current_tournament = program_file.get_last_tournament()
        # get players in tournament
        player_in_tournament1 = current_tournament.get_player_in_tournament(player1_national_chess_identifier)
        player_in_tournament2 = current_tournament.get_player_in_tournament(player2_national_chess_identifier)
        # update players' score
        player_in_tournament1.add_score(score_player1)
        player_in_tournament2.add_score(score_player2)
        # update players' has_played opponents
        p1_has_played_p2 = self.player_in_tournament_control.has_already_played(
                program_file,
                player1_national_chess_identifier,
                player2_national_chess_identifier
            )
        p2_has_played_p1 = self.player_in_tournament_control.has_already_played(
                program_file,
                player2_national_chess_identifier,
                player1_national_chess_identifier
            )
        if not p1_has_played_p2:
            player_in_tournament1.add_has_played(player2_national_chess_identifier)
        if not p2_has_played_p1:
            player_in_tournament2.add_has_played(player1_national_chess_identifier)

        # increment next match counter
        current_round.increment_next_match()

        # Update tournament data with the round data
        current_tournament.round_list[current_tournament.current_round - 1] \
            = current_round
        # Update program_file with last tournament data and update json_file
        program_file.update_ongoing_tournament(current_tournament)

    @staticmethod
    def is_round_finished(program_file: ProgramData) -> bool:
        """
        Checks if the ongoing round is finished: all matches scores have been
        provided
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return: checks if the next match pointer is higher than the number
        of matchs for the round
        :rtype: bool
        """
        current_round = program_file.get_current_round()
        return current_round.next_match > program_file.get_last_tournament().\
            get_number_of_matches_per_round()

    @staticmethod
    def is_last_round(program_file: ProgramData):
        """
        Checks if the ongoing round is the last one
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return: checks if the current round is higher than the total
        number of rounds of the tournament
        :rtype: bool
        """
        ongoing_tournament = program_file.get_last_tournament()
        return ongoing_tournament.current_round \
            > ongoing_tournament.total_rounds

    @staticmethod
    def is_solution_possible(player_list: list) -> bool:
        """
        Check if a solution is possible with a provided list of players
        :param player_list: list of players for which we want to test if a solution is feasible
        :type player_list: list
        :return: check that no player has all other players in its has_played list
        :rtype: bool
        """
        solution = True
        for player_x in player_list:
            remaining_players_id = []
            for player_y in player_list[1:]:
                remaining_players_id.append(player_y.national_chess_identifier)

            check = all(item in player_x.has_played for item in remaining_players_id)

            if check:
                solution = False
                break

        return solution

    @staticmethod
    def look_for_trouble_maker(player_list: list) -> bool:
        """
        Looks for the trouble_maker not allowing to find a solution
        :param player_list: list of players for which we want to test if a solution is feasible
        :type player_list: list
        :return: player blocking the generation of a solution
        :rtype: bool
        """
        trouble_maker = None
        for player_x in player_list:
            remaining_players_id = []
            for player_y in player_list[1:]:
                remaining_players_id.append(player_y.national_chess_identifier)

            check = all(item in player_x.has_played for item in remaining_players_id)

            if check:
                trouble_maker = player_x
                break

        return trouble_maker

    @staticmethod
    def sort_player_list_by_score(program_file: ProgramData) -> list:
        """
        Sort a list of players by score. players of the same scored are randomly sorted.
        :param program_file: program file in which program data is saved
        :type program_file: ProgramData
        :return: list of players sorted by score
        :rtype: list
        """
        current_tournament = program_file.get_last_tournament()
        current_tournament_player_list = list(current_tournament.player_dict.values())
        # Shuffle players in order to randomly put together players with the
        # same score
        random.shuffle(list(current_tournament_player_list))
        # sort players by score
        player_list_sorted = sorted(
            current_tournament_player_list,
            key=lambda x: x.score,
            reverse=True)
        return player_list_sorted


if __name__ == "__main__":
    player2 = PlayerInTournament(
        national_chess_identifier="AB12345",
        score=1,
        has_played=["AA12345", "AD12345", "FD12345"]
    )
    player1 = PlayerInTournament(
        national_chess_identifier="AA12345",
        score=1,
        has_played=["AB12345", "AC12345", "AD12345"]
    )
    player3 = PlayerInTournament(
        national_chess_identifier="AC12345",
        score=1,
        has_played=["AA12345", "AF12345", "AG12345"]
    )
    player4 = PlayerInTournament(
        national_chess_identifier="AD12345",
        score=1,
        has_played=["AA12345", "AH12345", "AE12345"]
    )

    player_list = [player1, player2, player3, player4]

    round_view = RoundView()

    round_controller = ControlRound(round_view)

    solution_possible = round_controller.is_solution_possible(player_list)
    trouble_maker = round_controller.look_for_trouble_maker(player_list)

    print(solution_possible)
    print(trouble_maker)
