import customtkinter as ctk
from PIL import Image
import pandas as pd
import random
import csv

root = ctk.CTk()
root.geometry("1300x600")
root.title("Password Manager")
ctk.set_appearance_mode("dark")

# determines whether the passwords are decrypted or encrypted
encrypted = True

personal_data = pd.read_csv("files/data.csv")

# normal font
FONT = ctk.CTkFont(family="Arial", size=15)
# font for pop up authentication
AUTH_FONT = ctk.CTkFont(family="Arial", size=17)

CHARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "o", "p", "q", "r", "s", "t", "u", "v",
         "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "O", "P", "Q", "R",
         "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "?", "%",
         "&", "/", "(", ")", "=", "$", "{", "}"]
KEY = ['a', 'L', 'p', 'R', 'O', 'F', 'u', 'I', 'h', 'C', '4', 'c', 'k', '!', 'w', '8', '9', 'M', '/', 'Z', 'z', '=',
       'r', 'K', '0', 'j', '7', '$', 'J', 'U', 'E', 's', '3', 'V', ')', 'i', 'T', 'P', 'A', 'o', '&', 'x', 'v', 'm',
       '}', 'f',
       'e', 'g', 'Y', '%', 't', 'q', '5', 'Q', '{', 'G', '(', 'W', 'd', '2', 'D', 'l', 'B', 'H', 'X', '?', 'S', '6',
       '1', 'y', 'b']


# generates a random password of different letters, numbers and symbols
def generate_password():
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "o", "p", "q", "r", "s", "t", "u", "v",
               "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "O", "P", "Q", "R",
               "S", "T", "U", "V", "W", "X", "Y", "Z"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    symbols = ["!", "?", "%", "&", "/", "(", ")", "=", "$", "{", "}"]

    dict_kind = {0: letters, 1: numbers, 2: symbols}
    password = ""

    password_length = random.randint(11, 15)
    for i in range(password_length):
        kind = random.randint(0, 2)
        index = random.randint(0, len(dict_kind[kind]) - 1)
        password += dict_kind[kind][index]
    password_entry.delete(0, len(password_entry.get()))
    password_entry.insert(0, password)


# toggles the password in the password entry field
def toggle_password():
    if show_password_checkbox.get():
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")


# reloads the dataframe
def reload_csv():
    global personal_data
    personal_data = pd.read_csv("files/data.csv")


# toggles the token in the authentication pop up frame
def toggle_token(checkbox, token_entry):
    if checkbox.get():
        token_entry.configure(show="")
    else:
        token_entry.configure(show="*")


# writes data to the csv
def write_data():
    with open("files/data.csv", mode="a") as file:
        fieldnames = ["application", "username/email", "tags", "password"]
        writer = csv.DictWriter(file, fieldnames, lineterminator="\n")
        application = app_entry.get()
        name = name_entry.get()
        tags = tags_entry.get()
        password = encrypt(password_entry.get())

        if application != "" and name != "" and tags != "" and password != "":
            writer.writerow({"application": application, "username/email": name, "tags": tags, "password": password})


# clears all entry fields
def clear_entry_fields():
    password_entry.delete(0, "end")
    name_entry.delete(0, "end")
    tags_entry.delete(0, "end")
    app_entry.delete(0, "end")


# encrypts a string using the key
def encrypt(password):
    encrypted_password = ""

    for letter in password:
        index = CHARS.index(letter)
        encrypted_password += KEY[index]

    return encrypted_password


# decrypts a string using the key
def decrypt(password):
    decrypted_password = ""

    for letter in password:
        index = KEY.index(letter)
        decrypted_password += CHARS[index]

    return decrypted_password


# clears the displayed data in the table
def clear_boxes():
    app_box.delete("0.0", "end")
    password_box.delete("0.0", "end")
    name_box.delete("0.0", "end")


