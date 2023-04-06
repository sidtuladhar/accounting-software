from tkinter import *
import tkinter.ttk
import datetime
from PIL import ImageTk, Image
import sqlite3

# home window
root = Tk()
root.attributes('-fullscreen', True)
root.title("Maitreya Bodhi Pharmacy")

connect = sqlite3.connect("Medicine.db")
cursor = connect.cursor()
# cursor.execute("CREATE TABLE sold_drugs (medicine_name text, sold_quantity integer, sell_price real, date_time text)")
# cursor.execute("CREATE TABLE income (date text, sold_quantity integer, revenue real, profit real)")
# cursor.execute("CREATE TABLE drugs_entry
# (medicine_name text, quantity integer, marked price real, expiry text, supplier text, date_time text)")
# cursor.execute("CREATE TABLE drugs_stock
# (medicine_name text, quantity integer, marked price real, expiry text, supplier text, date_time text)")
cursor.execute("SELECT * FROM drugs_entry")
for row in cursor:
    print(row)
cursor.execute("DELETE FROM drugs_entry WHERE quantity = 100")
connect.commit()
connect.close()


def add_product():
    window1 = Toplevel()
    window1.attributes('-fullscreen', True)

    # database to display recent entries
    connect = sqlite3.connect("Medicine.db")
    cursor = connect.cursor()
    cursor.execute("SELECT medicine_name, quantity, marked, date_time FROM drugs_entry")
    fetchall = cursor.fetchall()
    connect.close()

    # style of tree
    style = tkinter.ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri', 12), background="lightblue", foreground="black")
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 15, "bold"), foreground="black")
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Creation of tree
    tree = tkinter.ttk.Treeview(window1, style="mystyle.Treeview", column=("c1", "c2", "c3", "c4"), show='headings',
                                height=35)

    for row in fetchall:
        tree.insert("", 0, values=row)

    tree.column("#1", anchor=CENTER, width=250)
    tree.heading("#1", text="Medicine Name")
    tree.column("#2", anchor=CENTER, width=80)
    tree.heading("#2", text="Quantity")
    tree.column("#3", anchor=CENTER, width=170)
    tree.heading("#3", text="Marked Price (per unit)")
    tree.column("#4", anchor=W)
    tree.heading("#4", text="Date and Time")

    # entry boxes
    medicine_name = Entry(window1, fg="black", bg="white", width=32, font=("arial", 15))
    quantity = Entry(window1, fg="black", bg="white", width=32, font=("arial", 15))
    marked_price = Entry(window1, fg="black", bg="white", width=32, font=("arial", 15))
    expiry_date = Entry(window1, fg="black", bg="white", width=32, font=("arial", 15))
    supplier = Entry(window1, fg="black", bg="white", width=32, font=("arial", 15))

    def submit():
        # enter entries into database
        connect = sqlite3.connect("Medicine.db")
        cursor = connect.cursor()
        cursor.execute("INSERT INTO drugs_stock VALUES (:medicine_name, :quantity, :marked_price,"
                       " :expiry, :supplier,:date_time)",

                       dict(medicine_name=medicine_name.get(), quantity=quantity.get(), marked_price=marked_price.get(),
                            expiry=expiry_date.get(), supplier=supplier.get(), date_time=datetime.datetime.now())

                       )
        cursor.execute("INSERT INTO drugs_entry VALUES (:medicine_name, :quantity, :marked_price,"
                       " :expiry, :supplier,:date_time)",

                       dict(medicine_name=medicine_name.get(), quantity=quantity.get(), marked_price=marked_price.get(),
                            expiry=expiry_date.get(), supplier=supplier.get(), date_time=datetime.datetime.now())

                       )
        cursor.execute("SELECT medicine_name FROM drugs_entry")
        cursor.execute("DELETE FROM drugs_entry WHERE medicine_name = ''")
        cursor.execute("SELECT medicine_name FROM drugs_stock")
        cursor.execute("DELETE FROM drugs_stock WHERE medicine_name = ''")
        connect.commit()
        connect.close()

        # delete entries
        medicine_name.delete(0, END)
        quantity.delete(0, END)
        marked_price.delete(0, END)
        expiry_date.delete(0, END)
        supplier.delete(0, END)

    # formatting labels in add product window
    format_box9 = Label(window1, text="             ", fg="black", pady=10)

    # labels for entry
    medicine_name_entry_label = Label(window1, fg="black", text="                    Enter Medicine Name:",
                                      font=("arial", 17))
    quantity_entry_label = Label(window1, fg="black", text="                               Enter Quantity:",
                                 font=("arial", 17))
    marked_price_entry_label = Label(window1, fg="black", text="       Enter Marked Price (Per Unit):",
                                     font=("arial", 17))
    expiry_date_entry_label = Label(window1, fg="black", text="Enter Expiry Date (YYYY-MM-DD):", font=("arial", 17))
    supplier_entry_label = Label(window1, fg="black", text="                                Enter Supplier:",
                                 font=("arial", 17))
    submit_button = Button(window1, text="Submit", fg="black", command=submit, padx=50, pady=20, font=("arial", 17))
    exit_button2 = Button(window1, text="Exit", fg="black", command=window1.destroy, padx=60, pady=20,
                          font=("arial", 15))

    # label of latest entries
    latest_entries_title = Label(window1, fg="black", text="Latest Entries", font=("Arial", 20, "bold"))

    # display for add product window (left)
    format_box9.grid(row=0)
    medicine_name.grid(row=1, column=1, pady=10)
    medicine_name_entry_label.grid(row=1, column=0, pady=10)
    quantity.grid(row=2, column=1, pady=10)
    quantity_entry_label.grid(row=2, column=0, pady=10)
    marked_price.grid(row=3, column=1, padx=50, pady=10)
    marked_price_entry_label.grid(row=3, column=0, padx=50, pady=10)
    expiry_date.grid(row=4, column=1, pady=10)
    expiry_date_entry_label.grid(row=4, column=0, pady=10)
    supplier.grid(row=5, column=1, pady=10)
    supplier_entry_label.grid(row=5, column=0, pady=10)
    submit_button.grid(row=6, column=1)
    exit_button2.grid(row=7, column=1)

    # display for add product window (right)
    latest_entries_title.grid(row=0, column=2)
    tree.grid(row=1, column=2, rowspan=8)

    window1.mainloop()


