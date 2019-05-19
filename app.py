import os
import sys
from copy import deepcopy

from constants import PLAYERS, TEAMS


def clear_screen():
    """clear the data on the screen
    """
    os.system("cls" if os.name == "nt" else "clear")


def check_exit(leave_game):
    """Check if the user really intended to end the game with crtl-c

    Parameters
    ----------
    leave_game : string
        Response from the user to question if he wants to quit the game.
    """
    if leave_game.lower() == 'y':
        print("\n Thanks for using the tool, see you next time!")
        sys.exit(1)


def clean_player_data(players_data):
    """clean the list of players so that dimensions are ints,  experience
     is showing True or False and the guardians are split into a list

    Parameters
    ----------
    players_data : list
        List of players data that requires cleaning

    Returns
    -------
    list
        list of cleaned player data
    """
    for player in players_data:
        player["dimension"] = player["height"][3:]
        player["height"] = int(player["height"][:2])

        if player["experience"] == 'YES':
            player["experience"] = True
        else:
            player["experience"] = False

        player["guardians"] = player["guardians"].split(' and ')

    return players_data


def wrong_entry(message):
    """Display message to the user that made a wrong entry and setup the screen
    for a new entry.
    """
    print(f"\n{message}")
    input("Press enter to continue")
    clear_screen()
    show_menu()


def process_user_input(option_range):
    try:
        menu_selection = int(input("\nEnter your option: > "))
    except (ValueError, KeyboardInterrupt):
        wrong_entry("You made a wrong entry! Please select a valid option")
    else:
        if menu_selection in option_range:
            return menu_selection
        else:
            wrong_entry("You made a wrong entry! Please select a valid option")


def show_menu():
    """Show the menu to the user and collect the user entry

    Returns
    -------
    int
        Return the user decision to the caller.
    """
    title1 = " WELCOME "
    title2 = "TO THE"
    title3 = "BASKETBALL STATISTICS TOOL."
    title4 = " MENU "

    print("*" * len(title3))
    print(title1.center(len(title3)))
    print(title2.center(len(title3)-1))
    print(title3)
    print("*" * len(title3), end="\n\n")
    print(title4.center(len(title3), "+",), end="\n\n")
    print("You have the following choices:")
    print("\t1. Display a teams statistics")
    print("\t2. Quit ")


def show_team_options():
    print("\nThere are statistics on the following teams:\n")
    for index, team in enumerate(TEAMS, start=1):
        print(f"{index}) {team}")


def display_stats():
    pass


def team_balancing(clean_player_data):
    pass


def main():
    player_data = deepcopy(PLAYERS)  # Create a working copy of PLAYERS
    clean_player_data(player_data)
    clear_screen()
    show_menu()
    menu_selection = process_user_input((1, 2))
    if menu_selection == 1:
        show_team_options()
    if menu_selection == 2:
        sys.exit(1)

    team_selection = process_user_input(
        (index for index, _ in enumerate(TEAMS, start=1)))

    if team_selection == 1:
        print("Panthers")
    if team_selection == 2:
        print("Bandits")
    if team_selection == 3:
        print("Warriors")


if __name__ == "__main__":
    main()
