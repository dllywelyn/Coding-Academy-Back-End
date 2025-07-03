import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import *
import datetime
from datetime import date
import random
from tkinter import messagebox, PhotoImage

# Database credentials, defining for the connection function
SERVER = 'LAPTOP-1URVB9OH\SQLEXPRESS'  # Or 'localhost\\SQLEXPRESS' if using a named instance
DATABASE = 'Project_Video'
USERNAME = 'LAPTOP-1URVB9OH/dewig'
DRIVER = "ODBC Driver 18 for SQL Server"


# Establish a connection with the SQL database, call this function to retrieve/modify table data
def get_db_connection():
    """Establish a connection to SQL Server using ODBC."""
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={USERNAME};'
            "Trusted_Connection=yes;"
            #f'PWD={PASSWORD};'
            f'Encrypt=yes;'
            f'TrustServerCertificate=yes;'
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

# Test connection is working
def test_connection():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            #Uses an SQL Query to retrieve data from table
            sqlquery = "SELECT * FROM Staff"
            cursor.execute(sqlquery)
            results = cursor.fetchall()
            if results:
                for row in results:
                    # prints Staff table, so if i see it in the terminal upon login i know it works
                    print(row)  
            else:
                print("No records found in Tasks table.")
        except Exception as e:
            print(f"Error during query execution: {e}")
        finally:
            conn.close()
    else:
        print("Failed to establish a connection.")
 
# Function to delete inserted text and turn the font black
def on_entry_click_user(event):
    if username_entry.get() == 'Enter Username':
        username_entry.delete(0, "end")
        username_entry.config(fg='black', font=("Helvetica", 8, "bold"))

# Function to insert grey text to show user where to type username
def on_focusout_user(event):
    if username_entry.get() == '':
        username_entry.insert(0, 'Enter Username')
        username_entry.config(fg='grey')

# Function to delete inserted text and turn the font black
def on_entry_click_pass(event):
    if password_entry.get() == 'Enter Password':
        password_entry.delete(0, "end")
        password_entry.config(fg='black',  show="*")

# Function to insert grey text to show user where to type password
def on_focusout_pass(event):
    if password_entry.get() == '':
        password_entry.insert(0, 'Enter Password')
        password_entry.config(fg='grey')

# Login Function: Select ID, Username and Password from SQL to verify user, retrieve position for permissions and last login date
def login():
    global start_panel, username_entry, password_entry, username, position, user, first_name
    global previous_login, last_login_date, current_date, current_time, previous_date, previous_time

    username = username_entry.get()
    password = password_entry.get()

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Staff_ID FROM Staff WHERE Staff_Username = ? AND Staff_Password = ?", (username, password))
        user = cursor.fetchone()
        
        # Use datetime.now function to create current login timestamp
        if user:     
            user = user[0]
            print(user)
            cursor.execute(f"SELECT First_Name FROM Staff WHERE Staff_ID = ?", (user))
            sql_fname = cursor.fetchone()
            first_name = sql_fname[0]
            print(first_name)    

            cursor.execute(f"SELECT Position FROM Staff WHERE Staff_ID = ?", (user))
            sqlposition = cursor.fetchone()
            position = sqlposition[0]
            print(position)         
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT Login_Time FROM Staff Where Staff_ID = ?", (user))
                previous_login = cursor.fetchone()
                print(previous_login)
                previous_login = str(previous_login[0])  # need to convert into string for split to work
                print(previous_login)
                if previous_login == 'None':
                    previous_message = "This is your first time here! Please make sure a colleague is here to train you"
                else:
                    previous_date, previous_time = map(str, previous_login.split(" ")) 
                    previous_message = f"Your last login was at {previous_time}\non {previous_date}"

                messagebox.showinfo("Login Success", f"Welcome {first_name}!\n{previous_message}")

                #simpigy by grabbing whole date here
                current_login = datetime.datetime.now()
                last_login_date = current_login.strftime('%Y-%m-%d %H:%M:%S')
                current_date, current_time = map(str, last_login_date.split(" ")) 
                cursor.execute(f"UPDATE Staff SET Login_Time = '{last_login_date}' \
                Where Staff_ID = ?", (user))
                ### Forgot that INSERT (below) is for new data, should use UPDATE as above for changing values
                #cursor.execute(f"INSERT INTO STAFF (Login_Time, Login_Date) \  
                #Values ('{last_login_time}', '{last_login_date}') WHERE Staff_ID = ?", (user))
                conn.commit()
                conn.close()

                start.destroy()
                home_page()

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# This is the login window that calls the functions above
def start_panel():
    global start, username_entry, password_entry

    #Initialize Tkinter Window
    start = tk.Tk() 
    start.title("The Nineties Nook") 
    start.geometry("790x480") 
    start.resizable(False, False) 
    start.configure(background='black')
    # Images for company logo with entry boxes for login details and 'Play' (enter) and 'Stop' (exit) pictures for buttons
    bg_image = PhotoImage(file="colour_cassette.png")
    play_image = PhotoImage(file="play.png")
    stop_image = PhotoImage(file="stop.png")

    start.grab_set()

    # Create a label to display the image
    bg_image_label = tk.Label(start, image=bg_image)
    bg_image_label.pack()


    # UI Elements
    #tk.Label(start, text="Username:", bg= "white").place(x=290, y=135) 
    username_entry = tk.Entry(start, width=14, relief = "flat", font=("Arial", 7) ,fg="grey")
    username_entry.insert(0, 'Enter Username')
    username_entry.bind('<FocusIn>', on_entry_click_user)
    username_entry.place(x=420, y=164)

    #tk.Label(start, text="Password:", bg= "white").place(x=290, y=180) 
    password_entry = tk.Entry(start, width=14, relief="flat",  font=("Arial", 7), fg="grey")
    password_entry.insert(0, 'Enter Password')
    password_entry.bind('<FocusIn>', on_entry_click_pass)
    password_entry.place(x=420, y=208) 

    tk.Button(start, image=play_image, command=login).place(x=320, y=413)
    tk.Button(start, image=stop_image, command=lambda:start.quit()).place(x=410, y=413)
    start.mainloop()

