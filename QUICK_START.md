# Quick Start Guide - 5 دقائق فقط

## طريقة الاستخدام الأسرع مع Docker 🚀

### المتطلبات:
- Docker و Docker Compose فقط

### التثبيت والتشغيل:

```bash
# 1. استنسخ المشروع
git clone https://github.com/amido57/comprehensive-erp-system.git
cd comprehensive-erp-system

# 2. شغل Docker
docker-compose up -d

# 3. انتظر 30 ثانية ليتم جاهز كل شيء

# 4. افتح المتصفح على:
http://localhost
```

## تسجيل الدخول

```
Email: admin@erp.test
Password: password
```

## توقف التطبيق

```bash
docker-compose down
```

## حل المشاكل

### الميناء مستخدم
```bash
docker-compose down
docker system prune -a
docker-compose up -d
```

### لم تحمل الصفحة
```bash
# انتظر 1 دقيقة والمحاول مرة أخرى
# أو تحقق من السجلات:
docker-compose logs -f app
```

---

## بدون Docker - الطريقة التقليدية

### المتطلبات:
- PHP 8.2+
- MySQL
- Node.js 18+

```bash
# Backend
cd backend
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan serve

# في terminal آخر - Frontend
cd frontend
npm install
npm run dev
```

---

## الملفات المهمة للقراءة

1. **README.md** - نظرة عامة
2. **INSTALLATION.md** - تثبيت متفصل
3. **BACKEND_SETUP.md** - جميع APIs
4. **ARCHITECTURE.md** - البنية التقنية

---

## ماذا بعد التشغيل؟

### استكشف النظام:
- افتح المتصفح: http://localhost
- سجل دخول بـ admin@erp.test / password
- اضغط على "المنتجات" وأضف منتج جديد
- اضغط على "المبيعات" وأنشئ فاتورة
- استكشف التقارير والإحصائيات

### API Testing:
```bash
# احصل على قائمة المنتجات
curl -X GET http://localhost:8000/api/products \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## معلومات مفيدة

- **قاعدة البيانات:** http://localhost:3306
  - Username: root
  - Password: root_password
  - Database: erp_system

- **Redis:** http://localhost:6379

- **Frontend Server:** http://localhost:5173 (إذا شغلت npm run dev مباشرة)

---

## الدعم

- GitHub Issues: https://github.com/amido57/comprehensive-erp-system/issues
- اقرأ الملفات الأخرى للمزيد من المعلومات

**Happy coding! 🎉**
