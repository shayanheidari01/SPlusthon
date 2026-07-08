---
hide:
  - navigation
---

# API کامل

SPlusthon از API کامل سروش‌پلاس پشتیبانی می‌کند. می‌توانید از متدهای پیشرفته برای کنترل دقیق‌تر استفاده کنید.

---

## استفاده از API خام

### ارسال درخواست خام

```python
from splusthon.tl.functions.messages import SendMessageRequest

await client(SendMessageRequest(
    peer='username',
    message='سلام!',
    random_id=client._get_request_msg_id()
))
```

### دریافت اطلاعات کاربر

```python
from splusthon.tl.functions.users import GetUsersRequest

users = await client(GetUsersRequest(
    id=['username1', 'username2']
))
```

### دریافت اطلاعات کانال

```python
from splusthon.tl.functions.channels import GetFullChannelRequest

full_channel = await client(GetFullChannelRequest('channel_username'))
```

---

## متدهای پیشرفته

### ارسال فایل با کنترل کامل

```python
from splusthon.tl.functions.messages import SendMediaRequest
from splusthon.tl.types import InputMediaUploadedDocument

# آپلود فایل
file = await client.upload_file('/path/to/file.jpg')

# ارسال فایل
await client(SendMediaRequest(
    peer='username',
    media=InputMediaUploadedDocument(
        file=file,
        caption='توضیحات فایل'
    ),
    random_id=client._get_request_msg_id()
))
```

### ویرایش پیام

```python
from splusthon.tl.functions.messages import EditMessageRequest

await client(EditMessageRequest(
    peer='username',
    id=message_id,
    message='متن جدید'
))
```

### حذف پیام

```python
from splusthon.tl.functions.messages import DeleteMessagesRequest

await client(DeleteMessagesRequest(
    id=[message_id_1, message_id_2],
    revoke=True
))
```

---

## کار با چت‌ها و کانال‌ها

### عضویت در کانال

```python
from splusthon.tl.functions.channels import JoinChannelRequest

await client(JoinChannelRequest(channel))
```

### خروج از کانال

```python
from splusthon.tl.functions.channels import LeaveChannelRequest

await client(LeaveChannelRequest(input_channel))
```

### عضویت با لینک دعوت

```python
from splusthon.tl.functions.messages import ImportChatInviteRequest

updates = await client(ImportChatInviteRequest('AAAAAEHbEkejzxUjAUCfYg'))
```

### اضافه کردن کاربر به چت

```python
from splusthon.tl.functions.messages import AddChatUserRequest

await client(AddChatUserRequest(
    chat_id,
    user_to_add,
    fwd_limit=10  # اجازه دیدن ۱۰ پیام آخر
))
```

### اضافه کردن کاربر به کانال

```python
from splusthon.tl.functions.channels import InviteToChannelRequest

await client(InviteToChannelRequest(
    channel,
    [users_to_add]
))
```

---

## کار با پروفایل

### دریافت اطلاعات کامل کاربر

```python
from splusthon.tl.functions.users import GetFullUserRequest

full = await client(GetFullUserRequest(user))
bio = full.full_user.about
```

### بروزرسانی نام و بیوگرافی

```python
from splusthon.tl.functions.account import UpdateProfileRequest

await client(UpdateProfileRequest(
    first_name='نام جدید',
    last_name='نام خانوادگی جدید',
    about='بیوگرافی جدید'
))
```

### بروزرسانی یوزرنیم

```python
from splusthon.tl.functions.account import UpdateUsernameRequest

await client(UpdateUsernameRequest('new_username'))
```

### بروزرسانی عکس پروفایل

```python
from splusthon.tl.functions.photos import UploadProfilePhotoRequest

await client(UploadProfilePhotoRequest(
    await client.upload_file('/path/to/photo.jpg')
))
```

---

## کار با رسانه‌ها

### دانلود عکس پروفایل

```python
# دانلود عکس پروفایل خودتان
await client.download_profile_photo('me')

# دانلود عکس پروفایل کاربر دیگر
await client.download_profile_photo('username')
```

### دانلود فایل از پیام

```python
async for message in client.iter_messages('username'):
    if message.photo:
        path = await message.download_media()
        print(f'فایل ذخیره شد: {path}')
    if message.document:
        path = await message.download_media()
        print(f'فایل ذخیره شد: {path}')
```

### آپلود فایل

```python
file = await client.upload_file('/path/to/file.jpg')
```

---

## مثال‌های پیشرفته

### جستجوی پیام‌ها

```python
from splusthon.tl.functions.messages import SearchRequest

messages = await client(SearchRequest(
    peer='username',
    q='کلمه جستجو',
    limit=100
))
```

### دریافت شرکت‌کنندگان گروه

```python
from splusthon.tl.functions.channels import GetParticipantsRequest
from splusthon.tl.types import ChannelParticipantsSearch

participants = await client(GetParticipantsRequest(
    channel='username',
    filter=ChannelParticipantsSearch(''),
    limit=100,
    offset=0
))
```

### افزایش تعداد بازدید در کانال

```python
from splusthon.tl.functions.messages import GetMessagesViewsRequest

await client(GetMessagesViewsRequest(
    peer=channel,
    id=msg_ids,
    increment=True
))
```

!!! note "یادداشت"
    توجه داشته باشید که این کار فقط **یک یا دو بار در روز** برای هر حساب قابل انجام است.

---

## نکات مهم

1. **از متدهای پیشرفته با احتیاط استفاده کنید**: برخی متدها ممکن است منجر به محدودیت حساب شوند
2. **کد را با متدهای ساده جایگزین کنید**: مگر اینکه به کنترل دقیق نیاز داشته باشید
3. **از مدیریت خطا استفاده کنید**: API خام ممکن است خطاهای بیشتری تولید کند
4. **مستندات API را مطالعه کنید**: https://tl.splusthon.dev/

---

## مرحله بعدی

برای یادگیری بیشتر درباره مقایسه Bot API و MTProto، بخش [مقایسه Bot API و MTProto](botapi-vs-mtproto.md) را مطالعه کنید.
