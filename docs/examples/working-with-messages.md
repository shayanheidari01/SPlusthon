---
layout: default
title: کار با پیام‌ها
nav_order: 3
parent: مثال‌ها
---

# کار با پیام‌ها

در این بخش مثال‌هایی برای کار با پیام‌ها در SPlusthon آورده شده است.

---

## ارسال پیام متنی

### ارسال به خودتان

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال به خودتان
        await client.send_message('me', 'سلام، خودم!')
        
        # ارسال با قالب‌بندی
        await client.send_message('me', 'این پیام **بولد**، `کد` و __ایتالیک__ است.')

import asyncio
asyncio.run(main())
```

### ارسال به یوزرنیم

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال به یوزرنیم
        await client.send_message('username', 'سلام از SPlusthon!')

import asyncio
asyncio.run(main())
```

### ارسال به شماره تلفن

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال به شماره تلفن (باید در لیست مخاطبین باشد)
        await client.send_message('+989123456789', 'سلام دوست من!')

import asyncio
asyncio.run(main())
```

### ارسال به شناسه چت

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال به شناسه چت
        await client.send_message(-100123456, 'سلام گروه!')

import asyncio
asyncio.run(main())
```

---

## ارسال فایل

### ارسال عکس

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال عکس
        await client.send_file('me', '/path/to/photo.jpg')
        
        # ارسال عکس با توضیحات
        await client.send_file('me', '/path/to/photo.jpg', caption='این یک عکس است.')

import asyncio
asyncio.run(main())
```

### ارسال فایل

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال فایل
        await client.send_file('me', '/path/to/file.pdf')
        
        # ارسال فایل با عنوان
        await client.send_file('me', '/path/to/file.pdf', caption='فایل مهم')

import asyncio
asyncio.run(main())
```

### ارسال ویدیو

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال ویدیو
        await client.send_file('me', '/path/to/video.mp4')
        
        # ارسال ویدیو با توضیحات
        await client.send_file('me', '/path/to/video.mp4', caption='ویدیوی آموزشی')

import asyncio
asyncio.run(main())
```

---

## دریافت پیام‌ها

### دریافت آخرین پیام‌ها

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت آخرین ۱۰ پیام
        messages = await client.get_messages('me', limit=10)
        
        for message in messages:
            print(f'{message.id}: {message.text}')

import asyncio
asyncio.run(main())
```

### دریافت پیام‌های خاص

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت پیام با شناسه
        message = await client.get_messages('me', ids=123)
        print(f'پیام: {message.text}')
        
        # دریافت چند پیام با شناسه‌ها
        messages = await client.get_messages('me', ids=[123, 456, 789])
        for message in messages:
            print(f'{message.id}: {message.text}')

import asyncio
asyncio.run(main())
```

### جستجوی پیام‌ها

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # جستجوی پیام‌ها
        messages = await client.get_messages('me', search='کلمه جستجو')
        
        for message in messages:
            print(f'{message.id}: {message.text}')

import asyncio
asyncio.run(main())
```

---

## ویرایش و حذف پیام‌ها

### ویرایش پیام

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال پیام
        message = await client.send_message('me', 'پیام اصلی')
        
        # ویرایش پیام
        await client.edit_message(message, 'پیام ویرایش شده')

import asyncio
asyncio.run(main())
```

### حذف پیام

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال پیام
        message = await client.send_message('me', 'پیام برای حذف')
        
        # حذف پیام
        await client.delete_messages([message.id])
        
        # حذف پیام با شناسه
        await client.delete_messages([123, 456])

import asyncio
asyncio.run(main())
```

---

## پاسخ به پیام‌ها

### پاسخ مستقیم

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت پیام
        message = await client.get_messages('me', ids=123)
        
        # پاسخ به پیام
        await message.reply('این یک پاسخ است!')

import asyncio
asyncio.run(main())
```

### پاسخ با استفاده از event

```python
from splusthon import SoroushClient, events

client = SoroushClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    # پاسخ به پیام
    await event.reply('پاسخ خودکار!')
    
    # ارسال پیام بدون reply
    await event.respond('این یک پیام جداگانه است.')

client.start()
client.run_until_disconnected()
```

---

## دانلود رسانه‌ها

### دانلود عکس

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت پیام‌ها
        messages = await client.get_messages('me', limit=10)
        
        for message in messages:
            if message.photo:
                # دانلود عکس
                path = await message.download_media()
                print(f'عکس ذخیره شد: {path}')

import asyncio
asyncio.run(main())
```

### دانلود فایل

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت پیام‌ها
        messages = await client.get_messages('me', limit=10)
        
        for message in messages:
            if message.document:
                # دانلود فایل
                path = await message.download_media()
                print(f'فایل ذخیره شد: {path}')

import asyncio
asyncio.run(main())
```

---

## نکات مهم

{: .note }
> - برای ارسال فایل از `send_file` استفاده کنید
> - برای دانلود رسانه‌ها از `download_media` استفاده کنید
> - برای ویرایش پیام از `edit_message` استفاده کنید
> - برای حذف پیام از `delete_messages` استفاده کنید

---

## مرحله بعدی

برای یادگیری بیشتر، بخش [هشدار مهم]({% link examples/word-of-warning.md %}) را مطالعه کنید.
