# استفاده از تصویر رسمی پایتون
FROM python:3.12-slim-bookworm

# نصب وابستگی‌های مورد نیاز
RUN apt-get update && apt-get install -y \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    libpq-dev

# تنظیم مسیر کاری
WORKDIR /app

# کپی کردن فایل‌های پروژه
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه داخل کانتینر
COPY . /app/

# اجرای سرور
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
