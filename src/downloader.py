from datetime import date
from pathlib import Path

import requests

puzzles_endpoint = "https://edge.games.nyti.nyt.net/svc/crosswords/v3/35806626/puzzles.json"
puzzle_print_url_format = f"https://www.nytimes.com/svc/crosswords/v2/puzzle/print/{_}.pdf"
puzzle_url_format = f"https://www.nytimes.com/svc/crosswords/v2/puzzle/{_}.pdf"
