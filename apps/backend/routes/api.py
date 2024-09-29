from flask import Blueprint, Flask, jsonify, request
from constants import cricket_format_dict
from calculate_and_plot_dismissal_probability import calculate_and_plot_dismissal_probability
import os
import json

api_blueprint = Blueprint('api', __name__)



@api_blueprint.route('/teams', methods=['GET'])
@api_blueprint.route('/teams', methods=['GET'])
def get_teams():
    cricket_format = request.args.get('format')
    print(f"Received request for format: {cricket_format}")
    
    if cricket_format not in cricket_format_dict:
        print(f"Invalid format: {cricket_format}")
        return jsonify({"error": "Invalid format"}), 400
    
    teams_set = set()
   
    try:
        directory = cricket_format_dict[cricket_format]["file_name"]
        print(f"Attempting to read directory: {directory}")
        
        file_sample_set = os.listdir(directory)
        
        for filename in file_sample_set:
            if filename.endswith(".json"):
                file_path = os.path.join(directory, filename)
                print(f"Reading file: {file_path}")
                with open(file_path) as file:
                    match_data = json.load(file)
                    info = match_data.get("info", {})
                    teams = info.get("teams", [])
                    teams_set.update(teams)
        
        print(f"Teams found: {teams_set}")
        return jsonify(list(teams_set))
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/players', methods=['GET'])
def get_players():
    cricket_format = request.args.get('format')
    team = request.args.get('team')    
    
    # Initialize a set to hold unique players for the team
    players_set = set()
    
    # List all files for the selected format
    file_sample_set = os.listdir(cricket_format_dict[cricket_format]["file_name"])
    
    for filename in file_sample_set:
        if filename.endswith(".json"):
            file_path = os.path.join(cricket_format_dict[cricket_format]["file_name"], filename)
            with open(file_path) as file:
                match_data = json.load(file)
                info = match_data.get("info", {})
                teams = info.get("teams", [])
                
                # Check if the team is in the file
                if team in teams:
                    players = info.get("players", {})
                    players_set.update(players.get(team, []))
    
    return jsonify(list(players_set))

@api_blueprint.route('/player_stats', methods=['GET'])
def get_player_stats():
    batter_name = request.args.get('batter_name')
    cricket_format = request.args.get('format')
    
    # Call the function from your script to get the dismissal data
    dismissal_counts, dismissal_probabilities = calculate_and_plot_dismissal_probability(batter_name, cricket_format)
    
    # Return the results as JSON
    return jsonify({
        'batter_name': batter_name,
        'dismissal_counts': dismissal_counts,
        'dismissal_probabilities': dismissal_probabilities
    })




