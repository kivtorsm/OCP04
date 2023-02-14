
class MenuView:
    """
    Main menu view
    """
    @staticmethod
    def prompt_for_main_menu_choice(program_status: list) -> int:
        """
        Main menu view. Shows at programs start-up and asks for user input depending on the program status
        :param program_status: provides information on available data :
            program_file empty,
            ongoing_tournament,
            existing_report_data,
            existing_player_data,
            existing_tournament_data
        :type program_status: list
        :return: user choice depending on the options given by the program status
        :rtype: int
        """
        program_file_empty = program_status[0]
        ongoing_tournament = program_status[1]
        existing_report_data = program_status[2]
        existing_player_data = program_status[3]
        existing_tournament_data = program_status[4]
        option = "c"
        result = "c"
        print(f"\nBienvenue au menu principal")

        # if empty file the only option is to create a nez tournament
        if program_file_empty:
            input("Appuyez sur entrée pour démarrer un nouveau tournoi\n")
            result = 0
        # if ongoing_tournament but no existing report data the only option is to carry-on with the tournament
        elif ongoing_tournament and not existing_report_data:
            input("Appuyez sur entrée pour continuer le tournoi en cours\n")
            result = 1

        # if NO ongoing_tournament and existing_report_data : new tournament or consult reports
        elif not ongoing_tournament and existing_tournament_data and existing_player_data:
            while option not in [str(1), str(2), str(3)]:
                print("Veuillez choisir une option :")
                option = input("1 - Démarrer un nouveau tournoi \n"
                               "2 - Consulter la liste des joueurs inscrits dans la base des données \n"
                               "3 - Consulter la liste des tournois \n")
                try:
                    if int(option) == 1:
                        result = 0
                    elif int(option) == 2:
                        result = 2
                    elif int(option) == 3:
                        result = 3
                except ValueError:
                    pass

        # if ongoing_tournament, existing player data and existing tournament data :
        # carry-on with tournament or consult reports
        elif ongoing_tournament and existing_tournament_data and existing_player_data:
            while option not in [str(1), str(2), str(3)]:
                print("Veuillez choisir une option :")
                option = input("1 - Continuer le tournoi en cours \n"
                               "2 - Consulter la liste des joueurs inscrits dans la base des données \n"
                               "3 - Consulter la liste des tournois \n")
                try:
                    if int(option) == 1:
                        result = 1
                    elif int(option) == 2:
                        result = 2
                    elif int(option) == 3:
                        result = 3
                except ValueError:
                    pass
        elif ongoing_tournament and not existing_tournament_data and existing_player_data:
            while option not in [str(1), str(2)]:
                print("Veuillez choisir une option :")
                option = input("1 - Continuer le tournoi en cours \n"
                               "2 - Consulter la liste des joueurs inscrits dans la base des données \n")
                try:
                    if int(option) == 1:
                        result = 1
                    elif int(option) == 2:
                        result = 2
                except ValueError:
                    pass
        elif ongoing_tournament and existing_tournament_data and not existing_player_data:
            while option not in [str(1), str(3)]:
                print("Veuillez choisir une option :")
                option = input("1 - Continuer le tournoi en cours \n"
                               "3 - Consulter la liste des tournois \n")
                try:
                    if int(option) == 1:
                        result = 1
                    elif int(option) == 3:
                        result = 3
                except ValueError:
                    pass
        elif not ongoing_tournament and not existing_tournament_data and existing_player_data:
            while option not in [str(1), str(2)]:
                print("Veuillez choisir une option :")
                option = input("1 - Démarrer un nouveau tournoi \n"
                               "2 - Consulter la liste des joueurs inscrits dans la base des données \n")
                try:
                    if int(option) == 1:
                        result = 0
                    elif int(option) == 2:
                        result = 2
                except ValueError:
                    pass
        elif not ongoing_tournament and existing_tournament_data and not existing_player_data:
            while option not in [str(1), str(3)]:
                print("Veuillez choisir une option :")
                option = input("1 - Démarrer un nouveau tournoi \n"
                               "3 - Consulter la liste des tournois \n")
                try:
                    if int(option) == 1:
                        result = 0
                    elif int(option) == 3:
                        result = 3
                except ValueError:
                    pass

        return result