def sell_product():
    window2 = Toplevel()
    window2.attributes('-fullscreen', True)

    # database connection
    db_connect = sqlite3.connect('medicine.db')
    db_cursor = db_connect.cursor()
    db_cursor.execute("SELECT medicine_name FROM drugs_stock ORDER BY medicine_name ASC")
    records = db_cursor.fetchall()
    db_connect.close()

    # takes the medicine name from the database
    med_list = []
    for record in records:
        med_list.append(record[0])

    def submit():
        # enter entries into database
        connect = sqlite3.connect("Medicine.db")
        cursor = connect.cursor()
        cursor.execute("SELECT date, sold_quantity, revenue FROM income")
        cursor.execute(f"UPDATE income SET "
                       f"revenue = revenue + ({sell_price.get()} * {quantity.get()}), "
                       f"sold_quantity = sold_quantity + {quantity.get()} "
                       f"WHERE date = '{datetime.date.today()}'")

        cursor.execute("SELECT medicine_name, quantity FROM drugs_stock")
        cursor.execute(f"UPDATE drugs_stock SET quantity = quantity - '{quantity.get()}' "
                       f"WHERE medicine_name = '{medicine_name.get()}'")
        cursor.execute(f"SELECT marked FROM drugs_stock WHERE medicine_name = '{medicine_name.get()}'")
        fetch_marked_price = cursor.fetchall()
        marked_price = ''
        for mp in fetch_marked_price:
            marked_price = float(mp[0])
        cursor.execute(f"UPDATE income SET profit = profit + "
                       f"(({sell_price.get()} - '{marked_price}') * {quantity.get()})")
        cursor.execute("INSERT INTO sold_drugs VALUES (:medicine_name, :quantity, :sold_price, :date_time)",

                       dict(medicine_name=medicine_name.get(), quantity=quantity.get(), sold_price=sell_price.get(),
                            date_time=datetime.datetime.now())

                       )
        connect.commit()
        connect.close()

        # delete entries
        medicine_name.delete(0, END)
        quantity.delete(0, END)
        sell_price.delete(0, END)

        return

    # entry boxes
    medicine_name = Entry(window2, fg="black", bg="white", width=30, font=("arial", 15))
    quantity = Entry(window2, fg="black", bg="white", width=30, font=("arial", 15))
    sell_price = Entry(window2, fg="black", bg="white", width=30, font=("arial", 15))

    # list for medicine database
    list_box = Listbox(window2, fg="black", bg="lightblue", width=50, height=30, font=("Arial", 20))

    # updates the listbox with medicine names
    def update(data):
        list_box.delete(0, END)

        for item in data:
            list_box.insert(END, item)

    # updates the click on the listbox to occur in the entry box
    def callback(event):
        selection = event.widget.curselection()
        medicine_name.delete(0, END)
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            medicine_name.insert(0, data)

    def check(event):
        typed = medicine_name.get()

        if typed == '':
            data = med_list
        else:
            data = []
            for item in med_list:
                if typed.lower() in item.lower():
                    data.append(item)

        # update the listbox with relevant items from typing
        update(data)

    update(med_list)

    # bind click on listbox to medicine name entry
    list_box.bind("<<ListboxSelect>>", callback)

    medicine_name.bind("<KeyRelease>", check)

    # labels for entry
    medicine_name_entry_label = Label(window2, fg="black", text="Enter Medicine Name:", font=("arial", 15))
    quantity_entry_label = Label(window2, fg="black", text="Enter Quantity:", font=("arial", 15))
    sell_price_entry_label = Label(window2, fg="black", text="Enter Selling Price (Per Unit):", font=("arial", 15))

    # label of latest entries
    medicine_entries_title = Label(window2, fg="black", text="Medicine in Stock", font=("Arial", 20, "bold"))

    # Buttons in sell product window
    submit_button = Button(window2, text="Submit", fg="black", command=submit, padx=50, pady=20, font=("arial", 15))
    exit_button3 = Button(window2, text="Exit", fg="black", command=window2.destroy, padx=60, pady=20,
                          font=("arial", 15))

    # formatting labels in add product window
    format_box9 = Label(window2, text="             ", fg="black", pady=20)

    # Display of sell product window (left)
    format_box9.grid(row=0)
    medicine_name.grid(row=2, column=1)
    medicine_name_entry_label.grid(row=2, column=0)
    quantity.grid(row=4, column=1)
    quantity_entry_label.grid(row=4, column=0)
    sell_price.grid(row=6, column=1, padx=50)
    sell_price_entry_label.grid(row=6, column=0, padx=50)
    submit_button.grid(row=7, column=1)
    exit_button3.grid(row=8, column=1, padx=50)

    # Display of sell product window (right)
    medicine_entries_title.grid(row=1, column=2)
    list_box.grid(row=2, column=2, padx=90, rowspan=8)

    window2.mainloop()


