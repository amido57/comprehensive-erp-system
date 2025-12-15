from flask import Flask, render_template_string, jsonify
import os
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive ERP System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { background: white; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); padding: 40px; max-width: 800px; width: 90%; }
        h1 { color: #667eea; margin-bottom: 20px; text-align: center; }
        .info { background: #f0f4ff; border-left: 4px solid #667eea; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .modules { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 30px 0; }
        .module { background: #f5f5f5; padding: 15px; border-radius: 5px; text-align: center; cursor: pointer; transition: all 0.3s; border: 2px solid #ddd; }
        .module:hover { background: #667eea; color: white; border-color: #667eea; }
        .footer { text-align: center; margin-top: 30px; color: #999; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Comprehensive ERP System</h1>
        <div class="info">
            <strong>Status:</strong> <span style="color: #28a745;">✓ Online & Running</span><br>
            <strong>Version:</strong> 1.0.0 (Demo)<br>
            <strong>Time:</strong> {{ timestamp }}
        </div>
        <div style="background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #667eea; margin-bottom: 10px;">Module Features</h3>
            <ul style="list-style: none;">
                <li>✓ Accounting & Finance Management</li>
                <li>✓ Inventory Management</li>
                <li>✓ Human Resources</li>
                <li>✓ Sales & CRM</li>
                <li>✓ Purchase Management</li>
                <li>✓ Reports & Analytics</li>
                <li>✓ Bilingual Support (Arabic & English)</li>
            </ul>
        </div>
        <div class="modules">
            <div class="module">📊 Accounting</div>
            <div class="module">📦 Inventory</div>
            <div class="module">👥 HR</div>
            <div class="module">💼 Sales</div>
            <div class="module">🛒 CRM</div>
            <div class="module">📈 Reports</div>
        </div>
        <div class="footer">
            <p>Built with Flask | Deployed on Railway | Bilingual ERP Solution</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'online',
        'version': '1.0.0',
        'modules': [
            'Accounting',
            'Inventory',
            'HR',
            'Sales',
            'CRM',
            'Reports'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
