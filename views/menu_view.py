

class MenuView:
    def prompt_for_main_menu_choice(self, program_status):
        program_file_empty = program_status[0]
        ongoing_tournament = program_status[1]
        existing_report_data = program_status[2]
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

        # if ongoing_tournament and existing_report_data : carry-on with tournament or consult reports
        elif ongoing_tournament and existing_report_data:
            while option not in [1, 2]:
                print("Veuillez choisir une option :")
                option = input("1 - Continuer le tournoi en cours \n"
                               "2 - Consulter les rapports du programme \n")
                try:
                    if int(option) == 1:
                        result = 1
                    elif int(option) == 2:
                        result = 2
                except ValueError:
                    pass

        # if NO ongoing_tournament and existing_report_data : new tournament or consult reports
        elif not ongoing_tournament and existing_report_data:
            print("Veuillez choisir une option :")
            option = input("1 - Démarrer un nouveau tournoi \n"
                           "2 - Consulter les rapports du programme\n")
            if int(option) == 1:
                result = 0
            else:
                result = self.prompt_for_report_menu_choice(program_status)
        print(result)
        return result

    @staticmethod
    def prompt_for_report_menu_choice(program_status):
        existing_player_data = program_status[3]
        existing_tournament_data = program_status[4]
        option = "c"
        print(f"\nBienvenue à la consultation de rapports")
        # if No player data user can consult tournament database
        if not existing_player_data:
            while option not in [str(0), (1)]:
                print("Veuillez choisir une option :")
                option = input("0 - Revenir au menu principal"
                               "1 - Consulter la base de données des tournois \n")
                try:
                    if int(option) == 0:
                        result = 0
                    elif int(option) == 1:
                        result = 3
                except ValueError:
                    pass
        # if No tournament data user user can consult player database
        elif not existing_tournament_data:
            while option not in [str(0), str(1)]:
                print("Veuillez choisir une option :")
                option = input("0 - Revenir au menu principal"
                               "1 - Consulter la base de données des joueurs \n")
                try:
                    if int(option) == 0:
                        result = 0
                    elif int(option) == 1:
                        result = 4
                except ValueError:
                    pass
        # if ongoing_tournament and existing_report_data : carry-on with tournament or consult reports
        else:
            while option not in [str(0), str(1), str(2)]:
                print("Veuillez choisir une option :")
                option = input("0 - Revenir au menu principal\n"
                               "1 - Consulter la base de données des joueurs \n"
                               "2 - Consulter la base de données des tournois \n")
                try:
                    if int(option) == 0:
                        result = 0
                    elif int(option) == 1:
                        result = 4
                    elif int(option) == 2:
                        result = 3
                except ValueError:
                    pass

        return result
