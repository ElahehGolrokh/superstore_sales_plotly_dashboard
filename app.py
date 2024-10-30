from src.dashboard import get_app

def main():
    app = get_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()