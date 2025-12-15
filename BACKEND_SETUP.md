# ERP System - Backend Complete Setup Guide

## Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/amido57/comprehensive-erp-system.git
cd comprehensive-erp-system/backend

# 2. Install dependencies
composer install

# 3. Create environment file
cp .env.example .env

# 4. Generate app key
php artisan key:generate

# 5. Setup database
php artisan migrate
php artisan db:seed

# 6. Install Laravel Passport (for API)
php artisan passport:install

# 7. Create storage symlink
php artisan storage:link

# 8. Start the server
php artisan serve
```

## Docker Setup

```bash
cd comprehensive-erp-system
docker-compose up -d
```

## .env Configuration

```
APP_NAME="ERP System"
APP_ENV=local
APP_KEY=base64:YOUR_KEY_HERE
APP_DEBUG=true
APP_URL=http://localhost:8000
APP_LOCALE=ar
APP_FALLBACK_LOCALE=en

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=erp_system
DB_USERNAME=erp_user
DB_PASSWORD=erp_password

CACHE_DRIVER=redis
QUEUE_CONNECTION=redis
SESSION_DRIVER=redis

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

JWT_SECRET=your_jwt_secret_here
JWT_ALGORITHM=HS256
```

## API Routes

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/profile` - Get authenticated user

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create product
- `GET /api/products/{id}` - Get product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Inventory
- `GET /api/inventory` - List inventory
- `POST /api/inventory/adjust` - Adjust stock
- `GET /api/inventory/movements` - Get movements

### Invoices
- `GET /api/invoices` - List invoices
- `POST /api/invoices` - Create invoice
- `GET /api/invoices/{id}` - Get invoice
- `PUT /api/invoices/{id}` - Update invoice
- `DELETE /api/invoices/{id}` - Delete invoice
- `POST /api/invoices/{id}/pdf` - Export to PDF

### Customers/Suppliers
- `GET /api/contacts?type=customer` - List customers
- `GET /api/contacts?type=supplier` - List suppliers
- `POST /api/contacts` - Create contact
- `GET /api/contacts/{id}` - Get contact details
- `PUT /api/contacts/{id}` - Update contact
- `DELETE /api/contacts/{id}` - Delete contact

### Reports
- `GET /api/reports/dashboard` - Dashboard data
- `GET /api/reports/sales` - Sales report
- `GET /api/reports/inventory` - Inventory report
- `GET /api/reports/profit-loss` - Profit/Loss report
- `GET /api/reports/accounting` - Accounting report

### Accounting
- `GET /api/accounting/chart-of-accounts` - Get chart
- `GET /api/accounting/journal-entries` - List entries
- `POST /api/accounting/journal-entries` - Create entry
- `GET /api/accounting/trial-balance` - Trial balance

### HR
- `GET /api/employees` - List employees
- `POST /api/employees` - Create employee
- `GET /api/employees/{id}` - Get employee
- `PUT /api/employees/{id}` - Update employee
- `POST /api/payroll/process` - Process payroll

## Database Tables

All tables are created automatically by migrations. Key tables:
- users
- companies
- contacts (customers/suppliers)
- products
- inventory
- inventory_movements
- invoices
- invoice_items
- payments
- chart_of_accounts
- journal_entries
- employees
- payroll_records
- attendance_records

## Testing

```bash
# Run tests
php artisan test

# Run specific test
php artisan test tests/Unit/ProductTest.php

# Generate test coverage
php artisan test --coverage
```

## Production Deployment

```bash
# Set production environment
export APP_ENV=production

# Run migrations on production
php artisan migrate --force

# Clear cache
php artisan cache:clear
php artisan config:cache
php artisan route:cache

# Optimize
php artisan optimize

# Install SSL
php artisan tinker
# Then: \App\Models\User::where('role', 'admin')->first()->forceFill(['password' => Hash::make('newpassword')])->save();
```

## Key Features

✅ RESTful API
✅ JWT Authentication
✅ Role-Based Access Control
✅ Multi-language Support (AR/EN)
✅ Real-time Notifications
✅ Comprehensive Logging
✅ Error Handling
✅ Request Validation
✅ API Rate Limiting
✅ Database Transactions

## Support

For issues: https://github.com/amido57/comprehensive-erp-system/issues
