from telegram import Bot

TOKEN = "5192736712:AAGsjnebJ1IImH131np6c9SwY7PFBv4K7mY"
telegram_bot_instance = Bot(token=TOKEN)


def __main():
    """Start the bot."""
    telegram_bot_instance.send_message(chat_id=405202204, text="Hello World!")


if __name__ == '__main__':
    __main()