# reads the csv files and displays the data in the table
def display_data(data, restriction=None):
    app_box.configure(state="normal")
    password_box.configure(state="normal")
    name_box.configure(state="normal")

    clear_boxes()

    rows = data.shape[0]
    cols = data.shape[1]

    for row in range(rows):
        for col in range(cols):
            if restriction is None:
                # if restriction is None, there is nothing in the searchbar and the whole csv will be displayed
                if col == 0:
                    app_box.insert("0.0", personal_data.iloc[row][col] + '\n')
                    app_box.insert("0.0", '\n')
                elif col == 1:
                    name = personal_data.iloc[row][col]
                    name_box.insert("0.0", name.split("/")[0] + '\n')
                    name_box.insert("0.0", '\n')
                elif col == 3:
                    if encrypted:
                        # if encrypted mode is true, the password will be encrypted
                        password_box.insert("0.0", personal_data.iloc[row][col] + '\n')
                        password_box.insert("0.0", '\n')
                    else:
                        # else, the password will be decrypted
                        password_box.insert("0.0", decrypt(personal_data.iloc[row][col]) + '\n')
                        password_box.insert("0.0", '\n')

            else:
                # if there is a restriction, the input of the searchbar will be compared to the different tags of the
                # entries and if there is a match, the data will be displayed in the table
                tags = personal_data.iloc[row][2]
                if restriction.lower() in tags.lower():
                    if col == 0:
                        app_box.insert("0.0", personal_data.iloc[row][col] + '\n')
                        app_box.insert("0.0", '\n')
                    elif col == 1:
                        name = personal_data.iloc[row][col]
                        name_box.insert("0.0", name.split("/")[0] + '\n')
                        name_box.insert("0.0", '\n')
                    elif col == 3:
                        if encrypted:
                            password_box.insert("0.0", personal_data.iloc[row][col] + '\n')
                            password_box.insert("0.0", '\n')
                        else:
                            password_box.insert("0.0", decrypt(personal_data.iloc[row][col]) + '\n')
                            password_box.insert("0.0", '\n')

    app_box.configure(state="disabled")
    password_box.configure(state="disabled")
    name_box.configure(state="disabled")


# writes token to txt file
def create_access_token(token):
    with open("files/token.txt", "w") as file:
        file.write(encrypt(token))


# compares entered token to the actual token and displays the decrypted passwords
def authenticate(token):
    with open("files/token.txt", "r") as file:
        real_token = file.readline()
        if real_token == encrypt(token):
            global encrypted
            encrypted = False
            display_data(personal_data, restriction=search_bar.get())


# opens authentication window based on whether the access token has already been created or not
def create_auth_window():
    with open("files/token.txt", mode="r") as file:
        token = file.readline()
        if len(token) == 0:

            authentication_frame = ctk.CTkToplevel()
            authentication_frame.geometry("400x250")
            authentication_frame.after(20, authentication_frame.lift)

            authentication_label = ctk.CTkLabel(authentication_frame, text="Please create your personal Access Token:",
                                                font=AUTH_FONT)
            authentication_label.pack(pady=10)

            token_label = ctk.CTkLabel(authentication_frame, text="Token", font=AUTH_FONT, text_color="red")
            token_label.pack(pady=(10, 5))

            token_entry = ctk.CTkEntry(authentication_frame, show="*")
            token_entry.pack(pady=(5, 10))

            create_button = ctk.CTkButton(authentication_frame, text="Create Token", font=AUTH_FONT, fg_color="red",
                                          hover_color="#C40000",
                                          command=lambda: [create_access_token(token_entry.get()),
                                                           display_data(personal_data),
                                                           authentication_frame.destroy()])
            create_button.pack(pady=10)

            show_password_checkbox = ctk.CTkCheckBox(authentication_frame, text="Show Token", onvalue=True,
                                                     offvalue=False,
                                                     command=lambda: toggle_token(show_password_checkbox, token_entry))
            show_password_checkbox.pack(pady=10)

        else:
            authentication_frame = ctk.CTkToplevel()
            authentication_frame.geometry("400x250")
            authentication_frame.after(20, authentication_frame.lift)

            authentication_label = ctk.CTkLabel(authentication_frame, text="Please enter your personal Access Token:",
                                                font=AUTH_FONT)
            authentication_label.pack(pady=10)

            token_label = ctk.CTkLabel(authentication_frame, text="Token", font=AUTH_FONT, text_color="red")
            token_label.pack(pady=(10, 5))

            token_entry = ctk.CTkEntry(authentication_frame, show="*")
            token_entry.pack(pady=(5, 10))

            decrypt_button = ctk.CTkButton(authentication_frame, text="Decrypt Passwords", font=AUTH_FONT,
                                           fg_color="red",
                                           hover_color="#C40000",
                                           command=lambda: [authenticate(token_entry.get()),
                                                            authentication_frame.destroy()])
            decrypt_button.pack(pady=10)

            show_password_checkbox = ctk.CTkCheckBox(authentication_frame, text="Show Token", onvalue=True,
                                                     offvalue=False,
                                                     command=lambda: toggle_token(show_password_checkbox, token_entry))
            show_password_checkbox.pack(pady=10)


