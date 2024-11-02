import pandas as pd

from src.dashboard import get_app, Controller
from src.utils import clean


def main():
    # Incorporate data
    df = pd.read_csv('data/superstore_final_dataset (1).csv', encoding='latin-1')
    df = clean(df)
    app = get_app(df)
    print(app.config.assets_folder)
    Controller(df).add_callbacks(app)
    app.run(debug=True)


if __name__ == '__main__':
    main()
