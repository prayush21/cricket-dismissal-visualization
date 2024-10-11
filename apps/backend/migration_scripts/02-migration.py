import sys
import os
import json
import psycopg2
from collections import defaultdict
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import cricket_format_dict

# Establish a connection to PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "my-dummy-cricket-db"),
    user=os.getenv("DB_USER", "prayushdave"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost")
)
cursor = conn.cursor()

print('Connection to DB successful', conn)
# Step 1: Traverse the directories and process each JSON file
formats_dirs = {
    'ODI': 'odis_json',
    'T20': 't20s_json',
    'IPL': 'ipl_json'
}

# Dictionaries to store unique players, teams, and their relationships
players = {}
teams = {}
players_teams = set()
teams_formats = set()
player_stats = defaultdict(lambda: defaultdict(lambda: {'max_runs_scored': 0, 'dismissals_on_ball': defaultdict(int), 'dismissals_on_run': defaultdict(int)}))

def printLogInningsScoreCard(innings_score_card):
    print('Innings Score Card:'.center(100, '#'))
    for player_id, stats in innings_score_card.items():
        print('Player ID: ', player_id, ' Runs: ', stats.get('runs', 0), 'Balls Faced: ', stats.get('balls_faced', 0), 'Is Out: ', stats.get('is_out', False), 'Has Played: ', stats.get('has_played', False))
        print('\n')
    print('#'*100)

def get_id_map(cursor, table_name, id_column='id', key_column='json_id'):
    """
    Create a mapping between two columns in a database table.
    
    :param cursor: Database cursor
    :param table_name: Name of the table to query
    :param id_column: Column to use as the value in the mapping (default: 'id')
    :param key_column: Column to use as the key in the mapping (default: 'json_id')
    :return: Dictionary mapping key_column to id_column
    """
    query = f"SELECT {id_column}, {key_column} FROM {table_name}"
    cursor.execute(query)
    return {row[1]: row[0] for row in cursor.fetchall()}

for format_name, folder in formats_dirs.items():
    folder_path = cricket_format_dict[format_name]["file_name"]
    
    file_sample_set = os.listdir(folder_path)
    print('Starting migration for format: ', format_name)
    for file_name in file_sample_set:
        if file_name.endswith('.json'):
            with open(os.path.join(folder_path, file_name)) as f:
                print('Processing file: ', file_name)
                match_data = json.load(f)
                info = match_data['info']
                match_format = info['match_type']  # T20, ODI, or IPL

                # Step 2: Populate Teams
                match_teams = info.get('teams', [])
                for team in match_teams:
                    teams[team] = teams.get(team, team)  # Ensure uniqueness
                    teams_formats.add((team, format_name))

                # Step 3: Populate Players and Players-Teams Relationships
                match_players = info.get('players', {})
                for team, team_players in match_players.items():
                    for player in team_players:
                        player_id = info['registry']['people'].get(player)
                        if player_id:  # Ensure the player has an ID
                            players[player] = player_id
                            players_teams.add((player_id, team))

                match_score_card = {}
                registry = info['registry']['people']
                for team in info.get('players'):
                    for player in info.get('players')[team]:
                        player_id = registry.get(player)
                        match_score_card[player_id] = {'runs': 0, 'balls_faced': 0, 'is_out': False, 'has_played': False}
                # Step 4: Collect player statistics

                innings = match_data.get('innings', [])
                
                for inning in innings:                    
 
                    overs = inning.get('overs', [])                    
                    
                    # innings_score_card = {}
                    for over in overs:
                        deliveries = over.get('deliveries', [])
                        
                    
                        for delivery in deliveries:                            
                            batter = delivery.get('batter')
                            non_striker = delivery.get('non_striker')                        
                            batter_id = info['registry']['people'].get(batter)
                            non_striker_id = info['registry']['people'].get(non_striker)
                            # if batter_id == '5661ef90':
                            #     print('Batter ID: ', batter_id, batter)
                            # if non_striker_id == '5661ef90':
                            #     print('Non-Striker ID: ', non_striker_id, non_striker)
                            match_score_card[batter_id]['has_played'] = True
                            match_score_card[non_striker_id]['has_played'] = True

                            if batter_id in match_score_card:
                                match_score_card[batter_id]['runs'] += delivery.get('runs', {}).get('batter', 0)
                                match_score_card[batter_id]['balls_faced'] += 1      
                                if 'extras' in delivery:
                                    if 'wides' in delivery['extras'] or 'noballs' in delivery['extras']:
                                        match_score_card[batter_id]['balls_faced'] += -1                                                                                                      
                            else:
                                match_score_card[batter_id] = {'runs': delivery.get('runs', {}).get('batter', 0), 'balls_faced': 1, 'is_out': False}                                                                    
                            if 'wickets' in delivery:
                                for wicket in delivery['wickets']:
                                    player_out = wicket.get('player_out')
                                    player_out_id = info['registry']['people'].get(player_out)                                    
                                    # innings_score_card[player_out_id]['is_out'] = True
                                    match_score_card[player_out_id]['is_out'] = True
                    
                printLogInningsScoreCard(match_score_card)
                for player_id, stats in match_score_card.items():
                    if stats.get('is_out', False) and stats.get('has_played'):
                        player_stats[player_id][match_format]['dismissals_on_ball'][stats['balls_faced']] = player_stats[player_id][match_format]['dismissals_on_ball'].get(stats['balls_faced'], 0) + 1
                        player_stats[player_id][match_format]['dismissals_on_run'][stats['runs']] = player_stats[player_id][match_format]['dismissals_on_run'].get(stats['runs'], 0) + 1                            
                    if stats.get('has_played'):
                        player_stats[player_id][match_format]['matches_played'] = player_stats[player_id][match_format].get('matches_played', 0) + 1
                        player_stats[player_id][match_format]['max_runs_scored'] = max(player_stats[player_id][match_format].get('max_runs_scored', 0), stats.get('runs', 0))

                    
                    # print('-'*100)
                                

