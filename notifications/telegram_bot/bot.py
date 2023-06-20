import os

from telegram import Bot

# load_all_tokens()
TOKEN = os.environ["TELEGRAM_TOKEN"]
telegram_bot_instance = Bot(token=TOKEN)


def __main():
    """Start the bot."""
    telegram_bot_instance.send_message(chat_id=405202204, text="Hello World!")


if __name__ == '__main__':
    __main()
