```rst
.. raw:: html

   <div align="center">

   <img src="logo.svg" width="200" alt="SPlusthon Logo">

   <h1>SPlusthon</h1>

   <p>
   <strong>کتابخانه‌ای قدرتمند برای Python 3 مبتنی بر asyncio جهت تعامل با API پیام‌رسان سروش پلاس</strong>
   </p>

   <p>
   ساخته‌شده بر پایه Telethon و سازگار با معماری اختصاصی سروش پلاس
   </p>

   </div>

----

کتابخانه **SPlusthon** یک کتابخانه قدرتمند برای **Python 3** مبتنی بر **asyncio** است که
امکان تعامل با API پیام‌رسان
`سروش پلاس <https://web.splus.ir>`_
را به‌عنوان **کاربر** یا **ربات** (جایگزین Bot API) فراهم می‌کند.

این پروژه بر پایه فورک **Telethon** توسعه یافته و به‌طور کامل برای معماری
سروش پلاس سازگار شده است. SPlusthon از **TL Schema اختصاصی سروش (Layer 182)**،
**مسیریابی DC**، **کلیدهای RSA** و **ارتباط WebSocket** پشتیبانی می‌کند تا
تجربه‌ای سریع، پایدار و نزدیک به کلاینت رسمی ارائه دهد.

.. note::

   استفاده از این کتابخانه بر عهده کاربر است. لطفاً هنگام توسعه برنامه‌های خود،
   قوانین و شرایط استفاده سروش پلاس را رعایت کنید تا از محدود شدن یا مسدود شدن
   حساب کاربری جلوگیری شود.

ویژگی‌ها
--------

- ارتباط با API سروش پلاس به‌عنوان کاربر یا ربات
- پشتیبانی کامل از TL Schema اختصاصی سروش (Layer 182)
- پشتیبانی از DC Routing، RSA و WebSocket
- مدیریت Session و ذخیره‌سازی نشست
- پشتیبانی از هر دو حالت **async** و **sync**
- بدون نیاز به API ID و API Hash اختصاصی

این کتابخانه چیست؟
------------------

کتابخانه SPlusthon توسعه برنامه‌های مبتنی بر سروش پلاس را تا حد زیادی ساده می‌کند.

به‌جای درگیر شدن با جزئیات پیچیده پروتکل، احراز هویت، رمزنگاری و ارتباطات شبکه،
می‌توانید تنها با چند خط کد به امکانات سروش پلاس دسترسی داشته باشید و تمرکز خود
را روی توسعه برنامه قرار دهید.

نصب
---

از طریق PyPI:

.. code-block:: bash

   pip install splusthon

یا آخرین نسخه توسعه از GitHub:

.. code-block:: bash

   pip install git+https://github.com/shayanheidari01/SPlusthon.git

شروع کار
--------

کتابخانه SPlusthon به‌صورت پیش‌فرض شامل اطلاعات موردنیاز برای اتصال به API سروش پلاس است؛
بنابراین برای ساخت کلاینت نیازی به **API ID** یا **API Hash** نخواهید داشت.

.. code-block:: python

    from splusthon import SoroushClient, events, sync
    from splusthon.sessions import StringSession

    client = SoroushClient(StringSession())
    client.start()

نمونه استفاده
-------------

.. code-block:: python

    # دریافت اطلاعات حساب
    print(client.get_me().stringify())

    # ارسال پیام
    client.send_message(
        "username",
        "سلام! این پیام توسط SPlusthon ارسال شده است."
    )

    # ارسال فایل
    client.send_file(
        "username",
        "/home/myself/Pictures/holidays.jpg"
    )

    # دانلود تصویر پروفایل
    client.download_profile_photo("me")

    # دریافت پیام‌ها
    messages = client.get_messages("username")
    messages[0].download_media()

    # دریافت رویداد پیام جدید
    @client.on(events.NewMessage(pattern="(?i)hi|hello"))
    async def handler(event):
        await event.respond("سلام!")

استفاده از Session ذخیره‌شده
----------------------------

اگر قبلاً Session خود را ذخیره کرده باشید، می‌توانید به‌سادگی آن را دوباره بارگذاری کنید.

.. code-block:: python

    from splusthon import SoroushClient
    from splusthon.sessions import StringSession

    session_string = "1AwA..."

    with SoroushClient(StringSession(session_string)) as client:
        print(client.get_me())

وابستگی‌ها
----------

وابستگی‌های اصلی:

- ``pyaes`` — پیاده‌سازی رمزنگاری AES
- ``rsa`` — پیاده‌سازی رمزنگاری RSA
- ``aiohttp`` — ارتباطات HTTP ناهمگام

وابستگی اختیاری:

- ``cryptg`` — افزایش سرعت عملیات رمزنگاری

لینک‌ها
-------

- گیت هاب: https://github.com/shayanheidari01/SPlusthon
- مستندات: https://shayanheidari01.github.io/SPlusthon/
- سروش پلاس: https://web.splus.ir

مجوز
----

این پروژه تحت مجوز
`GNU General Public License v3.0 <LICENSE>`_
منتشر شده است.

----

**توسعه و نگهداری توسط**

`ShayanHeidari <https://github.com/shayanheidari01>`_
```
