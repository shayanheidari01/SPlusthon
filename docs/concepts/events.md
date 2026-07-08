---
layout: default
title: رویدادها (Events)
nav_order: 3
parent: مفاهیم پایه
---

# رویدادها (Events)

رویدادها موضوع مهمی در یک پلتفرم پیام‌رسان مانند سروش‌پلاس هستند. در نهایت، می‌خواهید هنگام رسیدن پیام جدید، عضویت عضو جدید، تایپ کردن و غیره نوتیفیکیشن دریافت کنید. برای این کار می‌توانید از **رویدادها** استفاده کنید.

---

## شروع کار

بیایید با یک مثال برای پاسخ خودکار شروع کنیم:

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

این کد زیاد نیست، اما ممکن است برخی چیزها نامفهوم باشد. بیایید آن را تجزیه کنیم:

### ایجاد کلاینت

```python
from splusthon import SoroushClient, events

client = SoroushClient('anon', api_id, api_hash)
```

ایجاد عادی است (البته نام session، API ID و hash را پاس دهید). چیزی نیست که قبلاً ندانیم.

### decorator رویداد

```python
@client.on(events.NewMessage)
```

این decorator پایتون خود را به تعریف `my_event_handler` متصل می‌کند و به طور اساسی به این معنی است که *در* یک رویداد `NewMessage`، تابع callback که قرار است تعریف کنید فراخوانی خواهد شد:

### handler رویداد

```python
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')
```

اگر رویداد `NewMessage` رخ دهد و `'hello'` در متن پیام باشد، ما به رویداد با پیام `'hi!'` پاسخ می‌دهیم.

{: .note }
> handler‌های رویداد **باید** `async def` باشند. در نهایت، SPlusthon یک کتابخانه ناهمگام بر پایه asyncio است که رویکرد ایمن‌تر و اغلب سریع‌تری نسبت به threads است.
>
> **باید** تمام فراخوانی‌های متدی که از درخواست شبکه استفاده می‌کنند را `await` کنید، که بیشتر آنها هستند.

---

## انواع رویدادهای اصلی

### NewMessage

وقتی پیام جدیدی دریافت می‌شود:

```python
@client.on(events.NewMessage)
async def handler(event):
    print(event.raw_text)
```

### NewMessage با فیلتر

فیلتر کردن پیام‌های خروجی:

```python
@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    # فقط پیام‌هایی که شما ارسال کرده‌اید
    print(event.raw_text)
```

فیلتر کردن با regex:

```python
@client.on(events.NewMessage(pattern=r'\.save'))
async def handler(event):
    # فقط پیام‌هایی که با ".save" شروع می‌شوند
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        await client.download_profile_photo(sender)
        await event.respond('عکس شما ذخیره شد {}'.format(sender.username))
```

### MessageEdited

وقتی پیامی ویرایش می‌شود:

```python
@client.on(events.MessageEdited)
async def handler(event):
    print('پیام ویرایش شد:', event.raw_text)
```

### MessageDeleted

وقتی پیامی حذف می‌شود:

```python
@client.on(events.MessageDeleted)
async def handler(event):
    print('پیام حذف شد:', event.message_id)
```

### CallbackQuery

وقتی روی دکمه اینلاین کلیک می‌شود:

```python
@client.on(events.CallbackQuery)
async def handler(event):
    print('کلیک روی دکمه:', event.data)
    await event.answer('شما روی دکمه کلیک کردید!')
```

### ChatAction

وقتی عضو جدید وارد چت می‌شود یا خارج می‌شود:

```python
@client.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
        print('عضو جدید وارد شد:', event.user_id)
    if event.user_left:
        print('عضو خارج شد:', event.user_id)
```

### InlineQuery

وقتی کوئری اینلاین دریافت می‌شود:

```python
@client.on(events.InlineQuery)
async def handler(event):
    # پاسخ به کوئری اینلاین
    await event.answer([
        event.builder.article('نتیجه ۱', text='متن نتیجه ۱')
    ])
```

### UserUpdate

وقتی اطلاعات کاربر تغییر می‌کند:

```python
@client.on(events.UserUpdate)
async def handler(event):
    print('کاربر به روز شد:', event.status)
```

---

## مثال‌های بیشتر

### حذف پیام‌های حاوی کلمه خاص

بیایید پیام‌هایی حاوی "heck" را حذف کنیم. اینجا فحش مجاز نیست:

```python
@client.on(events.NewMessage(pattern=r'(?i).*heck'))
async def handler(event):
    await event.delete()
```

با regex `r'(?i).*heck'`، "heck" را به صورت حساس به حرف بزرگ/کوچک در هر جای پیام تطبیق می‌دهیم. Regex بسیار قدرتمند است و می‌توانید در https://regexone.com/ بیشتر یاد بگیرید.

### پاسخ به پیام خاص

```python
@client.on(events.NewMessage(pattern=r'(?i)hi|hello'))
async def handler(event):
    await event.respond('سلام! چطور می‌توانم کمک کنم؟')
```

### ارسال پیام به کانال خاص

```python
@client.on(events.NewMessage(chats='channel_username'))
async def handler(event):
    # فقط پیام‌های کانال خاصی
    print(event.raw_text)
```

### فیلتر پیام‌های خروجی و ورودی

```python
# فقط پیام‌های خروجی (پیام‌هایی که شما ارسال کرده‌اید)
@client.on(events.NewMessage(outgoing=True))
async def handler_outgoing(event):
    print('شما ارسال کردید:', event.raw_text)

# فقط پیام‌های ورودی (پیام‌هایی که دیگران ارسال کرده‌اید)
@client.on(events.NewMessage(incoming=True))
async def handler_incoming(event):
    print('شما دریافت کردید:', event.raw_text)
```

---

## دسترسی به Entity‌ها در رویدادها

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

## نکات مهم

{: .important }
> فراموش نکنید که logging را هنگام کار با رویدادها فعال کنید، زیرا خطاها در handler‌های رویداد به طور پیش‌فرض پنهان هستند. لطفاً قطعه کد زیر را در بالای فایل خود اضافه کنید:

```python
import logging
logging.basicConfig(format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
```

---

## خلاصه

رویدادها به شما امکان می‌دهند به پیام‌ها و اتفاقات مختلف در سروش‌پلاس پاسخ دهید. با استفاده از decorator‌های `@client.on()` می‌توانید handler‌های مختلفی برای انواع رویدادها ثبت کنید.

---

## مرحله بعدی

برای یادگیری بیشتر درباره String Sessions، بخش [String Sessions]({% link concepts/string-sessions.md %}) را مطالعه کنید.
