from dotenv import load_dotenv

from app.telegram.bot import run_bot


def main() -> None:
    load_dotenv()
    run_bot()


if __name__ == "__main__":
    main()


