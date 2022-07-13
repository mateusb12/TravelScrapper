import json
import os
from pathlib import Path
from typing import Optional

from dotenv import dotenv_values

from references.paths import get_tokens_reference


class TokenLoadErrorException(Exception):
    """Error when loading tokens from a file."""
    pass


def load_env_file() -> dict[str, Optional[str]]:
    file = Path(get_tokens_reference(), ".env")
    file_content = dotenv_values(file)
    if len(file_content) != 0:
        return file_content
    else:
        raise TokenLoadErrorException(f"Error: could not find .env file in {get_tokens_reference()}")


def load_env_tags():
    ref = get_tokens_reference()
    env_tag_file_ref = Path(ref, "environmental_tags.json")
    with open(env_tag_file_ref, "r") as env_tag_file:
        return json.load(env_tag_file)["tags"]


def load_environment_tokens() -> None:
    env_config = load_env_file()
    env_tags = load_env_tags()
    for tag in env_tags:
        if tag in env_config:
            os.environ[tag] = env_config[tag]
        else:
            raise TokenLoadErrorException(f"Error: could not find {tag} in .env file")
    # os.environ["KIWI_TOKEN"] = env_config["KIWI_TOKEN"]
    # os.environ["TELEGRAM_TOKEN"] = env_config["TELEGRAM_TOKEN"]


def existing_env_file() -> bool:
    file = Path(get_tokens_reference(), ".env")
    return file.exists()


def __main():
    # print(existing_env_file())
    print(load_environment_tokens())
    for item in os.environ:
        print(item)
    # env_c = load_env_file()
    # print(env_c)


if __name__ == "__main__":
    __main()
