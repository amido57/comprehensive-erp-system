# دليل النشر والتشغيل الشامل | Comprehensive Deployment Guide

## المتطلبات الأساسية | Prerequisites

### Option 1: Docker (الخيار الموصى به)
- Docker Desktop (Windows/Mac) أو Docker Engine (Linux)
- Docker Compose v2.0+
- 4GB RAM minimum
- 20GB Free Disk Space

### Option 2: التثبيت التقليدي بدون Docker
- PHP 8.2+ with extensions: curl, json, mbstring, pdo, pdo_mysql, redis
- MySQL 8.0+
- Node.js 18+
- Composer
- Redis 7+

---

## الطريقة الأولى: Docker (مفضل) 🐳

### الخطوة 1: استنساخ المشروع
```bash
git clone https://github.com/amido57/comprehensive-erp-system.git
cd comprehensive-erp-system
```

### الخطوة 2: إنشاء ملفات البيئة
```bash
cp .env.example .env
```

### الخطوة 3: بدء جميع الخدمات
```bash
docker-compose up -d
```

**المدة المتوقعة:** 30-60 ثانية للمرة الأولى

### الخطوة 4: التحقق من حالة الحاويات
```bash
docker-compose ps
```

يجب أن ترى:
- erp_app (backend) - running
- erp_db (mysql) - running
- erp_redis (redis) - running
- erp_frontend (node) - running
- erp_nginx (web server) - running

### الخطوة 5: تشغيل Migrations وSeeders
```bash
docker-compose exec app php artisan migrate --seed
```

### الخطوة 6: الوصول للتطبيق

**الواجهة الرئيسية:**
- **URL:** http://localhost
- **Email:** admin@erp.test
- **Password:** password

**الواجهات الأخرى:**
- Frontend Dev Server: http://localhost:5173
- Backend API: http://localhost:8000/api
- Database: localhost:3306
- Redis: localhost:6379

---

## الطريقة الثانية: التثبيت التقليدي بدون Docker

### Backend Setup (Laravel)

```bash
cd backend

# 1. تثبيت Dependencies
composer install

# 2. إعداد ملف البيئة
cp .env.example .env

# 3. توليد Application Key
php artisan key:generate

# 4. تشغيل Migrations
php artisan migrate --seed

# 5. إنشاء Symbolic Link للـ Storage
php artisan storage:link

# 6. تشغيل Development Server
php artisan serve
```

**Backend سيعمل على:** http://localhost:8000

### Frontend Setup (Vue.js + Vite)

في terminal جديد:

```bash
cd frontend

# 1. تثبيت Dependencies
npm install

# 2. تشغيل Dev Server
npm run dev
```

**Frontend سيعمل على:** http://localhost:5173

### Database Setup

تأكد من أن MySQL يعمل:

```bash
mysql -u root -p

CREATE DATABASE erp_system;
CREATE USER 'erp_user'@'localhost' IDENTIFIED BY 'erp_password';
GRANT ALL PRIVILEGES ON erp_system.* TO 'erp_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Redis Setup

تأكد من تشغيل Redis:

```bash
# Linux/Mac
redis-server

# أو على Windows
redis-server.exe
```

---

## التحقق من التشغيل السليم ✅

### 1. فحص الـ API

```bash
# الحصول على قائمة المنتجات
curl -X GET http://localhost:8000/api/products \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Accept: application/json"

# تسجيل الدخول
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@erp.test",
    "password": "password"
  }'
```

### 2. فحص قاعدة البيانات

```bash
mysql -h localhost -u erp_user -p erp_system

SHOW TABLES;
SELECT COUNT(*) FROM users;
```

### 3. فحص Redis

```bash
redis-cli
PING  # يجب أن يرد: PONG
IEXISTS users
```

---

## حل المشاكل الشائعة 🔧

### المشكلة 1: Port مستخدم بالفعل

```bash
# إيقاف الحاويات الحالية
docker-compose down

# تنظيف الموارد
docker system prune -a

# البداية من جديد
docker-compose up -d
```

### المشكلة 2: عدم تحميل الصفحة

```bash
# انتظر دقيقة ثم جرب مرة أخرى
# أو تحقق من السجلات
docker-compose logs -f app
```

### المشكلة 3: خطأ في قاعدة البيانات

```bash
# أعد تشغيل الحاويات
docker-compose down -v
docker-compose up -d

# ثم قم بالـ Migration من جديد
docker-compose exec app php artisan migrate --seed
```

### المشكلة 4: عدم تسجيل الدخول

```bash
# أعد تعيين كلمات المرور
docker-compose exec app php artisan tinker

# ثم أكتب:
App\Models\User::first()->update(['password' => bcrypt('password')]);
```

---

## بدء التطوير 👨‍💻

### إضافة ميزة جديدة

```bash
# 1. اختبر النسخة الحالية
http://localhost

# 2. أنشئ migration جديد
docker-compose exec app php artisan make:migration create_new_table

# 3. أنشئ model جديد
docker-compose exec app php artisan make:model NewModel -m

# 4. قم بالـ Migration
docker-compose exec app php artisan migrate

# 5. أنشئ API Controller
docker-compose exec app php artisan make:controller Api/NewModelController --resource
```

### تشغيل الاختبارات

```bash
docker-compose exec app php artisan test
```

### عرض السجلات

```bash
# جميع السجلات
docker-compose logs -f

# سجلات تطبيق معين
docker-compose logs -f app
docker-compose logs -f frontend
```

---

## الإيقاف والتنظيف 🛑

### إيقاف التطبيق

```bash
docker-compose stop
```

### حذف البيانات والبدء من جديد

```bash
docker-compose down -v
```

### تنظيف كامل

```bash
docker-compose down -v
docker system prune -a
```

---

## معلومات قاعدة البيانات 🗄️

```
Host: localhost (Docker) أو db (من داخل Container)
Port: 3306
Database: erp_system
Username: erp_user
Password: erp_password
Root Password: root_password
```

---

## معلومات Redis 📦

```
Host: localhost (Docker) أو redis (من داخل Container)
Port: 6379
Database: 0
```

---

## الميزات الرئيسية المتاحة ✨

✅ **الإدارة الشاملة للمبيعات**
✅ **إدارة المخزون المتقدمة**
✅ **الحسابات والفاتورة**
✅ **إدارة الموارد البشرية**
✅ **التقارير والتحليلات**
✅ **نقطة البيع (POS)**
✅ **الدعم متعدد اللغات (عربي/إنجليزي)**
✅ **واجهة عصرية وسهلة الاستخدام**
✅ **API RESTful كاملة**
✅ **دعم الأدوار والأذونات**

---

## الدعم والمساعدة 💬

- 📖 اقرأ [QUICK_START.md](QUICK_START.md) للبدء السريع
- 📚 اقرأ [ARCHITECTURE.md](ARCHITECTURE.md) لفهم البنية
- 🔧 اقرأ [BACKEND_SETUP.md](BACKEND_SETUP.md) للـ API
- 💻 اقرأ [INSTALLATION.md](INSTALLATION.md) للتثبيت التفصيلي
- 🐛 أنشئ [Issue](https://github.com/amido57/comprehensive-erp-system/issues) للمشاكل

---

## ملاحظات مهمة 📝

⚠️ **لا تستخدم المشروع في الإنتاج بدون تغيير كلمات المرور الافتراضية**

⚠️ **تأكد من تفعيل HTTPS في الإنتاج**

⚠️ **قم بنسخ احتياطية من قاعدة البيانات بانتظام**

⚠️ **حدّث PHP وMySQL والمكتبات بانتظام**

---

**Happy Deploying! 🚀**
