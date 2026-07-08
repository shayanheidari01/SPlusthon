# مستندات SPlusthon

این دایرکتوری شامل مستندات فارسی کتابخانه SPlusthon برای GitHub Pages است.

## ساختار مستندات

```
docs/
├── _config.yml              # تنظیمات Jekyll
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
└── README.md                # این فایل
```

## نحوه استفاده

### اجرای محلی

1. Jekyll را نصب کنید:
   ```bash
   gem install jekyll bundler
   ```

2. به دایرکتوری docs بروید:
   ```bash
   cd docs
   ```

3. سرور محلی را اجرا کنید:
   ```bash
   bundle exec jekyll serve
   ```

4. مرورگر را به `http://localhost:4000` باز کنید.

### استقرار در GitHub Pages

1. تغییرات را commit کنید:
   ```bash
   git add .
   git commit -m "Add Persian documentation"
   git push origin main
   ```

2. در تنظیمات مخزن GitHub، GitHub Pages را از دایرکتوری `docs` فعال کنید.

## ویژگی‌ها

- **پشتیبانی RTL**: مستندات به زبان فارسی با پشتیبانی راست به چپ
- **طراحی واکنش‌گرا**: نمایش صحیح در تمام دستگاه‌ها
- **فهرست مطالب**: ناوبری آسان بین بخش‌ها
- **کد با رنگ‌بندی**: نمایش زیبای کدهای نمونه
- **جستجو**: قابلیت جستجو در مستندات

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

## مشارکت

برای مشارکت در توسعه مستندات:

1. مخزن را fork کنید
2. تغییرات خود را ایجاد کنید
3. Pull Request ارسال کنید

## پشتیبانی

- [GitHub Issues](https://github.com/shayanheidari01/SPlusthon/issues/)
- [مستندات کامل API](https://tl.splusthon.dev/)