def check_stock():
    window3 = Toplevel()
    window3.attributes('-fullscreen', True)

    # database to display recent entries
    connect = sqlite3.connect("Medicine.db")
    cursor = connect.cursor()
    cursor.execute("SELECT *, oid FROM drugs_stock")
    cursor.execute("DELETE FROM drugs_stock WHERE quantity = 0")
    cursor.execute("SELECT * FROM drugs_stock ORDER BY date_time DESC")
    fetchall = cursor.fetchall()
    connect.close()

    # style of tree
    style = tkinter.ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri', 15), foreground="black")
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 17, "bold"), foreground="black")
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Creation of tree
    tree = tkinter.ttk.Treeview(window3, style="mystyle.Treeview", column=("c1", "c2", "c3", "c4", "c5"),
                                show='headings', height=35)

    for row in fetchall:
        if str(datetime.date.today() + datetime.timedelta(30)) > row[3]:
            tree.insert("", END, values=row, tag=("expiry",))
        else:
            tree.insert("", END, values=row, tag=("not_expiry",))

    tree.tag_configure('not_expiry', background='lightblue')
    tree.tag_configure('expiry', background='red')

    tree.column("#1", anchor=CENTER, width=300)
    tree.heading("#1", text="Medicine Name")
    tree.column("#2", anchor=CENTER, width=100)
    tree.heading("#2", text="Quantity")
    tree.column("#3", anchor=CENTER, width=200)
    tree.heading("#3", text="Marked Price (per unit)")
    tree.column("#4", anchor=CENTER, width=200)
    tree.heading("#4", text="Expiry Date")
    tree.column("#5", anchor=CENTER, width=200)
    tree.heading("#5", text="Supplier")

    def delete():
        item = tree.selection()
        record = tree.item(item, 'value')[5]
        print(record)
        connect = sqlite3.connect("Medicine.db")
        cursor = connect.cursor()
        cursor.execute("SELECT medicine_name, quantity, marked price, date_time FROM drugs_stock")
        cursor.execute(f"DELETE FROM drugs_stock WHERE date_time = '{record}';")
        tree.delete(item)
        connect.commit()
        connect.close()

    tree.bind("<<TreeviewSelect>>", delete)

    delete_button = Button(window3, text="Delete", fg="black", command=delete, padx=55, pady=20,
                           font=("arial", 20))

    exit_button4 = Button(window3, text="Exit", fg="black", command=window3.destroy, padx=67, pady=20,
                          font=("arial", 20))

    tree.grid(row=0, column=0, rowspan=10)
    delete_button.grid(row=6, column=1)
    exit_button4.grid(row=7, column=1, pady=25)
    window3.mainloop()


