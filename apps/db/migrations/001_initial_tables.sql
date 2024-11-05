CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL, 
  json_id VARCHAR(255) NOT NULL
);

CREATE TABLE teams (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE formats (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  folder_path VARCHAR(255)
);

CREATE TABLE players_teams (
  player_id INT REFERENCES players(id),
  team_id INT REFERENCES teams(id),
  PRIMARY KEY (player_id, team_id)
);

CREATE TABLE teams_formats (
  team_id INT REFERENCES teams(id),
  format_id INT REFERENCES formats(id),
  PRIMARY KEY (team_id, format_id)
);

CREATE TABLE player_stats (
  id SERIAL PRIMARY KEY,
  player_id INT REFERENCES players(id),
  format_id INT REFERENCES formats(id),
  max_runs_scored INT,
  dismissals_on_ball JSONB,
  dismissals_on_run JSONB,
  matches_played INT
);

ALTER TABLE player_stats
ADD CONSTRAINT unique_player_format UNIQUE (player_id, format_id);