# Step 4: Insert Data into Tables

print('Players: ', len(players))
print('-'*100)
print('Teams: ', len(teams))
print('-'*100)
print('Players-Teams: ', len(players_teams))
print('-'*100)
print('Teams-Formats: ', len(teams_formats))
print('-'*100)
print('Player Stats: ', len(player_stats))
print('-'*100)


# Fetch player_id to json_id mapping
player_id_map = get_id_map(cursor, 'players')
print('player_id_map', len(player_id_map))
# print('player_id_map', player_id_map)

# Insert player statistics into player_stats table
cursor.execute("SELECT id, name FROM formats")
format_id_map = get_id_map(cursor, 'formats', key_column='name')

# print('Format ID Map: ', format_id_map)
player_stats_data = []
for player_id, formats in player_stats.items():
    for format_name, stats in formats.items():
        # print(f"Attempting to access player_id: {player_id}")
        if player_id not in player_id_map:
            print(f"Player ID {player_id} not found in player_id_map")
        else:
            player_stats_data.append((
                player_id_map[player_id],
                format_id_map[format_name],
                stats['max_runs_scored'],
                json.dumps(stats['dismissals_on_ball']),
                json.dumps(stats['dismissals_on_run']),
                stats['matches_played']
            ))

cursor.executemany("""
    INSERT INTO player_stats (player_id, format_id, max_runs_scored, dismissals_on_ball, dismissals_on_run, matches_played)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (player_id, format_id) DO UPDATE SET
    max_runs_scored = GREATEST(player_stats.max_runs_scored, EXCLUDED.max_runs_scored),
    dismissals_on_ball = player_stats.dismissals_on_ball || EXCLUDED.dismissals_on_ball,
    dismissals_on_run = player_stats.dismissals_on_run || EXCLUDED.dismissals_on_run,
    matches_played = player_stats.matches_played + EXCLUDED.matches_played
""", player_stats_data)
conn.commit()

# Step 5: Close the connection
cursor.close()
conn.close()

print('Migration complete')