def check_sold_stock():
    window4 = Toplevel()
    window4.attributes('-fullscreen', True)

    # database to display recent entries
    connect = sqlite3.connect("Medicine.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM sold_drugs ORDER BY date_time DESC")
    fetchall = cursor.fetchall()
    connect.close()

    # style of tree
    style = tkinter.ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri', 15), foreground="black", background="lightblue")
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 17, "bold"), foreground="black")
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Creation of tree
    tree = tkinter.ttk.Treeview(window4, style="mystyle.Treeview", column=("c1", "c2", "c3", "c4"),
                                show='headings', height=35)

    for row in fetchall:
        tree.insert("", END, values=row)

    tree.column("#1", anchor=CENTER, width=300)
    tree.heading("#1", text="Medicine Name")
    tree.column("#2", anchor=CENTER, width=100)
    tree.heading("#2", text="Quantity")
    tree.column("#3", anchor=CENTER, width=200)
    tree.heading("#3", text="Sold Price (per unit)")
    tree.column("#4", anchor=CENTER, width=220)
    tree.heading("#4", text="Date and Time")

    exit_button5 = Button(window4, text="Exit", fg="black", command=window4.destroy, padx=67, pady=20,
                          font=("arial", 20))

    tree.grid(row=0, column=0, rowspan=10)
    exit_button5.grid(row=7, column=1, padx=50)
    window4.mainloop()


