import sqlite3, hashlib
from tkinter import *
from tkinter import simpledialog, Menu
from functools import partial

# Database Code
with sqlite3.connect(".db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

# Create PopUp
def popUp(text):
    answer = simpledialog.askstring("type", text)

    return answer


# Credit Window
root = Tk()
root.geometry('860x430+550+350')
root.overrideredirect(True)

bg = PhotoImage(file = "credit.png")

my_canvas = Canvas(root, width=860, height=430)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0,0, image=bg, anchor="nw")

btn = Button(root, text="Start", font=('Arial, 16'),fg = "white", bg="black", borderwidth=0,command=root.destroy)
btn_window = my_canvas.create_window(828, 40, anchor="s", window=btn)

root.mainloop()

# Initiate Window
window = Tk()
window.resizable(0,0)
window.iconbitmap('icon.svg')
window.title("Password Vault")

def hashPassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash

# First Screen
def firstScreen():
    window.geometry('250x150')
    window.configure(background="lightblue")

    lbl = Label(window, text="Create Master Password", bg="lightblue")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window, text="Re-enter Password", bg="lightblue")
    lbl1.pack()

    txt1 = Entry(window, width=20, show="*")
    txt1.pack()
    txt1.focus()

    lbl2 = Label(window, bg="lightblue")
    lbl2.pack()

    def savePassword():
        if txt.get() == txt1.get():
            txt.config(bg="lightgreen")
            txt1.config(bg="lightgreen")
            
            hashedPassword = hashPassword(txt.get().encode('utf-8'))

            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashedPassword)])
            db.commit()

            passwordVault()
        else:
            txt.config(bg="lightpink")
            txt1.config(bg="lightpink")
            
            lbl2.config(text="Password Do Not Match", bg="lightblue", fg='red')

    btn = Button(window, text="Save", bg="lightgreen", borderwidth=0,command=savePassword)
    btn.pack(pady=10)
    
# Login Screen
def loginScreen():
    window.geometry('250x100')
    window.configure(background="lightblue")

    lbl = Label(window, text="Enter Master Password", bg="lightblue")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window, bg="lightblue")
    lbl1.pack()

    def getMasterPassword():
        checkHashedPassword = hashPassword(txt.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        return cursor.fetchall()

    def checkPassword():
        match = getMasterPassword()

        if match:
            passwordVault()
            txt.config(bg='lightgreen')
        else:
            txt.delete(0, 'end')
            lbl1.config(text="Wrong Password", fg='red')
            txt.config(bg='lightpink')

    btn = Button(window, text="Login", bg="lightgreen", borderwidth=0, command=checkPassword)
    btn.pack(pady=10)

def passwordVault():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry():
        text1 = "Website & App"
        text2 = "Username"
        text3 = "Password"

        website = popUp(text1)
        username = popUp(text2)
        password = popUp(text3)

        insert_fields = """INSERT INTO vault(website,username,password)
        VALUES(?,?,?)"""

        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        passwordVault()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()

        passwordVault()
        
    window.geometry('850x400')
    window.configure(background="lightblue")

    lbl = Label(window, text="Password Vault", bg="lightblue", font=("Helvetica", 12))
    lbl.grid(column=1)
# Plus button
    btn = Button(window, text="+", borderwidth=0, bg='lightgreen', font=("Helvetica", 12), command=addEntry)
    btn.grid(row=1,column=1,pady=10)
# Vault
    menu=Menu(window)
    a=Menu(menu,tearoff=0)
    menu.add_cascade(label='Privacy policy',menu=a)
    a.add_command(label='Term')
    a.add_command(label='Privacy policy')
    b=Menu(menu,tearoff=0)
    menu.add_cascade(label='Help',menu=b)
    b.add_command(label='About Password Manager')
    b.add_command(label='Password Manager Help')
    b.add_command(label='Password Manager Docs')
    window.config(menu=menu)

    lbl = Label(window, text="Website & App", bg="lightblue", font=("Helvetica", 12))
    lbl.grid(row=2, column=0, padx=80)
    lbl = Label(window, text="Username", bg="lightblue", font=("Helvetica", 12))
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text="Password", bg="lightblue", font=("Helvetica", 12))
    lbl.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM vault")
    if(cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            lbl1 = Label(window, text=(array[i][1]), font=("Helvetica", 12), bg="lightblue")
            lbl1.grid(column=0, row=i+3)
            lbl1 = Label(window, text=(array[i][2]), font=("Helvetica", 12), bg="lightblue")
            lbl1.grid(column=1, row=i+3)
            lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12), bg="lightblue")
            lbl1.grid(column=2, row=i+3)
# Delete Button
            btn = Button(window, text="Delete", font=("Helvetica", 13), bg="lightpink", borderwidth=0,command=partial(removeEntry, array[i][0]))
            btn.grid(column=3, row=i+3, pady=10)

            i = i+1

            cursor.execute("SELECT * FROM vault")
            if (len(cursor.fetchall()) <= i):
                break
            
    
cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginScreen()
else:
    firstScreen()

window.mainloop()
