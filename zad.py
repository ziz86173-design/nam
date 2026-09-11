import asyncio
import datetime
import os

from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest


# ==============================
# إعدادات من Railway Variables
# ==============================

API_ID = int(os.environ["39813032"])
API_HASH = os.environ["5b2cb0003f325440321a1fdcf0bdd072"]

# الاسم الذي سيظهر قبل الوقت
BASE_NAME = "ZAD nvr run"

# اسم ملف Session
SESSION_NAME = "session_name"


# ==============================
# إنشاء Telegram Client
# ==============================

client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH
)


# ==============================
# تحويل الأرقام إلى أرقام مزخرفة
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
# تحديث الاسم بالوقت
# ==============================

async def update_time_name():

    await client.start()

    print("✅ تم تسجيل الدخول إلى Telegram")
    print("🟢 السكريبت بدأ العمل")

    last_time = ""

    while True:

        try:
            # الوقت الحالي
            raw_time = datetime.datetime.now().strftime("%H:%M")

            # تحويل الأرقام
            fancy_time = to_fancy_digits(raw_time)

            # التحديث فقط عند تغير الدقيقة
            if fancy_time != last_time:

                new_name = f"{BASE_NAME} {fancy_time}"

                await client(
                    UpdateProfileRequest(
                        first_name=new_name
                    )
                )

                last_time = fancy_time

                print(
                    f"✅ تم تغيير الاسم إلى: {new_name}"
                )

            # فحص كل 30 ثانية
            await asyncio.sleep(30)

        except Exception as e:

            print(f"❌ حدث خطأ: {e}")

            await asyncio.sleep(60)


# ==============================
# تشغيل البرنامج
# ==============================

if __name__ == "__main__":
    asyncio.run(update_time_name())