# Switch user functions, 'logs off' by closing the window and going back to login start page
def switch_user():
    home.destroy()
    start_panel()

# Function to add staff member, opens new window to input user details
def add_user():
    #creating a new window
    add_user_window = Toplevel(home)
    add_user_window.title("New Staff Registration")
    add_user_window.geometry("300x600")
    add_user_window.resizable(TRUE, TRUE)

    add_user_window.staff_image = PhotoImage(file="vhs_white.png")
    staff_image_label = tk.Label(add_user_window, image=add_user_window.staff_image)
    staff_image_label.pack()
    
    add_user_window.grab_set()

    tk.Label(add_user_window, text = "First Name").pack(pady=5)
    adduser_fname_entry = tk.Entry (add_user_window, width =25)
    adduser_fname_entry.pack(pady =5)

    tk.Label(add_user_window, text = "Last Name").pack(pady=5)
    adduser_lname_entry = tk.Entry (add_user_window, width =25)
    adduser_lname_entry.pack(pady =5)

    tk.Label(add_user_window, text ="password").pack(pady =5)
    password_entry = tk.Entry(add_user_window, width =25, show = "*")
    password_entry.pack(pady =5)

    tk.Label(add_user_window, text ="confirm_password").pack(pady =5)
    confirm_password_entry = tk.Entry(add_user_window, width =25, show = "*")
    confirm_password_entry.pack(pady =5)

    tk.Label(add_user_window, text="Position:").pack(pady =5)
    position_select = ttk.Combobox(add_user_window, values=["Manager", "Assistant", "Cashier"], state="readonly") 
    position_select.pack(pady =5)
    
    # Function to verify new user details, SQL INSERT query to add to table
    def register_user():
        First_Name = adduser_fname_entry.get()
        Last_Name = adduser_lname_entry.get()
        Staff_Password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        Staff_Username = str(First_Name + Last_Name[:1])
        Position = position_select.get()

        if not First_Name or not Last_Name or not Staff_Password or not Position :
            messagebox.showerror("Error", "Please fill in all fields")
        elif Staff_Password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                # There was a problem retrieving new users because the program couldn't read IDENTITY PK in staff table, 
                # So I had to make my own incremental ID number fro PK by selecting last ID number and adding 1
                cursor.execute("SELECT TOP 1 Staff_ID FROM staff ORDER BY Staff_ID DESC")
                last_staffid = cursor.fetchone()
                Staff_ID = (last_staffid[0])+1
                print(Staff_ID)
                cursor.execute(f"INSERT INTO Staff ( Staff_ID, Last_Name, First_Name, Staff_Username, Staff_Password, Position )\
Values ('{Staff_ID}', '{Last_Name}', '{First_Name}','{Staff_Username}', '{Staff_Password}','{Position}')")
                conn.commit()
                conn.close()
                messagebox.showinfo ("Congratulations", "User Added")
                print(f'{Last_Name}, {First_Name}, {Staff_Username}, {Staff_Password}, {Position}')
                add_user_window.destroy()
                
    # Buttons for user choices, register (calls above function) or cancel (cancel shuts down window)
    button_frame = Frame(add_user_window)
    button_frame.pack(pady=15)
    
    Button(button_frame, text="Register", command=register_user, bg=("green")).pack(side=LEFT,padx=5)

    Button(button_frame, text="Cancel", command=add_user_window.destroy, bg=("red")).pack(side=RIGHT, padx=5)
    
