import os


def load_qss(filename):
    """Загружает QSS файл и возвращает его содержимое."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qss_file = os.path.join(current_dir, filename)

    with open(qss_file, "r", encoding="utf-8") as f:
        return f.read()
