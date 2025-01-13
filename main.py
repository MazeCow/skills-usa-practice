# Isaac Trost
# NBA Tournament Builder

from dataclasses import dataclass
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
    def win_loss_ratio(self):
        return f"{self.wins}-{self.losses}"
    
    @property
    def conference_win_loss_ratio(self):
        return f"{self.conference_wins}-{self.conference_losses}"
    
    @property
    def division_win_loss_ratio(self):
        return f"{self.division_wins}-{self.division_losses}"
    
    @property
    def win_percent(self):
        return self.wins / {self.wins + self.losses}
    
    @property
    def conference_win_percent(self):
        return self.conference_wins / {self.conference_wins + self.conference_losses}
    
    @property
    def division_win_percent(self):
        return self.division_wins / {self.division_wins + self.division_losses}
    
    
def parse_csv() -> object:
    DATA_PATH = "./data.csv"
    # Object to store the extracted team data.
    teams: object = []
    with open(DATA_PATH, "r") as f:
        # Skips csv headers.
        f.readline()
        # Enumerate through each line the file.
        for line in f:
            # Parse the line into a team object and add it to the teams list.
            values = line[:-1].split(",")
            new_team = Team(*values)
            teams.append(new_team)
    # Return the list of teams.
    return teams
            
def group_teams(team_obj: list[Team]):
    divisions: dict[list[Team]] = {}
    for team in team_obj:
        # Unpack value for easy access.
        division = team.division
        # Check if the team name key exists, initialize it if not.
        if division not in divisions:
            divisions[division] = []
        # Append the team to the correct group.
        divisions[division].append(team)
        
    return divisions
            
def compare_teams(team_1: Team, team_2: Team):
    """Returns 1 if team one has better stats. Otherwise returns 0.

    Args:
        team_1 (Team), team_2 (Team)
    """
    if team_1.win_loss_ratio > team_2.win_loss_ratio:
        return 1
    elif team_1.win_loss_ratio == team_2.win_loss_ratio:
        if team_1.conference_win_loss_ratio > team_2.conference_win_loss_ratio:
            return 1
        elif team_1.conference_win_loss_ratio == team_2.conference_win_loss_ratio:
            if team_1.division_win_loss_ratio > team_2.division_win_loss_ratio:
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
    for key in divisions_obj.keys():
        division = divisions_obj[key]
        divisions_obj[key] = sort_team(division)
    return divisions_obj
        
        
# Converts data objects to json.
def to_json(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__, indent=2)
    

    
    
    
def print_divisions(sorted_divisions):
    for division in sorted_divisions:
        print(division)
        
    
    
def main():
    teams_data = parse_csv()
    grouped_teams = group_teams(teams_data)
    sorted_divisions = sort_divisions(grouped_teams)
    
    print(to_json(sorted_divisions))


if __name__ == "__main__":
    main()