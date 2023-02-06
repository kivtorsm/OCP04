

class View:
    # def program_file_created(self, path):
    #     print(f"Fichier de programme créé : \n{path}")

    # def program_file_already_exists(self, path):
    #     print(f"Nous avons trouvé le fichier de programme : \n{path}")

    # def program_file_empty(self):
    #     print('Aucune information contenue dans le fichier de programme')

    def prompt_for_main_menu_choice(self, program_status):
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

    def prompt_for_tournament_creation(self):
        tournament_data = {}
        input_data = input("\nVeuillez saisir le nom du tournoi :\n")
        tournament_data['name'] = input_data
        input_data = input("Veuillez saisir le lieu du tournoi :\n")
        tournament_data['place'] = input_data
        print("Veuillez saisir la date de début du tournoi :")
        start_date_day = input("Jour (jj) : ")
        # TODO: contrôler qu'il s'agit du bon input
        start_date_month = input("Mois (mm) : ")
        # TODO: contrôler qu'il s'agit du bon input
        start_date_year = input("Année (aaaa) : ")
        # TODO: contrôler qu'il s'agit du bon input
        input_data = f"{start_date_day}/{start_date_month}/{start_date_year}"
        tournament_data['start_date'] = input_data
        print("Veuillez saisir la date de fin du tournoi :")
        end_date_day = input("Jour (jj) : ")
        # TODO: contrôler qu'il s'agit du bon input
        end_date_month = input("Mois (mm) : ")
        # TODO: contrôler qu'il s'agit du bon input
        end_date_year = input("Année (aaaa) : ")
        # TODO: contrôler qu'il s'agit du bon input
        # TODO: contrôler que date de fin > date de début
        input_data = f"{end_date_day}/{end_date_month}/{end_date_year}"
        tournament_data['end_date'] = input_data
        rounds = input("Veuillez saisir le nombre de tours du tournoi (4 par défaut) :\n")
        try:
            input_data = int(rounds)
        except ValueError:
            input_data = 4
            print("Tournoi à 4 tours")
        finally:
            tournament_data['rounds'] = input_data
        input_data = input("Veuillez saisir une description du tournoi :\n")
        tournament_data['description'] = input_data

        return tournament_data

    def prompt_for_national_chess_identifier(self):
        national_chess_identifier = input(
            "\nVeuillez rentrer le numéro d'identification d'échecs du joueur à inscrire au tournoi :\n"
        )
        national_chess_identifier_upper = national_chess_identifier.upper()
        return national_chess_identifier_upper

    def prompt_for_player_data(self):
        player_data = {}
        input_data = input("Veuillez rentrer le prénom du joueur:\n")
        player_data['first_name'] = input_data
        input_data = input("Veuillez rentrer le nom de famille du joueur:\n")
        player_data['last_name'] = input_data
        print("Veuillez rentrer la date de naissance du joueur : \n")
        birth_date_day = input("Jour (jj) : ")
        # TODO: contrôler qu'il s'agit du bon input
        birth_date_month = input("Mois (mm) : ")
        # TODO: contrôler qu'il s'agit du bon input
        birth_date_year = input("Année (aaaa) : ")
        # TODO: contrôler qu'il s'agit du bon input
        # TODO: contrôler que date de fin > date de début
        input_data = f"{birth_date_day}/{birth_date_month}/{birth_date_year}"
        player_data['birth_date'] = input_data
        return player_data

    def prompt_for_new_player_options(self):
        print("\nVous n'êtes pas suffisamment nombreux ou pas un nombre pair de joueurs.")
        print("Que souhaitez-vous faire ?")
        choice = input("1 - Revenir au menu principal\n"
                       "2 - Ajouter un nouveau joueur\n")
        return choice

    def prompt_for_running_tournament_options(self):
        print("\nVous êtes suffisamment nombreux et un nombre pair de joueurs.")
        print("Que souhaitez-vous faire ?")
        choice = input("1 - Revenir au menu principal\n"
                       "2 - Ajouter un nouveau joueur\n"
                       "3 - Lancer le tournoi\n")
        return choice

    def prompt_for_new_player(self):
        choice = input("\nVoulez-vous inscrire un nouveau joueur ? (y/n)\n")
        return choice
