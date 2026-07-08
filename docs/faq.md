---
hide:
  - navigation
---

# سوالات متداول

پاسخ به سوالات رایج کاربران SPlusthon.

---

## سوالات نصب و راه‌اندازی

### چگونه SPlusthon را نصب کنم؟

```bash
pip install splusthon
```

### چگونه نسخه توسعه‌دهنده را نصب کنم؟

```bash
pip install --upgrade https://github.com/shayanheidari01/SPlusthon/archive/v1.zip
```

### چگونه نصب را تأیید کنم؟

```bash
python3 -c "import splusthon; print(splusthon.__version__)"
```

### وابستگی‌های اختیاری چیست؟

- **cryptg**: افزایش سرعت رمزگذاری
- **Pillow**: تغییر اندازه خودکار تصاویر
- **aiohttp**: دانلود فایل‌های WebDocument
- **hachoir**: استخراج متادیتا از فایل‌ها

---

## سوالات احراز هویت

### چگونه API ID و Hash دریافت کنم؟

1. به [my.telegram.org](https://my.telegram.org/) بروید
2. با شماره تلفن حساب خود وارد شوید
3. روی "API Development tools" کلیک کنید
4. اطلاعات برنامه خود را پر کنید
5. روی "Create application" کلیک کنید

### آیا می‌توانم بدون API ID از SPlusthon استفاده کنم؟

بله، SPlusthon API credentials پیش‌فرض دارد:

```python
from splusthon import SoroushClient
from splusthon.sessions import StringSession

client = SoroushClient(StringSession())
client.start()
```

### چگونه با ربات وارد شوم؟

```python
from splusthon.sync import SoroushClient

api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'
bot_token = '12345:0123456789abcdef0123456789abcdef'

bot = SoroushClient('bot', api_id, api_hash).start(bot_token=bot_token)
```

---

## سوالات پیام‌رسانی

### چگونه پیام ارسال کنم？

```python
await client.send_message('username', 'سلام!')
await client.send_message('me', 'سلام، خودم!')
await client.send_message('+989123456789', 'سلام دوست من!')
```

### چگونه فایل ارسال کنم？

```python
await client.send_file('me', '/path/to/file.jpg')
await client.send_file('me', '/path/to/file.pdf', caption='توضیحات')
```

### چگونه پیام دریافت کنم？

```python
messages = await client.get_messages('me', limit=10)
for message in messages:
    print(message.text)
```

### چگونه به پیام پاسخ دهم？

```python
message = await client.get_messages('me', ids=123)
await message.reply('این یک پاسخ است!')
```

---

## سوالات رویدادها

### چگونه به پیام‌های جدید پاسخ دهم؟

```python
from splusthon import SoroushClient, events

client = SoroushClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if 'سلام' in event.raw_text:
        await event.reply('سلام! چطور می‌توانم کمک کنم؟')

client.start()
client.run_until_disconnected()
```

### چگونه فقط به پیام‌های خاصی پاسخ دهم؟

```python
@client.on(events.NewMessage(pattern=r'(?i)hi|hello'))
async def handler(event):
    await event.reply('سلام!')

@client.on(events.NewMessage(outgoing=True))
async def handler_outgoing(event):
    print('پیام خروجی:', event.raw_text)
```

---

## سوالات Session

### Session چیست؟

Session فایلی است که اطلاعات احراز هویت و کش entity را ذخیره می‌کند.

### StringSession چیست؟

StringSession نوعی Session است که اطلاعات را به صورت رشته ذخیره می‌کند:

```python
from splusthon.sessions import StringSession

session = StringSession()
string = session.save()
```

### چگونه Session را ذخیره کنم؟

```python
# ذخیره به صورت فایل
client = SoroushClient('session_name', api_id, api_hash)

# ذخیره به صورت رشته
string = client.session.save()
```

---

## سوالات خطایابی

### خطای FloodWaitError چیست؟

خطایی است که وقتی خیلی سریع درخواست ارسال می‌کنید رخ می‌دهد. باید صبر کنید:

```python
from splusthon.errors import FloodWaitError

try:
    await client.send_message('username', 'سلام!')
except FloodWaitError as e:
    print(f'صبر کنید {e.seconds} ثانیه')
```

### خطای PeerFloodError چیست؟

خطایی است که وقتی به محدودیت ارسال پیام رسیدید رخ می‌دهد:

```python
from splusthon.errors import PeerFloodError

try:
    await client.send_message('username', 'سلام!')
except PeerFloodError:
    print('محدودیت ارسال پیام. لطفاً صبر کنید.')
```

### چگونه خطاها را مدیریت کنم？

```python
from splusthon.errors import RPCError, FloodWaitError, PeerFloodError

async def safe_send(client, entity, message):
    try:
        await client.send_message(entity, message)
        return True
    except FloodWaitError as e:
        import asyncio
        await asyncio.sleep(e.seconds)
        return True
    except PeerFloodError:
        print('محدودیت ارسال پیام')
        return False
    except RPCError as e:
        print(f'خطا: {e}')
        return False
```

---

## سوالات پیشرفته

### چگونه از پروکسی استفاده کنم؟

```python
proxy = {
    'proxy_type': 'socks5',
    'addr': '1.1.1.1',
    'port': 5555,
    'username': 'foo',
    'password': 'bar',
    'rdns': True
}

client = SoroushClient('anon', api_id, api_hash, proxy=proxy)
```

### چگونه از MTProto Proxy استفاده کنم؟

```python
from splusthon import SoroushClient, connection

client = SoroushClient(
    'anon', api_id, api_hash,
    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    proxy=('mtproxy.example.com', 2002, 'secret')
)
```

### چگونه چندین کلاینت را همزمان اجرا کنم？

```python
import asyncio
from splusthon import SoroushClient

async def run_client(name, api_id, api_hash):
    client = SoroushClient(name, api_id, api_hash)
    await client.start()
    await client.run_until_disconnected()

async def main():
    await asyncio.gather(
        run_client('client1', api_id1, api_hash1),
        run_client('client2', api_id2, api_hash2)
    )

asyncio.run(main())
```

---

## سوالات امنیتی

### چگونه credentialهای خود را ایمن نگه دارم؟

1. از متغیرهای محیطی استفاده کنید
2. credentialها را در کد آشکار نکنید
3. فایل‌های session را آنلاین به اشتراک نگذارید
4. از رمزگذاری استفاده کنید

### آیا SPlusthon امن است؟

SPlusthon یک کتابخانه شخص ثالث است. مراقب باشید:

- از منابع معتبر دانلود کنید
- credentialهای خود را با کسی به اشتراک نگذارید
- قوانین سروش‌پلاس را رعایت کنید

---

## سوالات توسعه

### چگونه باگ گزارش کنم؟

به [GitHub Issues](https://github.com/shayanheidari01/SPlusthon/issues/) بروید و باگ جدید ایجاد کنید.

### چگونه مشارکت کنم؟

1. مخزن را fork کنید
2. تغییرات خود را ایجاد کنید
3. Pull Request ارسال کنید

### چگونه مستندات را مطالعه کنم؟

- [مرجع کامل API](https://tl.splusthon.dev/)
- [GitHub SPlusthon](https://github.com/shayanheidari01/SPlusthon)

---

## سوالات دیگر

### SPlusthon چیست؟

SPlusthon یک کتابخانه پایتون asyncio است که برای تعامل با API سروش‌پلاس طراحی شده است.

### SPlusthon از چه نسخه پایتونی پشتیبانی می‌کند؟

پایتون 3.7 یا بالاتر.

### آیا SPlusthon رایگان است؟

بله، SPlusthon کاملاً رایگان و متن‌باز است.

### چگونه از SPlusthon استفاده کنم؟

مستندات را مطالعه کنید و مثال‌ها را دنبال کنید.
