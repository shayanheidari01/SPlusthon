# مستندات SPlusthon

این دایرکتوری شامل مستندات فارسی کتابخانه SPlusthon برای GitHub Pages با استفاده از MkDocs است.

## ساختار مستندات

```
docs/
├── index.md                 # صفحه اصلی
├── installation.md          # نصب و راه‌اندازی
├── quick-start.md           # شروع سریع
├── api-reference.md         # مرجع API
├── faq.md                   # سوالات متداول
├── concepts/                # مفاهیم پایه
│   ├── index.md             # فهرست مفاهیم
│   ├── entities.md          # Entity (موجودیت)
│   ├── sessions.md          # Session (نشست)
│   ├── events.md            # رویدادها
│   ├── string-sessions.md   # String Sessions
│   ├── errors.md            # مدیریت خطاها
│   ├── full-api.md          # API کامل
│   ├── botapi-vs-mtproto.md # مقایسه Bot API و MTProto
│   └── asyncio.md           # Mastering asyncio
├── examples/                # مثال‌ها
│   ├── index.md             # فهرست مثال‌ها
│   ├── users.md             # کاربران
│   ├── chats-and-channels.md # چت‌ها و کانال‌ها
│   ├── working-with-messages.md # کار با پیام‌ها
│   └── word-of-warning.md   # هشدار مهم
├── stylesheets/
│   └── extra.css            # استایل‌های اضافی
└── README.md                # این فایل
```

## نحوه استفاده

### نصب MkDocs

```bash
pip install mkdocs mkdocs-material mkdocs-static-i18n
```

### اجرای محلی

1. به دایرکتوری ریشه پروژه بروید:
   ```bash
   cd SPlusthon
   ```

2. سرور محلی را اجرا کنید:
   ```bash
   mkdocs serve
   ```

3. مرورگر را به `http://localhost:8000` باز کنید.

### استقرار در GitHub Pages

1. تغییرات را commit کنید:
   ```bash
   git add .
   git commit -m "Update Persian documentation"
   git push origin main
   ```

2. مستندات به صورت خودکار استقرار می‌یابند.

### استقرار دستی

```bash
mkdocs gh-deploy
```

## ویژگی‌ها

- **پشتیبانی RTL**: مستندات به زبان فارسی با پشتیبانی راست به چپ
- **طراحی واکنش‌گرا**: نمایش صحیح در تمام دستگاه‌ها
- **فهرست مطالب**: ناوبری آسان بین بخش‌ها
- **کد با رنگ‌بندی**: نمایش زیبای کدهای نمونه
- **جستجو**: قابلیت جستجو در مستندات
- **تم Material**: طراحی زیبا و مدرن
- **پشتیبانی از i18n**: پشتیبانی از چند زبان

## محتوا

### بخش‌های اصلی

1. **نصب و راه‌اندازی**: راهنمای نصب کتابخانه و وابستگی‌ها
2. **شروع سریع**: راهنمای سریع برای شروع کار
3. **مفاهیم پایه**: توضیحات جامع درباره مفاهیم اساسی
4. **مثال‌ها**: مثال‌های عملی و کاربردی
5. **مرجع API**: مستندات کامل API
6. **سوالات متداول**: پاسخ به سوالات رایج

### بخش UserBot

این مستندات فقط بخش **UserBot** را پوشش می‌دهد. برای مستندات ربات، به بخش مربوطه مراجعه کنید.

## تنظیمات MkDocs

فایل `mkdocs.yml` در دایرکتوری ریشه پروژه تنظیمات MkDocs را شامل می‌شود:

- **تم**: Material
- **زبان**: فارسی
- **جهت**: راست به چپ (RTL)
- **افزونه‌ها**: search, i18n
- **extensiion‌های Markdown**: admonition, code highlighting, و غیره

## مشارکت

برای مشارکت در توسعه مستندات:

1. مخزن را fork کنید
2. تغییرات خود را ایجاد کنید
3. Pull Request ارسال کنید

## پشتیبانی

- [GitHub Issues](https://github.com/shayanheidari01/SPlusthon/issues/)
- [مستندات کامل API](https://tl.splusthon.dev/)
