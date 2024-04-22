import mysql.connector


def login(user_id, password):
  try:
    mydb = mysql.connector.connect(
      host='localhost',
      user='root',
      password='Kl@w$li3e!',
      database='UniversityABC',
      auth_plugin='mysql_native_password'
    )
    
    mycursor = mydb.cursor()
    sql = "SELECT * FROM User WHERE UserID = %s AND Password = %s"
    values = (user_id, password)
    mycursor.execute(sql, values)
    user = mycursor.fetchone()
    
    if user is not None:  # Check if user exists
      print("Login successful!")
    else:
      print("Invalid userid or password.")
              
    mycursor.close()
    mydb.close()
  except mysql.connector.Error as e:
    print("Error connecting to MySQL database:", e)
    


def register_user(password, first_name, last_name, email, phone_num, birth_date, major, type):
  try:
    mydb = mysql.connector.connect(
      host='localhost',
      user='root',
      password='Kl@w$li3e!',
      database='UniversityABC',
      auth_plugin='mysql_native_password'
    )
    
    mycursor = mydb.cursor()
    sql = "INSERT INTO User (Password, FirstName, LastName, Email, PhoneNum, BirthDate, Major, Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (password, first_name, last_name, email, phone_num, birth_date, major, type)
    mycursor.execute(sql, values)
    mydb.commit()
    
    print("User registered successfully!")
    
    mycursor.close()
    mydb.close()
  except mysql.connector.Error as e:
    print("Error registering user:", e)


def change_password(user_id, new_password):
  try:
    mydb = mysql.connector.connect(
      host='localhost',
      user='root',
      password='Kl@w$li3e!',
      database='UniversityABC',
      auth_plugin='mysql_native_password'
    )
    
    mycursor = mydb.cursor()
    sql = "UPDATE User SET Password = %s WHERE UserID = %s"
    values = (new_password, user_id)
    mycursor.execute(sql, values)
    mydb.commit()
    
    print("Password changed successfully!")
    
    mycursor.close()
    mydb.close()
  except mysql.connector.Error as e:
    print("Error changing password:", e)


def delete_user(user_id):
  try:
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Kl@w$li3e!',
        database='UniversityABC',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()
    
    sql_delete_user = "DELETE FROM User WHERE UserID = %s"
    mycursor.execute(sql_delete_user, (user_id,))
    
    if mycursor.rowcount > 0:
      print("User deleted successfully!")
    else:
      print("User not found.")

    mydb.commit()

    mycursor.close()
    mydb.close()
  except mysql.connector.Error as e:
    print("Error deleting user:", e)

# Test functions
def main():
  user_id = input("Enter your userid: ")
  password = input("Enter your password: ")
  login(user_id, password)

def register():
  first_name = input("Enter your first name: ")
  last_name = input("Enter your last name: ")
  email = input("Enter your email: ")
  phone_num = input("Enter your phone number: ")
  birth_date = input("Enter your birth date (YYYY-MM-DD): ")
  password = input("Enter your password: ")
  major = input("Enter your major: ")
  type = input("Enter 'Student' or 'Professor': ")
  register_user(password, first_name, last_name, email, phone_num, birth_date, major, type)

def password_reset():
  user_id = input("Enter user ID: ")
  new_password = input("Enter new password: ")
  change_password(user_id, new_password)

def remove_user():
  user_id = input("Enter your userid: ")
  delete_user(user_id)

if __name__ == "__main__":
  main()
  # register()
  # password_reset()
  # remove_user()

