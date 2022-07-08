import os


# os.environ["KIWI_TOKEN"] = "yYmWm5MOPD_f00ARApQ9WW5KeX9FrPtv"
# os.environ["TELEGRAM_TOKEN"] = "5192736712:AAGsjnebJ1IImH131np6c9SwY7PFBv4K7mY"

class TokenErrorException(Exception):
    def __init__(self, token_type: str):
        self.token_type = token_type
        super().__init__(f"Error: could not find [{token_type}] in environment variables.")


def load_environment_tokens():
    os.environ["KIWI_TOKEN"] = "yYmWm5MOPD_f00ARApQ9WW5KeX9FrPtv"
    os.environ["TELEGRAM_TOKEN"] = "5192736712:AAGsjnebJ1IImH131np6c9SwY7PFBv4K7mY"


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


def __main():
    load_environment_tokens()
    print(load_kiwi_token())
    print(load_telegram_token())


if __name__ == '__main__':
    __main()
