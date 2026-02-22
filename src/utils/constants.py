from dotenv import load_dotenv


import os
import json
import pathlib


load_dotenv()


class BotConfig:
    BOT_CONFIG_PATH: pathlib.Path = (
        pathlib.Path(os.getcwd()).joinpath("storage").joinpath("bot_config.json")
    )

    @staticmethod
    def get_discord_token() -> str:
        return os.getenv("DISCORD_BOT_TOKEN")

    @staticmethod
    def set_bot_logging_channel_id(channel_id: int) -> None:
        config_manager = DataManager(BotConfig.BOT_CONFIG_PATH)
        config_manager.set_data("logging_channel_id", channel_id)

    @staticmethod
    def get_bot_logging_channel_id() -> int | None:
        config_manager = DataManager(BotConfig.BOT_CONFIG_PATH)
        return config_manager.get_data("logging_channel_id", None)


class DataManager:
    def __init__(self, file_path: pathlib.Path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> dict:
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, "r") as f:
            return json.load(f)

    def save_data(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_data(self, key: str, default=None):
        return self.data.get(key, default)

    def set_data(self, key: str, value) -> None:
        self.data[key] = value
        self.save_data()
