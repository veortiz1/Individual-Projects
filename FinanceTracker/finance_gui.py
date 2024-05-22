import tkinter as tk
import psycopg2
from tkcalendar import Calendar
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
conn = psycopg2.connect(
    dbname="finance",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
currentuser=""
cur = conn.cursor()

def deposit():
    def deposit1():
        value=deposit_entry.get()
        try:
            result = int(value)
            split1=cal.get_date()
            date=split1.split("-")
            depo_label.config(text="$"+deposit_entry.get()+" Deposited On "+ cal.get_date())
            cur.execute("INSERT INTO deposited (uid,amount,month,day,year) VALUES (%s,%s,%s,%s,%s)", (currentuser,result,date[1],date[2],date[0]))
            conn.commit()
        except ValueError:
            depo_label.config(text="ERROR Deposited value must be a numerical value")
        print(deposit_entry.get()+" ON "+ cal.get_date())
    for widget in root.winfo_children():
        widget.destroy()
    select_date_label=tk.Label(root,text="Select Date")
    select_date_label.pack()
    cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd",showweeknumbers=False,showothermonthdays=False)
    cal.pack()
    despoit_frame=tk.Frame(root)
    despoit_frame.pack()
    deposit_label=tk.Label(despoit_frame,text="Deposit")
    deposit_label.pack(side=tk.LEFT)
    deposit_entry=tk.Entry(despoit_frame)
    deposit_entry.pack(side=tk.LEFT)
    deposit_entry.focus_set()
    deposit_button=tk.Button(root,text="Deposit",command=deposit1)
    deposit_button.pack()
    depo_label=tk.Label(root,text="")
    depo_label.pack()
    back_button=tk.Button(root,text="Back",command=homescreen)
    back_button.pack()


def withdrawn():
    def withdraw_1():
        value=withdraw_entry.get()
        try:
            result = int(value)
            split1=cal.get_date()
            date=split1.split("-")
            print(date)
            with_label.config(text="$"+value+" Withdrawn On "+ cal.get_date()+"\nFor the reason: "+var.get())
            cur.execute("INSERT INTO withdrawn (uid,amount,reason,month,day,year) VALUES (%s,%s,%s,%s,%s,%s)", (currentuser,result,var.get(),date[1],date[2],date[0]))
            conn.commit()
        except ValueError:
            with_label.config(text="ERROR Deposited value must be a numerical value")
    for widget in root.winfo_children():
        widget.destroy()
    select_date_label=tk.Label(root,text="Select Date")
    select_date_label.pack()
    cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd",showweeknumbers=False,showothermonthdays=False)
    cal.pack()
    withdraw_frame=tk.Frame(root)
    withdraw_frame.pack()
    withdraw_label=tk.Label(withdraw_frame,text="Deposit")
    withdraw_label.pack(side=tk.LEFT)
    withdraw_entry=tk.Entry(withdraw_frame)
    withdraw_entry.pack(side=tk.LEFT)
    withdraw_entry.focus_set()
    reasons_Frame=tk.Frame(root)
    reasons_Frame.pack()
    reason_label=tk.Label(reasons_Frame,text="Reason for spending:")
    reason_label.pack(side=tk.LEFT)
    reasons=["Gas","Grocery","Food","Shopping","Health","Car","Rent","Other"]
    var = tk.StringVar(root)
    var.set(reasons[0])
    reason_menu = tk.OptionMenu(reasons_Frame, var, *reasons)
    reason_menu.pack(side=tk.LEFT)
    withdraw_button=tk.Button(root,text="Withdraw",command=withdraw_1)
    withdraw_button.pack()
    with_label=tk.Label(root,text="")
    with_label.pack()
    back_button=tk.Button(root,text="Back",command=homescreen)
    back_button.pack()
    
    
    
def spendingsummary():
    def ss():
        totaldep=0
        totalwith=0
        text_box.delete("1.0", tk.END)
        cur.execute("SELECT amount FROM deposited WHERE uid=%s AND month=%s AND year=%s", (currentuser, month_entry.get(), year_entry.get()))
        results=cur.fetchall()
        cur.execute("SELECT day,month FROM deposited WHERE uid=%s AND month=%s AND year=%s", (currentuser, month_entry.get(), year_entry.get()))
        results1=cur.fetchall()
        datearr=[]
        for a in results1:
            tempstring=a[1]+"/"+a[0]
            datearr.append(tempstring)
        error_label.config(text="")
        finalstring=""
        if not results:
            print("None")
            error_label.config(text="No results for entered month and year for DEPOSITS")
        else:
            count=0
            for a in results:
                print(a[0])
                finalstring=finalstring+"$"+str(a[0])+" deposited"+" on "+datearr[count]+"\n"
                totaldep=totaldep+a[0]
                count=count+1
        cur.execute("SELECT day,month FROM withdrawn WHERE uid=%s AND month=%s AND year=%s", (currentuser, month_entry.get(), year_entry.get()))
        results1=cur.fetchall()
        cur.execute("SELECT amount FROM withdrawn WHERE uid=%s AND month=%s AND year=%s", (currentuser, month_entry.get(), year_entry.get()))
        results=cur.fetchall()
        datearr=[]
        if not results1:
            print("None")
            error_label.config(text="No results for entered month and year for withdraws")
        else:
            for a in results1:
                tempstring=a[1]+"/"+a[0]
                datearr.append(tempstring)
            count=0
            for a in results:
                print(a[0])
                finalstring=finalstring+"$"+str(a[0])+" withdrawn"+" on "+datearr[count]+"\n"
                totalwith=totalwith+a[0]
                count=count+1
        text_box.insert(tk.END, finalstring)
        total_dep_label.config(text="Total Deposited $"+str(totaldep))
        total_with_label.config(text="Total Withdrawn $"+str(totalwith))
            
        
    for widget in root.winfo_children():
        widget.destroy()
    enter_month_frame=tk.Frame(root)
    enter_month_frame.pack()
    month_label=tk.Label(enter_month_frame,text="Enter a month(e.g. Janurary is 01 feburary is 02,etc.)")
    month_label.pack(side=tk.LEFT)
    month_entry=tk.Entry(enter_month_frame)
    month_entry.pack(side=tk.LEFT)
    month_entry.focus_set()
    enter_year_frame=tk.Frame(root)
    enter_year_frame.pack()
    year_label=tk.Label(enter_year_frame,text="Enter Year(e.g 2020)")
    year_label.pack(side=tk.LEFT)
    year_entry=tk.Entry(enter_year_frame)
    year_entry.pack(side=tk.LEFT)
    error_label=tk.Label(root,text="")
    error_label.pack()
    confirm_button=tk.Button(root,text="Confirm",command=ss)
    confirm_button.pack()
    text_box = tk.Text(root,height=20, width=80)
    text_box.pack()
    total_dep_label=tk.Label(root,text="Total Spent $0")
    total_dep_label.pack()
    total_with_label=tk.Label(root,text="Total Withdrawn $0")
    total_with_label.pack()

    



    back_button=tk.Button(root,text="Back",command=homescreen)
    back_button.pack()

def withdrawsummary():
    for widget in root.winfo_children():
        widget.destroy()
    def withdraw_alltime():
        reasons=["Gas","Grocery","Food","Shopping","Health","Car","Rent","Other"]
        reasons_value=[]
        for reas in reasons:
            cur.execute("SELECT amount FROM withdrawn WHERE uid=%s AND reason=%s", (currentuser,reas))
            results=cur.fetchall()
            final_value=0
            if not results:
                reasons_value.append(0)
            else:
                for res in results:
                    final_value=final_value+res[0]
                reasons_value.append(final_value)
        print(reasons_value)
        i = 0
        while i < len(reasons):
            if reasons_value[i] == 0:
                del reasons[i]
                del reasons_value[i]
            else:
                i += 1
        print(reasons_value)
        plt.figure(figsize=(6, 6))
        plt.pie(reasons_value, labels=reasons, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.savefig('withdraw.png')
        new_image = Image.open("withdraw.png")
        resized_new_image = new_image.resize((400, 400), Image.LANCZOS)
        new_photo = ImageTk.PhotoImage(resized_new_image)
        image_label.config(image=new_photo)
        image_label.image = new_photo
    def withdraw_month():
        year=year_entry.get()
        month=month_entry.get()
        reasons=["Gas","Grocery","Food","Shopping","Health","Car","Rent","Other"]
        reasons_value=[]
        for reas in reasons:
            cur.execute("SELECT amount FROM withdrawn WHERE uid=%s AND reason=%s AND month=%s AND year=%s", (currentuser,reas,month,year))
            results=cur.fetchall()
            final_value=0
            if not results:
                reasons_value.append(0)
            else:
                for res in results:
                    final_value=final_value+res[0]
                reasons_value.append(final_value)
        print(reasons_value)
        i = 0
        while i < len(reasons):
            if reasons_value[i] == 0:
                del reasons[i]
                del reasons_value[i]
            else:
                i += 1
        print(reasons_value)
        plt.figure(figsize=(6, 6))
        plt.pie(reasons_value, labels=reasons, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.savefig('withdraw.png')
        new_image = Image.open("withdraw.png")
        resized_new_image = new_image.resize((400, 400), Image.LANCZOS)
        new_photo = ImageTk.PhotoImage(resized_new_image)
        image_label.config(image=new_photo)
        image_label.image = new_photo
    all_time_button=tk.Button(root,text="View All Time withdraw summary",command=withdraw_alltime)
    all_time_button.pack()
    enter_month_frame=tk.Frame(root)
    enter_month_frame.pack()
    month_label=tk.Label(enter_month_frame,text="Enter a month(e.g. Janurary is 01 feburary is 02,etc.)")
    month_label.pack(side=tk.LEFT)
    month_entry=tk.Entry(enter_month_frame)
    month_entry.pack(side=tk.LEFT)
    month_entry.focus_set()
    enter_year_frame=tk.Frame(root)
    enter_year_frame.pack()
    year_label=tk.Label(enter_year_frame,text="Enter Year(e.g 2020)")
    year_label.pack(side=tk.LEFT)
    year_entry=tk.Entry(enter_year_frame)
    year_entry.pack(side=tk.LEFT)
    error_label=tk.Label(root,text="")
    error_label.pack()
    confirm_button=tk.Button(root,text="View Withdraw chart for entered month",command=withdraw_month)
    confirm_button.pack()
    warning_label=tk.Label(root,text="IF the image is white that means theres no result for entered month and year")
    warning_label.pack()
    image = Image.open("origional_withdraw.png")
    resized_image = image.resize((200, 200), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(root, image=photo)
    image_label.image = photo  
    image_label.pack()
    back_button=tk.Button(root,text="Back",command=homescreen)
    back_button.pack()

        
def logged_out():
    for widget in root.winfo_children():
        widget.destroy()
    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack()
    register_button = tk.Button(root, text="Register", command=register)
    register_button.pack()


def homescreen():
    for widget in root.winfo_children():
        widget.destroy()
    deposit_button=tk.Button(root,text="Deposit",command=deposit)
    deposit_button.pack()
    withdraw_button=tk.Button(root,text="Withdrawn",command=withdrawn)
    withdraw_button.pack()    
    spending_summary_button=tk.Button(root,text="Spending Summary",command=spendingsummary)
    spending_summary_button.pack()
    withdraw_summary=tk.Button(root,text="Withdraw Summary",command=withdrawsummary)
    withdraw_summary.pack()
    logout_button=tk.Button(root,text="Logout",command=logged_out)
    logout_button.pack()

def login():
    def login1():
        global currentuser
        cur.execute("SELECT pass FROM login WHERE uid = %s", (login_entry.get(),))
        row = cur.fetchone()
        if row==None:
            return
        print(row[0])
        passw=row[0]
        if password_entry.get()==passw:
            currentuser=login_entry.get()
            homescreen()
        else:
            error_label.config(text="Either Username or password is invalid")
            
    for widget in root.winfo_children():
        widget.destroy()
    login_frame=tk.Frame(root)
    login_frame.pack()
    login_label=tk.Label(login_frame,text="User Id: ")
    login_label.pack(side=tk.LEFT)
    login_entry = tk.Entry(login_frame)
    login_entry.pack(side=tk.LEFT)
    login_entry.focus_set()
    password_frame=tk.Frame(root)
    password_frame.pack()
    password_label=tk.Label(password_frame,text="Password: ")
    password_label.pack(side=tk.LEFT)
    password_entry = tk.Entry(password_frame)
    password_entry.pack(side=tk.LEFT)
    password_entry.focus_set()
    login = tk.Button(root, text="Login",command=login1)
    login.pack()
    error_label=tk.Label(root,text="")
    error_label.pack()
    logout_button=tk.Button(root,text="Back",command=logged_out)
    logout_button.pack()
def register():
    def register1():
        try:
            cur.execute("INSERT INTO login (uid,pass) VALUES (%s,%s)", (login_entry1.get(),password_entry1.get()))
            conn.commit()
            error_label=tk.Label(root,text="User "+login_entry1.get()+" Created!")
            error_label.pack()
        except psycopg2.errors.UniqueViolation as e:
            print("Error:", e)
            conn.rollback()
            error_label=tk.Label(root,text="ERROR USERNAME ALREADY EXISTS!")
            error_label.pack()
    for widget in root.winfo_children():
        widget.destroy()
    login_frame1=tk.Frame(root)
    login_frame1.pack()
    login_label1=tk.Label(login_frame1,text="User Id: ")
    login_label1.pack(side=tk.LEFT)
    login_entry1 = tk.Entry(login_frame1)
    login_entry1.pack(side=tk.LEFT)
    login_entry1.focus_set()
    password_frame1=tk.Frame(root)
    password_frame1.pack()
    password_label1=tk.Label(password_frame1,text="Password: ")
    password_label1.pack(side=tk.LEFT)
    password_entry1 = tk.Entry(password_frame1)
    password_entry1.pack(side=tk.LEFT)
    password_entry1.focus_set()
    register = tk.Button(root, text="Register",command=register1)
    register.pack()
    logout_button=tk.Button(root,text="Back",command=logged_out)
    logout_button.pack()
    
    


    
root = tk.Tk()
root.title("Simple Tkinter Window")
root.geometry("500x500")
login_button = tk.Button(root, text="Login", command=login)
login_button.pack()
register_button = tk.Button(root, text="Register", command=register)
register_button.pack()
root.mainloop()