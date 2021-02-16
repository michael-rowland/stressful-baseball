import os

import pandas as pd

DATA_DIRECTORY = './game_data/'

def combine_files(input_loc: str, path: str = None, verbose: bool = False) -> pd.DataFrame:
    """
    Combine multiple ``csv`` files into a single DataFrame
    This function assumes all input files have consistent column names 

    Parameters
    ----------
    input_loc : str
        Location of files to combine
    path : str, default None
        Location to write the combined .csv file to
        ex: './combined.csv'
    verbose : bool, default False
        Print status of combining operation

    Returns
    -------
    pd.DataFrame
        Also, combined ``csv`` is written to path parameter location
    """
    if not path:
        path = input_loc + 'combined.csv'

    df = pd.DataFrame()

    for file in os.listdir(input_loc):
        if file.endswith(".csv"):
            df = pd.concat([df, pd.read_csv(DATA_DIRECTORY+file)])
            df = df.drop_duplicates()
            if verbose:
                print(f'File: {file}\tDataFrame size: {df.shape}')

    df.to_csv(path_or_buf=path, index=False)
    return df


if __name__ == '__main__':
    combine_files(
        input_loc=DATA_DIRECTORY,
        path='./combined.csv',
        verbose=True
    )