import tkinter as tk
import random
import pyperclip
import csv
import os

def get_char(char_list, number):
    return [random.choice(char_list) for x in range(number)]

def generate_password():
    try:

        num_char = int(total_char_entry.get())
        num_upper = int(upper_entry.get())
        num_lower = int(lower_entry.get())
        num_digit = int(digit_entry.get())
        num_symbol = int(symbol_entry.get())

        if num_char < num_upper + num_lower + num_digit + num_symbol:
            result_label.config(text="Error: Total characters do not match the sum of the specified requirements.")
            return

        upper_list = [chr(i) for i in range(65, 65 + 26)]
        lower_list = [chr(i) for i in range(97, 97 + 26)]
        digit_list = [str(i) for i in range(0, 10)]
        symbol_list = [chr(i) for i in range(32, 48)] + [chr(i) for i in range(58, 65)] + [chr(i) for i in range(91, 97)] + [chr(i) for i in range(123, 127)]

        upper_char = get_char(upper_list, num_upper)
        lower_char = get_char(lower_list, num_lower)
        digit_char = get_char(digit_list, num_digit)
        symbol_char = get_char(symbol_list, num_symbol)

        all_chars = upper_list + lower_list + digit_list + symbol_list
        remaining_char = get_char(all_chars, num_char - num_upper - num_lower - num_digit - num_symbol)

        password_list = upper_char + lower_char + digit_char + symbol_char + remaining_char
        random.shuffle(password_list)
        password = "".join(password_list)

        result_label.config(text="Generated Password: " + password)
        return password
    except ValueError:
        result_label.config(text="Error: Please enter valid numbers.")

def save_password():
    service = service_entry.get()
    username = username_entry.get()
    password = generate_password()

    if not (service and username and password):
        result_label.config(text="Error: All fields are required!")
        return

    with open("passwords.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([service, username, password])

    result_label.config(text="Password saved successfully!")

def view_saved_passwords():
    if os.path.exists("passwords.csv"):
        with open("passwords.csv", "r") as file:
            reader = csv.reader(file)
            saved_data = "\n".join([f"Service: {row[0]}, Username: {row[1]}, Password: {row[2]}" for row in reader])
            result_label.config(text=saved_data)
    else:
        result_label.config(text="No saved passwords found.")

def clear_all():
    if os.path.exists("passwords.csv"):
        os.remove("passwords.csv")
        result_label.config(text="All saved passwords have been cleared.")
    else:
        result_label.config(text="No passwords to clear.")

def copy_to_clipboard():
    password = generate_password()
    if password:
        pyperclip.copy(password)
        result_label.config(text="Password copied to clipboard!")

root = tk.Tk()
root.title("Terminal-Style Password Generator")
root.configure(bg="black")

root.geometry("600x600")
root.option_add("*Font", "Courier 12")
root.option_add("*Foreground", "lime")
root.option_add("*Background", "black")

tk.Label(root, text="Total Characters: ").grid(row=0, column=0, padx=5, pady=5, sticky="e")
total_char_entry = tk.Entry(root)
total_char_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Uppercase Letters: ").grid(row=1, column=0, padx=5, pady=5, sticky="e")
upper_entry = tk.Entry(root)
upper_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Lowercase Letters: ").grid(row=2, column=0, padx=5, pady=5, sticky="e")
lower_entry = tk.Entry(root)
lower_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Digits: ").grid(row=3, column=0, padx=5, pady=5, sticky="e")
digit_entry = tk.Entry(root)
digit_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Symbols: ").grid(row=4, column=0, padx=5, pady=5, sticky="e")
symbol_entry = tk.Entry(root)
symbol_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Service Name: ").grid(row=5, column=0, padx=5, pady=5, sticky="e")
service_entry = tk.Entry(root)
service_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Username: ").grid(row=6, column=0, padx=5, pady=5, sticky="e")
username_entry = tk.Entry(root)
username_entry.grid(row=6, column=1, padx=5, pady=5)

generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.grid(row=7, column=0, columnspan=2, pady=5)

save_button = tk.Button(root, text="Save Password", command=save_password)
save_button.grid(row=8, column=0, columnspan=2, pady=5)

view_button = tk.Button(root, text="View Saved Passwords", command=view_saved_passwords)
view_button.grid(row=9, column=0, columnspan=2, pady=5)

copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=10, column=0, columnspan=2, pady=5)

clear_button = tk.Button(root, text="Clear All", command=clear_all)
clear_button.grid(row=11, column=0, columnspan=2, pady=5)

result_label = tk.Label(root, text="")
result_label.grid(row=12, column=0, columnspan=2, pady=10)

root.mainloop()