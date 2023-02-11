

class MenuView:

    @staticmethod
    def prompt_for_main_menu_choice(program_status):
        program_file_empty = program_status[0]
        ongoing_tournament = program_status[1]
        existing_report_data = program_status[2]
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
            print("Veuillez choisir une option :")
            option = input("1 - Continuer le tournoi en cours \n"
                           "2 - Consulter les rapports du programme \n")
            if int(option) == 1:
                result = 1
            else:
                result = 2
        # if NO ongoing_tournament and existing_report_data : new tournament or consult reports
        elif not ongoing_tournament and existing_report_data:
            print("Veuillez choisir une option :")
            option = input("1 - Démarrer un nouveau tournoi \n"
                           "2 - Consulter les rapports du programme\n")
            if int(option) == 1:
                result = 0
            else:
                result = 2
        return result
