import os
import getpass
# import src.create_database
from dotenv import load_dotenv


def main():
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")
    else:
        print(os.environ["GOOGLE_API_KEY"])


    # DATA_PATH = "data/books/alice.txt"
    # chunks_splitter(DATA_PATH)


if __name__ == "__main__":
    main()

