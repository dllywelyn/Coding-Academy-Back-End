import tkinter as tk
from tkinter import messagebox
from tkinter import *

# Function for menu commands

details_dic = {"User":"Password"}

def exit_app():
    root.quit()

login_status = 0
def loggedin():
    global username, login_status
    if login_status == 0:
        root_title = "Staff access required"
    else:
        root_title = f"Logged in as {username}"
    return root_title


#functio for login
def new_user():
    #creating a new window
    login_window = Toplevel(root)
    login_window.title("New User Registration")
    login_window.geometry("300x400")
    login_window.resizable(False, True)

    
    login_window.grab_set()

    tk.Label(login_window, text = "New User", font=("Arial", 14))
    tk.Label(login_window, text = "Username").pack(pady=5)
    username_entry = tk.Entry (login_window, width =25)
    username_entry.pack(pady =5)
    tk.Label(login_window, text ="password").pack(pady =5)
    password_entry = tk.Entry(login_window, width =25, show = "*")
    password_entry.pack(pady =5)

    tk.Label(login_window, text ="confirm_password").pack(pady =5)
    confirm_password_entry = tk.Entry(login_window, width =25, show = "*")
    confirm_password_entry.pack(pady =5)
    

    def register_user():
        #global username_entry
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not username or not password:
            messagebox.showerror("please fill in all fields")
        elif password != confirm_password:
            messagebox.showerror("password do not match")
        else:
            details_dic[username] = password  # new key, add 
            messagebox.showinfo("success")
            login_window.destroy()
            print(details_dic)

    button_frame = Frame(login_window)
    button_frame.pack(pady=15)
 
    Button(button_frame, text="Register", command=register_user, bg=("green")).pack(side=LEFT,padx=5)
 
    Button(button_frame, text="Cancel", command=login_window.destroy, bg=("green")).pack(side=RIGHT, padx=5)




def existing_user():
    global details_dic
    login_window = Toplevel(root)
    login_window.title("Existing User")
    login_window.geometry("300x400")
    login_window.resizable(False, True)

    login_window.grab_set()

    tk.Label(login_window, text = "New User", font=("Arial", 14))
    tk.Label(login_window, text = "Username").pack(pady=5)
    username_entry = tk.Entry (login_window, width =25)
    username_entry.pack(pady =5)
    tk.Label(login_window, text ="password").pack(pady =5)
    password_entry = tk.Entry(login_window, width =25, show = "*")
    password_entry.pack(pady =5)

    

    def login_user():
        global details_dic, user_title, login_status, username, password
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Invalid", "Please fill in all fields")            
        elif ((username, password) in details_dic.items()) == True:
            print("yes")
            messagebox.showinfo("Valid", f"Welcome Back {username}")
            user_title = username
            login_status = 1
            root = tk.Tk()
            root.title(loggedin())     # Correctly testing title does change, need to update parent root 
            root.geometry ("380x288")
            login_window.destroy()
        else:
            messagebox.showerror("Invalid", "Please enter correct details")

    button_frame = Frame(login_window)
    button_frame.pack(pady=15)
 
    Button(button_frame, text="Login", command=login_user, bg=("green")).pack(side=LEFT,padx=5)
    Button(button_frame, text="Close", command=login_window.destroy, bg=("green")).pack(side=RIGHT, padx=5)



# Create the main window
root = tk.Tk()
#current_user=loggedin()
root.title(loggedin())
root.geometry ("380x288")

# Create a menu bar
menu_bar = tk.Menu(root)

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
users_menu = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="File", menu=file_menu)
# making a submenu inside File called Users
file_menu.add_cascade(label="Users", menu=users_menu)
users_menu.add_command(label="New User", command=new_user)
users_menu.add_command(label="Login", command=existing_user)

file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# Attach the menu bar to the window
root.config(menu=menu_bar)
# Run the application
root.mainloop ()
