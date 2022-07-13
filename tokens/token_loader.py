import os

from tokens.token_registry import load_environment_tokens, existing_env_file


class TokenErrorException(Exception):
    def __init__(self, token_type: str):
        self.token_type = token_type
        super().__init__(f"Error: could not find [{token_type}] in environment variables.")


def check_env_variable(var_name: str) -> bool:
    return var_name in os.environ


def load_all_tokens():
    if existing_env_file():
        load_environment_tokens()


load_all_tokens()


def load_kiwi_token() -> str:
    tag = "KIWI_TOKEN"
    if tag in os.environ:
        return os.environ[tag]
    else:
        raise TokenErrorException(tag)


def load_telegram_token() -> str:
    tag = "TELEGRAM_TOKEN"
    if tag in os.environ:
        return os.environ[tag]
    else:
        raise TokenErrorException(tag)


def get_postgres_credentials() -> dict:
    tags = ["POSTGRES_HOST", "POSTGRES_DATABASE", "POSTGRES_USER", "POSTGRES_PASSWORD"]
    for tag in tags:
        if tag not in os.environ:
            raise TokenErrorException(tag)
    return {"host": os.environ["POSTGRES_HOST"],
            "database": os.environ["POSTGRES_DATABASE"],
            "user": os.environ["POSTGRES_USER"],
            "password": os.environ["POSTGRES_PASSWORD"]}


def __main():
    load_all_tokens()
    aux = dict(os.environ)
    print(load_kiwi_token())
    print(load_telegram_token())
    print(get_postgres_credentials())


if __name__ == '__main__':
    __main()
