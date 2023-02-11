# coding: utf-8

from controllers.tournament_controller import MainController
from controllers.control_program_file import ControlProgramFile

from views.view import View


def main():
    # initialize view
    view = View()

    # initialize controllers
    program_file_control = ControlProgramFile()

    # initialize main controller
    tournament_manager = MainController(view, program_file_control)

    # run main controller
    tournament_manager.run_program()


if __name__ == "__main__":
    main()
