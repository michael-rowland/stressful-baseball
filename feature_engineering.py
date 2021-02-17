import pandas as pd

DATA_FILE = './combined.csv'

def read_data(filepath: str) -> pd.DataFrame:
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
    print(f'Combined shape: {df.shape}')
    df = df.dropna(subset=['events'])

    df['score_diff'] = df['home_score'] - df['away_score']
    df['score_diff'] = df['score_diff'].apply(lambda x: 4 if x > 4 else (-4 if x < -4 else x))
    df['inning_pre'] = df['inning']
    df['inning'] = df['inning'].apply(lambda x: 9 if x >= 9 else x)
    df['on_1b'] = df['on_1b'].apply(lambda x: True if x > 0 else False)
    df['on_2b'] = df['on_2b'].apply(lambda x: True if x > 0 else False)
    df['on_3b'] = df['on_3b'].apply(lambda x: True if x > 0 else False)
    df['outs'] = df['outs_when_up']

    return df


def generate_lookup(path: str = None) -> pd.DataFrame:

    if not path:
        path = './tidy_lookup.csv'

    df = pd.read_csv('https://raw.githubusercontent.com/michael-rowland/stressful-baseball/main/li_lookup.csv')

    # Converts bases to boolean on seperate columns
    # https://chrisalbon.com/python/data_wrangling/pandas_expand_cells_containing_lists/
    bases = (
        df['bases']
        .apply(lambda x: [True if base.isnumeric() else False for base in x.split(' ')])
        .apply(pd.Series)
        .rename(columns = lambda x: f'on_{x+1}b')
    )
    df = pd.concat([df[:], bases[:]], axis=1)

    # make data "tidy"
    df = df.melt(
        id_vars=['inning', 'inning_topbot', 'outs', 'on_1b', 'on_2b', 'on_3b'],
        value_vars=['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'],
        var_name='score_diff',
        value_name='leverage'
    )
    df['score_diff'] = df['score_diff'].astype(int)
    df = df.dropna(subset=['leverage'])

    df.to_csv(path_or_buf=path, index=False)
    return df

if __name__ == "__main__":
    df = read_data(DATA_FILE)
    lookup = generate_lookup()

    pre_merge_size = df.shape
    df = pd.merge(df, lookup, on=['inning', 'inning_topbot', 'outs', 'on_1b', 'on_2b', 'on_3b', 'score_diff'])
    post_merge_size = df.shape
    
    print(pre_merge_size)
    print(post_merge_size)
    assert(pre_merge_size[0] == post_merge_size[0])

    df.to_csv(path_or_buf='./play_events.csv', index=False)