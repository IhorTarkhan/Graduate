import os
from pathlib import Path


def get_downloads_folder() -> str:
    home = Path.home()
    for x in os.scandir(home):
        if x.name.lower() == "downloads":
            return os.path.join(home, x.name)
