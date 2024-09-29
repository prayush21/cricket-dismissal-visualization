import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt


# Path where IPL JSON files are stored
IPL_DATA_DIR = './ipl_json'
ODI_DATA_DIR = './odis_json'
T20_DATA_DIR = './t20s_json'

# Dismissal dictionary to track dismissals on nth ball

def get_dismissal_distribution(DATA_DIR, title):
    dismissal_distribution = defaultdict(int)
    
    file_sample_set = os.listdir(DATA_DIR)
    print('dir',file_sample_set)
    # Loop through all JSON files in the IPL folder
    for filename in file_sample_set:
        if filename.endswith(".json"):
            file_path = os.path.join(DATA_DIR, filename)
            
            with open(file_path) as file:
                match_data = json.load(file)
                # print('match_data',match_data)
                # Loop through innings and deliveries
                batter_map = defaultdict(int)
                for inning in match_data.get("innings", []):
                    
                    for over_data in inning.get("overs", []):
                        for delivery in over_data.get("deliveries", []):
                            batter = delivery["batter"]
                            batter_map[batter] += 1
                            if 'wickets' in delivery:
                                # Identify batter and number of balls faced before dismissal
                                ball_faced = batter_map[batter]
                                if ball_faced:
                                    dismissal_distribution[ball_faced] += 1

    
    ball_numbers = list(dismissal_distribution.keys())
    dismissal_counts = list(dismissal_distribution.values())

    plt.bar(ball_numbers, dismissal_counts)
    plt.xlabel('Ball Number')
    plt.ylabel('Dismissal Count')
    plt.title('Dismissals by Ball Number for '+ title)
    plt.show()

    return dismissal_distribution


                            
# Display the distribution of dismissals by ball number
# for ball_number, count in sorted(get_dismissal_distribution().items()):
#     print(f"Batsman got out {count} times on ball number {ball_number}")

dismissal_distribution_ipl = get_dismissal_distribution(IPL_DATA_DIR, 'IPL')
# dismissal_distribution_odi = get_dismissal_distribution(ODI_DATA_DIR, 'ODI')
# dismissal_distribution_t20 = get_dismissal_distribution(T20_DATA_DIR, 'T20')

# Plot the distribution
