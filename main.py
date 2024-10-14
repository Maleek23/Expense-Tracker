import logging
from flask import render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app_init import create_app
from database import db
import csv
from io import StringIO
from sqlalchemy import text

app = create_app()

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        
        new_expense = Expense(date=date, amount=amount, category=category, description=description)
        db.session.add(new_expense)
        db.session.commit()
        
        return jsonify({"message": "Expense added successfully"}), 201
    
    expenses = Expense.query.order_by(Expense.date.desc()).limit(10).all()
    return render_template('expenses.html', expenses=expenses)

@app.route('/import-statement', methods=['POST'])
def import_statement():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        for row in csv_reader:
            date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
            amount = float(row['Amount'])
            category = row['Category']
            description = row['Description']
            
            new_expense = Expense(date=date, amount=amount, category=category, description=description)
            db.session.add(new_expense)
        
        db.session.commit()
        return jsonify({"message": "Statement imported successfully"}), 201
@app.route('/download-project')
def download_project():
    import zipfile
    import io
    import os

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py') or file.endswith('.html') or file.endswith('.css') or file.endswith('.js'):
                    file_path = os.path.join(root, file)
                    zf.write(file_path, file_path)

    memory_file.seek(0)
    return send_file(memory_file, download_name='financial_tracker_project.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)