---
hide:
  - navigation
---

# Mastering asyncio

SPlusthon بر پایه asyncio ساخته شده است. برای استفاده مؤثر از کتابخانه، باید مفاهیم پایه asyncio را درک کنید.

---

## asyncio چیست؟

asyncio یک ماژول استاندارد پایتون است که امکان نوشتن کد ناهمگام (asynchronous) را فراهم می‌کند. این به شما امکان می‌دهد عملیاتی که زمان‌بر هستند (مانند درخواست‌های شبکه) را بدون مسدود کردن اجرای اصلی برنامه انجام دهید.

---

## مفاهیم پایه

### coroutine

یک تابع `async def` یک coroutine است:

```python
async def my_function():
    print('شروع')
    await some_async_operation()
    print('پایان')
```

### await

واژه کلیدی `await` منتظر اتمام یک عملیات ناهمگام می‌شود:

```python
async def main():
    result = await client.get_me()
    print(result.stringify())
```

### event loop

حلقه رویداد (event loop) مسئول اجرای coroutineها است:

```python
import asyncio

async def main():
    # کد شما اینجا اجرا می‌شود
    pass

# اجرای حلقه رویداد
asyncio.run(main())
```

---

## استفاده از asyncio در SPlusthon

### ساختار پایه

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

### استفاده از with block

```python
import asyncio
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        me = await client.get_me()
        print(me.stringify())
        
        await client.run_until_disconnected()

asyncio.run(main())
```

### استفاده از client.loop

```python
from splusthon import SoroushClient

client = SoroushClient('anon', api_id, api_hash)

async def main():
    me = await client.get_me()
    print(me.stringify())
    
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
```

---

## مثال‌های کاربردی

### ارسال پیام‌های متعدد

```python
import asyncio
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # ارسال چند پیام
        for i in range(5):
            await client.send_message('me', f'پیام {i+1}')
            await asyncio.sleep(1)  # تاخیر ۱ ثانیه‌ای

asyncio.run(main())
```

### دریافت و پردازش پیام‌ها

```python
import asyncio
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        async for message in client.iter_messages('me'):
            print(f'پیام {message.id}: {message.text}')
            
            # پردازش همزمان پیام‌ها
            await asyncio.sleep(0.1)

asyncio.run(main())
```

### handler‌های رویداد همزمان

```python
import asyncio
from splusthon import SoroushClient, events

client = SoroushClient('anon', api_id, api_hash)

@client.on(events.NewMessage(pattern=r'(?i)hi|hello'))
async def handler1(event):
    await event.reply('سلام! (از handler 1)')

@client.on(events.NewMessage(pattern=r'(?i)help'))
async def handler2(event):
    await event.reply('کمک! (از handler 2)')

async def main():
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())
```

---

## نکات مهم

### ۱. از await استفاده کنید

تمام متدهایی که با شبکه کار می‌کنند باید با `await` فراخوانی شوند:

```python
# درست
me = await client.get_me()
await client.send_message('me', 'سلام')

# اشتباه
me = client.get_me()  # خطا!
client.send_message('me', 'سلام')  # خطا!
```

### ۲. handler‌ها باید async باشند

handler‌های رویداد باید `async def` باشند:

```python
# درست
@client.on(events.NewMessage)
async def handler(event):
    await event.reply('پاسخ')

# اشتباه
@client.on(events.NewMessage)
def handler(event):
    event.reply('پاسخ')  # خطا!
```

### ۳. از asyncio.sleep استفاده کنید

برای تاخیر در کد ناهمگام از `asyncio.sleep` استفاده کنید:

```python
import asyncio

# درست
await asyncio.sleep(1)

# اشتباه
import time
time.sleep(1)  # حلقه رویداد را مسدود می‌کند!
```

### ۴. از gather برای عملیات همزمان استفاده کنید

```python
import asyncio

async def main():
    # اجرای همزمان چندین coroutine
    await asyncio.gather(
        client.send_message('user1', 'سلام ۱'),
        client.send_message('user2', 'سلام ۲'),
        client.send_message('user3', 'سلام ۳')
    )
```

---

## عیب‌یابی مشکلات asyncio

### خطای "This event loop is already running"

```python
# اشتباه
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# درست
asyncio.run(main())
```

### خطای "Cannot run the event loop while another loop is running"

```python
# اشتباه
async def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(some_coroutine())

# درست
async def main():
    await some_coroutine()
```

### مسدود شدن حلقه رویداد

```python
# اشتباه
import time
async def main():
    time.sleep(1)  # حلقه رویداد را مسدود می‌کند!

# درست
import asyncio
async def main():
    await asyncio.sleep(1)  # حلقه رویداد را مسدود نمی‌کند
```

---

## منابع آموزشی

- [مستندات رسمی asyncio](https://docs.python.org/3/library/asyncio.html)
- [آموزش asyncio در پایتون](https://realpython.com/async-io-python/)
- [مثال‌های asyncio](https://docs.python.org/3/library/asyncio-task.html)

---

## نتیجه‌گیری

asyncio یک ابزار قدرتمند برای نوشتن کد ناهمگام در پایتون است. با درک مفاهیم پایه مانند coroutine، await و event loop، می‌توانید به طور مؤثر از SPlusthon استفاده کنید.

---

## مرحله بعدی

برای یادگیری بیشتر، بخش [مثال‌ها](../examples/index.md) را مطالعه کنید.
