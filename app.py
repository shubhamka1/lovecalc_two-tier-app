from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def init_db():
    db = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword"
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS love_calculator")
    cursor.execute("USE love_calculator")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name1 VARCHAR(255),
            name2 VARCHAR(255),
            score INT
        )
    """)
    db.commit()
    cursor.close()
    db.close()

# Call the init_db function to ensure the database and table are created
init_db()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="love_calculator"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    name1 = request.form['name1']
    name2 = request.form['name2']
    
    # Dummy love calculation algorithm
    love_score = (len(name1) + len(name2)) % 100
    
    # Insert data into the database
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO results (name1, name2, score) VALUES (%s, %s, %s)", (name1, name2, love_score))
    db.commit()
    cursor.close()
    db.close()
    
    return render_template('result.html', score=love_score, name1=name1, name2=name2)

if __name__ == '__main__':
    app.run(debug=True)