def check_revenue():
    window5 = Toplevel()
    window5.attributes('-fullscreen', True)

    # database to display recent entries
    connect = sqlite3.connect("Medicine.db")
    cursor = connect.cursor()
    cursor.execute("SELECT date FROM income ORDER BY date ASC")
    # cursor.execute("DELETE FROM income")
    fetchall = cursor.fetchall()
    date = ''
    for recent_db_date in fetchall:
        date = recent_db_date[0]
    if str(date) == str(datetime.date.today()):
        cursor.execute("SELECT * FROM income ORDER BY date DESC")
    else:
        cursor.execute(f"INSERT INTO income (date, sold_quantity, revenue, profit)"
                       f"VALUES('{datetime.date.today()}', 0, 0, 0);"
                       )
        cursor.execute("SELECT * FROM income ORDER BY date DESC")
    fetchall = cursor.fetchall()
    connect.commit()
    connect.close()

    # style of tree
    style = tkinter.ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri', 15), background="lightblue", foreground="black")
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 17, "bold"), foreground="black")
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Creation of tree
    tree = tkinter.ttk.Treeview(window5, style="mystyle.Treeview", column=("c1", "c2", "c3", "c4"), show='headings',
                                height=40)

    for row in fetchall:
        tree.insert("", END, values=row)

    tree.column("#1", anchor=CENTER, width=300)
    tree.heading("#1", text="Date")
    tree.column("#2", anchor=CENTER, width=150)
    tree.heading("#2", text="Quantity Sold")
    tree.column("#3", anchor=CENTER, width=200)
    tree.heading("#3", text="Revenue")
    tree.column("#4", anchor=CENTER, width=200)
    tree.heading("#4", text="Profit/Loss")

    exit_button4 = Button(window5, text="Exit", fg="black", command=window5.destroy, padx=67, pady=20,
                          font=("arial", 20))

    tree.grid(row=0, column=0, rowspan=8)
    exit_button4.grid(row=7, column=1, padx=50)
    window5.mainloop()


# formatting in home menu
format_box1 = Label(root, text="                           ", fg="black")
format_box2 = Label(root, text="       ", fg="black")

# buttons in home menu
add_product = Button(root, text="Add New Product", command=add_product, fg="black", padx=25, pady=20,
                     font=("arial", 15))
sell_product = Button(root, text="Sell Product", command=sell_product, fg="black", padx=40, pady=20, font=("arial", 15))
stock = Button(root, text="Show Stock", command=check_stock, fg="black", padx=40, pady=20, font=("arial", 15))
sold_stock = Button(root, text="Show Sold Stock", command=check_sold_stock, fg="black", padx=23, pady=20,
                    font=("arial", 15))
revenue = Button(root, text="Check Revenue", command=check_revenue, fg="black", padx=28, pady=20, font=("arial", 15))
exit_button = Button(root, text="Exit", fg="black", command=root.quit, padx=67, pady=20, font=("arial", 15))
myImg = ImageTk.PhotoImage(Image.open("/Users/siddharthatuladhar/Downloads/logo3.png"))
labelImg = Label(root, image=myImg)
reminder = Label(root, text="Reminder: Open Check Revenue at the beginning of every day.", fg="black", bg="pink",
                 padx=20, pady=20, font=("arial", 15))
bottomLabel = Label(root, text="Maitreya Bodhi Home Care and Clinic 2021 ", fg="black", bd=1, relief=SUNKEN, anchor=E)

# display in home menu
format_box1.grid(column=0, row=0)
format_box2.grid(column=2, row=0)
labelImg.grid(column=1, row=0, columnspan=4)
add_product.grid(column=2, row=2, pady=19)
sell_product.grid(column=2, row=4, pady=19)
stock.grid(column=2, row=6, pady=19)
sold_stock.grid(column=2, row=7, pady=19)
revenue.grid(column=2, row=8, pady=20)
exit_button.grid(column=4, row=7)
reminder.grid(column=4, row=8, ipadx=60, pady=0)
bottomLabel.grid(sticky=W + E, column=0, columnspan=6)

root.mainloop()
