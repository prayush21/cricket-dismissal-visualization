import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt

def get_dismissal_probability_distribution(DATA_DIR, title):
    dismissal_distribution = defaultdict(int)
    players_at_ball = defaultdict(int)
    batter_map = defaultdict(int)
    
    file_sample_set = os.listdir(DATA_DIR)[:1]
    print('dir', file_sample_set)
    
    # Loop through all JSON files in the folder
    for filename in file_sample_set:
        if filename.endswith(".json"):
            file_path = os.path.join(DATA_DIR, filename)
            
            with open(file_path) as file:
                match_data = json.load(file)
                
                # Loop through innings and deliveries
                
                for inning in match_data.get("innings", []):
                    overs = inning.get("overs", [])
                    for over_number, over_data in enumerate(overs):
                        print(over_number)
                        deliveries = over_data.get("deliveries", [])
                        for delivery_number, delivery in enumerate(deliveries):
                            batter = delivery["batter"]
                            batter_map[batter] += 1
                            players_at_ball[batter_map[batter]] += 1
                            
                            if 'wickets' in delivery:
                                # Identify batter and number of balls faced before dismissal
                                ball_faced = batter_map[batter]
                                if ball_faced:
                                    dismissal_distribution[ball_faced] += 1
                            
                            
                                
    
    # Calculate probability distribution
    probability_distribution = {}
    # total_players = sum(players_at_ball.values())
    total_players = len(batter_map.keys())
    print(batter_map.keys())
    players_remaining = total_players
    
    for ball in sorted(players_at_ball.keys()):
        if players_remaining > 0:
            # if ball >= 38:
            print(ball, players_remaining, dismissal_distribution[ball], total_players)

            probability = dismissal_distribution[ball] / players_remaining if players_remaining > 0 else 0
            probability_distribution[ball] = probability
            players_remaining -= dismissal_distribution[ball]
    
    ball_numbers = list(probability_distribution.keys())
    dismissal_probabilities = list(probability_distribution.values())

    plt.bar(ball_numbers, dismissal_probabilities)
    plt.xlabel('Ball Number')
    plt.ylabel('Dismissal Probability')
    plt.title('Dismissal Probability by Ball Number for ' + title)
    plt.show()

    return probability_distribution

IPL_DATA_DIR = './ipl_json'
ODI_DATA_DIR = './odis_json'
T20_DATA_DIR = './t20s_json'

dismissal_distribution_ipl = get_dismissal_probability_distribution(IPL_DATA_DIR, 'IPL')
# dismissal_distribution_odi = get_dismissal_probability_distribution(ODI_DATA_DIR, 'ODI')
# dismissal_distribution_t20 = get_dismissal_probability_distribution(T20_DATA_DIR, 'T20')