import pandas as pd

from src.dashboard import get_app, Controller
from src.utils import clean


def main():
    # Incorporate data
    data_path = 'data/superstore_final_dataset (1).csv'
    df = pd.read_csv(data_path,
                     encoding='latin-1')
    df = clean(df)
    app = get_app()
    server = app.server
    print(app.config.assets_folder)
    Controller(df).add_callbacks(app)
    app.run(debug=True, host="0.0.0.0", port=8050)


if __name__ == '__main__':
    main()
