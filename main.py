# coding: utf-8

from controllers.controller import Controller
from views.view import View


def main():
    view = View()
    game = Controller(view)
    game.run_program()


if __name__ == "__main__":
    main()
