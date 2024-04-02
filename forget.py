import tkinter as tk
from tkinter import ttk
import string
import mysql.connector
import random


# Placeholder function to connect to the database (replace with actual implementation)
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Update with your MySQL password
        database="personal_finance"
    )


# Placeholder function to retrieve hashed password for a given username from the database
def get_hashed_password(username):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def generate_reset_token():
    # Generate a reset token (for simplicity, let's just use a random string)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def verify_reset_token(token):
    # Placeholder function to verify the reset token
    # You should implement this according to your application's logic
    return True


def reset_password_with_token(token, new_password):
    # Placeholder function to update password using the reset token
    # You should implement this according to your application's logic
    print("Password updated successfully!")


def forgot_password():
    # Open the forgot password window
    forgot_screen = tk.Toplevel(main_screen)
    forgot_screen.title("Forgot Password")
    forgot_screen.geometry("320x250")

    tk.Label(forgot_screen, text="Forgot Your Password?", font=("Calibri", 14)).pack(pady=10)

    tk.Label(forgot_screen, text="Enter your username to reset password:", font=("Calibri", 12)).pack(pady=5)
    username_entry = ttk.Entry(forgot_screen)
    username_entry.pack(pady=5)

    ttk.Button(forgot_screen, text="Send Reset Token",
               command=lambda: display_reset_token(username_entry.get(), forgot_screen)).pack(pady=5)


def display_reset_token(username, forgot_screen):
    reset_token = generate_reset_token()
    if verify_reset_token(reset_token):
        reset_token_label = tk.Label(forgot_screen, text=f"Reset Token: {reset_token}", font=("Calibri", 12),
                                     fg="green")
        reset_token_label.pack(pady=5)

        # Provide fields to enter new password and the reset token
        tk.Label(forgot_screen, text="Enter Reset Token:", font=("Calibri", 12)).pack(pady=5)
        token_entry = ttk.Entry(forgot_screen)
        token_entry.pack(pady=5)

        tk.Label(forgot_screen, text="Enter New Password:", font=("Calibri", 12)).pack(pady=5)
        new_password_entry = ttk.Entry(forgot_screen, show="*")  # Show asterisks for password entry
        new_password_entry.pack(pady=5)

        ttk.Button(forgot_screen, text="Reset Password",
                   command=lambda: reset_password_with_token(token_entry.get(), new_password_entry.get())).pack(pady=5)
    else:
        tk.Label(forgot_screen, text="Invalid or expired reset token. Please try again.", font=("Calibri", 12),
                 fg="red").pack(pady=5)


# Create the main Tkinter window
main_screen = tk.Tk()
main_screen.geometry("400x300")
main_screen.title("Forgot Password")

# Label to explain the purpose of the button
ttk.Label(main_screen, text="Forgot Your Password? Click here to reset it.", font=("Calibri", 12)).pack(pady=10)

# Button to open forgot password screen
ttk.Button(main_screen, text="Forgot Password", command=forgot_password).pack(pady=10)

main_screen.mainloop()
