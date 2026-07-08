---
layout: default
title: مفاهیم پایه
nav_order: 4
---

# مفاهیم پایه

در این بخش مفاهیم اساسی SPlusthon را یاد خواهید گرفت. درک این مفاهیم برای استفاده مؤثر از کتابخانه ضروری است.

---

## فهرست مطالب

- [Entity (موجودیت)]({% link concepts/entities.md %})
- [Session (نشست)]({% link concepts/sessions.md %})
- [رویدادها (Events)]({% link concepts/events.md %})
- [String Sessions]({% link concepts/string-sessions.md %})
- [مدیریت خطاها]({% link concepts/errors.md %})
- [API کامل]({% link concepts/full-api.md %})
- [مقایسه Bot API و MTProto]({% link concepts/botapi-vs-mtproto.md %})
- [Mastering asyncio]({% link concepts/asyncio.md %})

---

## مفهوم Entity

**Entity** به هر شیء User، Chat یا Channel اشاره دارد که API در پاسخ به متدهای خاصی مانند `GetUsersRequest` برمی‌گرداند.

### چه چیزی به عنوان Entity استفاده می‌شود؟

- **یوزرنیم‌ها**: مانند `username`
- **شماره تلفن‌ها**: مانند `+989123456789`
- **لینک‌های چت**: مانند `t.me/username`
- **لینک‌های دعوت**: مانند `t.me/joinchat/AAAAAFFszQPyPEZ7wgxLtd`
- **شناسه‌ها**: مانند `123456`
- **آبجکت‌های خود**: مانند `User`، `Chat` یا `Channel`

### ترتیب استفاده از Entity

از **بهترین به بدترین** استفاده کنید:

1. **Input Entities**: مانند `event.input_chat` یا `message.input_sender`
2. **Entities**: مانند `user` یا `channel` (اگر از قبل دارید)
3. **شناسه‌ها**: از کش session استفاده می‌شود
4. **یوزرنیم‌ها، شماره تلفن‌ها و لینک‌ها**: کش استفاده می‌شود مگر اینکه `client.get_entity()` را فراخوانی کنید

---

## مفهوم Session

**Session** بخش مهمی از کتابخانه است که اطلاعات احراز هویت و کش entity را ذخیره می‌کند.

### انواع Session

1. **SQLiteSession**: پیش‌فرض. اطلاعات در فایل SQLite ذخیره می‌شود.
2. **MemorySession**: اطلاعات در حافظه ذخیره می‌شود.
3. **StringSession**: اطلاعات در حافظه ذخیره می‌شود اما می‌تواند به صورت رشته ذخیره شود.

### فایل Session

وقتی `SoroushClient('anon')` ایجاد می‌کنید، فایل `anon.session` در دایرکتوری جاری ایجاد می‌شود. این فایل شامل:

- آدرس IP سرور و پورت
- کلید احراز هویت
- اطلاعات entity‌های مشاهده شده
- access_hash کاربران و کانال‌ها

---

## مفهوم رویدادها (Events)

**رویدادها** برای دریافت نوتیفیکیشن از پیام‌های جدید، عضویت اعضا، تایپ کردن و غیره استفاده می‌شوند.

### انواع رویدادهای اصلی

- **NewMessage**: پیام جدید دریافت شد
- **MessageEdited**: پیام ویرایش شد
- **MessageDeleted**: پیام حذف شد
- **CallbackQuery**: کلیک روی دکمه اینلاین
- **ChatAction**: عضو جدید وارد شد یا خارج شد
- **InlineQuery**: کوئری اینلاین دریافت شد
- **UserUpdate**: اطلاعات کاربر تغییر کرد

### مثال استفاده از رویداد

```python
from splusthon import SoroushClient, events

client = SoroushClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')

client.start()
client.run_until_disconnected()
```

---

## درک Entity در رویدادها

وقتی نیاز به کاربر یا چتی دارید که رویداد در آن رخ داده است، **حتماً** از متدهای زیر استفاده کنید:

```python
async def handler(event):
    # درست
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender_id
    
    # اشتباه - این کار را نکنید
    chat = event.chat
    sender = event.sender
    chat_id = event.chat.id
    sender_id = event.sender.id
```

رویدادها مانند پیام‌ها هستند اما تمام اطلاعات پیام را ندارند! وقتی به صورت دستی پیامی را دریافت می‌کنید، تمام اطلاعات لازم را دارد. اما وقتی آپدیتی درباره پیام دریافت می‌کنید، **تمام اطلاعات را ندارد**، بنابراین باید از **متدها** استفاده کنید، نه ویژگی‌ها.

---

## API کامل

SPlusthon از API کامل سروش‌پلاس پشتیبانی می‌کند. می‌توانید از متدهای پیشرفته برای کنترل دقیق‌تر استفاده کنید.

### مثال استفاده از API خام

```python
from splusthon.tl.functions.messages import SendMessageRequest

await client(SendMessageRequest(
    peer='username',
    message='سلام!',
    random_id=client._get_request_msg_id()
))
```

---

## مقایسه Bot API و MTProto

| ویژگی | Bot API | MTProto (UserBot) |
|--------|---------|-------------------|
| نوع حساب | ربات | کاربر عادی |
| محدودیت پیام | محدود | نامحدود |
| دسترسی به اطلاعات | محدود | کامل |
| API | ساده | پیچیده |
| نیاز به اجازه کاربر | بله | خیر |

---

## Mastering asyncio

SPlusthon بر پایه asyncio ساخته شده است. برای استفاده مؤثر، باید مفاهیم پایه asyncio را درک کنید.

### مبانی

```python
import asyncio
from splusthon import SoroushClient

async def main():
    client = SoroushClient('anon', api_id, api_hash)
    
    # استفاده از await برای عملیات ناهمگام
    me = await client.get_me()
    print(me.stringify())
    
    # اجرای حلقه رویداد
    await client.run_until_disconnected()

# اجرای حلقه اصلی
asyncio.run(main())
```

### نکات مهم

1. تمام متدهایی که با شبکه کار می‌کنند باید با `await` فراخوانی شوند
2. handler‌های رویداد باید `async def` باشند
3. از `client.loop.run_until_complete()` برای اجرای کد ناهمگام در کد همگام استفاده کنید

---

## مرحله بعدی

برای یادگیری بیشتر، بخش‌های زیر را مطالعه کنید:

- [مثال‌ها]({% link examples/index.md %}): مثال‌های عملی و کاربردی
- [مرجع API]({% link api-reference.md %}): مستندات کامل API
