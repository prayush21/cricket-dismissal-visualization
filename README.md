# Cricket D3 - Dismissal Distribution Dashboard

This is a full-stack web application that provides a dashboard for cricket players' dismissal statistics. Users can select a cricket format (ODI, T20, or IPL), a team, and a player to view detailed statistics about their dismissals.

## Features

- Interactive dashboard to visualize cricket player dismissal statistics.
- Filter by cricket format (ODI, T20, IPL), team, and player.
- View player dismissal statistics graphically, with options to see dismissals by ball and by run.
- RESTful API to serve cricket data.

## Technologies Used

### Backend

- **Framework:** Flask
- **Language:** Python
- **Database:** PostgreSQL

### Frontend

- **Framework:** Next.js
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** Shadcn UI
- **Charting:** Chart.js

## Project Structure

The project is organized into three main directories:

- `apps/backend`: Contains the Flask backend application.
- `apps/frontend`: Contains the Next.js frontend application.
- `apps/db`: Contains the database schema and migration scripts.

### Backend Details

The backend is a Flask application that serves the cricket data. It reads data from JSON files located in the `apps/backend/` directory (`ipl_json`, `odis_json`, `t20s_json`). The main components of the backend are:

- `app.py`: The main application file that initializes the Flask app and registers the API blueprints.
- `routes/api.py` and `routes/api_v2.py`: These files define the API endpoints for fetching teams, players, and player statistics.
- `database.py`: Contains the logic for interacting with the PostgreSQL database.

### Frontend Details

The frontend is a Next.js application that provides the user interface for the dashboard. The main components of the frontend are:

- `src/app/page.tsx`: The main page of the application that renders the `CricketDashboard` component.
- `src/app/CricketDashboard.tsx`: The core component of the frontend that handles state management, data fetching, and rendering of the dashboard.
- `src/components/ui/`: Contains the reusable UI components used in the application.

### Database Details

The database is a PostgreSQL database with a schema designed to store information about players, teams, formats, and player statistics. The schema is defined in the `apps/db/migrations/001_initial_tables.sql` file.

## Setup and Installation

### Prerequisites

- Python 3.x
- Node.js and npm
- PostgreSQL

### Backend Setup

1.  Navigate to the `apps/backend` directory.
2.  Create a virtual environment: `python3 -m venv venv`
3.  Activate the virtual environment: `source venv/bin/activate`
4.  Install the required packages: `pip install -r requirements.txt`
5.  Run the application: `python app.py`

### Frontend Setup

1.  Navigate to the `apps/frontend` directory.
2.  Install the required packages: `npm install`
3.  Run the application: `npm run dev`

### Database Setup

1.  Make sure PostgreSQL is running.
2.  Create a database named `player_stats_db`.
3.  Run the migration scripts in the `apps/db/migrations` directory to create the tables.

## API Endpoints

The backend exposes the following API endpoints:

### API v1

- `GET /teams?format=<format>`: Get a list of teams for a given format.
- `GET /players?format=<format>&team=<team>`: Get a list of players for a given team and format.
- `GET /player_stats?batter_name=<batter_name>&format=<format>`: Get the dismissal statistics for a player.

### API v2

- `GET /api/v2/teams?format=<format>`: Get a list of teams for a given format.
- `GET /api/v2/players?format=<format>&team=<team>`: Get a list of players for a given team and format.
- `GET /api/v2/player-stats?format=<format>&player=<player>`: Get the dismissal statistics for a player.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
