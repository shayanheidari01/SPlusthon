---
layout: default
title: چت‌ها و کانال‌ها
nav_order: 2
parent: مثال‌ها
---

# چت‌ها و کانال‌ها

در این بخش مثال‌هایی برای کار با چت‌ها و کانال‌ها در SPlusthon آورده شده است.

---

## عضویت در کانال عمومی

```python
from splusthon import SoroushClient
from splusthon.tl.functions.channels import JoinChannelRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت اطلاعات کانال
        channel = await client.get_entity('channel_username')
        
        # عضویت در کانال
        await client(JoinChannelRequest(channel))
        
        print('در کانال عضو شدید')

import asyncio
asyncio.run(main())
```

---

## خروج از کانال

```python
from splusthon import SoroushClient
from splusthon.tl.functions.channels import LeaveChannelRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت اطلاعات کانال
        channel = await client.get_entity('channel_username')
        
        # خروج از کانال
        await client(LeaveChannelRequest(channel))
        
        print('از کانال خارج شدید')

import asyncio
asyncio.run(main())
```

---

## عضویت با لینک دعوت

```python
from splusthon import SoroushClient
from splusthon.tl.functions.messages import ImportChatInviteRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # عضویت با لینک دعوت
        # لینک دعوت: https://t.me/joinchat/AAAAAFFszQPyPEZ7wgxLtd
        # هش: AAAAFAFFszQPyPEZ7wgxLtd
        updates = await client(ImportChatInviteRequest('AAAAAFFszQPyPEZ7wgxLtd'))
        
        print('با لینک دعوت عضو شدید')

import asyncio
asyncio.run(main())
```

---

## اضافه کردن کاربر به چت

```python
from splusthon import SoroushClient
from splusthon.tl.functions.messages import AddChatUserRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت اطلاعات چت و کاربر
        chat = await client.get_entity('chat_username')
        user = await client.get_entity('user_username')
        
        # اضافه کردن کاربر به چت
        await client(AddChatUserRequest(
            chat_id=chat,
            user_id=user,
            fwd_limit=10  # اجازه دیدن ۱۰ پیام آخر
        ))
        
        print('کاربر به چت اضافه شد')

import asyncio
asyncio.run(main())
```

---

## اضافه کردن کاربر به کانال

```python
from splusthon import SoroushClient
from splusthon.tl.functions.channels import InviteToChannelRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت اطلاعات کانال و کاربر
        channel = await client.get_entity('channel_username')
        user = await client.get_entity('user_username')
        
        # اضافه کردن کاربر به کانال
        await client(InviteToChannelRequest(
            channel=channel,
            users=[user]
        ))
        
        print('کاربر به کانال اضافه شد')

import asyncio
asyncio.run(main())
```

---

## بررسی لینک دعوت

```python
from splusthon import SoroushClient
from splusthon.tl.functions.messages import CheckChatInviteRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # بررسی لینک دعوت
        result = await client(CheckChatInviteRequest('hash_from_link'))
        
        print(f'نام چت: {result.chat.title}')
        print(f'تعداد اعضا: {result.participants_count}')

import asyncio
asyncio.run(main())
```

---

## افزایش تعداد بازدید در کانال

```python
from splusthon import SoroushClient
from splusthon.tl.functions.messages import GetMessagesViewsRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت اطلاعات کانال
        channel = await client.get_entity('channel_username')
        
        # دریافت پیام‌های اخیر
        messages = await client.get_messages(channel, limit=10)
        msg_ids = [msg.id for msg in messages]
        
        # افزایش تعداد بازدید
        await client(GetMessagesViewsRequest(
            peer=channel,
            id=msg_ids,
            increment=True
        ))
        
        print('تعداد بازدید افزایش یافت')

import asyncio
asyncio.run(main())
```

{: .note }
> توجه داشته باشید که این کار فقط **یک یا دو بار در روز** برای هر حساب قابل انجام است.

---

## دریافت لیست اعضا

```python
from splusthon import SoroushClient
from splusthon.tl.functions.channels import GetParticipantsRequest
from splusthon.tl.types import ChannelParticipantsSearch

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت لیست اعضا
        result = await client(GetParticipantsRequest(
            channel='channel_username',
            filter=ChannelParticipantsSearch(''),
            limit=100,
            offset=0
        ))
        
        for user in result.users:
            print(f'{user.first_name} {user.last_name}: {user.username}')

import asyncio
asyncio.run(main())
```

---

## نکات مهم

{: .warning }
> - برای اضافه کردن کاربران به چت‌ها و کانال‌ها، فقط برای دوستان یا حساب‌های ربات استفاده کنید
> - سعی نکنید کاربران را به صورت انبوه اضافه کنید، زیرا ممکن است حساب شما به عنوان اسپمر شناسایی شود
> - همیشه از مدیریت خطا استفاده کنید

---

## مرحله بعدی

برای یادگیری بیشتر درباره کار با پیام‌ها، بخش [کار با پیام‌ها]({% link examples/working-with-messages.md %}) را مطالعه کنید.
