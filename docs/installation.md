---
hide:
  - navigation
---

# نصب و راه‌اندازی

راهنمای نصب SPlusthon و پیکربندی محیط توسعه.

---

## نصب پایتون

SPlusthon یک کتابخانه پایتون است، بنابراین ابتدا باید پایتون را از [python.org](https://www.python.org/downloads/) دانلود و نصب کنید (نسخه 3.7 یا بالاتر توصیه می‌شود).

!!! note "یادداشت"
    پس از نصب پایتون، pip را به آخرین نسخه ارتقا دهید:

```bash
python3 -m pip install --upgrade pip
```

---

## نصب کتابخانه

برای نصب SPlusthon، دستور زیر را اجرا کنید:

```bash
python3 -m pip install --upgrade splusthon
```

---

## نصب نسخه توسعه‌دهنده

اگر می‌خواهید آخرین تغییرات منتشر نشده را داشته باشید:

```bash
python3 -m pip install --upgrade https://github.com/shayanheidari01/SPlusthon/archive/v1.zip
```

!!! warning "هشدار"
    نسخه توسعه‌دهنده ممکن است باگ‌هایی داشته باشد و برای استفاده در محیط production توصیه نمی‌شود. اما هنگام گزارش باگ کتابخانه، باید این نسخه را تست کنید.

---

## تأیید نصب

برای اطمینان از نصب صحیح کتابخانه، دستور زیر را اجرا کنید:

```bash
python3 -c "import splusthon; print(splusthon.__version__)"
```

نسخه کتابخانه باید در خروجی نمایش داده شود.

---

## وابستگی‌های اختیاری

### cryptg

اگر cryptg نصب شود، **کتابخانه بسیار سریع‌تر کار می‌کند** زیرا رمزگذاری و رمزگشایی به جای پایتون، در C انجام می‌شود. اگر کد شما با تعداد زیادی رویداد سروکار دارد یا فایل‌های زیادی را دانلود/آپلود می‌کند، سرعت قابل توجهی را مشاهده خواهید کرد.

```bash
pip install cryptg
```

### Pillow

اگر pillow نصب شود، تصاویر بزرگ هنگام ارسال عکس به صورت خودکار تغییر اندازه داده می‌شوند تا از خطای "تصویر نامعتبر" جلوگیری شود.

```bash
pip install pillow
```

### aiohttp

اگر aiohttp نصب شود، کتابخانه قادر به دانلود فایل‌های رسانه WebDocument خواهد بود.

```bash
pip install aiohttp
```

### hachoir

اگر hachoir نصب شود، هنگام ارسال فایل‌ها، اطلاعات متادیتا استخراج می‌شود. سروش‌پلاس از این اطلاعات برای نمایش نام خواننده، هنرمند، عنوان، مدت زمان و اندازه ویدیوها استفاده می‌کند.

```bash
pip install hachoir
```

---

## نصب وابستگی‌های رایج

اگر سیستم شما مبتنی بر apt است، می‌توانید وابستگی‌های رایج را با دستور زیر نصب کنید:

```bash
apt update
apt install clang lib{jpeg-turbo,webp}-dev python{,-dev} zlib-dev
pip install -U --user setuptools
pip install -U --user splusthon cryptg pillow
```

---

## نصب پشتیبانی پروکسی

اگر نیاز به استفاده از پروکسی برای دسترسی به سروش‌پلاس دارید، باید پکیج python-socks را نصب کنید:

```bash
pip install python-socks[asyncio]
```

سپس پروکسی را به کلاینت پاس دهید:

```python
SoroushClient('session_name', api_id, api_hash, proxy=proxy_config)
```

---

## عیب‌یابی نصب

### خطای ImportError

اگر خطای `ImportError: cannot import name 'SoroushClient'` دریافت کردید:

1. مطمئن شوید نام فایل اسکریپت شما `splusthon.py` نیست
2. کتابخانه را دوباره نصب کنید: `pip install --upgrade splusthon`

### خطای نصب وابستگی‌ها

اگر در نصب وابستگی‌ها مشکل دارید:

```bash
pip install --upgrade setuptools wheel
pip install --upgrade splusthon
```

---

## مرحله بعدی

پس از نصب موفقیت‌آمیز کتابخانه، به بخش [شروع سریع](quick-start.md) بروید تا یاد بگیرید چگونه اولین کلاینت خود را ایجاد کنید.
