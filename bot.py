#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import logging
from telegram import __version__ as TG_VER

from utils import alternate, check_vless_trojan_format

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Send your v2ray url link (Currently VLESS and Trojan Supported)! Only one url at a time!",
        reply_markup=ForceReply(selective=True),
    )

    text = """ IPs are extracted and provided by @sudoer_grp (https://github.com/MortezaBashsiz/CFScanner)

Bot was developed by @WomanLifeFreedomVPN (https://github.com/wlfvpn/v2ray-url-changer). Nothing will get recorded but feel free to change uuid before submiting the url.

            """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send your v2ray url link (Currently VLESS and Trojan Supported)! Only one url at a time!")


async def get_alternate_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    url = update.message.text.split('\n')[0]
    if check_vless_trojan_format(url):
        alternate_urls = alternate(url)
        text = "`" + '\n'.join(alternate_urls) + "`"
        await update.message.reply_text(text, parse_mode="MarkdownV2")
    else:
        await update.message.reply_text("Sorry, this doesnt look like a vless or trojan link.")



def main() -> None:
    from utils import load_config
    """Start the bot."""
      # Load the config file
    config = load_config("config.yaml") 
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config['telegram_bot_token']).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_alternate_url))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()