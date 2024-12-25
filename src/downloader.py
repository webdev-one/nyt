from datetime import date
from http.cookiejar import MozillaCookieJar
from pathlib import Path
from pprint import pprint

import requests


# puzzles_endpoint = "https://www.nytimes.com/svc/crosswords/v3/puzzles.json"
puzzle_print_url_format = "https://www.nytimes.com/svc/crosswords/v2/puzzle/print/%s.pdf"
# puzzle_url_format = f"https://www.nytimes.com/svc/crosswords/v2/puzzle/{_}.pdf"


def download(cookies_path: str = "cookies.txt"):
    # params = {}
    out_dir = f"{date.today().year}/{date.today().month}"
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # response = requests.get(puzzles_endpoint, params).json()
    # pprint(response)

    with requests.Session() as session:
        # Initiate session
        cookies = MozillaCookieJar(cookies_path)
        cookies.load()
        session.cookies = cookies

        #Set source filename
        source_filename=date.today().strftime("%b%d%y")
        pprint(source_filename)

        # Set destination path and check for existing
        dest_filename = f"{date.today().year}{date.today().month}{date.today().day}"
        dest_path = f"{out_dir}/{dest_filename}"
        if Path(dest_path).exists():
            pprint(f"{dest_path} already downloaded.")

        # Download the puzzle file
        puzzle = session.get(puzzle_print_url_format % source_filename)
        if puzzle.status_code != 200:
            pprint("Request error.")
        else:
            print(dest_path)
            Path(dest_path).write_bytes(puzzle.content)