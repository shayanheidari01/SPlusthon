---
hide:
  - navigation
---

# مستندات SPlusthon

**SPlusthon** یک کتابخانه پایتون asyncio است که برای تعامل با API سروش‌پلاس طراحی شده است. این کتابخانه به شما امکان می‌دهد تا با استفاده از حساب کاربری خود، ربات‌ها و اسکریپت‌های مختلفی برای سروش‌پلاس بنویسید.

!!! note "یادداشت"
    این مستندات فقط بخش **UserBot** را پوشش می‌دهد. اگر به دنبال مستندات ربات هستید، به بخش مربوطه مراجعه کنید.

---

## چرا SPlusthon؟

- **سادگی**: API ساده و خوانا برای تعامل با سروش‌پلاس
- **کارایی**: پشتیبانی از asyncio برای عملیات همزمان
- **امکانات گسترده**: ارسال پیام، فایل، عکس و مدیریت مکالمات
- **پشتیبانی از رویدادها**: سیستم قدرتمند event برای پاسخ خودکار
- **امنیت**: ذخیره‌سازی امن session و credentialها

---

## بخش‌های اصلی مستندات

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } __شروع سریع__

    ---

    راهنمای سریع برای شروع کار با SPlusthon در کمتر از ۵ دقیقه.

    [:octicons-arrow-right-24: شروع کنید](quick-start.md)

-   :material-cog:{ .lg .middle } __نصب و راه‌اندازی__

    ---

    راهنمای نصب کتابخانه و وابستگی‌های اختیاری.

    [:octicons-arrow-right-24: نصب کنید](installation.md)

-   :material-book-open-variant:{ .lg .middle } __مفاهیم پایه__

    ---

    توضیحات جامع درباره مفاهیم اساسی مانند Entity، Session و رویدادها.

    [:octicons-arrow-right-24: یاد بگیرید](concepts/index.md)

-   :material-code-braces:{ .lg .middle } __مثال‌ها__

    ---

    مثال‌های عملی و کاربردی برای یادگیری بهتر.

    [:octicons-arrow-right-24: ببینید](examples/index.md)

-   :material-api:{ .lg .middle } __مرجع API__

    ---

    مستندات کامل API کتابخانه.

    [:octicons-arrow-right-24: بررسی کنید](api-reference.md)

-   :material-frequently-asked-questions:{ .lg .middle } __سوالات متداول__

    ---

    پاسخ به سوالات رایج کاربران.

    [:octicons-arrow-right-24: بخوانید](faq.md)

</div>

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
