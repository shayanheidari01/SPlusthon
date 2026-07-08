---
hide:
  - navigation
---

# هشدار مهم

هنگام استفاده از SPlusthon، مهم است که از قوانین و محدودیت‌های سروش‌پلاس آگاه باشید تا حساب شما مسدود نشود.

---

## قوانین مهم سروش‌پلاس

### ۱. عدم ارسال اسپم

- **هرگز** پیام‌های تبلیغاتی یا اسپم ارسال نکنید
- **هرگز** به صورت انبوه پیام ارسال نکنید
- **هرگز** بدون اجازه کاربران به آنها پیام ندهید

### ۲. رعایت حریم خصوصی

- **هرگز** اطلاعات شخصی کاربران را بدون اجازه جمع‌آوری نکنید
- **هرگز** اطلاعات خصوصی را به اشتراک نگذارید
- **هرگز** بدون اجازه وارد چت‌های خصوصی نشوید

### ۳. عدم نقض قوانین

- **هرگز** از SPlusthon برای اهداف غیرقانونی استفاده نکنید
- **هرگز** قوانین سروش‌پلاس را نقض نکنید
- **هرگز** حساب‌های دیگران را هک نکنید

---

## محدودیت‌های فنی

### محدودیت ارسال پیام

- **FloodWaitError**: اگر خیلی سریع پیام ارسال کنید، باید صبر کنید
- **PeerFloodError**: اگر به محدودیت ارسال پیام رسیدید، باید صبر کنید

### محدودیت درخواست‌ها

- **تعداد درخواست در ثانیه**: محدودیت در تعداد درخواست‌های API
- **تعداد درخواست در روز**: محدودیت در تعداد کل درخواست‌ها

### محدودیت حساب

- **مسدود شدن حساب**: اگر قوانین را رعایت نکنید، حساب شما ممکن است مسدود شود
- **محدود شدن حساب**: اگر محدودیت‌ها را رعایت نکنید، حساب شما ممکن است محدود شود

---

## نکات امنیتی

### ۱. حفاظت از credentialها

```python
# اشتباه - هرگز credentialها را در کد آشکار نکنید
api_id = 12345
api_hash = '0123456789abcdef'

# درست - از متغیرهای محیطی استفاده کنید
import os
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
```

### ۲. حفاظت از Session

```python
# اشتباه - هرگز Session را آنلاین به اشتراک نگذارید
session_string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi_Q25UOCzOAqzc...'

# درست - از رمزگذاری استفاده کنید
import os
session_string = os.environ.get('SESSION_STRING')
```

### ۳. محدود کردن دسترسی

```python
# اشتباه - هرگز دسترسی کامل ندهید
client = SoroushClient('session', api_id, api_hash)
await client.start()

# درست - فقط دسترسی‌های لازم را بدهید
# (این مثال فقط یک مفهوم است، SPlusthon به طور خودکار دسترسی‌ها را مدیریت می‌کند)
```

---

## بهترین شیوه‌ها

### ۱. استفاده از مدیریت خطا

```python
from splusthon.errors import FloodWaitError, PeerFloodError, RPCError

async def safe_send(client, entity, message):
    try:
        await client.send_message(entity, message)
        return True
    except FloodWaitError as e:
        import asyncio
        await asyncio.sleep(e.seconds)
        return True
    except PeerFloodError:
        print('محدودیت ارسال پیام. لطفاً صبر کنید.')
        return False
    except RPCError as e:
        print(f'خطا: {e}')
        return False
```

### ۲. استفاده از لاگینگ

```python
import logging
from splusthon import SoroushClient, events

logging.basicConfig(
    format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

client = SoroushClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    logging.info(f'پیام جدید: {event.raw_text}')
```

### ۳. محدود کردن تعداد درخواست‌ها

```python
import asyncio

async def rate_limited_send(client, entities, message, delay=1):
    for entity in entities:
        await client.send_message(entity, message)
        await asyncio.sleep(delay)  # تاخیر بین درخواست‌ها
```

### ۴. استفاده از String Session برای محیط‌های ابری

```python
from splusthon import SoroushClient
from splusthon.sessions import StringSession

# برای محیط‌های ابری مانند Heroku
import os
session_string = os.environ.get('SESSION_STRING')
client = SoroushClient(StringSession(session_string), api_id, api_hash)
```

---

## عیب‌یابی مشکلات رایج

### حساب مسدود شده

اگر حساب شما مسدود شده است:

1. با پشتیبانی سروش‌پلاس تماس بگیرید
2. دلیل مسدود شدن را بررسی کنید
3. از اشتباهات قبلی درس بگیرید

### FloodWaitError

اگر FloodWaitError دریافت کردید:

1. مدت زمان انتظار را رعایت کنید
2. سرعت ارسال پیام‌ها را کاهش دهید
3. از تاخیر بین درخواست‌ها استفاده کنید

### PeerFloodError

اگر PeerFloodError دریافت کردید:

1. مدت زمان انتظار را رعایت کنید
2. تعداد پیام‌های ارسالی را کاهش دهید
3. از ارسال انبوه پیام خودداری کنید

---

## منابع مفید

- [قوانین سروش‌پلاس](https://web.splus.ir/terms)
- [API مستندات سروش‌پلاس](https://core.splus.ir/)
- [GitHub SPlusthon](https://github.com/shayanheidari01/SPlusthon)

---

## نتیجه‌گیری

با رعایت قوانین و نکات امنیتی، می‌توانید از SPlusthon به طور ایمن و مؤثر استفاده کنید. همیشه از بهترین شیوه‌ها پیروی کنید و مراقب حساب خود باشید.
