from flask import Flask, render_template_string, jsonify, request
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Sample data storage (in-memory database)
data_store = {
    'transactions': [
        {'id': 1, 'date': '2025-12-01', 'description': 'Invoice #001', 'amount': 5000, 'type': 'income'},
        {'id': 2, 'date': '2025-12-02', 'description': 'Payment', 'amount': 2000, 'type': 'expense'},
        {'id': 3, 'date': '2025-12-03', 'description': 'Invoice #002', 'amount': 7500, 'type': 'income'},
    ],
    'inventory': [
        {'id': 1, 'product': 'Product A', 'quantity': 100, 'price': 50},
        {'id': 2, 'product': 'Product B', 'quantity': 75, 'price': 120},
        {'id': 3, 'product': 'Product C', 'quantity': 200, 'price': 25},
    ],
    'employees': [
        {'id': 1, 'name': 'Ahmed Hassan', 'position': 'Manager', 'salary': 5000},
        {'id': 2, 'name': 'Fatima Ahmed', 'position': 'Accountant', 'salary': 3500},
        {'id': 3, 'name': 'Mohammed Ali', 'position': 'Sales', 'salary': 3000},
    ],
    'sales': [
        {'id': 1, 'date': '2025-12-01', 'customer': 'Company A', 'amount': 5000, 'items': 5},
        {'id': 2, 'date': '2025-12-02', 'customer': 'Company B', 'amount': 3200, 'items': 8},
        {'id': 3, 'date': '2025-12-03', 'customer': 'Company C', 'amount': 7500, 'items': 12},
    ],
}

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive ERP System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        header h1 { font-size: 28px; margin-bottom: 5px; }
        header p { opacity: 0.9; }
        .container { max-width: 1200px; margin: 20px auto; padding: 0 20px; }
        .status-bar { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: flex; justify-content: space-around; flex-wrap: wrap; gap: 20px; }
        .status-item { text-align: center; }
        .status-label { color: #666; font-size: 14px; margin-bottom: 5px; }
        .status-value { font-size: 24px; font-weight: bold; color: #667eea; }
        .modules { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .module { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: all 0.3s; border-left: 5px solid #667eea; cursor: pointer; }
        .module:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.15); }
        .module h3 { color: #667eea; margin-bottom: 10px; font-size: 20px; }
        .module p { color: #666; font-size: 14px; margin-bottom: 15px; }
        .module button { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 14px; width: 100%; }
        .module button:hover { background: #764ba2; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .stat-card .label { color: #666; font-size: 14px; margin-bottom: 5px; }
        .stat-card .value { font-size: 28px; font-weight: bold; color: #667eea; }
        .data-table { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; }
        th { background: #f8f9fa; padding: 12px; text-align: left; color: #333; border-bottom: 2px solid #667eea; }
        td { padding: 12px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f8f9fa; }
        footer { text-align: center; padding: 20px; color: #666; margin-top: 30px; }
        .section-title { font-size: 20px; font-weight: bold; color: #333; margin: 30px 0 15px; }
    </style>
</head>
<body>
    <header>
        <h1>🚀 Comprehensive ERP System</h1>
        <p>Manage all your business operations in one place</p>
    </header>
    
    <div class="container">
        <div class="status-bar">
            <div class="status-item">
                <div class="status-label">System Status</div>
                <div class="status-value">✓ Online</div>
            </div>
            <div class="status-item">
                <div class="status-label">Version</div>
                <div class="status-value">2.0</div>
            </div>
            <div class="status-item">
                <div class="status-label">Last Updated</div>
                <div class="status-value">{{ timestamp }}</div>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="label">Total Revenue</div>
                <div class="value" id="total-revenue">15,700 ر.س</div>
            </div>
            <div class="stat-card">
                <div class="label">Inventory Items</div>
                <div class="value" id="inventory-count">375</div>
            </div>
            <div class="stat-card">
                <div class="label">Total Employees</div>
                <div class="value" id="employees-count">3</div>
            </div>
            <div class="stat-card">
                <div class="label">Active Sales</div>
                <div class="value" id="sales-count">3</div>
            </div>
        </div>
        
        <div class="section-title">📊 ERP Modules</div>
        <div class="modules">
            <div class="module">
                <h3>📈 Accounting</h3>
                <p>Manage financial transactions and reports</p>
                <button onclick="loadModule('accounting')">Open Accounting</button>
            </div>
            <div class="module">
                <h3>📦 Inventory</h3>
                <p>Track and manage product inventory</p>
                <button onclick="loadModule('inventory')">Open Inventory</button>
            </div>
            <div class="module">
                <h3>👥 HR Management</h3>
                <p>Manage employees and payroll</p>
                <button onclick="loadModule('hr')">Open HR</button>
            </div>
            <div class="module">
                <h3>💼 Sales & CRM</h3>
                <p>Track sales and customer relationships</p>
                <button onclick="loadModule('sales')">Open Sales</button>
            </div>
            <div class="module">
                <h3>📊 Reports</h3>
                <p>View comprehensive business reports</p>
                <button onclick="loadModule('reports')">View Reports</button>
            </div>
            <div class="module">
                <h3>⚙️ Settings</h3>
                <p>Configure system settings</p>
                <button onclick="loadModule('settings')">Go to Settings</button>
            </div>
        </div>
        
        <div class="section-title">📋 Recent Transactions</div>
        <div class="data-table">
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Description</th>
                        <th>Amount</th>
                        <th>Type</th>
                    </tr>
                </thead>
                <tbody id="transactions-table">
                    <!-- Loaded dynamically -->
                </tbody>
            </table>
        </div>
    </div>
    
    <footer>
        <p>Comprehensive ERP System v2.0 | Built with Flask | Deployed on Railway | Bilingual Support</p>
    </footer>
    
    <script>
        function loadModule(module) {
            alert('Loading ' + module + ' module...\\nModule: ' + module.toUpperCase());
            // In a real system, this would navigate to /module/name
            // window.location.href = '/' + module;
        }
        
        function loadData() {
            // Load transactions
            fetch('/api/transactions')
                .then(r => r.json())
                .then(data => {
                    const tbody = document.getElementById('transactions-table');
                    tbody.innerHTML = data.map(t => `
                        <tr>
                            <td>${t.date}</td>
                            <td>${t.description}</td>
                            <td>${t.amount}</td>
                            <td>${t.type}</td>
                        </tr>
                    `).join('');
                });
        }
        
        // Load data on page load
        window.onload = loadData;
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'online',
        'version': '2.0',
        'timestamp': datetime.now().isoformat(),
        'modules': ['Accounting', 'Inventory', 'HR', 'Sales', 'CRM', 'Reports', 'Settings'],
        'system_health': 'healthy'
    })

@app.route('/api/transactions')
def api_transactions():
    return jsonify(data_store['transactions'])

@app.route('/api/inventory')
def api_inventory():
    return jsonify(data_store['inventory'])

@app.route('/api/employees')
def api_employees():
    return jsonify(data_store['employees'])

@app.route('/api/sales')
def api_sales():
    return jsonify(data_store['sales'])

@app.route('/api/accounting')
def api_accounting():
    total_income = sum(t['amount'] for t in data_store['transactions'] if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in data_store['transactions'] if t['type'] == 'expense')
    return jsonify({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'transactions_count': len(data_store['transactions'])
    })

@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    total_revenue = sum(t['amount'] for t in data_store['transactions'] if t['type'] == 'income')
    inventory_count = sum(p['quantity'] for p in data_store['inventory'])
    return jsonify({
        'total_revenue': total_revenue,
        'inventory_items': inventory_count,
        'employees': len(data_store['employees']),
        'sales': len(data_store['sales'])
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
