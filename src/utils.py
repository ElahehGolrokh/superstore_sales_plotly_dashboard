import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Removes  nans and not informative columns from pandas dataframe"""
    df.drop(['Country', 'Customer_Name'], axis=1, inplace=True)
    df.dropna(inplace=True)
    return df
