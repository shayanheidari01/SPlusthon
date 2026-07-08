---
layout: default
title: مستندات SPlusthon
nav_order: 1
---

# مستندات SPlusthon

**SPlusthon** یک کتابخانه پایتون asyncio است که برای تعامل با API سروش‌پلاس طراحی شده است. این کتابخانه به شما امکان می‌دهد تا با استفاده از حساب کاربری خود، ربات‌ها و اسکریپت‌های مختلفی برای سروش‌پلاس بنویسید.

{: .note }
> این مستندات فقط بخش **UserBot** را پوشش می‌دهد. اگر به دنبال مستندات ربات هستید، به بخش مربوطه مراجعه کنید.

---

## چرا SPlusthon؟

- **سادگی**: API ساده و خوانا برای تعامل با سروش‌پلاس
- **کارایی**: پشتیبانی از asyncio برای عملیات همزمان
- **امکانات گسترده**: ارسال پیام، فایل، عکس و مدیریت مکالمات
- **پشتیبانی از رویدادها**: سیستم قدرتمند event برای پاسخ خودکار
- **امنیت**: ذخیره‌سازی امن session و credentialها

---

## بخش‌های اصلی مستندات

### [شروع سریع]({% link quick-start.md %})
راهنمای سریع برای شروع کار با SPlusthon در کمتر از ۵ دقیقه.

### [نصب و راه‌اندازی]({% link installation.md %})
راهنمای نصب کتابخانه و وابستگی‌های اختیاری.

### [مفاهیم پایه]({% link concepts/index.md %})
توضیحات جامع درباره مفاهیم اساسی مانند Entity، Session و رویدادها.

### [مثال‌ها]({% link examples/index.md %})
مثال‌های عملی و کاربردی برای یادگیری بهتر.

### [مرجع API]({% link api-reference.md %})
مستندات کامل API کتابخانه.

### [سوالات متداول]({% link faq.md %})
پاسخ به سوالات رایج کاربران.

---

## نمای کلی کتابخانه

```python
from splusthon import SoroushClient, events

# ایجاد کلاینت
client = SoroushClient('session_name')

# ارسال پیام
await client.send_message('username', 'سلام!')

# گوش دادن به رویدادها
@client.on(events.NewMessage(pattern='(?i)سلام'))
async def handler(event):
    await event.reply('سلام! خوش آمدید.')
```

---

## پیش‌نیازها

- پایتون 3.7 یا بالاتر
- pip (آخرین نسخه)
- آشنایی مقدماتی با asyncio در پایتون

---

## لینک‌های مفید

- [GitHub](https://github.com/shayanheidari01/SPlusthon)
- [سروش‌پلاس](https://web.splus.ir)
- [مرجع کامل API](https://tl.splusthon.dev/)
