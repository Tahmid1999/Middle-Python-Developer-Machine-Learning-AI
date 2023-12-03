import mysql.connector
import re


# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'qwe123',
    'database': 'user_db'
}

def is_valid_email(email):
    # Regular expression for basic email validation
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(email_pattern, email))

def check_and_create_database():
    connection = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )

    cursor = connection.cursor()

    cursor.execute("SHOW DATABASES")
    databases = [database[0] for database in cursor.fetchall()]

    if db_config['database'] not in databases:
        cursor.execute(f"CREATE DATABASE {db_config['database']}")

    cursor.close()
    connection.close()
       
def create_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
    """
    cursor.execute(create_table_query)

    connection.commit()
    cursor.close()
    connection.close()

def add_user(username, email):
    try:        
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if both username and email are provided
        if not username or not email:
            print("Error: Both username and email are required.")
            cursor.close()
            connection.close()
            return
        
        if not is_valid_email(email):
            print("Error: Invalid email.")
            cursor.close()
            connection.close()
            return

        insert_query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        user_data = (username, email)
        cursor.execute(insert_query, user_data)
        
        print(f"User {username} added successfully.")

        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print("Failed to add user to the database: {}".format(error))
    except Exception as exception:
        print("Error: {}".format(exception))

def get_all_users():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        select_all_query = "SELECT * FROM users"
        cursor.execute(select_all_query)
        all_users = cursor.fetchall()

        cursor.close()
        connection.close()

        return all_users
    except mysql.connector.Error as error:
        print("Failed to get users from the database: {}".format(error))
    except Exception as exception:
        print("Error: {}".format(exception))

def get_user(user_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        if not user_id:
            print("Error: User ID is required for the get operation.")
            cursor.close()
            connection.close()
            return

        # Check if the user with the given ID exists
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            print(f"Error: User with ID {user_id} does not exist.")
            cursor.close()
            connection.close()
            return
        
        select_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(select_query, (user_id,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user
    except mysql.connector.Error as error:
        print("Failed to get user from the database: {}".format(error))
    except Exception as exception:
        print("Error: {}".format(exception))

def update_user(user_id, new_username, new_email):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if user ID is provided
        if not user_id:
            print("Error: User ID is required for the update.")
            cursor.close()
            connection.close()
            return

        # Check if the user with the given ID exists
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            print(f"Error: User with ID {user_id} does not exist.")
            cursor.close()
            connection.close()
            return
        
        # Check if the user with the given ID exists
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            print(f"Error: User with ID {user_id} does not exist.")
            cursor.close()
            connection.close()
            return
        
        # Check if at least one field is provided for update
        if not new_username and not new_email:
            print("Error: Nothing to update. Please provide new username or email.")
            cursor.close()
            connection.close()
            return

        # Update username by ID
        if new_username:
            update_query = "UPDATE users SET username = %s WHERE id = %s"
            update_data = (new_username, user_id)
            cursor.execute(update_query, update_data)

        # Update email by ID
        if new_email:
            update_query = "UPDATE users SET email = %s WHERE id = %s"
            update_data = (new_email, user_id)
            cursor.execute(update_query, update_data)

        connection.commit()
        cursor.close()
        connection.close()
        
        print("User updated successfully.")
    except mysql.connector.Error as error:
        print("Failed to update user in the database: {}".format(error))
    except Exception as exception:
        print("Error: {}".format(exception))

def delete_user(user_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if user ID is provided
        if not user_id:
            print("Error: User ID is required for the delete operation.")
            cursor.close()
            connection.close()
            return

        # Check if the user with the given ID exists
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            print(f"Error: User with ID {user_id} does not exist.")
            cursor.close()
            connection.close()
            return
        
        # Delete user by ID
        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (user_id,))

        # Commit the transaction and close the connection
        connection.commit()
        cursor.close()
        connection.close()
        
        print("User deleted successfully.")
    except mysql.connector.Error as error:
        print("Failed to delete user from the database: {}".format(error))
    except Exception as exception:
        print("Error: {}".format(exception))

def main():
    try:
        check_and_create_database()
        create_table()

        while True:
            print("\nOptions:")
            print("1. Create User")
            print("2. Update User")
            print("3. Delete User")
            print("4. Show All Users")
            print("5. Show User by ID")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")

            if choice == "1":
                username = input("Enter username: ")
                email = input("Enter email: ")
            
                add_user(username, email)


            elif choice == "2":
                user_id = input("Enter user ID to update: ")
                print("Enter new details. If you don't want to change a field, leave it blank. Press enter to continue.")
                new_username = input("Enter new username: ")
                new_email = input("Enter new email: ")
                update_user(user_id, new_username, new_email)


            elif choice == "3":
                user_id = input("Enter user ID to delete: ")
                delete_user(user_id)

            elif choice == "4":
                print("\nAll users:")
                all_users = get_all_users()
                for user in all_users:
                    print(user)

            elif choice == "5":
                user_id = input("Enter user ID to show: ")
                user = get_user(user_id)
                print(user)

            elif choice == "6":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as exception:
        print("Error: {}".format(exception))

if __name__ == "__main__":
    main()



