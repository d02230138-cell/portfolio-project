from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="portfolio_db"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view')
def view():
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    return render_template('view.html', data=data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        address = request.form['address']

        cursor.execute(
            "INSERT INTO contacts (name, email, age, address) VALUES (%s, %s, %s, %s)",
            (name, email, age, address)
        )
        db.commit()

        return render_template('success.html', name=name)

    return render_template('contact.html')  

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)