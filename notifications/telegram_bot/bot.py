from telegram import Bot

TOKEN = open("api.txt", "r").read()
telegram_bot_instance = Bot(token=TOKEN)


def __main():
    """Start the bot."""
    telegram_bot_instance.send_message(chat_id=405202204, text="Hello World!")


if __name__ == '__main__':
    __main()
