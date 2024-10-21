import os
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
DIR_PATH = "data"


def generate_files():
    with open("members.json", "r") as membersJson:
        members = json.load(membersJson)["members"]
    today = datetime.today()
    week_num = today.isocalendar().week - 1

    sub_dir = f"week{week_num}"
    os.makedirs(f"{DIR_PATH}/{sub_dir}", exist_ok=True)
    for member in members:
        file_path = f"./{DIR_PATH}/{sub_dir}/{member}.html"
        if not os.path.isfile(file_path):
            with open(file_path, "w") as htmlFile:
                htmlFile.write("")
            logging.info(f"Created file: {file_path}")
        else:
            logging.info(f"File already exists: {file_path}")


if __name__ == "__main__":
    generate_files()
