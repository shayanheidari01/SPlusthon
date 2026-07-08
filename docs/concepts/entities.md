---
layout: default
title: Entity (موجودیت)
nav_order: 1
parent: مفاهیم پایه
---

# Entity (موجودیت)

کتابخانه به طور گسترده از مفهوم "Entity" استفاده می‌کند. Entity به هر شیء User، Chat یا Channel اشاره دارد که API ممکن است در پاسخ به متدهای خاصی مانند `GetUsersRequest` برگرداند.

---

## Entity چیست؟

بسیاری از متدها و درخواست‌ها برای کار به Entity نیاز دارند. به عنوان مثال، پیام را به یک Entity ارسال می‌کنید، یوزرنیم یک Entity را دریافت می‌کنید و غیره.

چیزهای زیادی به عنوان Entity عمل می‌کنند: یوزرنیم‌ها، شماره تلفن‌ها، لینک‌های چت، لینک‌های دعوت، شناسه‌ها و خود تایپ‌ها. یعنی می‌توانید از هر کدام از اینها استفاده کنید وقتی Entity مورد نیاز است.

{: .note }
> به یاد داشته باشید که شماره تلفن باید در لیست مخاطبین شما باشد قبل از اینکه بتوانید از آن استفاده کنید.

---

## ترتیب استفاده از Entity

از **بهترین به بدترین** استفاده کنید:

### 1. Input Entities
به عنوان مثال، `event.input_chat`، `message.input_sender` یا کش کردن Entity‌ای که زیاد استفاده می‌کنید:

```python
entity = await client.get_input_entity(...)
```

### 2. Entities
اگر از قبل Entity را دارید، می‌توانید از آن استفاده کنید:

```python
await client.send_message(user, 'سلام!')
```

### 3. شناسه‌ها
همیشه Entity را از کش جستجو می‌کند (فایل `*.session` Entity‌های مشاهده شده را کش می‌کند).

### 4. یوزرنیم‌ها، شماره تلفن‌ها و لینک‌ها
کش نیز استفاده می‌شود (مگر اینکه `client.get_entity()` را فراخوانی کنید)، اما ممکن است درخواست شبکه‌ای ارسال کند اگر یوزرنیم، شماره تلفن یا لینک هنوز پیدا نشده باشد.

---

## دریافت Entity‌ها

با استفاده از Session، کتابخانه به طور خودکار جفت شناسه و hash را به خاطر می‌سپارد:

```python
# (این مثال‌ها فرض می‌کنند که داخل یک "async def" هستید)
#
# Dialogs مکالمات باز شما هستند.
# این متد لیستی از Dialog برمی‌گرداند که ویژگی .entity و اطلاعات دیگر دارد.
#
# این بخش مهم است زیرا کش entity را پر می‌کند.
dialogs = await client.get_dialogs()

# تمام اینها کار می‌کنند و یک کار را انجام می‌دهند
username = await client.get_entity('username')
username = await client.get_entity('t.me/username')
username = await client.get_entity('https://telegram.dog/username')

# نوع دیگر Entity
channel = await client.get_entity('telegram.me/joinchat/AAAAAEkk2WdoDrB4-Q8-gg')
contact = await client.get_entity('+989123456789')
friend  = await client.get_entity(friend_id)

# دریافت Entity از طریق شناسه (User، Chat یا Channel)
entity = await client.get_entity(some_id)

# می‌توانید نوع را صریح‌تر مشخص کنید با پیچیدن آن در یک Peer
from splusthon.tl.types import PeerUser, PeerChat, PeerChannel

my_user    = await client.get_entity(PeerUser(some_id))
my_chat    = await client.get_entity(PeerChat(some_id))
my_channel = await client.get_entity(PeerChannel(some_id))
```

{: .note }
> **نیازی نیست قبل از استفاده، Entity را دریافت کنید!** بگذارید کتابخانه کار خود را انجام دهد. از شماره تلفن از مخاطبین، یوزرنیم، شناسه یا input entity (ترجیحی اما ضروری نیست)، هر چه دارید استفاده کنید.

---

## Entity در مقابل Input Entity

### Peer و InputPeer

روی تایپ‌های عادی، API همچنین از نسخه‌های `Input*` استفاده می‌کند. نسخه input یک Entity (مانند `InputPeerUser`، `InputChat` و غیره) فقط حداقل اطلاعاتی را که از سروش‌پلاس نیاز است برای شناسایی اینکه به چه کسی اشاره می‌کنید، دارد: **شناسه** و **hash** یک `Peer`.

شناسه Entity برای تمام کاربران و حساب‌های ربات یکسان است، اما hash **برای هر حساب متفاوت است**، بنابراین سعی نکنید hash access را از یک حساب در حساب دیگر استفاده کنید زیرا **کار نخواهد کرد**.

### Peer‌ها

