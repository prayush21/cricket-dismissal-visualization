from flask import Blueprint, jsonify, request
from database import get_db_connection
import logging


api_v2_blueprint = Blueprint('api_v2', __name__, url_prefix='/api/v2')

@api_v2_blueprint.route('/teams', methods=['GET'])
def get_teams():
    cricket_format = request.args.get('format')
    
    if not cricket_format:
        return jsonify({"error": "Format parameter is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT DISTINCT t.name
            FROM teams t
            JOIN teams_formats tf ON t.id = tf.team_id
            JOIN formats f ON f.id = tf.format_id
            WHERE f.name = %s
        """, (cricket_format,))
        
        teams = [row[0] for row in cursor.fetchall()]
        return jsonify(teams)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@api_v2_blueprint.route('/players', methods=['GET'])
def get_players():
    team = request.args.get('team')
    cricket_format = request.args.get('format')
    
    if not team or not cricket_format:
        return jsonify({"error": "Both team and format parameters are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT DISTINCT p.name
            FROM players p
            JOIN players_teams pt ON p.id = pt.player_id
            JOIN teams t ON t.id = pt.team_id
            JOIN teams_formats tf ON t.id = tf.team_id
            JOIN formats f ON f.id = tf.format_id
            WHERE t.name = %s AND f.name = %s
        """, (team, cricket_format))
        
        players = [row[0] for row in cursor.fetchall()]
        return jsonify(players)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@api_v2_blueprint.route('/player-stats', methods=['GET'])
def get_player_stats():
    player_name = request.args.get('player')
    cricket_format = request.args.get('format')
    
    if not player_name or not cricket_format:
        return jsonify({"error": "Both player and format parameters are required"}), 400

    print(player_name, cricket_format)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT ps.max_runs_scored, ps.dismissals_on_ball, ps.dismissals_on_run, ps.matches_played
            FROM player_stats ps
            JOIN players p ON p.id = ps.player_id
            JOIN formats f ON f.id = ps.format_id
            WHERE p.name like %s AND f.name like %s
        """, (player_name, cricket_format))
        
        result = cursor.fetchone()
        if result:
            max_runs, dismissals_on_ball, dismissals_on_run, matches_played = result
            return jsonify({
                "max_runs_scored": max_runs,
                "dismissals_on_ball": dismissals_on_ball,
                "dismissals_on_run": dismissals_on_run,
                "matches_played": matches_played
            })
        else:
            return jsonify({"error": "Player stats not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()