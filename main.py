from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
# Python module for copy and paste clipboard functions
import pyperclip
import json

FONT_NAME = "Courier"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letters_list + symbols_list + numbers_list
    shuffle(password_list)
    password = "".join(password_list)

    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = pass_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if website == "" or password == "":
        messagebox.showwarning(title='Empty field(s)!', message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are your entries:\nEmail: {email}\n"
                                                              f"Password: {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    # Reading old data
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    # Saving updated data
                    json.dump(new_data, file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as file:
                    # Saving updated data
                    json.dump(data, file, indent=4)

            website_entry.delete(0, 'end')
            pass_entry.delete(0, 'end')


# ---------------------------- FIND PASSWORD -------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as file:
            # Reading old data
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showwarning(title='Error', message="No Data File Found.")

    else:
        if website in data.keys():
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website,message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title=website, message=f"You don't have your info saved for this website.")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", font=(FONT_NAME, 14))
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", font=(FONT_NAME, 14))
email_label.grid(row=2, column=0)

pass_label = Label(text="Password:", font=(FONT_NAME, 14))
pass_label.grid(row=3, column=0)

website_entry = Entry(width=32)
website_entry.grid(row=1, column=1, sticky=W)
# set the cursor on website_entry
website_entry.focus()

email_entry = Entry(width=51)
email_entry.grid(row=2, column=1, columnspan=2, sticky=W)
# prepopulated email_entry
email_entry.insert(0, "fakemail@gmail.com")

pass_entry = Entry(width=32, text="")
pass_entry.grid(row=3, column=1, sticky=W)

generate_pass_button = Button(text="Generate Password", width=14, command=generate_password)
generate_pass_button.grid(row=3, column=2)

add_button = Button(text="Add", width=43, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky=W)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2, sticky=W)

window.mainloop()
