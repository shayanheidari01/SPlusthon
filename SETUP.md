# راهنمای راه‌اندازی مستندات

این فایل راهنمای کامل راه‌اندازی مستندات SPlusthon با استفاده از MkDocs است.

## پیش‌نیازها

- Python 3.7 یا بالاتر
- pip

## نصب وابستگی‌ها

```bash
pip install mkdocs mkdocs-material
```

## ساختار پروژه

```
SPlusthon/
├── mkdocs.yml                 # تنظیمات MkDocs
├── docs/                      # مستندات
│   ├── index.md              # صفحه اصلی
│   ├── installation.md       # نصب و راه‌اندازی
│   ├── quick-start.md        # شروع سریع
│   ├── api-reference.md      # مرجع API
│   ├── faq.md                # سوالات متداول
│   ├── concepts/             # مفاهیم پایه
│   ├── examples/             # مثال‌ها
│   └── stylesheets/          # استایل‌های اضافی
├── .github/workflows/        # GitHub Actions
│   └── deploy-docs.yml       # استقرار خودکار
└── test_mkdocs.py            # اسکریپت تست
```

## دستورات پرکاربرد

### اجرای محلی

```bash
mkdocs serve
```

مرورگر را به `http://localhost:8000` باز کنید.

### ساخت مستندات

```bash
mkdocs build
```

فایل‌های HTML در دایرکتوری `site/` ایجاد می‌شوند.

### استقرار در GitHub Pages

```bash
mkdocs gh-deploy
```

یا از GitHub Actions استفاده کنید (فایل `.github/workflows/deploy-docs.yml`).

### تست مستندات

```bash
python test_mkdocs.py
```

## ویژگی‌های MkDocs

- **تم Material**: طراحی زیبا و مدرن
- **پشتیبانی RTL**: مستندات فارسی با پشتیبانی راست به چپ
- **جستجو**: قابلیت جستجو در مستندات
- **رنگ‌بندی کد**: نمایش زیبای کدهای نمونه
- **فهرست مطالب**: ناوبری آسان
- **واکنش‌گرا**: نمایش صحیح در تمام دستگاه‌ها

## پیکربندی

فایل `mkdocs.yml` تنظیمات اصلی را شامل می‌شود:

- **site_name**: نام سایت
- **theme**: تم و تنظیمات نمایشی
- **nav**: ساختار ناوبری
- **plugins**: افزونه‌ها
- **markdown_extensions**: افزونه‌های Markdown

## استقرار خودکار

GitHub Actions workflow در `.github/workflows/deploy-docs.yml`:

1. در هر push به شاخه `main` اجرا می‌شود
2. مستندات را می‌سازد
3. در شاخه `gh-pages` استقرار می‌دهد

## عیب‌یابی

### خطای "command not found: mkdocs"

وابستگی‌ها را نصب کنید:

```bash
pip install mkdocs mkdocs-material
```

### خطای "No such file: docs/index.md"

مطمئن شوید در دایرکتوری ریشه پروژه هستید و دایرکتوری `docs` وجود دارد.

### خطای YAML در mkdocs.yml

سینتکس YAML را بررسی کنید و از فاصله‌گذاری صحیح استفاده کنید.

## منابع

- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