# Window where user inputs the details of the staff member to be removed (using PK Staff ID)
def remove_user():

    remove_window = Toplevel(home)
    remove_window.title("Remove Staff Member")
    remove_window.geometry("300x350")
    remove_window.resizable(False, True)

    remove_window.grab_set()

    remove_window.staff_image = PhotoImage(file="vhs_white.png")
    staff_image_label = tk.Label(remove_window, image=remove_window.staff_image)
    staff_image_label.pack()


    tk.Label(remove_window, text = "Please enter the Staff ID").pack(pady=5)
    remove_staff_id_entry = tk.Entry (remove_window, width =25)
    remove_staff_id_entry.pack(pady =5)

    # Function to remove staff member, selects User ID from SQL and deletes the corresponding row
    def delete_user():
        remove_id = remove_staff_id_entry.get()

        if not remove_id:
            messagebox.showerror("Error", "Please fill in the Staff member's ID number")
        else:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                # seperate executions to retrieve data because this was written before I realised I could do it in one query
                cursor.execute(f"SELECT Staff_ID FROM Staff WHERE Staff_ID = {remove_id}")
                removing_staff_id = cursor.fetchone()
                Staff_ID = (removing_staff_id[0])

                cursor.execute(f"SELECT First_Name FROM Staff WHERE Staff_ID = {remove_id}")
                removing_fname = cursor.fetchone()
                First_Name = (removing_fname[0])

                cursor.execute(f"SELECT Last_Name FROM Staff WHERE Staff_ID = {remove_id}")
                removing_fname = cursor.fetchone()
                Last_Name = (removing_fname[0])

                # message box to verify the Staff name corresponds to input Staff ID and to ask confirmation
                response = messagebox.askyesno("Confirmation Needed", f"Are you sure you'd like to remove this member of staff? \
\n\n {First_Name} {Last_Name} - ID: {Staff_ID} \n\n Please confirm the Staff ID is correct")
                if response:
                    cursor.execute(f"DELETE FROM Staff WHERE Staff_ID = {Staff_ID}")
                    conn.commit()
                    conn.close()
                    messagebox.showinfo (" ", "User Deleted")
                    remove_window.destroy() 
                else:
                    remove_window.destroy()



    # Buttons inside frame to offer choices, 'remove' calls above function, 'cancel' destroys window without making changes
    button_frame = Frame(remove_window)
    button_frame.pack(pady=15)

    Button(button_frame, text="Remove", command=delete_user, bg=("green")).pack(side=LEFT,padx=5)
    Button(button_frame, text="Cancel", command=remove_window.destroy, bg=("red")).pack(side=RIGHT, padx=5)

# Function to show details when 'help' is selected, displayed SQL values retrieved upon login
# Displays username, staff ID, position (and corresponding permissions), current login time and last login session
def show_about():
    if position == "Manager":
        permissions = "full access"
    elif position == "Assistant":
        permissions = "moderate access - till functions and inventory"
    else:
        permissions = "restricted access - till functions only" 
    
    if previous_login == 'None':
        previous_login_message = "This is your first login session. Good luck!"
    else:
        previous_login_message = f"You logged in to your most recent session at {previous_time} on {previous_date}"

    messagebox.showinfo("About", f"You are logged in as {username}: \n\nStaff ID: {user}. \
\nAs {position} you have {permissions}. \n\nYou have been logged in since {current_time}. \
    \n{previous_login_message}")

# message for functions that are not yet ready, shows when placeholders buttons are clicked
def beta():
    messagebox.showinfo("Incomplete", "This is still in beta and not yet ready.")

