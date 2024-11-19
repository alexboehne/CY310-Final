import hashlib # for storing hashed passwords
import mysql.connector
from mysql.connector import cursor

def customer_portal(db, current_cursor, user_data, user_list):
    # Print balance and options menu
    print(f'''
                |------------------|------------------|
                | Current balance:         ${'{0:.2f}'.format(user_data[3])}     |
                |------------------|------------------|
                ''')
    print('''   Options (enter number):
                1: Make deposit
                2: Make withdrawl
                3: Transfer funds
                4: Exit
                ''')
    selection = int(input("Choose an action: "))
    match selection:
        case 1:  # adds deposit to current balance and updates db
            deposit = float(input("Enter your deposit amount: "))
            new_balance = float(user_data[3]) + deposit
            current_cursor.execute(f'UPDATE user_db SET balance = {new_balance} WHERE uid = {user_data[0]}')
            db.commit()
            print("Transaction successful!\n------------------------------------")
        case 2:  # withdraws funds from balance and updates db
            withdrawl = float(input("Enter your withdrawl amount: "))
            new_balance = float(user_data[3]) - withdrawl
            current_cursor.execute(f'UPDATE user_db SET balance = {new_balance} WHERE uid = {user_data[0]}')
            db.commit()
            print("Transaction successful!\n------------------------------------")
        case 3:  # transfers funds from current user to selected user
            transfer_user = input("Enter the user to transfer funds to: ")
            for transfer_row in user_list:
                if transfer_row[1] == transfer_user:
                    transfer_funds = float(input("Enter amount of funds to transfer: "))
                    new_balance = float(user_data[3]) - transfer_funds
                    new_receiving_balance = float(transfer_row[3]) + transfer_funds
                    current_cursor.execute(f'UPDATE user_db SET balance = {new_balance} WHERE uid = {user_data[0]}')
                    db.commit()
                    current_cursor.execute(f'UPDATE user_db SET balance = {new_receiving_balance} WHERE uid = {transfer_row[0]}')
                    db.commit()
                    print("Transaction successful!\n------------------------------------")
        case 4:
            exit(0)

def main():
    try:  # attempts to access db
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="notcashapp"
        )
    except mysql.connector.Error as err: # if login fails
            print("Error connecting to SQL database; terminating program")
            exit(5)

    db_cursor = mydb.cursor() # creates cursor to interact with db

    uinput = input("Enter your username: ") # gets username
    pinput = input("Enter your password: ") # gets password

    newpass = hashlib.md5(pinput.encode()).hexdigest() # hashes user-inputted password

    # Code below will check user's uname/pass, update the local vars to reflect the db, and run the portal
    # Loop will stop when user chooses to exit
    while True:
        db_cursor.execute('SELECT * FROM user_db')
        sql_user_list = db_cursor.fetchall()
        for row in sql_user_list:
            if row[1] == uinput and row[2] == newpass: # if an entry has matching username and password
                user_info = row # turns current user details into list
                customer_portal(mydb, db_cursor, user_info, sql_user_list) # Opens customer portal


if __name__ == "__main__":
    main()