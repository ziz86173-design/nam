
import asyncio
import datetime
import os
from zoneinfo import ZoneInfo

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors import FloodWaitError




API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

BASE_NAME = os.getenv("BASE_NAME", "Z")




client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH,
    auto_reconnect=True,
    connection_retries=10,
    retry_delay=5
)


# =========================
# FANCY CLOCK
# =========================

def to_fancy_digits(text):

    normal_digits = "0123456789"
    fancy_digits = "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"

    digits_map = str.maketrans(
        normal_digits,
        fancy_digits
    )

    return str(text).translate(digits_map)




async def ensure_connection():

    if not client.is_connected():
        print("الاتصال انقطع، جاري إعادة الاتصال...")

        await client.connect()

    if not await client.is_user_authorized():
        raise RuntimeError(
            "SESSION_STRING غير صالحة أو انتهت صلاحيتها"
        )


# =========================
# UPDATE PROFILE NAME
# =========================

async def update_time_name():

    await ensure_connection()

    print("تم الاتصال بحساب Telegram")
    print("السكريبت يعمل الآن")

    last_time = ""

    while True:

        try:

            await ensure_connection()

            raw_time = datetime.datetime.now(
                ZoneInfo("Africa/Algiers")
            ).strftime("%H:%M")

            fancy_time = to_fancy_digits(raw_time)

            if fancy_time != last_time:

                new_name = f"{BASE_NAME} {fancy_time}"

                await client(
                    UpdateProfileRequest(
                        first_name=new_name
                    )
                )

                last_time = fancy_time

                print(f"الاسم أصبح: {new_name}")

            await asyncio.sleep(30)

        except FloodWaitError as e:

            print(
                f"Telegram FloodWait: انتظار {e.seconds} ثانية"
            )

            await asyncio.sleep(e.seconds + 1)

        except asyncio.CancelledError:
            raise

        except Exception as e:

            print(f"خطأ: {e}")

            await asyncio.sleep(10)

            try:
                await ensure_connection()
                print("تم استرجاع الاتصال بنجاح")

            except Exception as reconnect_error:
                print(
                    f"فشل الاتصال، إعادة المحاولة: {reconnect_error}"
                )

                await asyncio.sleep(15)




if __name__ == "__main__":

    try:
        asyncio.run(update_time_name())

    except KeyboardInterrupt:
        print("تم إيقاف البرنامج")

    except Exception as e:
        print(f"توقف البرنامج: {e}")

    finally:
        if client.is_connected():
            asyncio.run(client.disconnect())
