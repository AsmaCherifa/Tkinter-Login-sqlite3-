import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.messagebox import *
import sqlite3

# creer database
conn = sqlite3.connect('database.db')
c = conn.cursor()
# creer table 
c.execute('''CREATE TABLE IF NOT EXISTS user  (username text, password text)''')
# inserer 
c.execute("INSERT INTO user (username, password) VALUES ('asma', '123')")
conn.commit()

# fonction 1 : login
def login():
    username = username_entry.get()
    password = password_entry.get()
    c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone() 
    if user:
        login_window.withdraw()  # hide login page
        main_window.deiconify()  # Show main page
    else:
        showwarning('erreur', 'username or password is incorrect!')


# fonction 2 : register
def register():
    # Get the username and password
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username already exists in the database
    c.execute("SELECT * FROM user WHERE username=?", (username,))
    user_exists = c.fetchone()

    if user_exists:
        # If the username already exists
        showwarning('erreur', 'Username already exists')

    else:
        # If the username does not exist, insert the new user into the database
        c.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))       
        showwarning('erreur', 'Registration successful')


def select_image():
    # Allow user to select a file and display the image on the main page
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path)
    tk_image = ImageTk.PhotoImage(image)
    image_label.configure(image=tk_image, width=150, height=150)
    image_label.place(x = 300 , y = 100)
    image_label.image = tk_image  
    



def quitter():
    if askyesno('Sur?', 'Are you sure you want to quit ?'):
        main_window.withdraw()  # Hide the login window
    else:
        showinfo('Sur?', 'You better stay !')

def logout():
    main_window.withdraw()  # Hide the login window
    login_window.deiconify()  # Show the main window

def calculate_bmi():
    # Get the values
    height = float(height_entry.get())
    weight = float(weight_entry.get())

    # Calculate the BMI
    bmi = weight / (height/100)**2
    if bmi < 18.5:
        conclusion = "underweight"
        classification = "Underweight"
    elif bmi < 25:
        conclusion = "healthy weight"
        classification = "Normal Weight"
    elif bmi < 30:
        conclusion = "overweight"
        classification = "Overweight"
    else:
        conclusion = "obese"
        classification = "Obese"
    # Display the result
    result_label.config(text="Your BMI is: {:.2f} ({})".format(bmi, classification))
    conclusion_label.config(text="Conclusion: You are {}".format(conclusion))

    
# Create the login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("700x400")

# Create the login widgets
login_label = tk.Label(login_window, text="Login",foreground="#8090ff",font=("Arial", 14, "bold"))
login_label.place(x = 80, y = 90)
 
username_label = tk.Label(login_window, text="Username:")
username_label.place(x = 10, y = 120)

username_entry = tk.Entry(login_window)
username_entry.place(x = 80 , y = 120)

password_label = tk.Label(login_window, text="Password:")
password_label.place(x = 10 , y = 150)

password_entry = tk.Entry(login_window, show="*")
password_entry.place(x = 80 , y = 150)

login_button = tk.Button(login_window, text="Login", command=login, bg="#8090ff",width=15)
login_button.place(x = 40 , y = 200)

login_button = tk.Button(login_window, text="Register", command=register, bg="red",width=15)
login_button.place(x = 40 , y = 250)

image_file = "login.png"
image = tk.PhotoImage(file=image_file)

# Add a label with the image
image_label = tk.Label(login_window, image=image,width="400",height="400")
image_label.place(x = 300 , y = 0)

# Toplevel :creates a new window that is independent of the login window
main_window = tk.Toplevel()
main_window.title("Main")
main_window.geometry("800x500")
# Create the widgets for the main window
select_image_button = tk.Button(main_window, text="Select Image", command=select_image,bg="#8ab8bb")
image_label = tk.Label(main_window)

# get height
lbl =   tk.Label(main_window , text = "Your Height :")
lbl.place(x = 10 , y = 60)

height_entry = tk.Entry(main_window, width=30)
height_entry.place(x = 100 , y = 60)

# get weight
lbl =   tk.Label(main_window , text = "Your Weight :")
lbl.place(x = 10 , y = 120)

weight_entry = tk.Entry(main_window, width=30)
weight_entry.place(x = 100 , y = 120)

#calculate
btn = tk.Button(main_window , text = "validate" , command = calculate_bmi, bg="#e6b710")
btn.place(x = 200 , y = 200)

#RT : 
result_label =   tk.Label(main_window , text = "")
result_label.place(x = 100 , y = 180)

conclusion_label = tk.Label(main_window)
conclusion_label.place(x = 200 , y = 180)

#quitter
quit_button = tk.Button(main_window, text="X", bg="#f9584b",command=quitter,width=10)
quit_button.pack(side="top", anchor="ne")

#sign up
quit_button = tk.Button(main_window, text="Logout", bg="#fbaba5",command=logout,width=10)
quit_button.pack(side="top", anchor="ne")

# Pack the widgets for the main window
select_image_button.pack()
image_label.pack()
# Hide the main window initially
main_window.withdraw()

# Start the Tkinter main loop
login_window.mainloop()
