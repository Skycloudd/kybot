#!/usr/bin/env python3

import json
import logging

from bot import KyBot


def setup_logging() -> None:
    FORMAT = "%(asctime)s - [%(levelname)s]: %(message)s"
    DATE_FORMAT = "%d/%m/%Y (%H:%M:%S)"

    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        filename="discord.log", mode="a", encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)


def check_config(filename: str) -> None:
    try:
        with open(filename, "r") as f:
            f.read()
    except FileNotFoundError:

        token = input("bot setup - enter your bot token: ")
        with open(filename, "w+") as f:
            json.dump({"token": token}, f, indent=4)


def check_settings(filename: str) -> None:
    try:
        with open(filename, "r") as f:
            f.read()
    except FileNotFoundError:
        prefix = input("enter a space-seperated list of prefixes you want to use: ")
        prefixes = prefix.split()

        with open(filename, "w+") as f:
            json.dump({"prefixes": prefixes}, f, indent=4)


def check_jsons() -> None:
    check_config("config.json")
    check_settings("settings.json")


def run_bot() -> None:
    bot = KyBot()
    bot.run()


if __name__ == "__main__":
    setup_logging()

    check_jsons()

    run_bot()
