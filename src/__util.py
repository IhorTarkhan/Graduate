import os
import platform


def selenium_chrome_driver_path() -> str:
    p = platform.platform().lower()
    if "linux" in p:
        return "selenium/chrome/linux_107"
    elif "mac" in p:
        if "arm" not in p:
            return "selenium/chrome/mac_107"
        else:
            return "selenium/chrome/mac_arm_107"
    else:
        return "selenium/chrome/win_107.exe"


def path_of_audio(language: str, text: str = None) -> str:
    if text is None:
        return os.path.join(os.getcwd(), "data", "audio_files", language)
    else:
        return os.path.join(os.getcwd(), "data", "audio_files", language, text + ".mp3")
