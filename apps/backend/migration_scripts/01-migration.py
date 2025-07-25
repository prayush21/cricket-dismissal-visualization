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



for format_name, folder in formats_dirs.items():
    folder_path = cricket_format_dict[format_name]["file_name"]
    
    file_sample_set = os.listdir(folder_path)
    print('Starting migration for format: ', format_name)
    for file_name in file_sample_set:
        if file_name.endswith('.json'):
            with open(os.path.join(folder_path, file_name)) as f:
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

# Step 4: Insert Data into Tables

print('Players: ', len(players))
print('-'*100)
print('Teams: ', len(teams))
print('-'*100)
print('Players-Teams: ', len(players_teams))
print('-'*100)
print('Teams-Formats: ', len(teams_formats))

# Insert Players into players table
cursor.executemany(
    "INSERT INTO players (name, json_id) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET json_id = EXCLUDED.json_id",
    [(player_name, player_id) for player_name, player_id in players.items()]
)
conn.commit()

# Insert Teams into teams table
cursor.executemany(
    "INSERT INTO teams (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
    [(team_name,) for team_name in teams.values()]
)
conn.commit()

# Fetch player_id to json_id mapping
cursor.execute("SELECT id, json_id FROM players")
player_id_map = {json_id: id for id, json_id in cursor.fetchall()}

# Insert Players-Teams Associations
players_teams_data = []
for json_id, team_name in players_teams:
    if json_id in player_id_map:
        players_teams_data.append((player_id_map[json_id], team_name))

cursor.executemany("""
    INSERT INTO players_teams (player_id, team_id)
    SELECT %s, t.id FROM teams t WHERE t.name = %s
    ON CONFLICT (player_id, team_id) DO NOTHING
""", players_teams_data)
conn.commit()

# Insert Teams-Formats Associations
cursor.executemany("""
    INSERT INTO teams_formats (team_id, format_id)
    SELECT t.id, f.id FROM teams t, formats f WHERE t.name = %s AND f.name = %s
    ON CONFLICT (team_id, format_id) DO NOTHING
""", teams_formats)
conn.commit()

# Step 5: Close the connection
cursor.close()
conn.close()

print('Migration complete')