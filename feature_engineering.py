import pandas as pd

DATA_FILE = './combined.csv'

def read_data(filepath: str):
    """
    Read a single ``csv`` file into a single DataFrame
    Cleans data, dropping duplicates, drop pitches that do not result in event
    Returns a DataFrame

    Parameters
    ----------
    filepath : str
        Location of combined ``csv`` file

    Returns
    -------
    pd.DataFrame
    """
    target = [
        'game_pk', 'game_date', 'home_team', 'away_team', 'inning', 'inning_topbot',
        'events', 'des', 'description', 'on_1b', 'on_2b', 'on_3b', 'outs_when_up',
        'home_score', 'away_score'
    ]
    df = pd.read_csv(filepath, usecols=target)
    df = df.dropna(subset=['events'])
    return df

if __name__ == "__main__":
    df = read_data(DATA_FILE)
    print(df.head())