###################################################################################################
# search window for searching for movies with different criteria
def movie_search():
    cover_id = "Select"
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()

        sql_movie_list = "SELECT Movie_Title, Movie_ID FROM Movies"
        cursor.execute(sql_movie_list)
        movie_results = cursor.fetchall()
        movie_list = [title[0] for title in movie_results]
        print(movie_list)
        
        genrequery = "SELECT DISTINCT Genre FROM Movies"
        cursor.execute(genrequery)
        genre_results = cursor.fetchall()
        genre_list = [title[0] for title in genre_results]
        print(genre_list)

        genrequery = "SELECT DISTINCT Director FROM Movies"
        cursor.execute(genrequery)
        director_results = cursor.fetchall()
        director_list = [title[0] for title in director_results]
        print(director_list)
        print("\n".join(director_list))

        conn.commit()
        conn.close()

    def clear_other_boxes(a):
        if a == "movie":
            genre_combo_box.set("")
            director_combo_box.set("")
            youchose_label.config(text=f"Your chosen film is")
            details_label.place(relx=1.0, rely=0.5, anchor='e')
            image_label.place(relx=0.0, rely=0.5, anchor='w')

        if a == "genre":
            combo_box.set("")
            director_combo_box.set("")
            youchose_label.config(text=f"Your genre is")
            image_label.place_forget()
            details_label.place(relx=0.5, rely=0.2, anchor='center')

        if a == "director":
            combo_box.set("")
            genre_combo_box.set("")
            youchose_label.config(text=f"Your chosen director is")
            image_label.place_forget()
            details_label.place(relx=0.5, rely=0.2, anchor='center')


    def check_input(movie_event):
        print("check")
        movie_input = movie_event.widget.get()

        if movie_input == '':
            combo_box['values'] = movie_list
        else:
            title_data = []
            for title in movie_list:
                if movie_input.lower() in title.lower():
                    title_data.append(title)

            combo_box['values'] = title_data


    def on_select(event):
        global chosen_film, cover, cover_id
        conn = get_db_connection()
        if conn:
            chosen_film  = event.widget.get()
            clear_other_boxes("movie")
            # chosen film is now the variable for clicked item
            print("User selected:",chosen_film)
            search_label.config(text=f"{chosen_film}")

            cursor = conn.cursor()
            cursor.execute("SELECT Movie_ID, YEAR(Release) AS Release, Director, Genre, Rating FROM Movies WHERE Movie_Title = ?", (chosen_film))
            cover_id, release, director, genre, rating = cursor.fetchone()
            print(cover_id) 
            print(release, director, genre, rating)

            cover = PhotoImage(file= f"pics\{cover_id}.png")
            image_label.config(image=cover) # add height = 360 to show full size pic
            image_label.image = cover  # need this to keep the reference later, almost like global
            details_label.config(text=f"{chosen_film} is a {release} {genre} \ndirected by {director}.\
    \n\nIt is rated {rating}.", fg="white", borderwidth=2, border=5 , relief="groove", pady=10, padx=30)

        conn.commit()
        conn.close()

    def genre_input(genre_event):
        genre_input = genre_event.widget.get()

        if genre_input == '':
            genre_combo_box['values'] = genre_list
        else:
            genre_data = []
            for genre in genre_list:
                if genre_input.lower() in genre.lower():
                    genre_data.append(genre)

            genre_combo_box['values'] = genre_data

    def genre_select(event):
        conn = get_db_connection()
        if conn:
            global chosen_genre
            chosen_genre  = event.widget.get()
            clear_other_boxes("genre")
            # chosen film is now the variable for clicked item
            print("User selected:",chosen_genre)
            search_label.config(text=f"{chosen_genre}")

            cursor = conn.cursor()

            cursor.execute("SELECT Movie_Title FROM Movies WHERE Genre = ?", (chosen_genre))
            movie_results = cursor.fetchall()
            movie_titles = "\n".join([title[0] for title in movie_results])
            print(movie_titles)

            details_label.config(text=f"{movie_titles}.", fg="white", borderwidth=2, border=5 , relief="groove", pady=10, padx=30)
            

        conn.commit()
        conn.close()

    def director_input(director_event):
        director_input = director_event.widget.get()

        if director_input == '':
            director_combo_box['values'] = director_list
        else:
            director_data = []
            for director in director_list:
                if director_input.lower() in director.lower():
                    director_data.append(director)

            director_combo_box['values'] = director_data

    def director_select(event):
        conn = get_db_connection()
        if conn:
            global chosen_director
            chosen_director  = event.widget.get()
            clear_other_boxes("director")
            # chosen film is now the variable for clicked item
            print("User selected:",chosen_director)
            search_label.config(text=f"{chosen_director}")

            cursor = conn.cursor()

            cursor.execute("SELECT Movie_Title FROM Movies WHERE director = ?", (chosen_director))
            movie_results = cursor.fetchall()
            movie_titles = "\n".join([title[0] for title in movie_results])
            print(movie_titles)

            details_label.config(text=f"{movie_titles}.", fg="white", borderwidth=2, border=5 , relief="groove", pady=10, padx=30)
            
        conn.commit()
        conn.close()

    search_page = Toplevel() 
    search_page.geometry("700x700") 
    search_page.resizable(True,True) 
    search_page.configure(background='black')

    #Framce for label + combobox - MOVIES
    movie_frame = Frame(search_page, bg="black")
    movie_frame.pack(pady=15)
    # creating Combobox
    movie_label = tk.Label(movie_frame,  text="Search by Movie Title ", bg="black", fg="white", font=("Arial", 10, )).pack(side=LEFT,padx=5)
    combo_box = ttk.Combobox(movie_frame)
    combo_box['values'] = movie_list
    combo_box.bind('<KeyRelease>', check_input)
    combo_box.bind('<<ComboboxSelected>>', on_select)
    combo_box.pack(side=RIGHT,padx=5)

    genre_frame = Frame(search_page, bg="black")
    genre_frame.pack(pady=15)
    # Combobox for Genre
    genre_label = tk.Label(genre_frame,  text="Search by Movie Genre", bg="black", fg="white", font=("Arial", 10, )).pack(side=LEFT,padx=5)
    genre_combo_box = ttk.Combobox(genre_frame)
    genre_combo_box['values'] = genre_list
    genre_combo_box.bind('<KeyRelease>', genre_input)
    genre_combo_box.bind('<<ComboboxSelected>>', genre_select)
    genre_combo_box.pack(side=RIGHT,padx=5)
   
    director_frame = Frame(search_page, bg="black")
    director_frame.pack(pady=15)
    # Combobox for Director
    director_label = tk.Label(director_frame,  text="Search by Director   ", bg="black", fg="white", font=("Arial", 10, )).pack(side=LEFT,padx=5)
    director_combo_box = ttk.Combobox(director_frame)
    director_combo_box['values'] = director_list
    director_combo_box.bind('<KeyRelease>', director_input)
    director_combo_box.bind('<<ComboboxSelected>>', director_select)
    director_combo_box.pack(side=RIGHT,padx=5)

    # "You chose" heading label
    youchose_label = tk.Label(search_page,  text="", bg="black", fg="white", font=("Arial", 10, ))
    youchose_label.pack(pady =5)
    # Search result label
    search_label = tk.Label(search_page,  text="", bg="black", fg="white", font=("Arial", 14, "bold"))
    search_label.pack(pady =5)

    # Results_frame for holding image and details pane
    results_frame = Frame(search_page, bg="black", width=500, height=300)
    results_frame.pack(anchor='center', expand=True)

    image_label = tk.Label(results_frame, bg="black")
    image_label.place(relx=0.0, rely=0.5, anchor='w')  # Left side, vertically centered

    details_label = tk.Label(results_frame, text="", bg="black", font=("Arial", 10))
    details_label.place(relx=1.0, rely=0.5, anchor='e')  # Right side, vertically centered

    vhs_rent = PhotoImage(file="vhs_rent.png")
    #Button(search_page, image=vhs_rent, bg=("black")).pack(pady=5)

    search_page.mainloop()
