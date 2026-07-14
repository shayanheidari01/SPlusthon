<div align="center">

<img src="logo.svg" width="180" alt="SPlusthon Logo">

<h1>SPlusthon</h1>

<p>
  <strong>Asynchronous Python library for the Soroush Plus API</strong>
</p>

<p>
  Built on <strong>Telethon</strong> and fully adapted for the
  <strong>Soroush Plus</strong> protocol.
</p>

<p>

<a href="https://pypi.org/project/splusthon/">
  <img src="https://img.shields.io/pypi/v/splusthon.svg?style=for-the-badge" alt="PyPI">
</a>

<a href="https://pypi.org/project/splusthon/">
  <img src="https://img.shields.io/pypi/pyversions/splusthon.svg?style=for-the-badge" alt="Python">
</a>

<a href="LICENSE">
  <img src="https://img.shields.io/github/license/shayanheidari01/SPlusthon?style=for-the-badge" alt="License">
</a>

<a href="https://github.com/shayanheidari01/SPlusthon/stargazers">
  <img src="https://img.shields.io/github/stars/shayanheidari01/SPlusthon?style=for-the-badge" alt="Stars">
</a>

<a href="https://github.com/shayanheidari01/SPlusthon/issues">
  <img src="https://img.shields.io/github/issues/shayanheidari01/SPlusthon?style=for-the-badge" alt="Issues">
</a>

<a href="https://github.com/shayanheidari01/SPlusthon/actions">
  <img src="https://img.shields.io/github/actions/workflow/status/shayanheidari01/SPlusthon/tests.yml?style=for-the-badge" alt="Build">
</a>

</p>

<p>

<a href="https://shayanheidari01.github.io/SPlusthon/"><strong>Documentation</strong></a>
•
<a href="https://pypi.org/project/splusthon/"><strong>PyPI</strong></a>
•
<a href="https://github.com/shayanheidari01/SPlusthon"><strong>GitHub</strong></a>
•
<a href="https://web.splus.ir"><strong>Soroush Plus</strong></a>

</p>

</div>

---

کتابخانه SPlusthon یک کتابخانه مدرن و قدرتمند برای **Python 3** است که بر پایه
**asyncio** توسعه یافته و امکان تعامل مستقیم با **API پیام‌رسان سروش پلاس**
را به‌عنوان **کاربر** یا **ربات** فراهم می‌کند.

این پروژه بر پایه **Telethon** توسعه یافته و برای معماری اختصاصی سروش پلاس
بازطراحی شده است. کتابخانه از **TL Schema (Layer 182)**،
**RSA Encryption**، **DC Routing** و **WebSocket Transport**
پشتیبانی می‌کند و تجربه‌ای سریع، پایدار و نزدیک به کلاینت رسمی ارائه می‌دهد.

> **Note:** لطفاً هنگام استفاده از این کتابخانه، قوانین و شرایط استفاده سروش پلاس را
> رعایت کنید. مسئولیت استفاده از این پروژه بر عهده کاربر است.

## ویژگی‌ها

- پشتیبانی کامل از حساب کاربری و ربات
- مبتنی بر asyncio با کارایی بالا
- امکان استفاده به‌صورت Sync و Async
- پشتیبانی کامل از TL Schema اختصاصی سروش
- مدیریت Session و StringSession
- پشتیبانی از WebSocket
- پشتیبانی از DC Routing
- رمزنگاری RSA و AES
- بدون نیاز به API ID و API Hash
- API مشابه Telethon برای مهاجرت آسان

## نصب

از PyPI:

```bash
pip install splusthon
```

یا آخرین نسخه توسعه:

```bash
pip install git+https://github.com/shayanheidari01/SPlusthon.git
```

## شروع سریع

```python
from splusthon import SoroushClient
from splusthon.sessions import StringSession

client = SoroushClient(StringSession())

client.start()
```

## نمونه

```python
from splusthon import SoroushClient, events
from splusthon.sessions import StringSession

client = SoroushClient(StringSession())

@client.on(events.NewMessage)
async def handler(event):
    await event.reply("سلام 👋")

client.start()
client.run_until_disconnected()
```

ارسال پیام

```python
client.send_message(
    "username",
    "سلام از SPlusthon ❤️"
)
```

ارسال فایل

```python
client.send_file(
    "username",
    "/path/image.jpg"
)
```

دانلود رسانه

```python
message = client.get_messages("username", limit=1)[0]
message.download_media()
```

## Session ذخیره‌شده

```python
from splusthon import SoroushClient
from splusthon.sessions import StringSession

session = "1AwA..."

with SoroushClient(StringSession(session)) as client:
    print(client.get_me())
```

## وابستگی‌ها

- aiohttp
- pyaes
- rsa

اختیاری:

- cryptg (افزایش سرعت رمزنگاری)

## مستندات

مستندات کامل پروژه:

https://shayanheidari01.github.io/SPlusthon/

## مجوز

این پروژه تحت مجوز **GNU GPL v3** منتشر شده است.

---

<div align="center">

**Made with ❤️ by Shayan Heidari**

https://github.com/shayanheidari01

</div>
