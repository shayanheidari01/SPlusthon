---
hide:
  - navigation
---

# مرجع API

در این بخش مستندات کامل API کتابخانه SPlusthon آورده شده است.

---

## کلاس SoroushClient

کلاس اصلی کتابخانه برای تعامل با سروش‌پلاس.

### سازنده

```python
SoroushClient(session=None, api_id=None, api_hash=None, 
              connection_retries=None, timeout=timedelta(seconds=60), 
              request_retries=None, connection=None, 
              proxy=None, local_addr=None)
```

### پارامترها

| پارامتر | نوع | پیش‌فرض | توضیحات |
|---------|-----|---------|---------|
| session | str/Session | None | نام session یا شیء Session |
| api_id | int | None | شناسه API از my.telegram.org |
| api_hash | str | None | هش API از my.telegram.org |
| connection_retries | int | None | تعداد تلاش‌های اتصال مجدد |
| timeout | timedelta | 60 ثانیه | زمان انتظار برای درخواست‌ها |
| request_retries | int | None | تعداد تلاش‌های درخواست مجدد |
| connection | class | None | نوع اتصال |
| proxy | dict | None | تنظیمات پروکسی |
| local_addr | tuple | None | آدرس محلی |

---

## متدهای ارسال پیام

### send_message

```python
async def send_message(entity, message=None, *, parse_mode=None, 
                       link_preview=None, file=None, force_document=None, 
                       clear_draft=None, background=None, 
                       supports_streaming=None, schedule=None, 
                       noforwards=None, comment_to=None, 
                       reply_to=None, top_msg_id=None)
```

**پارامترها:**

- `entity`: مقصد پیام (یوزرنیم، شماره تلفن، شناسه چت)
- `message`: متن پیام
- `parse_mode`: حالت تجزیه (markdown/html)
- `link_preview`: نمایش پیش‌نمایش لینک
- `file`: فایل برای ارسال
- `reply_to`: پاسخ به پیام خاص

**مثال:**

```python
await client.send_message('username', 'سلام!')
await client.send_message('me', 'پیام با **بولد**')
await client.send_message('me', 'https://example.com', link_preview=False)
```

---

### send_file

```python
async def send_file(entity, file, *, caption=None, 
                    force_document=None, thumb=None, 
                    voice_note=None, video_note=None, 
                    attributes=None, supports_streaming=None, 
                    schedule=None, noforwards=None, 
                    reply_to=None, top_msg_id=None, 
                    comment_to=None, parse_mode=(), 
                    buttons=None, silent=None, 
                    background=None, clear_draft=None, 
                    video_start_ts=None, duration=None, 
                    title=None, performer=None, 
                    force_file=None, file_size=None, 
                    chunk_size=None, file_names=None, 
                    workers=1, api_hash=None)
```

**پارامترها:**

- `entity`: مقصد فایل
- `file`: مسیر فایل یا آبجکت file
- `caption`: توضیحات فایل

**مثال:**

```python
await client.send_file('me', '/path/to/photo.jpg')
await client.send_file('me', '/path/to/file.pdf', caption='فایل مهم')
```

---

## متدهای دریافت پیام

### get_messages

```python
async def get_messages(entity, limit=None, *, offset_date=None, 
                       offset_id=None, add_offset=None, 
                       search=None, from_user=None, 
                       ids=None, reverse=None, 
                       wait_time=None)
```

**پارامترها:**

- `entity`: منبع پیام‌ها
- `limit`: تعداد پیام‌ها
- `search`: عبارت جستجو
- `ids`: شناسه‌های پیام‌ها

**مثال:**

```python
messages = await client.get_messages('me', limit=10)
messages = await client.get_messages('me', search='کلمه جستجو')
message = await client.get_messages('me', ids=123)
```

---

### iter_messages

```python
def iter_messages(entity, limit=None, *, offset_date=None, 
                  offset_id=None, add_offset=None, 
                  search=None, from_user=None, 
                  ids=None, reverse=None, 
                  wait_time=None)
```

**مثال:**

```python
async for message in client.iter_messages('me', limit=10):
    print(f'{message.id}: {message.text}')
```

---

## متدهای ویرایش پیام

### edit_message

```python
async def edit_message(entity=None, message=None, *, 
                       text=None, parse_mode=None, 
                       link_preview=None, file=None, 
                       video_start_ts=None, 
                       force_document=None, 
                       schedule=None, noforwards=None)
```

**مثال:**

```python
await client.edit_message('username', message_id, 'متن جدید')
```

---

### delete_messages

```python
async def delete_messages(entity, messages, *, revoke=None)
```

**مثال:**

```python
await client.delete_messages('username', [123, 456])
```

---

## متدهای کار با Entity

### get_entity

```python
async def get_entity(entity)
```

**مثال:**

```python
user = await client.get_entity('username')
user = await client.get_entity('+989123456789')
user = await client.get_entity(123456)
```

---

### get_input_entity

```python
async def get_input_entity(entity)
```

**مثال:**

```python
input_user = await client.get_input_entity('username')
```

---

## متدهای رسانه

### download_profile_photo

```python
async def download_profile_photo(entity, file=None, *, 
                                  big=None, download_big=None)
```

**مثال:**

```python
await client.download_profile_photo('me')
await client.download_profile_photo('username')
```

---

### upload_file

```python
async def upload_file(file, *, file_size=None, 
                      part_size_kb=None, 
                      file_name=None, 
                      use_cache=None)
```

**مثال:**

```python
file = await client.upload_file('/path/to/file.jpg')
```

---

## رویدادها (Events)

### NewMessage

```python
@client.on(events.NewMessage)
async def handler(event):
    print(event.raw_text)
```

### پارامترهای NewMessage

| پارامتر | نوع | توضیحات |
|---------|-----|---------|
| incoming | bool | پیام‌های ورودی |
| outgoing | bool | پیام‌های خروجی |
| pattern | str | regex برای فیلتر |
| chats | list | چت‌های خاص |
| blacklist_chats | bool | لیست سیاه چت‌ها |

---

### MessageEdited

```python
@client.on(events.MessageEdited)
async def handler(event):
    print('پیام ویرایش شد:', event.raw_text)
```

---

### MessageDeleted

```python
@client.on(events.MessageDeleted)
async def handler(event):
    print('پیام حذف شد:', event.message_id)
```

---

### CallbackQuery

```python
@client.on(events.CallbackQuery)
async def handler(event):
    print('کلیک روی دکمه:', event.data)
    await event.answer('پاسخ')
```

---

### ChatAction

```python
@client.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
        print('عضو جدید وارد شد')
    if event.user_left:
        print('عضو خارج شد')
```

---

## خطاها

### RPCError

خطای اصلی API سروش‌پلاس.

### FloodWaitError

خطای انتظار اجباری.

```python
from splusthon.errors import FloodWaitError

try:
    await client.send_message('username', 'سلام!')
except FloodWaitError as e:
    print(f'صبر کنید {e.seconds} ثانیه')
```

---

### PeerFloodError

خطای محدودیت ارسال پیام.

```python
from splusthon.errors import PeerFloodError

try:
    await client.send_message('username', 'سلام!')
except PeerFloodError:
    print('محدودیت ارسال پیام')
```

---

## Session

### StringSession

```python
from splusthon.sessions import StringSession

# ایجاد StringSession
session = StringSession()

# استفاده از StringSession
client = SoroushClient(StringSession(string), api_id, api_hash)

# ذخیره StringSession
string = client.session.save()
```

---

## منابع

- [مرجع کامل API](https://tl.splusthon.dev/)
- [GitHub SPlusthon](https://github.com/shayanheidari01/SPlusthon)
