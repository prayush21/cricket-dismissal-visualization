import matplotlib.pyplot as plt
import json
import os
from collections import defaultdict

# Path where cricket JSON files are stored
cricket_format_dict = {
    "IPL": {
        "file_name": './ipl_json',
        "title": 'IPL'
    },
    "ODI": {
        "file_name": './odis_json',
        "title": 'ODI'
    },
    "T20": {
        "file_name": './t20s_json',
        "title": 'T20'
    }
}

# Function to calculate dismissal data for all players in a team
def calculate_team_dismissals(team_name, current_format, ball_ranges):
    # Dictionaries to store total balls faced and dismissals in ranges
    balls_faced = defaultdict(int)
    dismissals_in_range = defaultdict(int)
    
    file_sample_set = os.listdir(cricket_format_dict[current_format]["file_name"])[:]

    # Loop through all JSON files in the json folder
    for filename in file_sample_set:
        if filename.endswith(".json"):
            file_path = os.path.join(cricket_format_dict[current_format]["file_name"], filename)
            
            with open(file_path) as file:
                match_data = json.load(file)

                info = match_data.get("info", {})
                teams = info.get("teams", {})
                players = info.get("players", {})
                
                # Check if the team is playing in this match
                if team_name in teams:
                    # Loop through innings and deliveries
                    for inning in match_data.get("innings", []):
                        for over_data in inning.get("overs", []):
                            for delivery in over_data.get("deliveries", []):
                                batter = delivery["batter"]
                                # Check if the batter belongs to the team
                                if batter in players[team_name]:
                                    ball_faced_in_innings = 0

                                    # Track balls faced
                                    if 'wickets' not in delivery:
                                        ball_faced_in_innings += 1
                                        for ball_range in ball_ranges:
                                            if ball_range[0] < ball_faced_in_innings <= ball_range[1]:
                                                balls_faced[ball_range] += 1

                                    # Check if the batter got out on this ball
                                    if 'wickets' in delivery:
                                        for wicket in delivery['wickets']:
                                            if wicket['player_out'] == batter:
                                                for ball_range in ball_ranges:
                                                    if ball_range[0] < ball_faced_in_innings <= ball_range[1]:
                                                        dismissals_in_range[ball_range] += 1

    return dismissals_in_range, balls_faced

# Function to plot dismissal count per ball range for a team
def plot_team_dismissals(team_name, current_format):
    ball_ranges = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60)]
    
    dismissals_in_range, balls_faced = calculate_team_dismissals(team_name, current_format, ball_ranges)
    
    dismissal_counts = []
    range_labels = []
    
    for ball_range in ball_ranges:
        dismissal_counts.append(dismissals_in_range[ball_range])
        range_labels.append(f"{ball_range[0]+1}-{ball_range[1]}")
    
    # Plot the graph (dismissal count in each ball range)
    plt.figure(figsize=(10, 6))
    plt.bar(range_labels, dismissal_counts, color='skyblue')
    plt.title(f"Dismissal Counts per Ball Range for {team_name} in {cricket_format_dict[current_format]['title']}")
    plt.xlabel("Ball Range")
    plt.ylabel("Dismissal Count")
    plt.tight_layout()
    plt.show()

# Example: Calculate and plot dismissal counts for the Indian team in IPL
team_name = "India"
current_format = "ODI"
plot_team_dismissals(team_name, current_format)
