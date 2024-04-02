# login.py
import tkinter as tk
from tkinter import StringVar, Entry, Label, Toplevel, Button, END
import mysql.connector
import bcrypt
from tkinter import messagebox
import subprocess
from tkinter import ttk
from PIL import Image, ImageTk

# Establish a connection to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",  # Update with your MySQL host
    user="root",
    password="",  # Update with your MySQL password
    database="personal_finance"  # Update with your database name
)
cursor = db_connection.cursor()

def create_users_table():
    # Create the 'users' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    db_connection.commit()

def main_acc():
    create_users_table()  # Ensure 'users' table is created
    global main_screen
    main_screen = tk.Tk()
    main_screen.title("Main")

    # Open the image and resize it
    logo_image = Image.open("img.png")
    logo_image = logo_image.resize((80, 60), Image.BICUBIC)  # Use BICUBIC as an alternative

    # Convert the Image object to a PhotoImage object
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Create labels and buttons
    logo_label = tk.Label(main_screen, image=logo_photo)
    logo_label.pack(pady=5)

    tk.Label(main_screen, text="Login or Register", bg="#b1abf1", fg="white",
             width="300", height="2", font=("Calibri", 13)).pack(padx=20, pady=10)

    tk.Button(main_screen, text="LOGIN", height="2", width="15", fg="gray", command=login).pack(pady=5)
    tk.Button(main_screen, text="REGISTER", height="2", width="15", fg="black", command=register).pack(pady=5)

    # Update the main window size based on the content
    content_width = max(logo_label.winfo_reqwidth(), 400)  # Increased minimum width to 400
    content_height = sum(
        widget.winfo_reqheight() for widget in main_screen.winfo_children()) + 50  # Increased padding to 50

    main_screen.geometry(f"{content_width}x{content_height}")

    main_screen.protocol("WM_DELETE_WINDOW", on_closing)
    main_screen.mainloop()
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("320x350")

    global username_entry
    global password_entry

    username_entry = StringVar()
    password_entry = StringVar()

    tk.Label(register_screen, text="Enter Details Below to Register!", bg="#D8BFD8", fg="black",
             width="300", height="2", font=("Calibri", 13)).pack(padx=20, pady=23)
    tk.Label(register_screen, text="").pack()

    unLabel = tk.Label(register_screen, text="Username", fg="black", bg="#D8BFD8")
    unLabel.pack(pady=5)

    username_entry = Entry(register_screen, textvariable=username_entry)
    username_entry.pack()

    passLabel = tk.Label(register_screen, text="Password", fg="black", bg="#D8BFD8")
    passLabel.pack(pady=5)

    password_entry = Entry(register_screen, textvariable=password_entry, show='*')
    password_entry.pack()

    tk.Label(register_screen, text="").pack()
    tk.Button(register_screen, text="Register", width=10, height=1, fg="black", command=register_user).pack(pady=5)
    tk.Button(register_screen, text= 'Reset', width= 10, height=1, fg= 'red', command= reset).pack(pady=5)


def reset():
    # Clear the contents of the Entry widgets by deleting the text
    username_entry.delete(0, 'end')
    password_entry.delete(0, 'end')


def login():
    global login_screen
    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry

    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("320x390")
    tk.Label(login_screen, text="Enter Details Below to Login!", bg="#c0ecc0", fg="black",
             width="300", height="2", font=("Calibri", 13)).pack(padx=20, pady=23)
    tk.Label(login_screen, text="").pack()

    username_verify = StringVar()
    password_verify = StringVar()

    tk.Label(login_screen, text="Username", fg="black", bg="#c0ecc0").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack(pady=5)

    tk.Label(login_screen, text="").pack()
    tk.Label(login_screen, text="Password", fg="black", bg="#c0ecc0").pack(pady=5)

    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()

    tk.Label(login_screen, text="").pack()
    tk.Button(login_screen, text="Login", width=10, fg="black", height=1, command=login_verify).pack( pady=5)
    tk.Button(login_screen, text='Reset', width=10, fg='Red', height=1 ,command= reset_log).pack(pady=5)
    tk.Button(login_screen, text='Forget Pasword', width=15, height=1, fg='red', command=forget).pack(pady=5)

def forget():
    subprocess.Popen(["python", "forget.py"])
def reset_log():
    # Clear the contents of the Entry widgets by deleting the text
    username_login_entry.delete(0, 'end')
    password_login_entry.delete(0, 'end')

def register_user():
    global username_entry
    global password_entry

    username_info = username_entry.get()
    password_info = password_entry.get()

    # Check if both username and password are not empty
    if not username_info or not password_info:
        messagebox.showerror("Error", "Both username and password are required!")
        return

    # Hash the password before storing it (use your preferred hashing method)
    hashed_password = bcrypt.hashpw(password_info.encode('utf-8'), bcrypt.gensalt())

    # Insert new user into the 'users' table
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username_info, hashed_password))
    db_connection.commit()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    messagebox.showinfo("Registration Success", "Registration is successful!")

    # Open the landing page
    open_landing_page()

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    # Retrieve user from 'users' table
    cursor.execute("SELECT * FROM users WHERE username = %s", (username1,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password1.encode('utf-8'), user[2].encode('utf-8')):
        login_sucess()
    else:
        password_not_recognised()

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    tk.Label(login_success_screen, text="Login Success").pack()
    tk.Button(login_success_screen, text="OK", command=delete_login_success).pack()
    open_landing_page()

def open_landing_page():
    # This function is called after successful login
    main_screen.destroy()  # Close the login window
    subprocess.Popen(['python', 'practice.py'])  # Replace 'python' with 'python3' if needed

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("ERROR")
    password_not_recog_screen.geometry("150x100")
    tk.Label(password_not_recog_screen, text="Invalid Password").pack()
    tk.Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("ERROR")
    user_not_found_screen.geometry("150x100")
    tk.Label(user_not_found_screen, fg="red", text="User Not Found!").pack(pady=20)
    tk.Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

def delete_login_success():
    login_success_screen.destroy()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()

def delete_user_not_found_screen():
    user_not_found_screen.destroy()

def on_closing():
    db_connection.close()
    main_screen.destroy()

main_acc()
