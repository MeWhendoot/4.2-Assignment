import json # For handling JSON data
import os # For checking file existence
import subprocess # For opening files in the default application
import platform # For determining the operating system

def EditTeams():
    # Creating an input for each team and its contestants
    teams = {}
    for i in range(1, 5): # Number of teams
        team_name = input(f"Enter name for Team {i}: ") 
        contestants = [] # List to hold contestants for the team
        for j in range(1, 6):
            contestant = input(f"Enter name for {team_name}'s Contestant {j}: ")
            contestants.append(contestant)
        teams[team_name] = {
            "contestants": contestants,
            "points": 0
        }

    # Save the teams to a JSON file
    with open("teams.json", "w") as f:
        json.dump(teams, f, indent=4)

    Start()

def RankTeams():
    # Ranks equal to their points value, from 1 to 4
    rank_points = [10, 5, 3, 2]

    # Check if teams.json exists
    if not os.path.exists("teams.json"):
        print("Please create your teams first!")
        Start()

    # Load the teams from the JSON file
    with open("teams.json", "r") as f:
        teams = json.load(f)
        
    # Creating a list to hold assigned ranks
    team_names = list(teams.keys())
    assigned_ranks = []

    # Prompt user for ranks
    print("\nAssign ranks to each team (1-4):")
    for team in team_names:
        while True:
            try:
                rank = int(input(f"What rank did {team} achieve? (1-4): "))
                if rank < 1 or rank > 4 or rank in assigned_ranks: # Check if rank is valid and not already assigned
                    raise ValueError
                assigned_ranks.append(rank)
                teams[team]["points"] += rank_points[rank - 1] # Assign points based on rank
                break
            except ValueError:
                print("Invalid or duplicate rank. Please enter a unique number from 1 to 4.")

    # Save the updated teams with points to the JSON file
    with open("teams.json", "w") as f:
        json.dump(teams, f, indent=4)

    Start()
    
def ShowScores():
    # Check if teams.json exists
    if not os.path.exists("teams.json"):
        print("No scores available. Please create your teams first!")
        return

    # Load the teams from the JSON file
    with open("teams.json", "r") as f:
        teams = json.load(f)

    # Sort teams by points in descending order
    sorted_teams = sorted(teams.items(), key=lambda item: item[1]["points"], reverse=True)

    # Display the scores
    print("\n--- Team Scores ---")
    for team_name, data in sorted_teams:
        print(f"{team_name}: {data['points']} points")

def OpenTeamsFile():
    file_path = "teams.json"

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

def Start():
    while True:
        print("\nChoose an option:",
        "\n1. Edit Teams",
        "\n2. Assign Ranks",
        "\n3. Show Scores",
        "\n4. Open Teams File",)
        option = input("> ")
        if option == "1":
            EditTeams()
        elif option == "2":
            RankTeams()
        elif option == "3":
            ShowScores()
        elif option == "4":
            OpenTeamsFile()
        elif option == "exit":
            exit(0)
        else:
            print("This is not a valid option!")

Start()
