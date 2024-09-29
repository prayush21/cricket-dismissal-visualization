import matplotlib.pyplot as plt
import json
import os
from collections import defaultdict
from constants import cricket_format_dict

# Path where IPL JSON files are stored
# circket_format_dict = {
#     "IPL": {
#         "file_name": './',
#         "title": 'IPL'
#     },
#     "ODI": {
#         "file_name": './odis_json',
#         "title": 'ODI'
#     },
#     "T20": {
#         "file_name": './t20s_json',
#         "title": 'T20'
#     }
# }

# IPL_DATA_DIR = './ipl_json'
# ODI_DATA_DIR = './odis_json'
# T20_DATA_DIR = './t20s_json'


# Function to calculate dismissal probabilities and draw a graph
def calculate_and_plot_dismissal_probability(batter_name, current_format, plot_graph=False):
    # Dictionaries to store total balls faced and dismissals on nth ball
    balls_faced = defaultdict(int)
    dismissals_on_ball = defaultdict(int)
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
                if batter_name in players[teams[0]] or batter_name in players[teams[1]]:
                    # Loop through innings and deliveries
                    # print("batter_name", batter_name, teams)
                    for inning in match_data.get("innings", []):
                        ball_faced_in_innings = 0
                        for over_data in inning.get("overs", []):
                            for delivery in over_data.get("deliveries", []):
                                # Check if the current delivery was faced by the specified batter
                                
                                if delivery["batter"] == batter_name:
                                                                                                                                          
                                    if 'wickets' not in delivery:                                        
                                        ball_faced_in_innings += 1
                                        balls_faced[ball_faced_in_innings] += 1
                                    
                                    # Check if the batter got out on this ball
                                    if 'wickets' in delivery:
                                        for wicket in delivery['wickets']:
                                            if wicket['player_out'] == batter_name:
                                                dismissals_on_ball[ball_faced_in_innings] += 1
                

    # Calculate probabilities and prepare for plotting
    ball_numbers = sorted(balls_faced.keys())
    dismissal_probabilities = []
    dismissal_counts = []

    for ball_number in ball_numbers:
        probability = dismissals_on_ball[ball_number] / balls_faced[ball_number]
        dismissal_probabilities.append(probability)
        dismissal_counts.append(dismissals_on_ball[ball_number])

    # Plot the graph (dismissal count) if plot_graph is True
    if plot_graph:
        plt.figure(figsize=(10, 6))
        plt.bar(ball_numbers, dismissal_counts, color='skyblue')
        plt.title(f"Dismissal Counts per Ball Faced by {batter_name} in {circket_format_dict[current_format]['title']}")
        plt.xlabel("Ball Number")
        plt.ylabel("Dismissal Count")
        plt.xticks(ball_numbers, rotation=45)
        plt.tight_layout()
        plt.show()

    return dismissal_counts, dismissal_probabilities

# Example usage (commented out)
# batter_name = "V Kohli"
# current_format = "IPL"
# dismissal_counts, dismissal_probabilities = calculate_and_plot_dismissal_probability(batter_name, current_format, plot_graph=True)

# Export the function
if __name__ == "__main__":
    # This block will only run if the script is executed directly
    # You can put any testing or example usage here
    pass