بعضی اوقات، سروش‌پلاس فقط نیاز دارد نوع Entity را همراه با شناسه‌اش مشخص کند. برای این منظور، نسخه‌های `Peer` از Entity‌ها نیز وجود دارند که فقط شناسه دارند. نمی‌توانید hash را از آنها بگیرید زیرا نباید به آن نیاز داشته باشید. کتابخانه احتمالاً قبلاً آن را کش کرده است.

Peers برای شناسایی یک Entity کافی هستند، اما برای ارسال درخواست با آنها کافی نیستند. باید hash آنها را بدانید قبل از اینکه بتوانید "از آنها استفاده کنید" و برای دانستن hash باید Entity را "ملاقات کنید"، چه در مکالمات، شرکت‌کنندگان، پیام‌های فوروارد شده و غیره.

{: .note }
> **می‌توانید از Peers با کتابخانه استفاده کنید.** در پشت صحنه، آنها با نسخه input جایگزین می‌شوند. Peers "به تنهایی کافی نیستند" اما کتابخانه کار بیشتری برای استفاده از نوع مناسب انجام می‌دهد.

---

## Input Entity در مقابل Entity کامل

همانطور که ذکر شد، فراخوانی‌های API نیازی به دانستن تمام اطلاعات Entity ندارند، فقط شناسه و hash آنها. به همین دلیل، متد `client.get_input_entity()` موجود است. این متد همیشه از کش استفاده می‌کند و در بیشتر مواقع هیچ درخواست API‌ای ارسال نمی‌کند.

وقتی درخواستی ارسال می‌شود، اگر Entity کامل را ارائه دهید (مثلاً یک `User`)، کتابخانه آن را به `InputPeer` مورد نیاز به طور خودکار تبدیل می‌کند.

**همیشه** `client.get_input_entity()` **را بر** `client.get_entity()` **ترجیح دهید!** فراخوانی متد دومی همیشه درخواست API برای دریافت آخرین اطلاعات Entity ارسال می‌کند، اما فراخوانی درخواست‌ها فقط به `InputPeer` نیاز دارند، نه اطلاعات کامل. فقط از `client.get_input_entity()` استفاده کنید اگر به اطلاعات واقعی مانند یوزرنیم، نام، عنوان و غیره نیاز دارید.

---

## Entity کامل

علاوه بر `PeerUser`، `InputPeerUser`، `User` (و متغیرهای آن برای چت‌ها و کانال‌ها)، مفهوم `UserFull` نیز وجود دارد.

این نسخه کامل اطلاعات اضافی مانند مسدود بودن کاربر، تنظیمات نوتیفیکیشن، بیوگرافی یا درباره کاربر و غیره را دارد.

همچنین `messages.ChatFull` معادل Entity کامل برای چت‌ها و کانال‌ها است که بخش درباره کانال را نیز دارد.

می‌توانید هر دو را با فراخوانی `GetFullUser`، `GetFullChat` و `GetFullChannel` دریافت کنید.

---

## دسترسی به Entity‌ها

وقتی مستندات می‌گوید "Bases: ChatGetter" به این معنی است که کلاسی که به آن نگاه می‌کنید، *همچنین* می‌تواند به عنوان کلاسی که بر آن استوار است عمل کند. در این مورد، `ChatGetter` می‌داند چگونه *چت* را که چیزی به آن تعلق دارد دریافت کند.

```python
# Message یک ChatGetter است
message.is_private
message.chat_id
await message.get_chat()
# ...و غیره

# SenderGetter مشابه است
message.user_id
await message.get_input_sender()
message.user
# ...و غیره
```

---

## خلاصه

TL;DR؛ اگر به دلیل "Could not find the input entity for" اینجا هستید، باید از خود بپرسید "چگونه این Entity را از طریق برنامه‌های رسمی پیدا کردم؟" حالا همان کار را با کتابخانه انجام دهید:

```python
# (این مثال‌ها فرض می‌کنند که داخل یک "async def" هستید)
async with client:
    # آیا یوزرنیم دارد؟ از آن استفاده کنید!
    entity = await client.get_entity(username)
    
    # آیا مکالمه بازی با آنها دارید؟ Dialogs را دریافت کنید.
    await client.get_dialogs()
    
    # آیا عضو گروهی هستند؟ آنها را دریافت کنید.
    await client.get_participants('username')
    
    # آیا Entity فرستنده اصلی پیام فوروارد شده است؟ آن را دریافت کنید.
    await client.get_messages('username', 100)
    
    # اکنون می‌توانید از شناسه استفاده کنید، هر جا!
    await client.send_message(123456, 'سلام!')
    
    entity = await client.get_entity(123456)
    print(entity)
```

وقتی کتابخانه Entity را "دیده باشد"، می‌توانید از شناسه **عددی** آن استفاده کنید. نمی‌توانید از Entity‌هایی استفاده کنید که کتابخانه ندیده است. باید کتابخانه آنها را *حداقل یک بار* ببیند و به درستی قطع اتصال کند.
