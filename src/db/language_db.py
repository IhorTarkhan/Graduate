import csv
import os


class Language:
    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name


def find_all() -> list[Language]:
    result: list[Language] = []
    with open(os.path.join("data", "audio_files", "options.csv")) as file:
        for line in csv.reader(file):
            result.append(Language(line[0], line[1]))
    return result


def find_count() -> int:
    return len(find_all())


def find_all_by_name_like(name: str) -> list[Language]:
    result: list[Language] = []
    with open(os.path.join("data", "audio_files", "options.csv")) as file:
        for line in csv.reader(file):
            if name.lower() in line[1].lower():
                result.append(Language(line[0], line[1]))
    return result
