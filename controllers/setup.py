# coding: utf-8

import os

from models.json_file import ProgramData

PROGRAM_FILE_FOLDER_PATH = os.path.abspath(f"./data")
PROGRAM_FILE_NAME = "chess_tournament_manager.json"
PROGRAM_FILE_PATH = f"{PROGRAM_FILE_FOLDER_PATH}\\{PROGRAM_FILE_NAME}"


def check_program_file():
    """
    Checks if the program file exists and creates it in case it doesn't exist
    :return: None
    :rtype: None
    """
    if not os.path.isfile(PROGRAM_FILE_PATH):
        os.makedirs(PROGRAM_FILE_FOLDER_PATH)
        with open(PROGRAM_FILE_PATH, 'w'):
            pass
        print(f"File {PROGRAM_FILE_PATH} Created ")
    else:
        print(f"File {PROGRAM_FILE_PATH} already exists")


def charge_program_file():
    """
    Creates program file object and gets data from program file if it exists
    :return: programData object with all the current program data in it
    :rtype: ProgramData
    """
    # creates ProgramData object with the constant file path
    program_file = ProgramData(PROGRAM_FILE_PATH)
    # charges json file data to ProgramData object
    program_file.update_data_object_from_json()
    return program_file


def main():
    check_program_file()
    program_file = charge_program_file()
    return program_file


if __name__ == "__main__":
    main()
