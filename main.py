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
    print("السكريبت يعمل الآن (عداد ثواني محسّن وسلس)")

    last_second = ""

    while True:
        try:
            now = datetime.datetime.now(ZoneInfo("Africa/Algiers"))
            raw_time = now.strftime("%H:%M:%S")
            
            # نتحقق إذا تغيرت الثانية فعلياً
            if raw_time != last_second:
                fancy_time = to_fancy_digits(raw_time)
                new_name = f"{BASE_NAME} {fancy_time}"

                await client(
                    UpdateProfileRequest(
                        first_name=new_name
                    )
                )

                last_second = raw_time
                print(f"الاسم أصبح: {new_name}")

            # فحص متكرر وسريع (كل 0.3 ثانية) لضمان التزامن الدقيق للثانية
            await asyncio.sleep(0.3)

        except Exception as e:
            print(f"خطأ مؤقت: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(update_time_name())
    except KeyboardInterrupt:
        print("تم إيقاف البرنامج")
    except Exception as e:
        print(f"توقف البرنامج: {e}")
        raise
