from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///erp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

db = SQLAlchemy(app)

# ============= DATABASE MODELS =============

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='viewer')  # admin, accountant, sales, store_manager, hr, viewer
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(100))
    unit_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    movement_type = db.Column(db.String(20))  # in, out, transfer
    quantity = db.Column(db.Float, nullable=False)
    reference_id = db.Column(db.String(50))  # PO, SO, etc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product')
    warehouse = db.relationship('Warehouse')

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(50), unique=True, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, received, invoiced
    total_amount = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    supplier = db.relationship('Supplier')
    creator = db.relationship('User')

class PurchaseOrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float)
    po = db.relationship('PurchaseOrder')
    product = db.relationship('Product')

class SalesOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    so_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(120))
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, invoiced, paid
    total_amount = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User')

class SalesOrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.Integer, db.ForeignKey('sales_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float)
    so = db.relationship('SalesOrder')
    product = db.relationship('Product')

class ChartOfAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(20))  # asset, liability, equity, revenue, expense
    balance = db.Column(db.Float, default=0)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))
    reference_type = db.Column(db.String(20))  # PO, SO, manual
    reference_id = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User')

class JournalEntryLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    je_id = db.Column(db.Integer, db.ForeignKey('journal_entry.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('chart_of_account.id'), nullable=False)
    debit = db.Column(db.Float, default=0)
    credit = db.Column(db.Float, default=0)
    je = db.relationship('JournalEntry')
    account = db.relationship('ChartOfAccount')

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(255))
    module = db.Column(db.String(50))
    record_id = db.Column(db.String(50))
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User')

# ============= AUTHENTICATION =============

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            user = User.query.get(session['user_id'])
            if not user or user.role != role:
                return jsonify({'error': 'Unauthorized'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============= ROUTES =============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401
    
    return '''<form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    po_count = PurchaseOrder.query.count()
    so_count = SalesOrder.query.count()
    products = Product.query.count()
    
    html = f'''<!DOCTYPE html>
    <html>
    <head>
        <title>ERP Dashboard</title>
        <style>
            body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
            .header {{ background: #667eea; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            .logout {{ float: right; }}
            .cards {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }}
            .card {{ background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .card h3 {{ color: #667eea; margin: 0; }}
            .card .value {{ font-size: 28px; font-weight: bold; color: #333; }}
            .nav {{ background: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .nav a {{ margin-right: 15px; text-decoration: none; color: #667eea; }}
            .nav a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 ERP System v3.0</h1>
            <p>Welcome, {session['username']} ({session['role']})</p>
            <a href="/logout" class="logout" style="color: white; text-decoration: none;">Logout</a>
        </div>
        
        <div class="nav">
            <a href="/purchases">📦 Purchases</a>
            <a href="/sales">🛒 Sales</a>
            <a href="/inventory">📊 Inventory</a>
            <a href="/accounting">💰 Accounting</a>
            <a href="/reports">📈 Reports</a>
            <a href="/api/status">🔗 API</a>
        </div>
        
        <div class="cards">
            <div class="card">
                <h3>Purchase Orders</h3>
                <div class="value">{po_count}</div>
            </div>
            <div class="card">
                <h3>Sales Orders</h3>
                <div class="value">{so_count}</div>
            </div>
            <div class="card">
                <h3>Products</h3>
                <div class="value">{products}</div>
            </div>
            <div class="card">
                <h3>Version</h3>
                <div class="value">3.0</div>
            </div>
        </div>
    </body>
    </html>'''
    return html

@app.route('/api/status')
def api_status():
    return jsonify({{'status': 'online', 'version': '3.0', 'timestamp': datetime.utcnow().isoformat()}})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
