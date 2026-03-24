from flask import Flask, render_template, request
import os
import psycopg2

app = Flask(__name__)


DATABASE_URL = "postgresql://mydb_g1lj_user:zNyAZkga43HqsdfncsjUcRLLfKVZLg64@dpg-d71a9o5actks738rekg0-a/mydb_g1lj"


if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgres://")

print("DB URL:", DATABASE_URL)


conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    age INT,
    address TEXT
);
""")
conn.commit()


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
        conn.commit()  

        return render_template('success.html', name=name)

    return render_template('contact.html')

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)