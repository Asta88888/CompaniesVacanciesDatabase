from configparser import ConfigParser
import os


def config(filename: str = "database.ini", section: str = "postgresql") -> dict[str, str]:
    """Получает данные из database.ini и возвращает в виде словаря"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, filename)

    parser = ConfigParser()
    parser.read(file_path)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} is not found in the {filename} file.")
    return db
