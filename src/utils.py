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

    # Dictionary for full state names to abbreviations
    state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
        'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
        'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
        'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
        'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
        'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
        'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }

    # Add a new column with state abbreviations
    df['State_Abbrev'] = df['State'].map(state_abbrev)

    # Ensure no missing values after mapping
    missing_abbreviations = df['State_Abbrev'].isnull().sum()
    if missing_abbreviations > 0:
        print(f"Warning: {missing_abbreviations} states could not be converted to abbreviations.")
    return df


def get_color_palette(*items: list) -> dict:
    color_discrete_map = dict()
    colors = ['#133E87', '#608BC1', '#088395', '#003161']
    for i, item in enumerate(*items):
        if item:
            color_discrete_map[item] = colors[i]
    return color_discrete_map
