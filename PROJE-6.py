#PROJECT - 6
import customtkinter
import tkinter as tk
import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox

#////////////////////////////////////////////////////////////////////////////////////////////#

r3 = customtkinter.CTk()
r3.title("RECIPE APP")

r2 = customtkinter.CTk()
r2.title("LOGIN")

r1 = customtkinter.CTk()
r1.title("REGISTER")

#////////////////////////////////////////////////////////////////////////////////////////////#

conn = sqlite3.connect("data6.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL,
        password TEXT NOT NULL)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        name TEXT NOT NULL,
        rating INTEGER)''')
                    

#////////////////////////////////////////////////////////////////////////////////////////////#

def register_to_login_page():
    r1.destroy()
    frame2 = customtkinter.CTkFrame(master=r2,
                                    width=350,
                                    height=350)
    frame2.pack(padx=20,pady=20)

    global username_entry_login
    global password_entry_login

    username_entry_login = customtkinter.CTkEntry(master=frame2,
                                                placeholder_text="Username",
                                                width=150,
                                                height=40)
    username_entry_login.place(relx=0.5, rely=0.2, anchor = tk.CENTER)

    password_entry_login = customtkinter.CTkEntry(master=frame2,
                                     placeholder_text="Password",
                                     width=150,
                                     height=40,
                                     show = "*")
    password_entry_login.place(relx=0.5, rely=0.35, anchor = tk.CENTER)

    verification_button = customtkinter.CTkButton(master=frame2,
                                          text="Verify and Continue!",
                                          command=loginaccount)
    verification_button.place(relx=0.5, rely=0.5, anchor = tk.CENTER)
    r2.mainloop()

def signup():
    username = username_entry_register.get()
    password = password_entry_register.get()
    if ((username != "") and (password != "")):
        cursor.execute("SELECT username FROM users WHERE username=?", [username])
        if(cursor.fetchone() is not None):
            messagebox.showerror("Error","Username already exists!")
        else:
            encodedpassword = password.encode("utf-8")
            hashedpassword = bcrypt.hashpw(encodedpassword, bcrypt.gensalt())
            print(hashedpassword)
            cursor.execute("INSERT into users VALUES(?, ?)", [username, hashedpassword])
            conn.commit()
            messagebox.showinfo("Sucsess!","Account has been created")
            register_to_login_page_button = customtkinter.CTkButton(master=r1,
                                                                    text="Go to Login Page",
                                                                    command=login,)
            register_to_login_page_button.place(relx=0.5, rely=0.6, anchor = tk.CENTER)
    else:
        messagebox.showerror("Error","Enter all data.")

def loginaccount():
    username = username_entry_login.get()
    password = password_entry_login.get()
    if ((username != "") and (password != "")):
        cursor.execute("SELECT password FROM users WHERE username=?", [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode("utf-8"), result[0]):
                messagebox.showinfo("Success", f"Logged in successfully, Welcome {username}")
                r2.destroy()
                
                #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
                # Create a frame for the recipe app
                recipe_app_frame = customtkinter.CTkFrame(master=r3,
                                                          width=100,
                                                          height=100)
                recipe_app_frame.pack(pady=20, padx=20, fill="both", expand=True, side="left")

                                # Create a listbox to display the recipes
                recipe_app_listbox = tk.Listbox(master=recipe_app_frame, height=30, width=50, bg=r3.cget('bg'), fg='white', font=("Arial", 16))
                recipe_app_listbox.grid(row=1, column=0, rowspan=5, padx=10)

                                # Create a label and entry for the recipe name
                recipe_app_name_label = customtkinter.CTkLabel(master=recipe_app_frame, text="Recipe Name:")
                recipe_app_name_label.grid(row=1, column=1, pady=10, padx=10, sticky="w")
                recipe_name_entry = customtkinter.CTkEntry(master=recipe_app_frame, placeholder_text="Enter Recipe Name")
                recipe_name_entry.grid(row=1, column=2, columnspan=2, pady=10, padx=10, sticky="ew")

                                # Create a label and entry for the ingredient name
                recipe_app_link_label = customtkinter.CTkLabel(master=recipe_app_frame, text="Ingredient Name:")
                recipe_app_link_label.grid(row=2, column=1, pady=10, padx=10, sticky="w")
                ingredient_name_entry = customtkinter.CTkEntry(master=recipe_app_frame, placeholder_text="Enter Ingredient Name")
                ingredient_name_entry.grid(row=2, column=2, columnspan=2, pady=10, padx=10, sticky="ew")

                                # Create a label and entry for the ingredient piece
                recipe_app_director_label = customtkinter.CTkLabel(master=recipe_app_frame, text="Ingredient Piece:")
                recipe_app_director_label.grid(row=3, column=1, pady=10, padx=10, sticky="w")
                ingredient_piece_entry = customtkinter.CTkEntry(master=recipe_app_frame, placeholder_text="Enter Ingredient Piece")
                ingredient_piece_entry.grid(row=3, column=2, columnspan=2, pady=10, padx=10, sticky="ew")

                                # Create a function to add the recipe to the listbox
                def add_recipe():
                    recipe_name = recipe_name_entry.get()
                    ingredient_name = ingredient_name_entry.get()
                    ingredient_piece = ingredient_piece_entry.get()

                    recipe_list = f"{recipe_name} - {ingredient_name} - {ingredient_piece}"
                    recipe_app_listbox.insert("end", recipe_list)

                def delete_item():
                    selected_index = recipe_app_listbox.curselection()
                    if selected_index:
                        recipe_app_listbox.delete(selected_index)


                                # Create a button to add the recipe
                add_recipe_button = customtkinter.CTkButton(master=recipe_app_frame, text="Add Recipe", command=add_recipe)
                add_recipe_button.grid(row=4, column=1, pady=10, padx=10, sticky="w")

                delete_recipe_button = customtkinter.CTkButton(master=recipe_app_frame, text="Delete Recipe", command=delete_item)
                delete_recipe_button.grid(row=4, column=2, pady=10, padx=10, sticky="w")

                #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

                rate_label = customtkinter.CTkLabel(master=recipe_app_frame, text="Your Rates:")
                rate_label.grid(row=4, column=3, pady=10, padx=10, sticky="w")

                average_label = customtkinter.CTkLabel(master=recipe_app_frame, text="Averages:")
                average_label.grid(row=4, column=6, pady=10, padx=10, sticky="w")

                rating_entry = customtkinter.CTkEntry(master=recipe_app_frame, width=10, placeholder_text="Rate the Recipe")
                rating_entry.grid(row=5, column=2, pady=10, padx=10, sticky="ew")

                                # Create a function to add the rating to the recipe
                rating_listbox = tk.Listbox(master=recipe_app_frame, height=10, width=15, bg=r3.cget('bg'), fg='white', font=("Arial", 10))
                rating_listbox.grid(row=4, column=5, rowspan=5, padx=10)

                average_listbox = tk.Listbox(master=recipe_app_frame, height=10, width=15, bg=r3.cget('bg'), fg='white', font=("Arial", 10))
                average_listbox.grid(row=4, column=7, rowspan=5, padx=10)

                def add_rating():
                    try:
                        rate = int(rating_entry.get())
                        if 0 <= rate <= 10:
                            rating_listbox.insert(customtkinter.END, rate)
                            rating_entry.delete(0, customtkinter.END)
                            calculate_average()
                        else:
                            messagebox.showerror("Error", "Please enter an integer between 0 and 10.")
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid integer between 0 and 10.")

                def calculate_average():
                    rates = [int(rt) for rt in rating_listbox.get(0, customtkinter.END)]
                    if rates:
                        total_sum = sum(rates)
                        average = total_sum / len(rates)
                        average_listbox.delete(0, customtkinter.END)
                        average_listbox.insert(customtkinter.END, f"Average: {average:.2f}")
                    else:
                        average_listbox.delete(0, customtkinter.END)
                        average_listbox.insert(customtkinter.END, "No numbers to calculate average.")
                
                add_rating_button = customtkinter.CTkButton(master=recipe_app_frame, text="Rate the Recipe!", command=add_rating)
                add_rating_button.grid(row=5, column=1, pady=10, padx=10, sticky="w")

                #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

                r3.mainloop()

                #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

            else:
                messagebox.showerror("Error", "Invalid password")
        else:
            messagebox.showerror("Error", "Invalid Username")
    else:
        messagebox.showerror("Error", "Enter all data")

def login():
    r1.destroy()
    frame2 = customtkinter.CTkFrame(master=r2,
                                    width=350,
                                    height=350)
    frame2.pack(padx=20,pady=20)

    global username_entry_login
    global password_entry_login

    username_entry_login = customtkinter.CTkEntry(master=frame2,
                                                placeholder_text="Username",
                                                width=150,
                                                height=40)
    username_entry_login.place(relx=0.5, rely=0.2, anchor = tk.CENTER)

    password_entry_login = customtkinter.CTkEntry(master=frame2,
                                     placeholder_text="Password",
                                     width=150,
                                     height=40,
                                     show = "*")
    password_entry_login.place(relx=0.5, rely=0.35, anchor = tk.CENTER)

    verification_button = customtkinter.CTkButton(master=frame2,
                                          text="Verify and Continue!",
                                          command=loginaccount)
    verification_button.place(relx=0.5, rely=0.5, anchor = tk.CENTER)
    r2.mainloop()

def entry_to_recipe_app():
        
        r2.destroy()
        #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

        # Create a frame for the recipe app
        recipe_app_frame = customtkinter.CTkFrame(master=r2)
        recipe_app_frame.pack(pady=20, padx=20, fill="both", expand=True, side="left")

        # Create a listbox to display the recipes
        recipe_app_listbox = tk.Listbox(master=recipe_app_frame, height=30, width=100, bg=r3.cget('bg'), fg='white', font="bold")
        recipe_app_listbox.grid(row=1, column=0, rowspan=5, padx=10)

        # Create a label and entry for the recipe name
        recipe_app_name_label = customtkinter.CTkLabel(master=recipe_app_frame, text="Recipe Name:")
        recipe_app_name_label.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        recipe_name_entry = customtkinter.CTkEntry(master=recipe_app_frame, placeholder_text="Enter Recipe Name")
        recipe_name_entry.grid(row=1, column=2, columnspan=2, pady=10, padx=10, sticky="ew")

        # Create a label and entry for the ingredient name
        recipe_app_link_label = customtkinter.CTkLabel(master=recipe_app_frame, text="Ingredient Name:")
        recipe_app_link_label.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        ingredient_name_entry = customtkinter.CTkEntry(master=recipe_app_frame, placeholder_text="Enter Ingredient Name")
        ingredient_name_entry.grid(row=2, column=2, columnspan=2, pady=10, padx=10, sticky="ew")

        # Create a label and entry for the ingredient piece
        recipe_app_director_label = customtkinter.CTkLabel(master=recipe_app_frame, text="Ingredient Piece:")
        recipe_app_director_label.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        ingredient_piece_entry = customtkinter.CTkEntry(master=recipe_app_frame, placeholder_text="Enter Ingredient Piece")
        ingredient_piece_entry.grid(row=3, column=2, columnspan=2, pady=10, padx=10, sticky="ew")

        # Create a function to add the recipe to the listbox
        def add_recipe():
            recipe_name = recipe_name_entry.get()
            ingredient_name = ingredient_name_entry.get()
            ingredient_piece = ingredient_piece_entry.get()

            recipe_list = f"{recipe_name} - {ingredient_name} - {ingredient_piece}"
            recipe_app_listbox.insert("end", recipe_list)

        def delete_item():
            selected_index = recipe_app_listbox.curselection()
            if selected_index:
                recipe_app_listbox.delete(selected_index)


        # Create a button to add the recipe
        add_recipe_button = customtkinter.CTkButton(master=recipe_app_frame, text="Add Recipe", command=add_recipe)
        add_recipe_button.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        delete_recipe_button = customtkinter.CTkButton(master=recipe_app_frame, text="Delete Recipe", command=delete_item)
        delete_recipe_button.grid(row=4, column=2, pady=10, padx=10, sticky="w")

        #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

        r3.mainloop()

#////////////////////////////////////////////////////////////////////////////////////////////#

frame1 = customtkinter.CTkFrame(master=r1,
                                width=350,
                                height=350)
frame1.pack(padx=20,pady=20)

username_entry_register = customtkinter.CTkEntry(master=frame1,
                                     placeholder_text="Username",
                                     width=150,
                                     height=40)
username_entry_register.place(relx=0.5, rely=0.2, anchor = tk.CENTER)

password_entry_register = customtkinter.CTkEntry(master=frame1,
                                     placeholder_text="Password",
                                     width=150,
                                     height=40,
                                     show = "*")
password_entry_register.place(relx=0.5, rely=0.35, anchor = tk.CENTER)

register_button = customtkinter.CTkButton(master=frame1,
                                          text="Create Your account!",
                                          command=signup)
register_button.place(relx=0.5, rely=0.5, anchor = tk.CENTER)

register_to_login_label = customtkinter.CTkLabel(master=frame1, 
                                                 text="Already have an account?")
register_to_login_label.place(relx=0.5, rely=0.7, anchor = tk.CENTER)

register_to_login_button = customtkinter.CTkButton(master=frame1,
                                          text="Login!",
                                          command=register_to_login_page)
register_to_login_button.place(relx=0.5, rely=0.8, anchor = tk.CENTER)

#////////////////////////////////////////////////////////////////////////////////////////////#

r1.mainloop()