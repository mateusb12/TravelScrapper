import os
from typing import Optional

from dotenv import dotenv_values

from references.paths import get_tokens_reference


class TokenLoadErrorException(Exception):
    """Error when loading tokens from a file."""
    pass


def load_env_file() -> dict[str, Optional[str]]:
    if file := dotenv_values(".env"):
        return dotenv_values(".env")
    else:
        raise TokenLoadErrorException(f"Error: could not find .env file in {get_tokens_reference()}")


def load_environment_tokens() -> None:
    # os.environ["KIWI_TOKEN"] = "yYmWm5MOPD_f00ARApQ9WW5KeX9FrPtv"
    # os.environ["TELEGRAM_TOKEN"] = "5192736712:AAGsjnebJ1IImH131np6c9SwY7PFBv4K7mY"
    env_config = load_env_file()
    os.environ["KIWI_TOKEN"] = env_config["KIWI_TOKEN"]
    os.environ["TELEGRAM_TOKEN"] = env_config["TELEGRAM_TOKEN"]


def __main():
    env_c = load_env_file()
    print(env_c)


if __name__ == "__main__":
    __main()
