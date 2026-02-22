from __future__ import annotations

import asyncio
import pathlib
import sys
import os

from src.discord_bot.bot import DiscordBot


def main():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        bot = DiscordBot()
        asyncio.run(bot.init())
    except KeyboardInterrupt:
        print("Shutting down bot...")
        return


if __name__ == "__main__":
    # Make launching via python.exe and python start_server.py possible
    path_to_this = pathlib.Path(__file__).absolute()
    os.chdir(os.path.dirname(path_to_this))
    main()