########################################################################################

def movie_summary():
    summary_page = Tk() 
    summary_page.geometry("500x600") 
    summary_page.title("Movies in Stock")
    summary_page.resizable(True,True) 
    summary_page.configure(background='black')
    summary_page.grab_set()

    # Title outside of loop so it doesn't get repeated
    heading_label = tk.Label(summary_page, text="MOVIES LIST", bg="black", fg= "white", font=("Arial", 11, ) )
    heading_label.pack(pady= 5)
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        # Select all values from the Movie_ID column of the Movies table
        sql_movie_list = "SELECT Movie_ID FROM Movies"
        cursor.execute(sql_movie_list)
        movie_results = cursor.fetchall()
        movie_list = [title[0] for title in movie_results]
        # Test movie list is functional
        print(movie_list)
        for movie in movie_list:
            cursor = conn.cursor()
            cursor.execute("SELECT Movie_Title, YEAR(Release) AS Release, Director, Genre, Rating FROM Movies WHERE Movie_ID = ?", (movie))
            movie_title, release, director, genre, rating = cursor.fetchone() 
            details_label = tk.Label(summary_page, text="", bg="black", fg= "white", font=("Arial", 9, ) )
            details_label.pack() 
            details_label.config(text= f"{movie_title} is a {release} {genre} film by {director}, rated {rating}\n")
            
    conn.commit()
    conn.close()

    summary_page.mainloop()



