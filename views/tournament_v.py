
import datetime


class TournamentView:
    """
    Tournament module view.
    """

    def prompt_for_tournament_creation(self) -> dict:
        """
        User inputs for tournament creation
        :return: tournament data
        :rtype: dict
        """
        tournament_data = {}
        input_data = input("\nVeuillez saisir le nom du tournoi :\n")
        tournament_data['name'] = input_data
        input_data = input("\nVeuillez saisir le lieu du tournoi :\n")
        tournament_data['place'] = input_data
        print("\nVeuillez saisir la date de début du tournoi :")
        start_date = self.prompt_for_date_input()
        tournament_data['start_date'] = start_date
        print("\nVeuillez saisir la date de fin du tournoi :")
        end_date = self.prompt_for_date_input()
        tournament_data['end_date'] = end_date
        rounds_input = "c"
        rounds = 4
        while not (rounds_input.isnumeric() or rounds_input == ""):
            rounds_input = input("\nVeuillez saisir le nombre de tours du "
                                 "tournoi (4 par défaut) :\n")
            if rounds_input == "":
                rounds = 4
            else:
                try:
                    rounds = int(rounds_input)
                except ValueError:
                    print("Input needs to be numeric or an empty field")
        tournament_data['rounds'] = rounds
        description = input("\nVeuillez saisir une description du tournoi :\n")
        tournament_data['description'] = description

        return tournament_data

    @staticmethod
    def prompt_for_date_input():
        """
        Function for data input with format controls
        :return: Input date in datetime format
        :rtype: Date
        """
        day = 32
        month = 13
        year = 0000
        while day not in range(1, 32, 1):
            try:
                day = int(input("Jour (jj) : "))
                if day not in range(1, 32, 1):
                    print(f"{day} n'est pas dans l'intervalle de valeurs "
                          f"1 - 31. Veuillez recommencer à nouveau.")
            except ValueError:
                print("Il faut saisir une valeur numérique")
        while month not in range(1, 13, 1):
            try:
                month = int(input("Mois (mm) : "))
                if month not in range(1, 13, 1):
                    print(f"{month} n'est pas dans l'intervalle de valeurs "
                          f"1 - 12. Veuillez recommencer à nouveau.")
            except ValueError:
                print("Il faut saisir une valeur numérique")
        while year not in range(1800, 9999, 1):
            try:
                year = int(input("Year (yyyy) : "))
                if year not in range(1800, 9999, 1):
                    print(f"{year} n'est pas dans l'intervalle de valeurs "
                          f"1800 - 9999. Veuillez recommencer à nouveau.")
            except ValueError:
                print("Il faut saisir une valeur numérique")
        date = datetime.date(year, month, day)
        date_isoformat = date.isoformat()
        return date_isoformat

    @staticmethod
    def prompt_for_national_chess_identifier() -> str:
        """
        Asks user to input national_chess_identifier and turns it into
        capital letters
        :return: national chess identifier
        :rtype: str
        """
        national_chess_identifier = input(
            "\nVeuillez rentrer le numéro d'identification d'échecs "
            "du joueur à inscrire au tournoi :\n"
        )
        national_chess_identifier_upper = national_chess_identifier.upper()
        return national_chess_identifier_upper

    def prompt_for_player_data(self) -> dict:
        """
        Asks user to input new player data
        :return: player data for Player object
        :rtype: dict
        """
        player_data = {}
        input_data = input("Veuillez rentrer le prénom du joueur:\n")
        player_data['first_name'] = input_data
        input_data = input("Veuillez rentrer le nom de famille du joueur:\n")
        player_data['last_name'] = input_data
        print("Veuillez rentrer la date de naissance du joueur : \n")
        birth_date = self.prompt_for_date_input()
        player_data['birth_date'] = birth_date
        return player_data

    @staticmethod
    def prompt_for_new_player_options() -> str:
        """
        Asks user what to do as long as there aren't enough players
        or that the number of players is not even
        :return: User choice : main menu or adding new player
        :rtype: str
        """
        print("\nVous n'êtes pas suffisamment nombreux ou pas un "
              "nombre pair de joueurs.")
        print("Que souhaitez-vous faire ?")
        while True:
            choice = input("1 - Revenir au menu principal\n"
                           "2 - Ajouter un nouveau joueur\n")
            if choice in ["1", "2"]:
                break
        return choice

    @staticmethod
    def prompt_for_running_tournament_options() -> str:
        """
        Asks user what to do once there are enough players and
        that the number of players is even
        :return: User choice : main menu / add new player / launch tournament
        :rtype: str
        """
        print("\nVous êtes suffisamment nombreux et un nombre "
              "pair de joueurs.")
        print("Que souhaitez-vous faire ?")
        while True:
            choice = input("1 - Revenir au menu principal\n"
                           "2 - Ajouter un nouveau joueur\n"
                           "3 - Lancer le tournoi\n")
            if choice in ["1", "2", "3"]:
                break
        return choice

    @staticmethod
    def prompt_for_new_player() -> str:
        """
        Asks user if he/she wants to sign-in a new player
        :return: user choice : y/n sign-in new player
        :rtype: str
        """
        while True:
            choice = input("\nVoulez-vous inscrire un "
                           "nouveau joueur ? (y/n)\n")
            if choice in ["y", "n"]:
                break
        return choice

    @staticmethod
    def show_player_already_signed_in(national_chess_identifier: str):
        """
        Prints message explaining that a national_chess_identifier
        is already used
        :param national_chess_identifier: player national_chess_identifier
        to be printed in the message
        :type national_chess_identifier: str
        :return: None
        :rtype:
        """
        print(f"Le joueur {national_chess_identifier} "
              f"est déjà inscrit au tournoi")

    @staticmethod
    def show_player_sign_in_confirmation(national_chess_identifier: str):
        """
        Prints message confirming that the player has been signed-in the tournament
        :param national_chess_identifier: player national_chess_identifier to be printed in the message
        :type national_chess_identifier: str
        :return: None
        :rtype:
        """
        print(f"\nLe joueur {national_chess_identifier} a bien été inscrit au tournoi")
