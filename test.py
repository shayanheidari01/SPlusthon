import ast
import base64
import operator
import random
import secrets
import string
import uuid
from datetime import datetime

from splusthon import SoroushClient, events
from splusthon.events import NewMessage

client = SoroushClient("my_account")

# =========================
# راهنما
# =========================

HELP_TEXT = """
✨ ═══ راهنمای دستورات ═══ ✨

🛠 ابزارهای کاربردی:
🏓 پینگ | نمایش سرعت پاسخ‌دهی
⏰ ساعت | نمایش ساعت فعلی
📅 تاریخ | نمایش تاریخ امروز
🕒 اکنون | نمایش تاریخ و ساعت دقیق
🆔 آیدی | نمایش شناسه عددی شما
🆔 شناسه | ساخت یک UUID تصادفی

💬 پردازش متن:
💬 بگو [متن] | تکرار متن شما
🔄 برعکس [متن] | معکوس کردن متن
🔠 بزرگ [متن] | تبدیل به حروف بزرگ
🔡 کوچک [متن] | تبدیل به حروف کوچک
📏 طول [متن] | شمارش تعداد کاراکترها

🔐 رمزنگاری و امنیت:
🔐 بیس64 [متن] | تبدیل متن به Base64
🔓 ازبیس64 [رشته] | تبدیل Base64 به متن
🔑 رمز [طول] | ساخت رمز عبور امن (پیش‌فرض: ۱۶)

🎲 سرگرمی و ریاضی:
🪙 شیرخط | پرتاب سکه شانس
🎲 تصادفی [کمینه] [بیشینه] | تولید عدد تصادفی
🧮 حساب [عبارت] | ماشین حساب هوشمند

💡 نمونه: حساب (5+3)*8
"""

@client.on(events.NewMessage(pattern=r"^راهنما$", outgoing=True))
async def help_cmd(event: NewMessage.Event):
    await event.reply(HELP_TEXT)

# =========================
# پینگ
# =========================

@client.on(events.NewMessage(pattern=r"^پینگ$", outgoing=True))
async def ping(event: NewMessage.Event):
    start = datetime.now()
    msg = await event.reply("🏓 در حال بررسی سرعت...")
    latency = (datetime.now() - start).total_seconds() * 1000
    await msg.edit(f"🏓 pong!\n\n⏱ زمان پاسخ‌دهی: {latency:.2f} میلی‌ثانیه")

# =========================
# ساعت
# =========================

@client.on(events.NewMessage(pattern=r"^ساعت$", outgoing=True))
async def time_cmd(event: NewMessage.Event):
    current_time = datetime.now().strftime("%H:%M:%S")
    await event.reply(f"⏰ ساعت فعلی:\n🕒 {current_time}")

# =========================
# تاریخ
# =========================

@client.on(events.NewMessage(pattern=r"^تاریخ$", outgoing=True))
async def date_cmd(event: NewMessage.Event):
    current_date = datetime.now().strftime("%Y-%m-%d")
    await event.reply(f"📅 تاریخ امروز:\n🗓 {current_date}")

# =========================
# اکنون
# =========================

@client.on(events.NewMessage(pattern=r"^اکنون$", outgoing=True))
async def datetime_cmd(event: NewMessage.Event):
    current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await event.reply(f"🕒 زمان فعلی:\n📆 {current_dt}")

# =========================
# آیدی
# =========================

@client.on(events.NewMessage(pattern=r"^آیدی$", outgoing=True))
async def id_cmd(event: NewMessage.Event):
    sender = await event.get_sender()
    await event.reply(f"🆔 شناسه شما:\n👤 {sender.id}")

# =========================
# بگو
# =========================

@client.on(events.NewMessage(pattern=r"^بگو (.+)", outgoing=True))
async def echo(event: NewMessage.Event):
    text = event.pattern_match.group(1)
    await event.reply(f"💬 پیام شما:\n\n「 {text} 」")

# =========================
# برعکس
# =========================

@client.on(events.NewMessage(pattern=r"^برعکس (.+)", outgoing=True))
async def reverse(event: NewMessage.Event):
    text = event.pattern_match.group(1)
    await event.reply(f"🔄 متن معکوس شده:\n\n「 {text[::-1]} 」")

# =========================
# بزرگ
# =========================

@client.on(events.NewMessage(pattern=r"^بزرگ (.+)", outgoing=True))
async def upper(event: NewMessage.Event):
    text = event.pattern_match.group(1).upper()
    await event.reply(f"🔠 حروف بزرگ:\n\n「 {text} 」")

# =========================
# کوچک
# =========================

