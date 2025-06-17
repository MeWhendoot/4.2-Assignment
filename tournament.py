import json # For handling JSON data
import os # For checking file existence
import subprocess # For opening files in the default application
import platform # For determining the operating system

TEAMS_FILE = "teams.json"  # Constant for the teams file
NUM_TEAMS = 4  # Number of teams
NUM_CONTESTANTS = 5  # Number of contestants per team
RANK_POINTS = [10, 5, 3, 2]  # Points for each rank

def edit_teams():
    """Prompt user to enter teams and contestants, then save to JSON."""
    
    # Creating an input for each team and its contestants
    teams = {}
    for i in range(1, NUM_TEAMS + 1):
        while True:
            team_name = input(f"Enter name for Team {i}: ").strip()
            if team_name:
                break
            print("Team name cannot be empty.")
        contestants = [] # List to hold contestants for the team
        for j in range(1, NUM_CONTESTANTS + 1):
            while True:
                contestant = input(f"Enter name for {team_name}'s Contestant {j}: ").strip()
                if contestant:
                    break
                print("Contestant name cannot be empty.")
            contestants.append(contestant)
        teams[team_name] = {
            "contestants": contestants,
            "points": 0
        }

    # Save the teams to a JSON file
    with open(TEAMS_FILE, "w") as f:
        json.dump(teams, f, indent=4)


def rank_teams():
    """Assign ranks to teams and update their points."""
    
    # Check if teams.json exists
    if not os.path.exists(TEAMS_FILE):
        print("Please create your teams first!")
        return

    # Load the teams from the JSON file
    with open(TEAMS_FILE, "r") as f:
        teams = json.load(f)
        
    # Creating a list to hold assigned ranks
    team_names = list(teams.keys())
    assigned_ranks = []

    # Prompt user for ranks
    print(f"\nAssign ranks to each team (1-{NUM_TEAMS}):")
    for team in team_names:
        while True:
            try:
                rank = int(input(f"What rank did {team} achieve? (1-{NUM_TEAMS}): "))
                if rank < 1 or rank > NUM_TEAMS or rank in assigned_ranks: # Check if rank is valid and not already assigned
                    raise ValueError
                assigned_ranks.append(rank)
                teams[team]["points"] += RANK_POINTS[rank - 1] # Assign points based on rank
                break
            except ValueError:
                print(f"Invalid or duplicate rank. Please enter a unique number from 1 to {NUM_TEAMS}.")

    # Save the updated teams with points to the JSON file
    with open(TEAMS_FILE, "w") as f:
        json.dump(teams, f, indent=4)


def show_scores():
    """Display the scores of all teams."""
    
    # Check if teams.json exists
    if not os.path.exists(TEAMS_FILE):
        print("No scores available. Please create your teams first!")
        return

    # Load the teams from the JSON file
    with open(TEAMS_FILE, "r") as f:
        teams = json.load(f)

    # Sort teams by points in descending order
    sorted_teams = sorted(teams.items(), key=lambda item: item[1]["points"], reverse=True)

    # Display the scores
    print("\n--- Team Scores ---")
    for team_name, data in sorted_teams:
        print(f"{team_name}: {data['points']} points")


def open_teams_file():
    """Open the teams.json file with the default application."""
    
    file_path = TEAMS_FILE

    # Check if teams.json exists
    if not os.path.exists(file_path):
        print("The teams file does not exist yet.")
        return

    system_name = platform.system()

    # Open the file using the appropriate application based on the operating system
    try:
        if system_name == "Windows":
            subprocess.Popen(["notepad", file_path])
        elif system_name == "Darwin":  # macOS
            subprocess.call(["open", file_path])
        elif system_name == "Linux":
            subprocess.call(["xdg-open", file_path])
        else:
            print("Unsupported operating system.")
    except Exception as e:
        print(f"Failed to open the file: {e}")


def start():
    """Main menu for the tournament program."""
    
    while True:
        print("\nChoose an option:",
        "\n1. Edit Teams",
        "\n2. Assign Ranks",
        "\n3. Show Scores",
        "\n4. Open Teams File",
        "\nType 'exit' to quit.")
        option = input("> ")
        if option == "1":
            edit_teams()
        elif option == "2":
            rank_teams()
        elif option == "3":
            show_scores()
        elif option == "4":
            open_teams_file()
        elif option.lower() == "exit":
            break
        else:
            print("This is not a valid option!")

if __name__ == "__main__":
    start()