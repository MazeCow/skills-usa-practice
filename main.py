# Isaac Trost
# NBA Tournament Builder

from dataclasses import dataclass
from tabulate import tabulate
import os

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
    
    @property
    def table_values(self):
        return [self.team_name, f"{self.wins}-{self.losses}", f"{self.win_percent:.3f}", f"{self.conference_wins}-{self.conference_losses}", f"{self.division_wins}-{self.division_losses}"]
    
    
def parse_csv() -> dict:
    # Data file location.
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

            # Unpack the variables.
            division = str(values[1])
            team_name = str(values[0])
            wins = int(values[2])
            losses = int(values[3])
            conference_wins = int(values[4])
            conference_losses = int(values[5])
            division_wins = int(values[6])
            division_losses = int(values[7])
            
            # Create an object with the values from the csv.
            new_team = Team(team_name, division, wins, losses, conference_wins, conference_losses, division_wins, division_losses)

            # Create a new division if it was previously not found.
            if not division in districts:
                districts[division] = []
                
            # Add each team to their respective division.
            districts[division].append(new_team)
    # Return the divisions.
    return districts
            
            
def compare_teams(team_1: Team, team_2: Team) -> int:
    """Returns 1 if team one has better stats, otherwise returns 0.

    Args:
        team_1 (Team): The first team to compare.
        team_2 (Team): The second team to compare.
    """
    stats = ["win_percent", "conference_win_percent", "division_win_percent"]
    for stat in stats:
        if getattr(team_1, stat) > getattr(team_2, stat):
            return 1
        elif getattr(team_1, stat) < getattr(team_2, stat):
            return 0
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
        
        
def sort_divisions(division_data: dict[list[Team]]):
    # Enumerate through the divisions dict.
    for key in division_data:
        division_teams = division_data[key]
        division_data[key] = sort_team(division_teams)

    return division_data


def prepare_table_data(division_data: dict[list[Team]]) -> dict[list[Team]]:
    """Prepares the divisions dictionary for table use.

    Args:
        divisions (dict[list[Team]]): A dictionary with a key-value pair of a district and a list of teams.

    Returns:
        dict[list[Team]]: A dictionary with 
    """

    table_data = {}
    for key in division_data:
        table_data[key] = []
        for team in division_data[key]:
            table_data[key].append(team.table_values)
    return table_data


def print_division_tables(table_data: dict):
    # Headers
    headers = ["Team Name", "W-L", "Win %", "Conf W-L", "Div W-L"]
    
    # Prints each division name and it's teams.
    for key in table_data:
        print(key)
        print(tabulate(table_data[key], headers=headers, tablefmt="rounded_grid"))
        print()


def get_matchups(division_data: dict[list[Team]]):
    best_teams = []
    worst_teams = []
   
    while len(division_data) > 1:
        worst_team = None
        best_team = None
        for key in division_data:
            for team in division_data[key]:
                if team in best_teams + worst_teams:
                    continue
                
                if worst_team is None:
                    worst_team = team
                elif team.win_percent < worst_team.win_percent:
                    worst_team = team
                        
                if best_team is None:
                    best_team = team
                elif team.win_percent > best_team.win_percent:
                    best_team = team
        best_teams.append(best_team)
        worst_teams.append(worst_team)
    return [best_teams, worst_teams]
        
        
        
            

def main():
    os.system('cls')
    
    # Parse the csv and sort by team win rate in each division.
    teams_data = sort_divisions(parse_csv())
    
    # Parse divisions data so it is usable in a table.
    table_data = prepare_table_data(teams_data)
    
    # Print each division's table.
    print_division_tables(table_data)
    
    print(get_matchups(teams_data))
    
    
    

if __name__ == "__main__":
    main()