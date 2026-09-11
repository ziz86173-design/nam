import asyncio
import datetime
import os

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest


# ==============================
# Railway Variables
# ==============================

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

BASE_NAME = os.getenv("BASE_NAME", "اسمك")


# ==============================
# Telegram Client
# ==============================

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)


# ==============================
# تحويل الأرقام
# ==============================

def to_fancy_digits(text):
    normal_digits = "0123456789"
    fancy_digits = "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"

    digits_map = str.maketrans(
        normal_digits,
        fancy_digits
    )

    return str(text).translate(digits_map)


# ==============================
# تحديث الاسم
# ==============================

async def update_time_name():

    await client.connect()

    # التأكد من أن الـSession صالحة
    if not await client.is_user_authorized():
        raise RuntimeError(
            "❌ SESSION_STRING غير صالحة أو انتهت صلاحيتها"
        )

    print("✅ تم الاتصال بحساب Telegram")
    print("🟢 السكريبت يعمل الآن")

    last_time = ""

    while True:

        try:
            # الوقت الحالي
            raw_time = datetime.datetime.now().strftime("%H:%M")

            # تحويل الأرقام
            fancy_time = to_fancy_digits(raw_time)

            # لا نحدث الاسم إلا عند تغير الدقيقة
            if fancy_time != last_time:

                new_name = f"{BASE_NAME} {fancy_time}"

                await client(
                    UpdateProfileRequest(
                        first_name=new_name
                    )
                )

                last_time = fancy_time

                print(
                    f"✅ الاسم أصبح: {new_name}"
                )

            # فحص كل 30 ثانية
            await asyncio.sleep(30)

        except Exception as e:

            print(f"❌ خطأ: {e}")

            await asyncio.sleep(60)


# ==============================
# تشغيل البرنامج
# ==============================

if __name__ == "__main__":
    try:
        asyncio.run(update_time_name())

    except KeyboardInterrupt:
        print("⛔ تم إيقاف البرنامج")

    except Exception as e:
        print(f"❌ توقف البرنامج: {e}")
        raise
