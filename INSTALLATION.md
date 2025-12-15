# Complete ERP System - Installation Guide

## System Requirements

### Minimum
- PHP 8.2+
- MySQL 8.0+ or PostgreSQL 15+
- Redis 7.0+
- Node.js 18+
- Docker & Docker Compose (optional)

### Recommended
- PHP 8.3+
- MySQL 8.1+
- Redis 7.2+
- Node.js 20+ LTS
- 4GB RAM minimum
- 20GB disk space

## Quick Start (Docker)

```bash
git clone https://github.com/amido57/comprehensive-erp-system.git
cd comprehensive-erp-system
docker-compose up -d

# Access the application
Frontend: http://localhost
Backend API: http://localhost:8000
MySQL: localhost:3306
Redis: localhost:6379
```

## Manual Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/amido57/comprehensive-erp-system.git
cd comprehensive-erp-system
```

### Step 2: Backend Setup
```bash
cd backend
composer install
cp .env.example .env
php artisan key:generate
```

### Step 3: Database Configuration
Edit `.env`:
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=erp_system
DB_USERNAME=root
DB_PASSWORD=password
```

### Step 4: Database Setup
```bash
php artisan migrate
php artisan db:seed
php artisan passport:install
```

### Step 5: Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

### Step 6: Start Application
```bash
# Terminal 1 - Backend
cd backend
php artisan serve

# Terminal 2 - Frontend  
cd frontend
npm run dev

# Terminal 3 - Queue (optional)
cd backend
php artisan queue:work
```

## Default Credentials

```
Email: admin@erp.test
Password: password
Role: Administrator
```

## Environment Setup

### Development
```bash
APP_ENV=local
APP_DEBUG=true
APP_LOG_LEVEL=debug
```

### Production
```bash
APP_ENV=production
APP_DEBUG=false
APP_LOG_LEVEL=error
```

## Nginx Configuration

```nginx
server {
    listen 80;
    server_name localhost;
    root /var/www/app/public;

    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

## Troubleshooting

### MySQL Connection Error
```bash
# Check MySQL is running
mysql -h127.0.0.1 -u root -p

# Verify credentials in .env
grep DB_ .env
```

### Permission Issues
```bash
chmod -R 775 storage bootstrap/cache
chown -R www-data:www-data .
```

### Redis Connection Error
```bash
# Check Redis
redis-cli ping

# Start Redis
redis-server
```

### Node Modules Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Features Checklist

✅ Multi-language (Arabic/English)
✅ RESTful API with JWT
✅ Role-Based Access Control
✅ Complete Accounting Module
✅ Inventory Management
✅ Sales & POS
✅ Purchasing
✅ HR & Payroll
✅ Dashboard & Reports
✅ Real-time Notifications
✅ Multi-company Support
✅ Advanced Filtering & Export

## API Testing

### Postman Collection
Import `postman_collection.json` in Postman

### cURL Example
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@erp.test",
    "password": "password"
  }'

# Get Products
curl -X GET http://localhost:8000/api/products \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Database Backup

```bash
# Backup
mysqldump -u root -p erp_system > backup.sql

# Restore
mysql -u root -p erp_system < backup.sql
```

## Support & Documentation

- GitHub Issues: https://github.com/amido57/comprehensive-erp-system/issues
- Wiki: https://github.com/amido57/comprehensive-erp-system/wiki
- API Docs: See BACKEND_SETUP.md

## License

MIT License - See LICENSE file
