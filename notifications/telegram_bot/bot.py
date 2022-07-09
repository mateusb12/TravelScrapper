from pathlib import Path

from telegram import Bot

from references.paths import get_telegram_bot_reference
from tokens.token_loader import load_all, load_telegram_token

token_ref = Path(get_telegram_bot_reference(), "telegram_api_token.txt")
# TOKEN = open(token_ref, "r").read()
load_all()
TOKEN = load_telegram_token()
telegram_bot_instance = Bot(token=TOKEN)


def __main():
    """Start the bot."""
    telegram_bot_instance.send_message(chat_id=405202204, text="Hello World!")


if __name__ == '__main__':
    __main()
