---
hide:
  - navigation
---

# مثال‌ها

در این بخش مثال‌های عملی و کاربردی برای یادگیری بهتر SPlusthon آورده شده است.

---

## فهرست مطالب

<div class="grid cards" markdown>

-   :material-account:{ .lg .middle } __کاربران__

    ---

    مثال‌هایی برای کار با کاربران در SPlusthon.

    [:octicons-arrow-right-24: ببینید](users.md)

-   :material-chat:{ .lg .middle } __چت‌ها و کانال‌ها__

    ---

    مثال‌هایی برای کار با چت‌ها و کانال‌ها.

    [:octicons-arrow-right-24: ببینید](chats-and-channels.md)

-   :material-message:{ .lg .middle } __کار با پیام‌ها__

    ---

    مثال‌هایی برای کار با پیام‌ها.

    [:octicons-arrow-right-24: ببینید](working-with-messages.md)

-   :material-alert:{ .lg .middle } __هشدار مهم__

    ---

    نکات مهم و هشدارها هنگام استفاده از SPlusthon.

    [:octicons-arrow-right-24: ببینید](word-of-warning.md)

</div>

---

## مثال‌های ساده

### ارسال پیام ساده

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        await client.send_message('me', 'سلام، خودم!')
        
        # ارسال با قالب‌بندی
        await client.send_message('me', 'این پیام **بولد** است.')
        
        # ارسال با پیش‌نمایش لینک غیرفعال
        await client.send_message('me', 'https://example.com', link_preview=False)

import asyncio
asyncio.run(main())
```

### دریافت پیام‌ها

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت آخرین پیام‌ها
        messages = await client.get_messages('me', limit=10)
        
        for message in messages:
            print(f'{message.id}: {message.text}')

import asyncio
asyncio.run(main())
```

### ارسال فایل

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال عکس
        await client.send_file('me', '/path/to/photo.jpg')
        
        # ارسال فایل با عنوان
        await client.send_file('me', '/path/to/file.pdf', caption='فایل مهم')

import asyncio
asyncio.run(main())
```

---

## مثال‌های رویدادی

### پاسخ خودکار به پیام‌ها

```python
from splusthon import SoroushClient, events

client = SoroushClient('anon', api_id, api_hash)

@client.on(events.NewMessage(pattern=r'(?i)hi|hello'))
async def handler(event):
    await event.reply('سلام! چطور می‌توانم کمک کنم؟')

@client.on(events.NewMessage(pattern=r'(?i)help'))
async def help_handler(event):
    await event.respond('این یک پیام کمکی است.')

client.start()
client.run_until_disconnected()
```

### پاسخ به پیام خاص

```python
from splusthon import SoroushClient, events

client = SoroushClient('anon', api_id, api_hash)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.save'))
async def handler(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        await client.download_profile_photo(sender)
        await event.respond(f'عکس شما ذخیره شد {sender.username}')

client.start()
client.run_until_disconnected()
```

---

## مثال‌های پیشرفته

### مدیریت خطا

```python
from splusthon import SoroushClient, events
from splusthon.errors import FloodWaitError, RPCError

client = SoroushClient('anon', api_id, api_hash)

async def safe_send(client, entity, message):
    try:
        await client.send_message(entity, message)
        return True
    except FloodWaitError as e:
        import asyncio
        await asyncio.sleep(e.seconds)
        return True
    except RPCError as e:
        print(f'خطا: {e}')
        return False

@client.on(events.NewMessage)
async def handler(event):
    await safe_send(client, 'me', 'پاسخ خودکار')

client.start()
client.run_until_disconnected()
```

### کار با چندین کلاینت

```python
import asyncio
from splusthon import SoroushClient

async def run_client(name, api_id, api_hash):
    client = SoroushClient(name, api_id, api_hash)
    await client.start()
    print(f'کلاینت {name} شروع شد')
    await client.run_until_disconnected()

async def main():
    await asyncio.gather(
        run_client('client1', api_id1, api_hash1),
        run_client('client2', api_id2, api_hash2)
    )

asyncio.run(main())
```

---

## نکات مهم

!!! note "یادداشت"
    این مثال‌ها فرض می‌کنند که شما API ID و Hash خود را از [my.telegram.org](https://my.telegram.org/) دریافت کرده‌اید.

---

## مرحله بعدی

برای یادگیری بیشتر، بخش‌های زیر را مطالعه کنید:

- [مرجع API](../api-reference.md): مستندات کامل API
- [سوالات متداول](../faq.md): پاسخ به سوالات رایج
