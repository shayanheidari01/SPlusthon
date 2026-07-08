---
hide:
  - navigation
---

# مدیریت خطاها

SPlusthon دارای سیستم مدیریت خطای قدرتمندی است که به شما امکان می‌دهد خطاهای مختلف API سروش‌پلاس را مدیریت کنید.

---

## خطاهای اصلی

### RPCError

خطاهای اصلی API سروش‌پلاس هستند. این خطاها زمانی رخ می‌دهند که درخواست شما با مشکلی مواجه شود.

```python
from splusthon.errors import RPCError, FloodWaitError, PeerFloodError

try:
    await client.send_message('username', 'سلام!')
except FloodWaitError as e:
    # صبر کنید تا زمان انتظار تمام شود
    print(f'صبر کنید {e.seconds} ثانیه')
except PeerFloodError:
    # محدودیت تعداد پیام
    print('شما به محدودیت ارسال پیام رسیده‌اید')
except RPCError as e:
    # سایر خطاهای API
    print(f'خطای API: {e}')
```

---

## انواع خطاهای رایج

### FloodWaitError

وقتی خیلی سریع درخواست ارسال می‌کنید و باید صبر کنید:

```python
from splusthon.errors import FloodWaitError

try:
    await client.send_message('username', 'سلام!')
except FloodWaitError as e:
    print(f'صبر کنید {e.seconds} ثانیه')
    # کتابخانه به طور خودکار صبر می‌کند
    # یا می‌توانید دستی صبر کنید
    import asyncio
    await asyncio.sleep(e.seconds)
```

### PeerFloodError

وقتی به محدودیت ارسال پیام رسیده‌اید:

```python
from splusthon.errors import PeerFloodError

try:
    await client.send_message('username', 'سلام!')
except PeerFloodError:
    print('شما به محدودیت ارسال پیام رسیده‌اید. لطفاً صبر کنید.')
```

### UserBannedInChannelError

وقتی حساب شما در کانالی مسدود شده است:

```python
from splusthon.errors import UserBannedInChannelError

try:
    await client.send_message('channel', 'سلام!')
except UserBannedInChannelError:
    print('حساب شما در این کانال مسدود شده است.')
```

### ChatWriteForbiddenError

وقتی اجازه نوشتن در چت را ندارید:

```python
from splusthon.errors import ChatWriteForbiddenError

try:
    await client.send_message('chat', 'سلام!')
except ChatWriteForbiddenError:
    print('شما اجازه نوشتن در این چت را ندارید.')
```

### UsernameNotOccupiedError

وقتی یوزرنیم وجود ندارد:

```python
from splusthon.errors import UsernameNotOccupiedError

try:
    await client.send_message('nonexistent_username', 'سلام!')
except UsernameNotOccupiedError:
    print('یوزرنیم وجود ندارد.')
```

### UsernameInvalidError

وقتی یوزرنیم نامعتبر است:

```python
from splusthon.errors import UsernameInvalidError

try:
    await client.send_message('invalid username!', 'سلام!')
except UsernameInvalidError:
    print('یوزرنیم نامعتبر است.')
```

---

## مدیریت خطاهای عمومی

### استفاده از try/except عمومی

```python
from splusthon.errors import RPCError

async def safe_send_message(client, entity, message):
    try:
        await client.send_message(entity, message)
        return True
    except RPCError as e:
        print(f'خطا در ارسال پیام: {e}')
        return False
    except Exception as e:
        print(f'خطای غیرمنتظره: {e}')
        return False
```

### ایجاد decorator برای مدیریت خطا

```python
from functools import wraps
from splusthon.errors import RPCError

def handle_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RPCError as e:
            print(f'خطای RPC: {e}')
            return None
        except Exception as e:
            print(f'خطای غیرمنتظره: {e}')
            return None
    return wrapper

@handle_errors
async def send_message(client, entity, message):
    await client.send_message(entity, message)
```

---

## ثبت handler برای خطاها

### استفاده از on_error

```python
from splusthon import SoroushClient, events

client = SoroushClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    await event.reply('پاسخ خودکار')

# مدیریت خطاها در handler‌ها
@client.on(events.NewMessage)
async def error_handler(event):
    try:
        # عملیات خطرناک
        await event.reply('پاسخ')
    except Exception as e:
        print(f'خطا در handler: {e}')
```

---

## لاگ کردن خطاها

### استفاده از logging

```python
import logging
from splusthon import SoroushClient, events

# تنظیم logging
logging.basicConfig(
    format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

client = SoroushClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    try:
        await event.reply('پاسخ')
    except Exception as e:
        logging.error(f'خطا در handler: {e}')
        raise  # خطا را دوباره raise کنید تا لاگ شود
```

---

## مثال‌های کاربردی

### ارسال پیام با مدیریت خطا

```python
from splusthon import SoroushClient, events
from splusthon.errors import FloodWaitError, PeerFloodError, RPCError

client = SoroushClient('anon', api_id, api_hash)

async def send_with_retry(client, entity, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            await client.send_message(entity, message)
            return True
        except FloodWaitError as e:
            import asyncio
            await asyncio.sleep(e.seconds)
        except PeerFloodError:
            print('محدودیت ارسال پیام. لطفاً صبر کنید.')
            return False
        except RPCError as e:
            print(f'خطا در تلاش {attempt + 1}: {e}')
            if attempt == max_retries - 1:
                return False
    return False
```

### handler با مدیریت خطا

```python
@client.on(events.NewMessage(pattern=r'(?i)help'))
async def help_handler(event):
    try:
        await event.respond('راهنمایی: این یک پیام کمکی است.')
    except Exception as e:
        # اگر پاسخ دادن موفق نبود، سکوت کنید
        pass
```

---

## نکات مهم

1. **همیشه خطاها را مدیریت کنید**: به خصوص `FloodWaitError` و `PeerFloodError`
2. **از logging استفاده کنید**: برای عیب‌یابی بهتر
3. **تعداد تلاش‌ها را محدود کنید**: برای جلوگیری از حلقه‌های بی‌نهایت
4. **از decorator برای مدیریت خطا استفاده کنید**: برای کد تمیزتر
5. **خطا را دوباره raise نکنید**: مگر اینکه بخواهید در سطح بالاتر مدیریت شود

---

## مرحله بعدی

برای یادگیری بیشتر درباره API کامل، بخش [API کامل](full-api.md) را مطالعه کنید.
