import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Removes  nans and not informative columns from pandas dataframe"""
    df.drop(['Country', 'Customer_Name'], axis=1, inplace=True)
    df.dropna(inplace=True)

    # Removing outliers
    df = df[df['Sales'] <= df['Sales'].quantile(0.99)]
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d/%m/%Y')
    df['Month'] = df['Order_Date'].apply(lambda x: x.month)
    df['Year'] = df['Order_Date'].apply(lambda x: x.year)
    return df


def get_color_palette(*items: list) -> dict:
    color_discrete_map = dict()
    colors = ['#133E87', '#608BC1', '#088395', '#003161']
    for i, item in enumerate(*items):
        if item:
            color_discrete_map[item] = colors[i]
    return color_discrete_map
