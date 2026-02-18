from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import sqlite3
import uuid
from datetime import datetime
from config import Config
from utils.qrcode_generator import generate_qr
from utils.pdf_generator import generate_pdf
from io import BytesIO

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS registrations (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        phone TEXT,
                        dob TEXT,
                        gender TEXT,
                        occupation TEXT,
                        city TEXT,
                        date TEXT
                    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        gender = request.form['gender']
        occupation = request.form['occupation']
        city = request.form['city']

        if not phone.startswith('2567') or len(phone)!=12:
            flash("Phone must be 2567XXXXXXXX")
            return redirect(url_for('register'))

        reg_id = str(uuid.uuid4())
        conn = get_db_connection()
        conn.execute('INSERT INTO registrations (id,name,email,phone,dob,gender,occupation,city,date) VALUES (?,?,?,?,?,?,?,?,?)',
                     (reg_id,name,email,phone,dob,gender,occupation,city,datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

        flash("Registration completed successfully!")
        return redirect(url_for('payment_status', reg_id=reg_id))

    return render_template('register.html')

@app.route('/payment_status/<reg_id>')
def payment_status(reg_id):
    conn = get_db_connection()
    reg = conn.execute('SELECT * FROM registrations WHERE id=?',(reg_id,)).fetchone()
    conn.close()
    if not reg:
        return "Registration not found",404

    qr_code = generate_qr(reg['id'])
    return render_template('payment_status.html', status='COMPLETED', registration=reg, qr_code=qr_code)

@app.route('/receipt/<reg_id>')
def download_receipt(reg_id):
    conn = get_db_connection()
    reg = conn.execute('SELECT * FROM registrations WHERE id=?',(reg_id,)).fetchone()
    conn.close()
    if not reg:
        return "Registration not found",404
    qr_code = generate_qr(reg['id'])
    pdf_file = generate_pdf(dict(reg), qr_code)
    return send_file(pdf_file, download_name=f"receipt_{reg['id']}.pdf", as_attachment=True)

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if username=='admin' and password=='admin123':
            session['admin']=True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials")
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    regs = conn.execute('SELECT * FROM registrations').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', registrations=regs)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin',None)
    return redirect(url_for('admin_login'))

@app.route('/admin/delete/<reg_id>')
def admin_delete(reg_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM registrations WHERE id=?',(reg_id,))
    conn.commit()
    conn.close()
    flash("Registration deleted")
    return redirect(url_for('admin_dashboard'))

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
