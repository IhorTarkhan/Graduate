import platform
from typing import Optional

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


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
