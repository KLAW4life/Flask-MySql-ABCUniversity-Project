from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Som3$ec5etK*y'  # Set a secret key for session management

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kl@w$li3e!',
    'database': 'UniversityABC',
    'auth_plugin': 'mysql_native_password'
}

@app.route('/')
def index():
    if 'user_id' in session:
        # return render_template('home.html')
        other_students = get_other_students(session['user_id'])  
        return render_template('home.html', other_students=other_students)
    else:
        return redirect(url_for('login'))
    
def get_other_students(user_id):
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        sql = "SELECT FirstName, LastName, Type FROM User WHERE Type = 'Student' AND UserID != %s"
        mycursor.execute(sql, (user_id,))
        other_students = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return other_students
    except mysql.connector.Error as e:
        print("Error fetching other students:", e)
        return []


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        if authenticate_user(user_id, password):
            session['user_id'] = user_id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid user ID or password')
    else:
        return render_template('login.html')

def authenticate_user(user_id, password):
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        sql = "SELECT * FROM User WHERE UserID = %s AND Password = %s"
        values = (user_id, password)
        mycursor.execute(sql, values)
        user = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        return user is not None
    except mysql.connector.Error as e:
        print("Error authenticating user:", e)
        return False
    
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_num = request.form['phone_num']
        birth_date = request.form['birth_date']
        password = request.form['password']
        major = request.form['major']
        user_type = request.form['type']

        # Call function to register user
        if register_user(password, first_name, last_name, email, phone_num, birth_date, major, user_type):
            return redirect(url_for('login')) 
        else:
            return render_template('register.html', error='Error registering user')
    else:
        # Fetch available majors from the database
        majors = get_available_majors()

        return render_template('register.html', majors=majors)
    
@app.route('/confirm_delete')
def confirm_delete():
    return render_template('confirm_delete.html')

# @app.route('/delete_account', methods=['POST'])
# def delete_account():
#     session.pop('user_id', None) 
#     return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' in session:
        user_id = session['user_id']
        try:
            mydb = mysql.connector.connect(**db_config)
            mycursor = mydb.cursor()
            sql_delete_user = "DELETE FROM User WHERE UserID = %s"
            mycursor.execute(sql_delete_user, (user_id,))
            mydb.commit()
            mycursor.close()
            mydb.close()
            session.pop('user_id')  # Remove user from session after deleting the account
            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            print("Error deleting user:", e)
            return render_template('error.html', message='Error deleting user')
    else:
        return redirect(url_for('login'))

def get_available_majors():
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT MajorName FROM Major")
        majors = [row[0] for row in mycursor.fetchall()]
        mycursor.close()
        mydb.close()
        return majors
    except mysql.connector.Error as e:
        print("Error fetching majors:", e)
        return []

def register_user(password, first_name, last_name, email, phone_num, birth_date, major, user_type):
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        sql = "INSERT INTO User (Password, FirstName, LastName, Email, PhoneNum, BirthDate, Major, Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (password, first_name, last_name, email, phone_num, birth_date, major, user_type)
        mycursor.execute(sql, values)
        mydb.commit()
        mycursor.close()
        mydb.close()
        return True
    except mysql.connector.Error as e:
        print("Error registering user:", e)
        return False
    
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        user_id = session.get('user_id')  
        if change_user_password(user_id, old_password, new_password):
            return redirect(url_for('login'))
        else:
            return render_template('change_password.html', error='Failed to change password. Please try again.')
    else:
        return render_template('change_password.html')

def change_user_password(user_id, old_password, new_password):
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Check if old password matches
        sql_check_password = "SELECT UserID FROM User WHERE UserID = %s AND Password = %s"
        mycursor.execute(sql_check_password, (user_id, old_password))

        if not mycursor.fetchone():
            return False  # Old password does not match
        
        sql_update_password = "UPDATE User SET Password = %s WHERE UserID = %s"
        mycursor.execute(sql_update_password, (new_password, user_id))
        mydb.commit()
        mycursor.close()
        mydb.close()
        return True
    except mysql.connector.Error as e:
        print("Error changing password:", e)
        return False



if __name__ == '__main__':
    app.run(debug=True)
