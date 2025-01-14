# Isaac Trost
# NBA Tournament Builder

from dataclasses import dataclass
from tabulate import tabulate
import json

@dataclass
class Team:
    team_name: str
    division: str
    wins: int
    losses: int
    conference_wins: int
    conference_losses: int
    division_wins: int
    division_losses: int
    
    @property
    def win_percent(self):
        return self.wins / (self.wins + self.losses)
    
    @property
    def conference_win_percent(self):
        return self.conference_wins / (self.conference_wins + self.conference_losses)
    
    @property
    def division_win_percent(self):
        return self.division_wins / (self.division_wins + self.division_losses)
    
def parse_csv() -> dict:
    DATA_PATH = "./data.csv"
    # Object to store the extracted team data.
    districts: dict = {}
    with open(DATA_PATH, "r") as f:
        # Skips csv headers.
        f.readline()
        # Enumerate through each line the file.
        for line in f:
            # Remove new line characters.
            line = line.replace("\n", "")
            # Split the line into values.
            values = line.split(",")

            # Unpack the variables and calculate new ones.
            division = str(values[1])
            team_name = str(values[0])
            wins = int(values[2])
            losses = int(values[3])
            win_percent = wins / (wins + losses)
            conference_wins = int(values[4])
            conference_losses = int(values[5])
            conference_win_percent = conference_wins / (conference_wins / conference_losses)
            division_wins = int(values[6])
            division_losses = int(values[7])
            division_win_percent = division_wins / (division_wins + division_losses)
            
            # Create an object with the values from the csv.
            new_team = {
                "team_name": team_name,
                "wins": wins,
                "losses": losses,
                "win_percent": win_percent,
                "conference_wins": conference_wins,
                "conference_losses": conference_losses,
                "conference_win_percent": conference_win_percent,
                "division_wins": division_wins,
                "division_losses": division_losses,
                "division_win_percent": division_win_percent
            }

            # Create a new division if it was previously not found.
            if not division in districts:
                districts[division] = []
            # Add each team to their respective division.
            districts[division].append(new_team)
    # Return the divisions.
    return districts
            
def compare_teams(team_1: Team, team_2: Team):
    """Returns 1 if team one has better stats. Otherwise returns 0.

    Args:
        team_1 (Team), team_2 (Team)
    """
    if team_1["win_percent"] > team_2["win_percent"]:
        return 1
    elif team_1["win_percent"] == team_2["win_percent"]:
        if team_1["conference_win_percent"] > team_2["conference_win_percent"]:
            return 1
        elif team_1["conference_win_percent"] == team_2["conference_win_percent"]:
            if team_1["division_win_percent"] > team_2["division_win_percent"]:
                return 1
    return 0
            
            
def sort_team(team_list: list[Team]) -> list[Team]:
    """Sorts a list of teams by win ratio using the bubble sort algorithm.

    Args:
        team_list (list[Team]): an unsorted list of team objects.

    Returns:
        list[Team]: a sorted list of team objects.
    """
    for i in range(1, len(team_list)):
        # This is the element we want to position in its
        # correct place
        key_item = team_list[i]
        j = i - 1
        while j >= 0 and compare_teams(team_list[j], key_item):
            team_list[j + 1] = team_list[j]
            j -= 1
        team_list[j + 1] = key_item

    team_list.reverse()
    return team_list
        
        
def sort_divisions(divisions_obj: dict[list[Team]]):
    # Enumerate through the divisions dict.
    for key in divisions_obj:
        division_teams = divisions_obj[key]
        divisions_obj[key] = sort_team(division_teams)

    return divisions_obj
        
# Converts data objects to json.
def to_json(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__, indent=2)
    
    
def filter_table_properties(data, allowed_keys):
    """
    Removes unneeded properties from a dictionary, keeping only the allowed keys.
    
    Args:
        data (dict): The original dictionary.
        allowed_keys (list or set): Keys to retain in the dictionary.
    
    Returns:
        dict: A filtered dictionary with only the allowed keys.
    """
    return {key: data[key] for key in allowed_keys if key in data}


def prepare_table_data(divisions):
    table_data = {}
    for key in divisions:
        table_data[key] = []
        for team in divisions[key]:
            table_data[key].append([
                team["team_name"],
                f"{team["wins"]}-{team["losses"]}",
                f"{team["win_percent"]:.2f}",
                f"{team["conference_wins"]}-{team["conference_losses"]}",
                f"{team["division_wins"]}-{team["division_losses"]}"
            ])
    return table_data



def print_divisions(table_data: dict):
    headers = ["Team Name", "W-L", "Win %", "Conf W-L", "Div W-L"]
    
    for key in table_data:
        print(key)
        print(tabulate(table_data[key], headers=headers, tablefmt="rounded_grid"))
        print()
        


def main():
    teams_data = parse_csv()
    sorted_divisions = sort_divisions(teams_data)
    table_data = prepare_table_data(sorted_divisions)
    print_divisions(table_data)
    


if __name__ == "__main__":
    main()