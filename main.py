import os
import time
import pytz
import datetime
from pyrogram import Client


SESSION_STRING = os.environ.get("SESSION_STRING", None)
API_ID = int(os.environ.get("API_ID", None))
API_HASH = os.environ.get("API_HASH", None)
BOTS = [i.strip() for i in os.environ.get("BOTS", None).split()]
BOT_OWNER = os.environ.get("BOT_OWNER", None)
UPDATE_CHANNEL = int(os.environ.get("UPDATE_CHANNEL", None))
MESSAGE_ID = int(os.environ.get("MESSAGE_ID", None))
TIME_LIMIT = int(os.environ.get("TIME_LIMIT", "300"))
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", "30"))
HEADING = os.environ.get("HEADING", "--**Bots Online Status**--")
ATTACH_LINK = os.environ.get("ATTACH_LINK", None)

User = Client(
    "Bot-Status-UserBot",
    SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH
)


def main():
    with User:
        while True:
            
            print("[INFO] starting to check uptime..")
            
            if ATTACH_LINK:
                hide_preview = False
                status_text = f"[\u2063]({ATTACH_LINK})" + HEADING + "\n"
            else:
                hide_preview = True
                status_text = HEADING + "\n"
            
            for bot in BOTS:
                print(f"[INFO] checking @{bot}")
                start_message = User.send_message(
                    chat_id=bot,
                    text='/start'
                )
                time.sleep(SLEEP_TIME)
                message = User.get_history(bot, 1)[0]
                if start_message.message_id == message.message_id:
                    print(f"[WARNING] @{bot} is down")
                    status_text += f"\n🤖 **Bot :-** [{bot}](https://telegram.me/{bot})" \
                                   f"\n**⚜ Status :-** `Offline` ❎\n"
                    User.send_message(
                        chat_id=BOT_OWNER,
                        text=f"@{bot} status: `Down`"
                    )
                else:
                    print(f"[INFO] all good with @{bot}")
                    status_text += f"\n🤖 **Bot :-** [{bot}](https://telegram.me/{bot})" \
                                 f"\n**⚜ Status :-** `Online` ✅\n"
                User.read_history(bot)
            
            limit = TIME_LIMIT // 60
            utc_now = datetime.datetime.now(pytz.timezone('UTC')).strftime("%I:%M %p %d/%m/%y")
            status_text += f"\n**Last checked:**\n{str(utc_now)} UTC ⏰"
            status_text += f"\n`Updated on every {limit} hours`"
            
            try:
                User.edit_message_text(
                    chat_id=UPDATE_CHANNEL,
                    message_id=MESSAGE_ID,
                    text=status_text,
                    disable_web_page_preview=hide_preview
                )
                print(f"[INFO] everything done! sleeping for {limit} hours...")
            except Exception as error:
                error_text = f"Error in editing status message.\nError :- {error}"
                print(error_text)
                User.send_message(
                    chat_id=BOT_OWNER,
                    text=error_text
                )
            
            time.sleep(TIME_LIMIT * 60)


if SESSION_STRING and API_HASH and API_ID and BOTS and BOT_OWNER and UPDATE_CHANNEL and MESSAGE_ID:
    main()
    print("Bot working fine")
else:
    print("Fill full variables")
