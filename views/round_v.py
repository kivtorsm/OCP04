

class RoundView:
    """
    Running round view
    """
    @staticmethod
    def prompt_for_start_round(round_number: int):
        """
        Asks user to press enter in order to start the round
        :param round_number: round number to be started
        :type round_number: int
        :return: None
        :rtype:
        """
        input(f"\nAppuie sur entrée pour démarrer le Round {round_number}")

    @staticmethod
    def prompt_for_score_input(player1_national_chess_identifier: str):
        """
        Asks user to input player's score
        :param player1_national_chess_identifier: player's national
        chess identifier for which to add score
        :type player1_national_chess_identifier: str
        :return: None
        :rtype:
        """
        score_player1 = input(f"\nEntrez le score du joueur "
                              f"{player1_national_chess_identifier}\n")
        return score_player1

    @staticmethod
    def show_score_value_error():
        """
        Prints score value error if the input is not an
        accepted value [0, 0.5, 1]
        :return: None
        :rtype:
        """
        print("Oups. Le score doit être 1, 0.5 ou 0\nEssayez de nouveau")
