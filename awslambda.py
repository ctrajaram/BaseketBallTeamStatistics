# lambda_function.py
from constants import TEAMS, PLAYERS
from copy import deepcopy
import json


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


def lambda_handler(event, context):
    # Process the input event to get the team name
    team_name = event.get('queryStringParameters', {}).get('team', '')

    # Call your existing logic to process the team stats
    cleaned_players = clean_data(PLAYERS)
    teams = balance_teams(TEAMS, cleaned_players)

    # Generate the response
    if team_name in teams:
        team_stats = teams[team_name]
        body = {"Team": team_name, "Stats": team_stats}
    else:
        body = {"Error": "Team not found"}

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
