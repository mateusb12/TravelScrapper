import os
from pathlib import Path
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
    env_config = load_env_file()
    os.environ["KIWI_TOKEN"] = env_config["KIWI_TOKEN"]
    os.environ["TELEGRAM_TOKEN"] = env_config["TELEGRAM_TOKEN"]


def existing_env_file() -> bool:
    file = Path(get_tokens_reference(), ".env")
    return file.exists()


def __main():
    print(existing_env_file())
    # env_c = load_env_file()
    # print(env_c)


if __name__ == "__main__":
    __main()
