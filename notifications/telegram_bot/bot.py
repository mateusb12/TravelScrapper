from telegram import Bot

from tokens.token_loader import load_all_tokens, load_telegram_token

# load_all_tokens()
TOKEN = load_telegram_token()
telegram_bot_instance = Bot(token=TOKEN)


def __main():
    """Start the bot."""
    telegram_bot_instance.send_message(chat_id=405202204, text="Hello World!")


if __name__ == '__main__':
    __main()
