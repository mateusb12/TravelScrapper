import os

from tokens.token_registry import load_environment_tokens, existing_env_file


class TokenErrorException(Exception):
    def __init__(self, token_type: str):
        self.token_type = token_type
        super().__init__(f"Error: could not find [{token_type}] in environment variables.")


def load_kiwi_token():
    tag = "KIWI_TOKEN"
    if tag in os.environ:
        return os.environ[tag]
    else:
        raise TokenErrorException(tag)


def load_telegram_token():
    tag = "TELEGRAM_TOKEN"
    if tag in os.environ:
        return os.environ[tag]
    else:
        raise TokenErrorException(tag)


def load_all():
    if existing_env_file():
        load_environment_tokens()
    load_kiwi_token()
    load_telegram_token()


def __main():
    load_all()
    aux = dict(os.environ)
    print(load_kiwi_token())
    print(load_telegram_token())


if __name__ == '__main__':
    __main()
