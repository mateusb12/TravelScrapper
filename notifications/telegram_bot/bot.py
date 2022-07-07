from pathlib import Path

from telegram import Bot

from references.paths import get_telegram_bot_reference

token_ref = Path(get_telegram_bot_reference(), "api.txt")
TOKEN = open(token_ref, "r").read()
telegram_bot_instance = Bot(token=TOKEN)


def __main():
    """Start the bot."""
    telegram_bot_instance.send_message(chat_id=405202204, text="Hello World!")


if __name__ == '__main__':
    __main()