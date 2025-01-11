from datetime import date
from http.cookiejar import MozillaCookieJar
from pathlib import Path
# from pprint import pprint

import logging
import requests


DOCKER_OUTPUT_ROOT_FOLDER = "/nyt/output"

DEBUG = False


if DEBUG:
    logging.basicConfig(level=logging.DEBUG)


puzzles_endpoint = "https://www.nytimes.com/svc/crosswords/v3/puzzles.json"
# puzzle_print_url_format = "https://www.nytimes.com/svc/crosswords/v2/puzzle/print/%s.pdf"
puzzle_url_format = "https://www.nytimes.com/svc/crosswords/v2/puzzle/%s.pdf"


def download(cookies_path: str = "cookies/cookies.txt"):
    # params = {}
    # out_dir = f"{date.today().year}/{date.today().month}"
    Path(DOCKER_OUTPUT_ROOT_FOLDER).mkdir(parents=True, exist_ok=True)

    response = requests.get(puzzles_endpoint).json()["results"]
    logging.debug(f"{response[0]=}")

    with requests.Session() as session:
        # Initiate session
        cookies = MozillaCookieJar(cookies_path)
        cookies.load()
        session.cookies = cookies

        # Set target date
        filename = date.today().strftime("%Y-%m-%d")
        logging.debug(f"{filename=}")

        # Check puzzle publication
        if response:
            if response[0]["print_date"] == filename:
                puzzle_id = response[0]["puzzle_id"]
                logging.debug(f"{puzzle_id=}")
            else:
                print(f"Current puzzle is {response[0]["print_date"]}. Check again later.")
                exit()
        else:
            print("No valid response received from JSON.")
            exit()

        # Set target file URL
        source_filename = puzzle_url_format % puzzle_id
        logging.debug(f"{source_filename=}")

        # Set destination path and check for existing
        dest_path = f"{DOCKER_OUTPUT_ROOT_FOLDER}/{filename}.pdf"
        month_path = f"{DOCKER_OUTPUT_ROOT_FOLDER}/{date.today().strftime("%Y-%m")}/{filename}.pdf"
        if Path(dest_path).exists():
            print(f"{dest_path} already downloaded.")
            exit()
        elif Path(month_path).exists():
            print(f"{month_path} already downloaded.")
            exit()

        # Download the puzzle file
        puzzle = session.get(source_filename)
        if puzzle.status_code != 200:
            print("Request error.")
        else:
            # print(dest_path)
            Path(dest_path).write_bytes(puzzle.content)
            print(f"Downloaded to {dest_path}.")
