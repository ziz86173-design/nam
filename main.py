import asyncio
import datetime
import os
from zoneinfo import ZoneInfo

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

BASE_NAME = os.getenv("BASE_NAME", "ZAD")

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)

def to_fancy_digits(text):
    normal_digits = "0123456789"
    fancy_digits = "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
    digits_map = str.maketrans(normal_digits, fancy_digits)
    return str(text).translate(digits_map)

async def update_time_name():
    await client.connect()

    if not await client.is_user_authorized():
        raise RuntimeError("SESSION_STRING غير صالحة أو انتهت صلاحيتها")

    print("تم الاتصال بحساب Telegram")
    print("السكريبت يعمل الآن (عداد الثواني)")

    while True:
        try:
            # جلب الوقت مع الثواني بتوقيت الجزائر
            raw_time = datetime.datetime.now(
                ZoneInfo("Africa/Algiers")
            ).strftime("%H:%M:%S")

            fancy_time = to_fancy_digits(raw_time)
            new_name = f"{BASE_NAME} {fancy_time}"

            # تحديث الاسم في تيليجرام
            await client(
                UpdateProfileRequest(
                    first_name=new_name
                )
            )

            print(f"الاسم أصبح: {new_name}")

            # الانتظار لمدة ثانية واحدة للعد الموالي
            await asyncio.sleep(1)

        except Exception as e:
            print(f"خطأ (قد يكون بسبب الحماية أو ضغط تيليجرام): {e}")
            # إذا تيليجرام دار حظر مؤقت، ننتظر 10 ثوانٍ ونعاودو
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(update_time_name())
    except KeyboardInterrupt:
        print("تم إيقاف البرنامج")
    except Exception as e:
        print(f"توقف البرنامج: {e}")
        raise
