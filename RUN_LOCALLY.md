# عان التطبيق السريع | Run the ERP System Locally

## التوطئة السريعة ⚨️

بلا أي عراقيل! هذه إرشادات بسيطة لحالات تنفيذ موحدة:

### المتطلبات:
- Docker Desktop (Windows/Mac) + WSL 2 أو Docker Engine (Linux)
- git
- **فقط!**

---

## الخطوات الأربع:

### 1. استنسخ المسروعة
```bash
git clone https://github.com/amido57/comprehensive-erp-system.git
cd comprehensive-erp-system
```

### 2. شغل Docker
```bash
docker-compose up -d
```

### 3. انتظر 60 ثانية ⏳

### 4. افتح التطبيق:

```
http://localhost
```

---

## بيانات الدخول:

```
Email: admin@erp.test
Password: password
```

---

## شو بعده؟

بعما ترغب بفعله:

1. **اعرض اللوحة الرئيسية** - رؤية ملخص العمل 
2. **عرض المنتجات** - إذا كان هناك منتجات
3. **إضافة منتج جديد** - اضغط "إضافة"
4. **عرض المبيعات** - الفواتير والتقارير
5. **القائمة** - تعريات مختلفة

---

## عناوين مفيدة 📄:

| العناوان | الوصف |
|----------|----|
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | التعليمات الكاملة |
| [QUICK_START.md](QUICK_START.md) | البداية السريعة |
| [ARCHITECTURE.md](ARCHITECTURE.md) | بنية النظام |
| [BACKEND_SETUP.md](BACKEND_SETUP.md) | API Reference |

---

## المشاكل العامة:

### التطبيق لم يظهر بعد نشر Docker

```bash
# انتظر 30 ثانية إضافية وجرب مرة أخرى
docker-compose logs -f

# إيقاف ورم من جديد
docker-compose restart
```

### منفذ مستخدم

```bash
docker system prune -a
docker-compose down -v
docker-compose up -d
```

---

## معلومات الاتصال:

```
التطبيق: http://localhost

Backend API: http://localhost:8000/api
Frontend Dev: http://localhost:5173

Database: localhost:3306
  - Username: erp_user
  - Password: erp_password
  - Database: erp_system

Redis: localhost:6379
```

---

## إيقاف التطبيق:

```bash
docker-compose down
```

---

## حذف كل البيانات والبداية من جديد:

```bash
docker-compose down -v
docker-compose up -d
```

---

🌟 **Great! التطبيق الآن راه تشتغل! Happy coding! 🚀**
