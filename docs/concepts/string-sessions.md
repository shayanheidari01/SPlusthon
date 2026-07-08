---
hide:
  - navigation
---

# String Sessions

String Sessions راهی راحت برای تعبیه credentialهای ورود مستقیماً در کد شما هستند. این روش به شما امکان می‌دهد بدون نیاز به ذخیره فایل session روی دیسک، از حساب خود استفاده کنید.

---

## مزایای String Sessions

- **قابلیت حمل بالا**: فقط یک رشته متنی است که می‌توانید آن را در هر جایی ذخیره کنید
- **مناسب برای محیط‌های ابری**: مانند Heroku که فایل‌سیستم موقت دارد
- **امنیت بیشتر**: نیازی به ذخیره فایل حساس روی دیسک نیست
- **سادگی استفاده**: فقط کافی است رشته را در کد خود قرار دهید

---

## تولید String Session

### روش ساده

```python
from splusthon.sync import SoroushClient
from splusthon.sessions import StringSession

with SoroushClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
```

این کد یک String Session جدید تولید و چاپ می‌کند.

### روش با استفاده از SQLite Session

```python
from splusthon.sync import SoroushClient
from splusthon.sessions import StringSession

# ابتدا با SQLite Session وارد شوید
client = SoroushClient('sqlite-session', api_id, api_hash)

# سپس آن را به String Session تبدیل کنید
string = StringSession.save(client.session)
print(string)
```

### روش با SoroushClient معمولی

```python
from splusthon import SoroushClient
from splusthon.sessions import StringSession

client = SoroushClient(StringSession())
await client.start()

# دریافت String Session
string_session = client.session.save()
print(string_session)
```

---

## استفاده از String Session

### بارگذاری و استفاده

```python
string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi_Q25UOCzOAqzc...'

with SoroushClient(StringSession(string), api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'سلام'))
```

### بارگذاری از فایل متنی

```python
# ذخیره String Session در فایل متنی
with open('session.txt', 'w') as f:
    f.write(string_session)

# بارگذاری از فایل متنی
with open('session.txt', 'r') as f:
    string = f.read()

with SoroushClient(StringSession(string), api_id, api_hash) as client:
    # استفاده از کلاینت
    pass
```

### بارگذاری از متغیر محیطی

```python
import os
from splusthon import SoroushClient
from splusthon.sessions import StringSession

string = os.environ.get('SESSION_STRING')
with SoroushClient(StringSession(string), api_id, api_hash) as client:
    # استفاده از کلاینت
    pass
```

---

## مثال کامل

### ایجاد و ذخیره String Session

```python
from splusthon import SoroushClient
from splusthon.sessions import StringSession

async def create_session():
    client = SoroushClient(StringSession())
    await client.start()
    
    # ذخیره String Session
    string = client.session.save()
    
    # ذخیره در فایل
    with open('my_session.txt', 'w') as f:
        f.write(string)
    
    print('String Session ذخیره شد:')
    print(string)
    
    await client.disconnect()

import asyncio
asyncio.run(create_session())
```

### استفاده از String Session ذخیره شده

```python
from splusthon import SoroushClient
from splusthon.sessions import StringSession

async def use_session():
    # بارگذاری String Session از فایل
    with open('my_session.txt', 'r') as f:
        string = f.read()
    
    # ایجاد کلاینت
    with SoroushClient(StringSession(string), api_id, api_hash) as client:
        # دریافت اطلاعات کاربر
        me = await client.get_me()
        print(f'وارد شدید به عنوان: {me.first_name}')
        
        # ارسال پیام
        await client.send_message('me', 'سلام از String Session!')

import asyncio
asyncio.run(use_session())
```

---

## نکات امنیتی

!!! warning "هشدار"
    **String Session را ایمن نگه دارید!** هر کسی با این رشته می‌تواند از آن برای ورود به حساب شما و هر کاری که می‌خواهد استفاده کند.
>
> این مشابه نشت فایل‌های `*.session` آنلاین است، اما نشت یک رشته آسان‌تر از نشت یک فایل است.

### نکات امنیتی مهم

1. **هرگز String Session را در کد منبع آنلاین قرار ندهید**
2. **از متغیرهای محیطی برای ذخیره String Session استفاده کنید**
3. **فایل‌های متنی حاوی String Session را git ignore کنید**
4. **از رمزگذاری برای ذخیره String Session استفاده کنید**
5. **دسترسی به فایل‌های حاوی String Session را محدود کنید**

---

## مقایسه با روش‌های دیگر

| روش | مزایا | معایب |
|------|--------|--------|
| **SQLite Session** | پیش‌فرض، پایدار | نیاز به فایل روی دیسک |
| **String Session** | قابلیت حمل بالا | نیاز به مدیریت رشته |
| **Memory Session** | سریع | اطلاعات در حافظه (موقت) |

---

## عیب‌یابی

### خطای String Session نامعتبر

اگر خطایی مانند "Invalid session" دریافت کردید:

1. مطمئن شوید String Session را به درستی کپی کرده‌اید
2. مطمئن شوید از همان API ID و Hash اصلی استفاده می‌کنید
3. String Session را دوباره تولید کنید

### String Session کار نمی‌کند

اگر String Session کار نمی‌کند:

1. مطمئن شوید String Session منقضی نشده است
2. مطمئن شوید حساب شما مسدود نشده است
3. با استفاده از String Session جدید دوباره امتحان کنید

---

## مرحله بعدی

برای یادگیری بیشتر درباره مدیریت خطاها، بخش [مدیریت خطاها](errors.md) را مطالعه کنید.