#===============================================# MAIN SHOP FUNCTIONS #==========================================================#
today = datetime.date.today()
# Add Member function
def add_member(): 
    
    #create the main window 
    add_mem_win = Toplevel(home) 
    add_mem_win.title("Add New Member") 
    add_mem_win.geometry("400x300") 
    add_mem_win.configure(background='black')
    add_mem_win.resizable(False, False) 

    #add UI widgets 
    tk.Label(add_mem_win, text="First Name:", bg="black", fg="white", font=("Arial", 10, "bold")).place(x=20, y=20) 

    #textbox 
    first_name = tk.Entry(add_mem_win)  #make an instance of tk.Entry 
    first_name.place(x=150, y =20) 

    #add UI widgets 
    tk.Label(add_mem_win, text="Last Name:", bg="black", fg="white", font=("Arial", 10, "bold")).place(x=20, y=60) 
    last_name = tk.Entry(add_mem_win)  #make an instance of tk.Ent 
    last_name.place(x=150, y =60) 

    #date of birth entry
    tk.Label(add_mem_win, text="Date of Birth:", bg="black", fg="white", font=("Arial", 10, "bold")).place(x=20, y=100)
    birth_date = tk.Entry(add_mem_win)
    birth_date.place(x=150, y= 100)

    tk.Label(add_mem_win, text="Membership:", bg="black", fg="white", font=("Arial", 10, "bold")).place(x=20, y=140) 
    plan_select = ttk.Combobox(add_mem_win, values=["Standard", "Star"],state="readonly") 
    plan_select.place(x=140, y=140) 
    plan_select.current(0) 

    def add_member_details():

        fname = str(first_name.get()) 
        lname = str(last_name.get()) 
        datebirth = birth_date.get()
        membership = plan_select.get()
        try:
            day,month,year = map(int, datebirth.split("/")) 
            age = today.year - year - ((today.month, today.day) < (month, day))
        except ValueError:
            messagebox.showerror("Date Format Error", "Please enter the date in DD/MM/YYYY format.")
        if age < 0:
            messagebox.showerror(title="INVALID RESPONSE", message="This date is in the future.")
        elif age <18:
            messagebox.showwarning(title="UNDERAGE", message="You must be over 18 for membership")
        else:
            first = fname[:3]
            last = lname[:3]
            year = str(year)
            if len(fname) == 1:
                first = f"{fname[:1]}xx"
            elif len(fname) == 2:
                first = f"{fname[:2]}x"
            if len(lname) == 1:
                last = f"{lname[:1]}xx"
            elif len(lname) == 2:
                last = f"{lname[:2]}x"
            #put this in loop ######    idnum = (random.randint(10,99))
            #put this in loop ######    idnum = str(idnum)
            #put this in loop ######    member_id = str(idnum+first.upper()+last.upper()+year[-2:])
            join_date = (f"{today.day}/{today.month}/{today.year}")
            sql_dob = (f"{year}-{month}-{day}")
            sql_join = (f"{today.year}-{today.month}-{today.day}")
            
            while True:
                idnum = (random.randint(10,99))
                idnum = str(idnum)
                member_id = str(idnum+first.upper()+last.upper()+year[-2:])
                conn = get_db_connection()
                if conn:
                                ## make sure that there are no duplicate mebership IDs
                    cursor = conn.cursor()
                    cursor.execute("SELECT (Member_ID) FROM Members WHERE Member_ID = ?", \
                    (member_id))
                    existing_memberid = cursor.fetchone()
                    print(member_id)
                    if existing_memberid:
                        # practical problem of giving away someone's password
                        #messagebox.showerror("Error", f"Username {member_id} already exists. Choose another.")
                        print(member_id, "already exists")
                    else:
                        print("success")
                        break
            label_result.config(text=f"Your membership I.D. number is {member_id}. \n Your join date is {join_date}", fg="white")
                    
            cursor.execute(f"INSERT INTO Members (Member_ID, First_Name, Last_Name, Date_of_Birth, Joined, Membership, Account) \
    Values ('{member_id}', '{fname}', '{lname}','{sql_dob}', '{sql_join}','{membership}', 'Active')")
            conn.commit()
            conn.close()

    add_option = Button(add_mem_win, image = vhs_add_member, command= add_member_details)
    add_option.place(x=120, y= 200)
    add_option.image = vhs_add_member

    label_result = tk.Label(add_mem_win, text="", bg="black", fg="white", font=("Arial", 12, "bold")) 
    label_result.place(x=20,y=180) 

    #run the app 
    add_mem_win.mainloop() 

#=============================================================================================================================