@client.on(events.NewMessage(pattern=r"^کوچک (.+)", outgoing=True))
async def lower(event: NewMessage.Event):
    text = event.pattern_match.group(1).lower()
    await event.reply(f"🔡 حروف کوچک:\n\n「 {text} 」")

# =========================
# طول
# =========================

@client.on(events.NewMessage(pattern=r"^طول (.+)", outgoing=True))
async def length(event: NewMessage.Event):
    text = event.pattern_match.group(1)
    await event.reply(f"📏 طول متن:\n🔢 {len(text)} کاراکتر")

# =========================
# Base64 Encode
# =========================

@client.on(events.NewMessage(pattern=r"^بیس64 (.+)", outgoing=True))
async def b64(event: NewMessage.Event):
    text = event.pattern_match.group(1)
    encoded = base64.b64encode(text.encode()).decode()
    await event.reply(f"🔐 تبدیل به Base64:\n\n{encoded}")

# =========================
# Base64 Decode
# =========================

@client.on(events.NewMessage(pattern=r"^ازبیس64 (.+)", outgoing=True))
async def ub64(event: NewMessage.Event):
    try:
        text = event.pattern_match.group(1)
        decoded = base64.b64decode(text).decode()
        await event.reply(f"🔓 تبدیل از Base64:\n\n{decoded}")
    except Exception:
        await event.reply("❌ رشته Base64 معتبر نیست. لطفاً دوباره تلاش کنید.")

# =========================
# UUID
# =========================

@client.on(events.NewMessage(pattern=r"^شناسه$", outgoing=True))
async def uuid_cmd(event: NewMessage.Event):
    uid = str(uuid.uuid4())
    await event.reply(f"🆔 شناسه یکتا (UUID):\n\n{uid}")

# =========================
# شیر یا خط
# =========================

@client.on(events.NewMessage(pattern=r"^شیرخط$", outgoing=True))
async def coin(event: NewMessage.Event):
    result = random.choice(["🪙 شیر", "🪙 خط"])
    await event.reply(f"🎲 نتیجه پرتاب سکه:\n\n{result}")

# =========================
# عدد تصادفی
# =========================

@client.on(events.NewMessage(pattern=r"^تصادفی (\d+) (\d+)$", outgoing=True))
async def rand(event: NewMessage.Event):
    a = int(event.pattern_match.group(1))
    b = int(event.pattern_match.group(2))

    if a > b:
        a, b = b, a

    num = random.randint(a, b)
    await event.reply(f"🎲 عدد تصادفی بین {a} و {b}:\n\n✨ {num}")

# =========================
# رمز عبور
# =========================

@client.on(events.NewMessage(pattern=r"^رمز(?: (\d+))?$", outgoing=True))
async def password(event: NewMessage.Event):
    length = event.pattern_match.group(1)
    length = int(length) if length else 16

    if length < 4:
        length = 4
    elif length > 100:
        length = 100  # جلوگیری از تولید رمزهای بیش از حد طولانی

    chars = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*()_+-="
    )

    pwd = "".join(
        secrets.choice(chars)
        for _ in range(length)
    )

    await event.reply(f"🔑 رمز عبور ساخته شده ({length} کاراکتر):\n\n{pwd}\n\n⚠️ لطفاً آن را در جای امنی ذخیره کنید.")

# =========================
# ماشین حساب
# =========================

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

def calc(expr):
    node = ast.parse(expr, mode="eval")

    def eval_node(n):
        if isinstance(n, ast.Expression):
            return eval_node(n.body)

        if isinstance(n, ast.Constant):
            return n.value

        if isinstance(n, ast.BinOp):
            return OPS[type(n.op)](
                eval_node(n.left),
                eval_node(n.right),
            )

        if isinstance(n, ast.UnaryOp):
            return OPS[type(n.op)](
                eval_node(n.operand)
            )

        raise ValueError

    return eval_node(node)

@client.on(events.NewMessage(pattern=r"^حساب (.+)", outgoing=True))
async def calculator(event: NewMessage.Event):
    expr = event.pattern_match.group(1)
    try:
        result = calc(expr)
        # تبدیل اعداد صحیح اعشاری (مثل 8.0) به عدد صحیح (8)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
            
        await event.reply(f"🧮 نتیجه محاسبه:\n\n{expr} = {result}")
    except Exception:
        await event.reply("❌ عبارت وارد شده معتبر نیست. لطفاً فرمت ریاضی را بررسی کنید.")

# =========================
# اجرای نهایی
# =========================

if __name__ == "__main__":
    print("✨ ربات با موفقیت اجرا شد! ✨")
    client.start()
    client.run_until_disconnected()