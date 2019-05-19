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
    """Process the user input where required and validate the entry

    Parameters
    ----------
    option_range : list
        Range of the options the user can enter

    Returns
    -------
    int
        returns the validate user selection back to the caller.
    """
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
    """Show the teams for which the user can see statistics
    """
    print("\nThere are statistics on the following teams:\n")
    for index, team in enumerate(TEAMS, start=1):
        print(f"{index}) {team}")


def average_height(team_name):
    """Calculate the average height of the team

    Parameters
    ----------
    team_name : list
        Team data

    Returns
    -------
    float
        The average height of the selected team
    """
    return sum(height["height"] for height in team_name) / len(team_name[0])


def display_stats(team_name, teams):
    """Display the team statistics

    Parameters
    ----------
    team_name : list
        The data of the selected team
    teams : string
        The name of the team
    """
    players = []
    guardian_names = []
    exp = len([player for player in team_name if player["experience"]])
    inexp = len([player for player in team_name if not player["experience"]])
    print(f"\nThe displayed stats are for the {teams}\n")
    print(f"The team consists of : {len(team_name[0])+1} players")
    print(f"\t{exp} experienced players")
    print(f"\t{inexp} inexperienced players")
    print("\nThe players on the team are:")
    for player in team_name:
        players.append(player['name'])

    print(f"\t{', '.join(players)}")

    for guardian in team_name:
        guardian_names.append(guardian["guardians"])
    print(f"\nThe guardians on the team are:")
    print(f"\t{', '.join(guardian for guard_list in guardian_names for guardian in guard_list)}")
    print(f"\nThe average height of the team is {average_height(team_name)}"
          f" inches")

    try:
        input("\n\t\tPress ENTER to continue")
    except KeyboardInterrupt:
        wrong_entry("")


def split_teams(player_list):
    """Split the list of players into the available number of teams

    Parameters
    ----------
    player_list : list
        List of players that needs to be split

    Returns
    -------
    list
        splitted list based on the number of teams are available.
    """
    return [player_list[index * len(player_list) // len(TEAMS):
                        (index + 1) * len(player_list) // len(TEAMS)]
            for index in range(len(TEAMS))]


def team_balancing(cleaned_player_data):
    """Balancing the experienced and inexperienced players across the
    available teams

    Parameters
    ----------
    cleaned_player_data : list
        List of the players data that needs to be split

    Returns
    -------
    lists
        splitted teams
    """
    experienced_players = [
        player for player in cleaned_player_data if player["experience"]]
    inexperienced_players = [
        player for player in cleaned_player_data if not player["experience"]]
    panthers_experience, bandits_experience, warriors_experience = split_teams(
        [player for player in experienced_players])
    panthers_inexperience, bandits_inexperience, warriors_inexperience = (
        split_teams([player for player in inexperienced_players]))
    panthers = (panthers_experience + panthers_inexperience)
    bandits = (bandits_experience + bandits_inexperience)
    warriors = (warriors_experience + warriors_inexperience)

    return panthers, bandits, warriors


def main():
    """The main loop of the program
    """
    while True:
        player_data = deepcopy(PLAYERS)  # Create a working copy of PLAYERS
        panthers, bandits, warriors = team_balancing(
            clean_player_data(player_data))
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
            display_stats(panthers, "Panthers")
        if team_selection == 2:
            display_stats(bandits, "Bandits")
        if team_selection == 3:
            display_stats(warriors, "Warriors")


if __name__ == "__main__":
    main()
