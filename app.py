from flask import Flask, render_template, request, redirect, session, url_for
import csv
import os

app = Flask(__name__)
app.secret_key = 'hospital_secret_key_123'  # Needed for session management

# Create CSV file if it doesn't exist
if not os.path.exists('complaints.csv'):
    with open('complaints.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Full Name', 'Email', 'Complaint'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    complaint = request.form['complaint']

    with open('complaints.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, email, complaint])

    return render_template('success.html', name=name)


# ✅ Admin Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Simple hardcoded login (can be changed to database later)
        if username == 'admin' and password == '12345':
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    return render_template('login.html')


# ✅ Admin Page (Protected)
@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    complaints = []
    with open('complaints.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            complaints.append(row)
    return render_template('admin.html', complaints=complaints)


# ✅ Logout
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
