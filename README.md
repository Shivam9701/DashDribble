---

### `README.md` for Dashdribble Project

# Dashdribble: Football Data Platform

Dashdribble is a football data platform designed to track leagues, teams, and standings from top European leagues. Our goal is to provide detailed analysis and modelling for everyone.

---

## Table of Contents

1. [Setup and Installation](#setup-and-installation)
2. [Usage](#usage)
3. [Database Schema](#database-schema)
4. [Contributing](#contributing)
5. [License](#license)

---

## Setup and Installation

### Prerequisites

Before setting up this project, ensure you have the following tools installed:

- Python 3.12+
- SQLite (for local database management)
- Git
- Node.js & npm (if you are using front-end development)

### Clone the Repository

First, clone the repository to your local machine.

```bash
git clone https://github.com/Shivam9701/DashDribble
cd dashdribble
```

### Install Python Dependencies

This project uses `uv` for dependency management. If you haven't installed `uv` yet, follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

Install dependencies using:

```bash
uv install
```

If you prefer `pip`, install dependencies via:

```bash
pip install -r requirements.txt
```

---

## Usage

### Database Setup

1. **Configuration**: 
   Set your database path in the `.env` file located in the `db/` folder. The path should point to your SQLite database.

   Example `.env` file:

   ```bash
   DB_PATH=path/to/dashdribble.db
   ```

2. **Create Database Schema**:
   Run the `db_*` scripts to create the database and tables:

   ```bash
   python db/scripts/db_*.py
   ```

### Inserting Data

1. **Inserting Leagues Data**:
   Data for the top leagues is stored as JSON files in `data/historical_winners/` folder. Run the script to insert this data into the `league_teams` table:

   ```bash
   python db/scripts/main.py insert_leagues
   ```

2. **Inserting Team Data**:
   Data for current teams and standings is stored in `data/current_league_teams/` folder. Run the script to insert this data into `league_teams` and `current_standings` tables:

   ```bash
   python db/scripts/main.py insert_teams
   ```

---

## Database Schema

The project uses an SQLite database with the following tables:

### `leagues`

- **id** (Primary Key): Unique identifier for each league.
- **name**: Name of the league.
- **code**: Short code for the league (e.g., "PL").
- **emblem**: URL to the league's emblem.
- **current_season_id**: ID of the current season (reference from a separate table).
- **current_matchday**: The current matchday in the league.

### `league_teams` (Static Table)

- **id** (Primary Key): Unique team identifier.
- **league_id** (Foreign Key): References `id` in `leagues`.
- **team_id**: Unique identifier for the team.
- **name**: Full name of the team.
- **short_name**: Short name of the team.
- **tla**: Three-letter abbreviation of the team.
- **crest**: URL to the team's crest.

### `current_standings` (Dynamic Table)

- **league_id** (Foreign Key): References `id` in `leagues`.
- **team_id** (Foreign Key): References `team_id` in `league_teams`.
- **position**: Current position of the team in the standings.
- **played_games**: Number of games played by the team.
- **won**: Number of games won by the team.
- **draw**: Number of games drawn by the team.
- **lost**: Number of games lost by the team.
- **points**: Current points of the team.
- **goals_for**: Goals scored by the team.
- **goals_against**: Goals conceded by the team.
- **goal_difference**: Difference between goals scored and conceded.

---

## Contributing

We welcome contributions! If you have any suggestions, fixes, or improvements:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Create a pull request.

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

Let me know if you'd like any further changes!