import os
import platform
from typing import Optional

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def path_of_audio(language: str, text: str = None) -> str:
    if text is None:
        return os.path.join(os.getcwd(), "data", "audio_files", language)
    else:
        return os.path.join(os.getcwd(), "data", "audio_files", language, text + ".mp3")


class FirefoxDriver(webdriver.Firefox):
    def __init__(self, download_dir: Optional[str] = None):
        options = Options()
        if "linux" in platform.system().lower():
            options.add_argument("--headless")
        if download_dir is not None:
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.download.dir", download_dir)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        super().__init__(options=options)
