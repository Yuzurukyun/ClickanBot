from __future__ import annotations

import asyncio
import pathlib
import sys
import os

from src.discord_bot.bot import DiscordBot


class Main:
    def __init__(self):
        self.python_version_check()

    @staticmethod
    def python_version_check():
        current_python_tuple = sys.version_info
        current_python_simple = "Python {}.{}.{}".format(*current_python_tuple[:3])
        if current_python_tuple < (3, 9):
            # This deliberately uses .format() because f-strings were not available prior to
            # Python 3.7, and 3.7 < 3.9
            msg = (
                "This bot requires at least Python 3.9. You currently have "
                "{}. Please refer to README.md for instructions on updating.".format(
                    current_python_simple
                )
            )
            raise RuntimeError(msg)

    @staticmethod
    def log_bot(message: str) -> None:
        print(f"[DISCORD] {message}")

    def main(self):
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        async def runner():
            await self.run_bot()

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass

    async def run_bot(self):
        """Runs the bot."""
        bot = DiscordBot()
        try:
            await bot.init()
        except KeyboardInterrupt:
            print("Shutting down bot immediately...")
            tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise


if __name__ == "__main__":
    # Make launching via python.exe and python main.py possible
    path_to_this = pathlib.Path(__file__).absolute()
    os.chdir(os.path.dirname(path_to_this))
    main = Main()
    main.main()
