import os
from typing import Optional

from selenium.webdriver.firefox.options import Options


def path_of_audio(language: str, text: str = None) -> str:
    if text is None:
        return os.path.join(os.getcwd(), "data", "audio_files", language)
    else:
        return os.path.join(os.getcwd(), "data", "audio_files", language, text + ".mp3")


class FirefoxOptions(Options):
    def __init__(self, download_dir: Optional[str] = None):
        super().__init__()
        self.add_argument("--headless")
        if download_dir is not None:
            self.set_preference("browser.download.folderList", 2)
            self.set_preference("browser.download.manager.showWhenStarting", False)
            self.set_preference("browser.download.dir", download_dir)
            self.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
