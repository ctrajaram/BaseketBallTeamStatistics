from constants import TEAMS, PLAYERS
from copy import deepcopy
from pprint import pprint
import sys


def main() -> None:
    """
    The main function of the program.
    Displays the game header and starts the statistics module of the basketball teams.
    """
    display_game_header()
    start_stats(balance_teams(TEAMS, clean_data(PLAYERS)))


def quit_stats():
    """
    Prints a goodbye message and exits the program.
    """
    print('Goodbye')
    sys.exit(0)


def start_stats(dct: dict):
    """
    Handles the initial user input for displaying team stats or quitting the program.

    Args:
    dct (dict): The dictionary containing team statistics.
    """
    choice: str = ""
    while choice.upper() not in ('A', 'B'):
        choice = input('Enter an option (A or B): A to display team stats and B to quit: ')
    if choice.upper() == 'B':
        quit_stats()
    else:
        display_stats(dct)


def print_stats(dct, k):
    """
    Prints the statistics of a specific team.

    Args:
    dct (dict): The dictionary containing team statistics.
    k (str): The key representing the team in the dictionary.
    """
    print('printing dict')
    pprint(dct)
    print('-' * 30)
    print(f"Team {k} Stats")
    print('-' * 30)
    print(f"Total Players: {len(dct[k])}")
    print(f"Total experienced: {len([item for item in dct[k] if item.get('experience')])}")
    print(f"Total inexperienced: {len([item for item in dct[k] if not item.get('experience')])}")
    print(f"Average Height: {sum([item['height'] for item in dct[k] ]) / len(dct[k])}")
    print("Players on Team: ")
    for item in dct[k]:
        print(item['name'], end=", " if dct[k].index(item) != 5 else "")
    print("\naGuardians: ")
    lst_guardians = []
    for item in dct[k]:
        lst_guardians.extend(item['guardians'])
    for item in lst_guardians:
        print(item, end=", " if lst_guardians.index(item) != 5 else "")
    print("\n")


def display_stats(dct: dict):
    """
    Handles user input for selecting a specific team to display stats for.

    Args:
    dct (dict): The dictionary containing team statistics.
    """
    while True:
        choice = input('Enter an option (A, B, or C): A for Panthers, B for Bandits, C for Warriors: ')
        if choice.upper() in ('A', 'B', 'C'):
            team_name = 'Panthers' if choice.upper() == 'A' else 'Bandits' if choice.upper() == 'B' else 'Warriors'
            print_stats(dct, team_name)
            input("Press ENTER to continue...")
            start_stats(dct)


def display_game_header() -> None:
    """
    Displays the game header and menu options.
    """
    print('*' * 40)
    print('BASKET BALL TEAM STATS TOOL')
    print('*' * 40)
    print('-' * 10 + 'MENU' + '-' * 10)
    print('Here are your choices: \nA) Display Team Stats\nB) Quit')


def clean_data(players_lst: list) -> list:
    """
    Cleans and processes the player data.

    Args:
    players_lst (list): A list of dictionaries containing player information.

    Returns:
    list: The cleaned list of player information.
    """
    players_copy = deepcopy(players_lst)
    cleaned_list = []
    for item in players_copy:
        # Splitting height and converting to integer
        item['height'] = int(item.get('height').split(" ")[0])
        # Converting experience to a boolean value
        item['experience'] = True if item['experience'] == 'YES' else False
        # Splitting guardians
        item['guardians'] = item['guardians'].split(" and ")
        cleaned_list.append(item)
    return cleaned_list


def balance_teams(teams_copy, cleaned_list) -> dict:
    """
    Balances the players across teams with equal no of experience and inexperienced players.

    Args:
    teams_copy (list): A list of team names.
    cleaned_list (list): The list of cleaned player data.

    Returns:
    dict: A dictionary mapping each team to its players.
    """
    no_of_players_per_team = int(len(cleaned_list) / len(teams_copy))
    no_of_players_per_team_halved = int(no_of_players_per_team // 2)
    teams_copy_local = deepcopy(teams_copy)
    cleaned_list_copy = deepcopy(cleaned_list)
    unique_keys = set()
    for d in cleaned_list_copy:
        unique_keys.update(d.keys())
    desired_keys = list(unique_keys)
    experienced_list = [{k: d[k] for k in desired_keys} for d in cleaned_list_copy if d.get("experience")]
    inexperienced_list = [{k: d[k] for k in desired_keys} for d in cleaned_list_copy if not d.get("experience")]
    dct = {}
    for t in teams_copy_local:
        # Assigning players to each team
        # dct[t] = cleaned_list_copy[:no_of_players_per_team]

        dct[t] = experienced_list[:no_of_players_per_team_halved] + inexperienced_list[:no_of_players_per_team_halved]
        # Removing assigned players
        del (experienced_list[:no_of_players_per_team_halved])
        del (inexperienced_list[:no_of_players_per_team_halved])
    return dct


if __name__ == "__main__":
    main()
