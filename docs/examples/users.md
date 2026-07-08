---
hide:
  - navigation
---

# کاربران

در این بخش مثال‌هایی برای کار با کاربران در SPlusthon آورده شده است.

---

## دریافت اطلاعات کامل کاربر

```python
from splusthon import SoroushClient
from splusthon.tl.functions.users import GetFullUserRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت اطلاعات کامل کاربر
        full = await client(GetFullUserRequest('username'))
        
        # دریافت بیوگرافی
        bio = full.full_user.about
        print(f'بیوگرافی: {bio}')
        
        # دریافت سایر اطلاعات
        user = full.users[0]
        print(f'نام: {user.first_name}')
        print(f'یوزرنیم: {user.username}')

import asyncio
asyncio.run(main())
```

---

## بروزرسانی نام و بیوگرافی

```python
from splusthon import SoroushClient
from splusthon.tl.functions.account import UpdateProfileRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # بروزرسانی نام و بیوگرافی
        await client(UpdateProfileRequest(
            first_name='نام جدید',
            last_name='نام خانوادگی جدید',
            about='بیوگرافی جدید من'
        ))
        
        print('پروفایل بروزرسانی شد')

import asyncio
asyncio.run(main())
```

---

## بروزرسانی یوزرنیم

```python
from splusthon import SoroushClient
from splusthon.tl.functions.account import UpdateUsernameRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # بروزرسانی یوزرنیم
        await client(UpdateUsernameRequest('new_username'))
        
        print('یوزرنیم بروزرسانی شد')

import asyncio
asyncio.run(main())
```

---

## بروزرسانی عکس پروفایل

```python
from splusthon import SoroushClient
from splusthon.tl.functions.photos import UploadProfilePhotoRequest

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # آپلود عکس جدید
        file = await client.upload_file('/path/to/photo.jpg')
        
        # بروزرسانی عکس پروفایل
        await client(UploadProfilePhotoRequest(file))
        
        print('عکس پروفایل بروزرسانی شد')

import asyncio
asyncio.run(main())
```

---

## دانلود عکس پروفایل

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دانلود عکس پروفایل خودتان
        await client.download_profile_photo('me')
        
        # دانلود عکس پروفایل کاربر دیگر
        await client.download_profile_photo('username')
        
        print('عکس پروفایل دانلود شد')

import asyncio
asyncio.run(main())
```

---

## دریافت لیست مخاطبین

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت مخاطبین
        contacts = await client.get_contacts()
        
        for contact in contacts:
            print(f'{contact.first_name} {contact.last_name}: {contact.username}')

import asyncio
asyncio.run(main())
```

---

## جستجوی کاربران

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # جستجوی کاربر با یوزرنیم
        user = await client.get_entity('username')
        print(f'نام کاربر: {user.first_name}')
        
        # جستجوی کاربر با شماره تلفن
        user = await client.get_entity('+989123456789')
        print(f'نام کاربر: {user.first_name}')

import asyncio
asyncio.run(main())
```

---

## بررسی وضعیت کاربر

```python
from splusthon import SoroushClient

async def main():
    with SoroushClient('anon', api_id, api_hash) as client:
        # دریافت اطلاعات کاربر
        user = await client.get_entity('username')
        
        # بررسی وضعیت‌های مختلف
        print(f'آیا آنلاین است: {user.status}')
        print(f'آیا محدود شده: {user.restricted}')
        print(f'آیا مسدود شده: {user.deleted}')

import asyncio
asyncio.run(main())
```

---

## نکات مهم

!!! note "یادداشت"
    - برای دریافت اطلاعات کامل کاربر از `GetFullUserRequest` استفاده کنید
    - برای بروزرسانی پروفایل از `UpdateProfileRequest` استفاده کنید
    - برای دانلود عکس پروفایل از `download_profile_photo` استفاده کنید
    - همیشه از مدیریت خطا استفاده کنید

---

## مرحله بعدی

برای یادگیری بیشتر درباره کار با چت‌ها و کانال‌ها، بخش [چت‌ها و کانال‌ها](chats-and-channels.md) را مطالعه کنید.