def rent(): 
    today = date.today()

    #create the main window 
    rent_win = Toplevel(home) 
    rent_win.title("Rent Tape") 
    rent_win.geometry("400x300") 
    rent_win.configure(background='black')
    rent_win.resizable(False, False) 

    #add UI widgets 
    tk.Label(rent_win, text="Please enter the Member ID", bg="black", fg="white", font=("Arial", 10, "bold")).pack(pady =5)
    member_rent_entry = tk.Entry (rent_win, width =25)
    member_rent_entry.pack(pady =5)

    def check_fines():
        member_id = str(member_rent_entry.get())
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT First_Name, Last_Name, Fines FROM Members WHERE Member_ID = ? ", (member_id,))
            fname, lname, fines = cursor.fetchone()
            print(fname)
                
                                
            if fines >= 15:
                messagebox.showerror("Account Frozen", f"The account of {fname} {lname} is frozen as they have a fine of £{fines}. \
                    \nThis must be paid in order to continue renting. ")
            elif fines > 0:
                messagebox.showerror("Unpaid Fines", f"{fname} {lname} has a £{fines} fine.\
                \nThey should ensure all tapes are returned and fines paid.")
            else:
                messagebox.showinfo("Congratulations!", "Enjoy your movie!")
                pass
            print(fines)
        conn.commit()
        conn.close()

    rent = Button(rent_win, text="submit member", borderwidth=2, relief="groove", 
    bg="black", fg="white", font=("Arial", 10, "bold"), command= check_fines)
    rent.pack(pady =5)
    rent.image = vhs_add_member

    tk.Label(rent_win, text="Please enter the Movie ID", bg="black", fg="white", font=("Arial", 10, "bold")).pack(pady =5)
    member_id_entry = tk.Entry (rent_win, width =25)
    member_id_entry.pack(pady =5)
    
    rent_option = Button(rent_win, image = vhs_rent, command=lambda:messagebox.showinfo("Congratulations!", "Enoy your movie!"))
    rent_option.place(x=120, y= 200)
    rent_option.image = vhs_rent

    rent.mainloop()

#=============================================================================================================================

def return_copies(): 
    today = date.today()

    #create the main window 
    return_copies = Toplevel(home) 
    return_copies.title("Return Tape") 
    return_copies.geometry("400x300") 
    return_copies.configure(background='black')
    return_copies.resizable(False, False) 

    #add UI widgets 
    tk.Label(return_copies, text="Please enter the Member ID", bg="black", fg="white", font=("Arial", 10, "bold")).pack(pady =5)
    return_member_entry = tk.Entry (return_copies, width =25)
    return_member_entry.pack(pady =5)

    def return_copies_details():
        returning_member = str(return_member_entry.get())
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT TOP 2 Copy_ID, Due_Date FROM Copies WHERE Member_ID = ? ", (returning_member))
            results = cursor.fetchall()
            if len(results) == 0:
                messagebox.showinfo("Error", "No copies found")
            elif len(results) == 1:
                copy_id1, due_date1 = results[0]
                messagebox.showinfo("One copy found:", f"Copy ID: {copy_id1}, Due Date: {due_date1}")
                print(copy_id1, due_date1, today)
            elif len(results) == 2:
                (copy_id1, due_date1), (copy_id2, due_date2) = results
                messagebox.showinfo("Two copies found:", f"Copy 1 — ID: {copy_id1}, Due: {due_date1} \
                \nCopy 2 — ID: {copy_id2}, Due: {due_date2}")
                print(copy_id1, copy_id2, due_date2, today)
            #year,month,day = map(int, due_date1.split("-"))
            #due_date = date(year, month, day)
            if today <= due_date1:
                messagebox.showinfo("Thank you!", "Returned on time")
            else:
                days_late = (today - due_date1).days
                #fixing the lower number as 1 for the first day, and the top of the range as the difference between today and the due date /
                # make a loop to show a £2 pound charge for each day that passes after the due date
                fine = days_late * 2
                messagebox.showinfo("Attention", f"This is returned late \nYour video is {days_late} day(s) past its due date and has incurred a £{fine} fine. ")


    return_option = Button(return_copies, image = vhs_return, command= return_copies_details)
    return_option.place(x=110, y= 200)
    return_option.image = vhs_return

    return_copies.mainloop() 

#=============================================================================================================================

def pay_fines(): 
    today = date.today()

    #create the main window 
    pay_fines_win = Toplevel(home) 
    pay_fines_win.title("Pay Fines") 
    pay_fines_win.geometry("400x150") 
    pay_fines_win.configure(background='black')
    pay_fines_win.resizable(False, False) 

    #add UI widgets 
    tk.Label(pay_fines_win, text="Please enter the Member ID", bg="black", fg="white", font=("Arial", 10, "bold")).pack(pady =5)
    member_id_entry = tk.Entry (pay_fines_win, width =25)
    member_id_entry.pack(pady =5)

    
    def check_fines():

        member_id = str(member_id_entry.get())
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT First_Name, Last_Name, Fines FROM Members WHERE Member_ID = ? ", (member_id))
            fname, lname, fines = cursor.fetchone()
            if fines:
                response = messagebox.askyesno("Member Fine", f"{fname} {lname} has a fine of £{fines} due. \
                \nHas this been paid?")
                if response:
                    messagebox.showinfo (" ", "User Deleted")
                    pay_fines_win.destroy() 
                else:
                    pay_fines_win.destroy()
            else:
                print(f"{fname} {lname} has no fine.")
            

    pay_fines_button = Button(pay_fines_win, image = vhs_pay_fines, command= check_fines)
    pay_fines_button.pack(pady=15)
    pay_fines_button.image = vhs_return

    pay_fines_win.mainloop()
    

