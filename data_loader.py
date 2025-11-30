import os
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def _path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)


def load_matches() -> pd.DataFrame:
    """Load matches from data/matches.csv"""
    path = _path('matches.csv')
    return pd.read_csv(path, parse_dates=['date'])


def load_players() -> pd.DataFrame:
    """Load players from data/players.csv"""
    path = _path('players.csv')
    return pd.read_csv(path)


def load_performances() -> pd.DataFrame:
    """Load player performance rows from data/player_performances.csv

    Numeric columns are coerced to numeric types when possible.
    """
    path = _path('player_performances.csv')
    df = pd.read_csv(path)
    # Convert some columns to numeric
    num_cols = [
        'minutes_played', 'passes_completed', 'passes_missed', 'pass_accuracy',
        'shots', 'shots_on_target', 'shot_accuracy', 'goals', 'assists',
        'yellow_cards', 'red_cards', 'tackles', 'interceptions'
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    return df


def load_all() -> dict:
    """Return a dict with all DataFrames: matches, players, performances"""
    return {
        'matches': load_matches(),
        'players': load_players(),
        'performances': load_performances()
    }


if __name__ == '__main__':
    print('Available data files:')
    for f in ['matches.csv', 'players.csv', 'player_performances.csv']:
        p = _path(f)
        print('-', f, '->', 'FOUND' if os.path.exists(p) else 'MISSING')

# python -m venv .venv; .\.venv\Scripts\Activate.ps1
# pip install -r analize\requirements.txt
# python analize\cli.py