# handles input in the searchbar
def redo_table(event):
    if event.keysym != "BackSpace":
        restriction = search_bar.get() + event.char
        display_data(personal_data, restriction=restriction)
    else:
        restriction = search_bar.get()[:-1]
        display_data(personal_data, restriction=restriction)


# -------------------------- left side of gui ------------------------------------------------------------

logo_image = ctk.CTkImage(Image.open("./img/lock1.png"), size=(230, 200))
logo_label = ctk.CTkLabel(root, image=logo_image, text="")
logo_label.grid(column=1, row=0)

app_text = ctk.CTkLabel(root, text="Application:", font=FONT)
app_text.grid(column=0, row=1, pady=10)
app_entry = ctk.CTkEntry(root, font=FONT, width=450)
app_entry.grid(column=1, row=1, columnspan=2)

name_text = ctk.CTkLabel(root, text="Username/Email:", font=FONT)
name_text.grid(column=0, row=2, padx=50, pady=10)
name_entry = ctk.CTkEntry(root, font=FONT, width=450)
name_entry.grid(column=1, row=2, columnspan=2)

password_entry = ctk.CTkEntry(root, font=FONT, width=300, show="*")
password_entry.grid(column=1, row=3, )
password_text = ctk.CTkLabel(root, text="Password:", font=FONT)
password_text.grid(column=0, row=3, pady=10)

generate_password_button = ctk.CTkButton(root, text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3, padx=(10, 0))

tags_text = ctk.CTkLabel(root, text="Tags:", font=FONT)
tags_text.grid(column=0, row=4)
tags_entry = ctk.CTkEntry(root, font=FONT, width=450, placeholder_text="tag1,tag2,tag3...",
                          placeholder_text_color="gray")

tags_entry.grid(column=1, row=4, pady=10, columnspan=2)

add_button = ctk.CTkButton(root, text="Add",
                           command=lambda: [write_data(), clear_entry_fields(), reload_csv(),
                                            display_data(personal_data)])
add_button.grid(column=1, row=5, pady=30)

show_password_checkbox = ctk.CTkCheckBox(root, text="Show Password", onvalue=True, offvalue=False,
                                         command=toggle_password)
show_password_checkbox.grid(column=2, row=5, pady=30)

# -------------------------- right side of gui ----------------------------------------------------------------

show_data_button = ctk.CTkButton(root, text="Decrypt Passwords", fg_color="red", hover_color="#C40000",
                                 command=create_auth_window)
show_data_button.place(x=910, y=560)

search_bar = ctk.CTkEntry(root, font=FONT, width=400, placeholder_text="search")
search_bar.place(x=770, y=50)
search_bar.bind("<Key>", redo_table)

data_frame = ctk.CTkScrollableFrame(root, width=520, height=400)
data_frame.place(x=710, y=140)

name_col_text = ctk.CTkLabel(root, text="Username/Email", font=FONT)
name_col_text.place(x=900, y=110)

app_col_text = ctk.CTkLabel(root, text="Application", font=FONT, width=100)
app_col_text.place(x=710, y=110)

password_col_text = ctk.CTkLabel(root, text="Password", font=FONT)
password_col_text.place(x=1070, y=110)

name_box = ctk.CTkTextbox(data_frame, height=900, width=180, text_color="#777777")
name_box.grid(column=1, row=0)

app_box = ctk.CTkTextbox(data_frame, height=900, width=170, text_color="#777777")
app_box.grid(column=0, row=0)

password_box = ctk.CTkTextbox(data_frame, height=900, text_color="red")
password_box.grid(column=2, row=0)

display_data(personal_data)

root.mainloop()