#=============================================================================================================================


# Homepage function, called when logged in
def home_page():
    global home, vhs_add_member, vhs_return, vhs_pay_fines, vhs_rent
    home = tk.Tk() 
    # Title displays details retireved upon login to show who is logged in and what permissions they have
    home.title(f"Logged in as: {first_name} - {position}") 
    home.geometry("500x500") 
    home.resizable(True,True) 
    home.configure(background='black')
    # Images for company logo and decorative buttons
    home_image = PhotoImage(file="colour_cassette_text.png")
    vhs_add_member= PhotoImage(file="vhs_add_member.png")
    vhs_rent= PhotoImage(file="vhs_rent.png")
    vhs_return= PhotoImage(file="vhs_return.png")
    vhs_pay_fines= PhotoImage(file="vhs_pay_fines.png")

    # Create a label to display the image
    image_label = tk.Label(home, image=home_image)
    image_label.pack()

    #Create menu bar at top of window
    menu_bar = tk.Menu(home)

    # Create menus
    file_menu = tk.Menu(menu_bar, tearoff=0)
    users_menu = tk.Menu(menu_bar, tearoff=0)
    stock_menu = tk.Menu(menu_bar, tearoff=0)
    
    # Add cascades, File attached to menu bar, users attached to file menu, i.e. a submenu
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_cascade(label="Users", menu=users_menu)
    menu_bar.add_cascade(label="Stock", menu=stock_menu)
    stock_menu.add_command(label="Search", command=movie_search)
    stock_menu.add_command(label="Stocklist Summary", command=movie_summary)
    stock_menu.add_separator()
    
    # Conditions to change status of menu items (Active or Disabled) depending on user position
    if position == "Manager":
        users_menu.add_command(label="Add New User", command=add_user)
        users_menu.add_command(label="Remove User", command=remove_user)
        stock_menu.add_command(label="Add Movie", command=lambda:messagebox.showinfo(title="SUCCESS", message="Movie Added."))
        stock_menu.add_command(label="Remove Movie", command=lambda:messagebox.showinfo(title="SUCCESS", message="Movie Removed."))
        stock_menu.add_command(label="Update Rewound Status", command=lambda:messagebox.showinfo(title="SUCCESS", message="Status Updated!."))
    elif position == "Assistant":
        users_menu.add_command(label="Manager Only", state= DISABLED)
        users_menu.add_separator()
        users_menu.add_command(label="Add New User", state= DISABLED)
        users_menu.add_command(label="Remove User", state= DISABLED)
        stock_menu.add_command(label="Add Movie", command=lambda:messagebox.showinfo(title="SUCCESS", message="Movie Added."))
        stock_menu.add_command(label="Remove Movie", command=lambda:messagebox.showinfo(title="SUCCESS", message="Movie Removed."))
        stock_menu.add_command(label="Update Rewound Status", command=lambda:messagebox.showinfo(title="SUCCESS", message="Status Updated!."))
    else:
        users_menu.add_command(label="Manager Only", state= DISABLED)
        users_menu.add_separator()
        users_menu.add_command(label="Add New User", state= DISABLED)
        users_menu.add_command(label="Remove User", state= DISABLED)
        stock_menu.add_command(label="Manager Only", state= DISABLED)
        stock_menu.add_separator()
        stock_menu.add_command(label="Add Movie", state= DISABLED)
        stock_menu.add_command(label="Remove Movie", state= DISABLED)
        stock_menu.add_command(label="Update Rewound Status", state= DISABLED)

    file_menu.add_separator()
    file_menu.add_command(label="Log Off", command=switch_user)
    file_menu.add_command(label="Exit", command=home.destroy)

    # Create a Help menu
    help_menu = tk. Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=show_about)
    menu_bar.add_cascade(label="Help", menu=help_menu)


    # Attach the menu bar to the window
    home.config(menu=menu_bar)

    # Buttons for program functions, not yet complete so they currently call 'beta' function

    new_button = Button(home, image = vhs_add_member, command= add_member).pack (pady=15)
    rent_button = Button(home, image=vhs_rent,  command= rent).pack (pady=15)
    return_button = Button(home, image=vhs_return, command= return_copies).pack (pady=15)
    fine_button = Button(home, image=vhs_pay_fines, command= pay_fines).pack (pady=15)



    home.mainloop()

    

# Call the test function
test_connection()
start_panel()




