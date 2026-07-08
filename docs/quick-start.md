---
layout: default
title: شروع سریع
nav_order: 3
---

# شروع سریع

راهنمای سریع برای شروع کار با SPlusthon. در این بخش یاد می‌گیرید چگونه اولین کلاینت خود را ایجاد کرده و عملیات اساسی را انجام دهید.

---

## ایجاد کلاینت

### روش ساده (بدون API ID و Hash)

SPlusthon دارای API credentials پیش‌فرض برای سروش‌پلاس است، بنابراین می‌توانید بدون دریافت کلیدهای خود، کلاینت ایجاد کنید:

```python
from splusthon import SoroushClient, events, sync
from splusthon.sessions import StringSession

# بدون نیاز به api_id یا api_hash
client = SoroushClient(StringSession())
client.start()
```

### روش استاندارد (با API ID و Hash)

برای استفاده استاندارد، ابتدا باید API ID و Hash خود را از [my.telegram.org](https://my.telegram.org/) دریافت کنید:

```python
from splusthon import SoroushClient

api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'

# اولین پارامتر نام فایل session است
with SoroushClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'سلام، خودم!'))
```

{: .important }
> نکته: از نام‌گذاری فایل اسکریپت خود به نام `splusthon.py` خودداری کنید! پایتون سعی می‌کند کلاینت را از آن فایل import کند و با خطا مواجه می‌شود.

---

## ارسال پیام

### ارسال به خودتان
```python
await client.send_message('me', 'سلام، خودم!')
```

### ارسال به یک چت با شناسه
```python
await client.send_message(-100123456, 'سلام، گروه!')
```

### ارسال به مخاطبین
```python
await client.send_message('+989123456789', 'سلام، دوست من!')
```

### ارسال به یوزرنیم
```python
await client.send_message('username', 'تست SPlusthon!')
```

### ارسال با قالب‌بندی
```python
message = await client.send_message(
    'me',
    'این پیام دارای **بولد**، `کد`، __ایتالیک__ و '
    'یک [وبسایت زیبا](https://example.com) است!',
    link_preview=False
)

# چاپ متن خام پیام
print(message.raw_text)
```

---

## دریافت اطلاعات کاربر

```python
# دریافت اطلاعات خودتان
me = await client.get_me()

# نمایش اطلاعات به صورت رشته
print(me.stringify())

# دسترسی به ویژگی‌ها
username = me.username
print(username)
print(me.phone)
```

---

## چاپ مکالمات

```python
async for dialog in client.iter_dialogs():
    print(dialog.name, 'دارای شناسه', dialog.id)
```

---

## پاسخ به پیام‌ها

```python
# اگر یک شیء پیام دارید، می‌توانید مستقیماً پاسخ دهید
await message.reply('عالی!')
```

---

## ارسال فایل

```python
await client.send_file('me', '/home/me/Pictures/holidays.jpg')
```

---

## چاپ تاریخچه پیام‌ها

```python
async for message in client.iter_messages('me'):
    print(message.id, message.text)
    
    # دانلود رسانه از پیام‌ها
    if message.photo:
        path = await message.download_media()
        print('فایل در مسیر ذخیره شد', path)
```

---

## مثال کامل

در اینجا یک مثال کامل برای شروع سریع آورده شده است:

```python
from splusthon import SoroushClient

api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'
client = SoroushClient('anon', api_id, api_hash)

async def main():
    # دریافت اطلاعات خودتان
    me = await client.get_me()
    print(me.stringify())
    
    # نام کاربری
    username = me.username
    print(username)
    print(me.phone)
    
    # چاپ تمام مکالمات
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'دارای شناسه', dialog.id)
    
    # ارسال پیام به خودتان
    await client.send_message('me', 'سلام، خودم!')
    
    # ارسال پیام به یک چت
    await client.send_message(-100123456, 'سلام، گروه!')
    
    # ارسال پیام به مخاطب
    await client.send_message('+989123456789', 'سلام، دوست من!')
    
    # ارسال پیام به یوزرنیم
    await client.send_message('username', 'تست SPlusthon!')
    
    # ارسال با قالب‌بندی
    message = await client.send_message(
        'me',
        'این پیام دارای **بولد**، `کد`، __ایتالیک__ و '
        'یک [وبسایت زیبا](https://example.com) است!',
        link_preview=False
    )
    
    print(message.raw_text)
    await message.reply('عالی!')
    
    # ارسال فایل
    await client.send_file('me', '/home/me/Pictures/holidays.jpg')
    
    # چاپ تاریخچه پیام‌ها
    async for message in client.iter_messages('me'):
        print(message.id, message.text)
        
        if message.photo:
            path = await message.download_media()
            print('فایل در مسیر ذخیره شد', path)

with client:
    client.loop.run_until_complete(main())
```

---

## نکات مهم

{: .important }
> SPlusthon یک کتابخانه ناهمگام (async) است و باید با asyncio کار کنید. به طور کلی، تمام کد خود را در داخل یک تابع `async def` بنویسید:

```python
client = ...

async def do_something(me):
    ...

async def main():
    # بیشتر کد شما باید اینجا باشد
    me = await client.get_me()
    await do_something(me)

with client:
    client.loop.run_until_complete(main())
```

---

## مرحله بعدی

پس از آشنایی با مبانی، به بخش [مفاهیم پایه]({% link concepts/index.md %}) بروید تا مفاهیم مهم مانند Entity، Session و رویدادها را بهتر درک کنید.
