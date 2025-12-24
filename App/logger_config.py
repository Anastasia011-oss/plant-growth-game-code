import logging
from pathlib import Path

def setup_logger():
    documents_path = Path.home() / "Documents"

    project_folder = documents_path / "PlantGame"
    project_folder.mkdir(exist_ok=True)

    log_file = project_folder / "game.log"

    logger = logging.getLogger("GameLogger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Старт программы")
    return logger
