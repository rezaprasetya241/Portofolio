  
import tkinter as tk
import time
import sqlite3
from datetime import datetime

current_balance = 1000

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {'Balance':tk.IntVar()}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,CreatePage, MenuPage, WithdrawPage, DepositPage, BalancePage,ExpensePage,IncomeHistoryPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent, bg='#710618')
        self.controller = controller
        self.controller.title("LOGIN")
        self.controller.state("zoomed")

        heading_label = tk.Label(self, text="MANAGE YOUR MONEY",font=('orbitron',45,'bold'), foreground="#ffffff",background='#710618')
        heading_label.pack(pady=25)

        logo_photo = tk.PhotoImage(file='logo1.png')
        space_label = tk.Label(self,image=logo_photo,bg="#710618")
        space_label.pack()
        space_label.image = logo_photo

        username_label = tk.Label(self, text = "ID",font=('orbitron',13),bg="#710618",fg="white")
        username_label.pack(pady=5)
        my_username = tk.StringVar()
        username_entry_box = tk.Entry(self,textvariable=my_username,width=22)
        username_entry_box.focus_set()
        username_entry_box.pack(ipady=7)

        password_label = tk.Label(self, text = "Password",font=('orbitron',13),bg="#710618",fg="white")
        password_label.pack(pady=5)
        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self,textvariable=my_password,width=22)
        password_entry_box.pack(ipady=7)

        def handle_focus_in(_):
            password_entry_box.configure(fg='black', show='*')
        password_entry_box.bind('<FocusIn>',handle_focus_in)
        def check():
            
            conn = sqlite3.connect("Management.db")
            db = conn.cursor()

            db.execute("SELECT *, oid FROM account")
            recods = db.fetchall()
            for record in recods:
                if my_username.get() == str(record[0]) and my_password.get() == str(record[1]):
                    my_password.set('')
                    incorrect['text']=''
                    controller.show_frame('MenuPage')
                else:
                    incorrect['text']='Password or ID is Incorrect'

            conn.commit()

            conn.close()
                
        enter_button = tk.Button(self,text='Enter',command=check,relief='raised',borderwidth = 3,width=30,height=2)
        enter_button.pack(pady=5)
        def signUp():
            controller.show_frame('CreatePage')

        signUp_button = tk.Button(self,text='Create account',command=signUp,relief='raised',borderwidth=3,width=30,height=2)
        signUp_button.pack(pady=5)

        incorrect = tk.Label(self,text='',font=('orbitron',13),fg='white',bg='#710618',anchor='n')
        incorrect.pack(fill='both',expand=True)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()
        
class CreatePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#710618')
        self.controller = controller
   
        heading_label = tk.Label(self,text='MAIN MENU',font=('orbitron',45,'bold'),foreground='#ffffff',background='#710618')
        heading_label.pack(pady=25)

        selection_label = tk.Label(self,text='Please make a selection',font=('orbitron',13),fg='white',bg='#710618',anchor='w')
        selection_label.pack()

        button_frame = tk.Frame(self,bg='#710618')
        button_frame.pack(fill='both',expand=True)

        nama_label = tk.Label(button_frame,text='Nama',foreground='#ffffff',background='#710618')
        nama_label.pack()

        nama = tk.StringVar()
        nama_entry = tk.Entry(button_frame,textvariable=nama,width=22)
        nama_entry.pack(ipady=7)

        nama_label = tk.Label(button_frame,text='ID',foreground='#ffffff',background='#710618')
        nama_label.pack()

        id = tk.StringVar()
        id_entry = tk.Entry(button_frame,textvariable=id,width=22)
        id_entry.pack(ipady=7)

        password_label = tk.Label(button_frame,text='PASSWORD',foreground='#ffffff',background='#710618')
        password_label.pack()

        password = tk.StringVar()
        password_entry = tk.Entry(button_frame,textvariable=password,width=22)
        password_entry.pack(ipady=7)
        def entry():
            conn = sqlite3.connect("Management.db")
            c = conn.cursor()
            c.execute("INSERT INTO account VALUES (:id, :password)",{
                'id': int(id.get()) ,
                'password': str(password.get())
            })
            now = datetime.now() 
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            c.execute("INSERT INTO identitas VALUES (:id, :nama, :saldo, :date)",{
                'id':id.get(),
                'nama': nama.get(),
                'saldo': 0,
                'date':dt_string
                })
            id.set('')
            nama.set('')
            password.set('')
            controller.show_frame("StartPage")


            id.set('')
            password.set('')
            # Commit Changes
            conn.commit()

            #Close Connection
            conn.close()


        enter_button = tk.Button(button_frame,text='ENTER',command=entry,relief='raised',borderwidth = 3,width=30,height=2)
        enter_button.pack(pady=5)


        def exit():
            controller.show_frame('StartPage')
            
        exit_button = tk.Button(button_frame,text='EXIT',command=exit,relief='raised',borderwidth=3,width=30,height=2)
        exit_button.pack(pady=5)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()



class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller
   
        heading_label = tk.Label(self,text='MAIN MENU',font=('orbitron',45,'bold'),foreground='#ffffff',background='#3d3d5c')
        heading_label.pack(pady=25)

        selection_label = tk.Label(self,text='Please make a selection',font=('orbitron',13),fg='white',bg='#3d3d5c',anchor='w')
        selection_label.pack()

        button_frame = tk.Frame(self,bg='#3d3d5c')
        button_frame.pack(fill='both',expand=True)

        def withdraw():
            controller.show_frame('WithdrawPage')
            
        withdraw_button = tk.Button(button_frame,text='WITHDRAW',command=withdraw,relief='raised',borderwidth=3,width=50,height=3)
        withdraw_button.pack(pady=5)

        def deposit():
            controller.show_frame('DepositPage')
            
        deposit_button = tk.Button(button_frame,text='INCOME',command=deposit,relief='raised',borderwidth=3,width=50,height=3)
        deposit_button.pack(pady=5)

        def balance():
            controller.show_frame('BalancePage')
            
        balance_button = tk.Button(button_frame,text='BALANCE',command=balance,relief='raised',borderwidth=3,width=50,height=3)
        balance_button.pack(pady=5)

        def expense():
            controller.show_frame('ExpensePage')
        expense_button = tk.Button(button_frame,text='EXPENSE',command=expense,relief='raised',borderwidth=3,width=50,height=3)
        expense_button.pack(pady=5)

        def historyIncome():
            controller.show_frame('IncomeHistoryPage')
        history_button = tk.Button(button_frame,text='INCOME HISTORY',command=historyIncome,relief='raised',borderwidth=3,width=50,height=3)
        history_button.pack(pady=5)


        def exit():
            controller.show_frame('StartPage')
            
        exit_button = tk.Button(button_frame,text='EXIT',command=exit,relief='raised',borderwidth=3,width=50,height=3)
        exit_button.pack(pady=5)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

class WithdrawPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller


        heading_label = tk.Label(self,text='MANAGE MONEY',font=('orbitron',45,'bold'),foreground='#ffffff',background='#3d3d5c')
        heading_label.pack(pady=25)

        choose_amount_label = tk.Label(self,text='WITHDRAW',font=('orbitron',13),fg='white',bg='#3d3d5c')
        choose_amount_label.pack()

        button_frame = tk.Frame(self,bg='#33334d')
        button_frame.pack(fill='both',expand=True)
        
        require_label = tk.Label(button_frame,text="Requirement",font=('orbitron',13),fg="white",bg='#33334d')
        require_label.pack(pady=5)
        
        require = tk.StringVar()
        require_entry = tk.Entry(button_frame,textvariable=require,width=50)
        require_entry.pack(pady=5,ipady=20)

        username_label = tk.Label(button_frame,text="ID",font=('orbitron',13),fg="white",bg='#33334d')
        username_label.pack(pady=5)

        username = tk.StringVar()
        username_entry = tk.Entry(button_frame,textvariable=username,width=50)
        username_entry.pack(pady=5,ipady=20)        
            
        cash = tk.StringVar()
        amount_label = tk.Label(button_frame,text="amount you want to withdraw",font=('orbitron',13),fg="white",bg='#33334d')
        amount_label.pack(pady=5)
        amount_entry = tk.Entry(button_frame,textvariable=cash,width=50,justify='right')
        amount_entry.pack(pady=5,ipady=20)

        
        def amount():
            # Create a database or connect to one
            conn = sqlite3.connect("Management.db")

            #create cursor
            c = conn.cursor()
            c.execute("UPDATE identitas SET saldo = saldo -"+str(cash.get())+" WHERE id = "+str(username.get()))
            now = datetime.now() 
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            
            c.execute("INSERT INTO expense VALUES (:require, :cash, :dt_string, :id)",{
                'require': require.get(),
                'cash': cash.get(),
                'dt_string':dt_string,
                'id': int(username.get()) 
            })
            
            # Commit Changes
            conn.commit()

            #Close Connection
            conn.close()
            username.set('')
            require.set('')
            cash.set('')
            controller.show_frame('MenuPage')


        enter_button = tk.Button(button_frame,text='Enter',command=amount,relief='raised',borderwidth=3,width=40,height=3)
        enter_button.pack(pady=10)
        
        def menu():
            controller.show_frame('MenuPage')
            
        menu_button = tk.Button(button_frame,command=menu,text='Menu',relief='raised',borderwidth=3,width=40,height=3)
        menu_button.pack(pady=5)

        


        # Bottom
        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()
   

class DepositPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,text='DEPOSIT',font=('orbitron',45,'bold'),foreground='#ffffff',background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self,height=4,bg='#3d3d5c')
        space_label.pack()

        enter_amount_label = tk.Label(self,text='Enter amount',font=('orbitron',13),bg='#3d3d5c',fg='white')
        enter_amount_label.pack(pady=10)

        sumber_label = tk.Label(self,text="Sumber",font=('orbitron',13),fg="white",bg='#3d3d5c')
        sumber_label.pack(pady=5)

        sumber = tk.StringVar()
        sumber_entry = tk.Entry(self,textvariable=sumber,width=22)
        sumber_entry.pack(pady=5,ipady=7)

        id_label = tk.Label(self,text="ID",font=('orbitron',13),fg="white",bg='#3d3d5c')
        id_label.pack(pady=5)

        id = tk.StringVar()
        id_entry = tk.Entry(self,textvariable=id,width=22)
        id_entry.pack(pady=5,ipady=7)

        deposit_label = tk.Label(self,text="Deposit",font=('orbitron',12),fg="white",bg='#3d3d5c')
        deposit_label.pack(pady=5) 

        cash = tk.StringVar()
        deposit_entry = tk.Entry(self,textvariable=cash,width=22)
        deposit_entry.pack(ipady=7)

        def deposit_cash():
            
            # Create a database or connect to one
            conn = sqlite3.connect("Management.db")

            #create cursor
            c = conn.cursor()
            c.execute("UPDATE identitas SET saldo = saldo +"+str(cash.get())+" WHERE id = "+str(id.get()))
            now = datetime.now() 
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            
            c.execute("INSERT INTO deposit VALUES (:sumber, :cash, :dt_string, :id)",{
                'sumber': sumber.get(),
                'cash': cash.get(),
                'dt_string':dt_string,
                'id': int(id.get()) 
            })
            

            sumber.set('')
            cash.set('')
            id.set('')
            # Commit Changes
            conn.commit()

            #Close Connection
            conn.close()
            cash.set('')
            controller.show_frame('MenuPage')
            
        enter_button = tk.Button(self,text='Enter',command=deposit_cash,relief='raised',borderwidth=3,width=40,height=3)
        enter_button.pack(pady=10)

        def menu():
            controller.show_frame('MenuPage')
            
        menu_button = tk.Button(self,command=menu,text='Menu',relief='raised',borderwidth=3,width=40,height=3)
        menu_button.pack(pady=5)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()


class BalancePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#E38FA0')
        self.controller = controller

        
        heading_label = tk.Label(self,text='DEPOSIT INFORMATION',font=('orbitron',45,'bold'),foreground='#ffffff',background='#E38FA0')
        heading_label.pack(pady=25)

        # global current_balance
        # controller.shared_data['Balance'].set(current_balance)
        # balance_label = tk.Label(self,textvariable=controller.shared_data['Balance'],font=('orbitron',13),fg='white',bg='#3d3d5c',anchor='w')
        # balance_label.pack(fill='x')

        button_frame = tk.Frame(self,bg='#E3BBC3')
        button_frame.pack(fill='both',expand=True)

        id_label = tk.Label(self,text="ID",background="#E38FA0",foreground="#ffffff")
        id_label.pack(pady=8)

        id = tk.StringVar()
        balance_entry = tk.Entry(self,textvariable=id,width=22)
        balance_entry.pack(pady=5,ipady=7)
        label = "Saldo \t\t Waktu "
        title_label=tk.Label(button_frame,text=label,bg="#E3BBC3",fg="#ffffff")
        title_label.pack()
        # cash = tk.StringVar()
        # deposit_entry = tk.Entry(self,textvariable=cash,width=22)
        # deposit_entry.pack(ipady=7)

        def money():
            conn = sqlite3.connect('Management.db')

            c = conn.cursor()
            c.execute("SELECT saldo,date FROM identitas WHERE id="+str(id.get()))
            records = c.fetchall()
            print_records = " "
            for record in records:
                print_records+= "Rp."+str(record[0])+"\t"+str(record[1])+"\n"
            query_label = tk.Label(button_frame,text=print_records,bg="#E3BBC3",fg="#ffffff")
            query_label.pack()
            
            conn.commit()
            conn.close()


        enter_button = tk.Button(self,text='Enter',command=money,borderwidth=3,width=22,height=1)
        enter_button.pack(pady=5)

        def menu():
            id.set('')
            for widget in button_frame.winfo_children():
                widget.destroy()
            controller.show_frame('MenuPage')   
        menu_button = tk.Button(self,command=menu,text='Menu',relief='raised',borderwidth=3,width=22,height=1)
        menu_button.pack(pady=5)

        # def exit():
        #     controller.show_frame('StartPage')  
        # exit_button = tk.Button(button_frame,text='Exit',command=exit,relief='raised',borderwidth=3,width=50,height=5)
        # exit_button.grid(row=1,column=0,pady=5)


        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

class ExpensePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#3d3d5c')
        self.controller = controller
    
        heading_label = tk.Label(self,text='EXPENSE INFORMATION',font=('orbitron',45,'bold'),foreground='#ffffff',background='#3d3d5c')
        heading_label.pack(pady=25)
        label = "Kebutuhan \t Pengeluaran \t\t Waktu \t\t ID "
        title_label=tk.Label(self,text=label)
        title_label.pack()


        button_frame = tk.Frame(self,bg='#33334d')
        button_frame.pack(fill='both',expand=True)
        id_label = tk.Label(self,text="ID",background="#3d3d5c",foreground="#ffffff")
        id_label.pack(pady=8)

        id = tk.StringVar()
        balance_entry = tk.Entry(self,textvariable=id,width=22)
        balance_entry.pack(pady=5,ipady=7)
        def history():
            conn = sqlite3.connect('Management.db')

            c = conn.cursor()
            c.execute("SELECT * FROM expense WHERE id = "+str(id.get()))
            records = c.fetchall()
            print_records = ''
            for record in records:
                print_records += str(record[0]) + " " +"\t\t"+" "+"Rp."+str(record[1]) + " " + "\t\t" +str(record[2]) + " " + "\t" + str(record[3])+"\n"
            query_label = tk.Label(button_frame,text=print_records)
            query_label.pack()
            
            
            conn.commit()
            conn.close()


        enter_button = tk.Button(self,text='Enter',command=history,borderwidth=3,width=22,height=1)
        enter_button.pack(pady=5)



        def menu():
            id.set('')
            for widget in button_frame.winfo_children():
                widget.destroy()
            controller.show_frame('MenuPage')   
        menu_button = tk.Button(self,command=menu,text='Menu',relief='raised',borderwidth=3,width=22,height=1)
        menu_button.pack(pady=5)


        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

class IncomeHistoryPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#33334d')
        self.controller = controller
    
        heading_label = tk.Label(self,text='INCOME INFORMATION',font=('orbitron',45,'bold'),foreground='#ffffff',background='#33334d')
        heading_label.pack(pady=25)
        label = "Kebutuhan \t Pemasukan \t\t Waktu \t\t "
        title_label=tk.Label(self,text=label,bg="#33334d",fg="#ffffff")
        title_label.pack()


        button_frame = tk.Frame(self,bg='#33334d')
        button_frame.pack(fill='both',expand=True)
        id_label = tk.Label(self,text="ID",background="#33334d",foreground="#ffffff")
        id_label.pack(pady=8)

        id = tk.StringVar()
        balance_entry = tk.Entry(self,textvariable=id,width=22)
        balance_entry.pack(pady=5,ipady=7)
        def history():
            conn = sqlite3.connect('Management.db')

            c = conn.cursor()
            c.execute("SELECT * FROM deposit WHERE id = "+ str(id.get()))
            records = c.fetchall()
            print_records = ''
            for record in records:
                print_records += str(record[0]) + " " +"\t\t"+" "+"Rp."+str(record[1]) + " " + "\t\t" +str(record[2]) + " " + "\t"+"\n"
            query_label = tk.Label(button_frame,text=print_records,bg="#33334d",fg="#ffffff")
            query_label.pack()
            
            
            conn.commit()
            conn.close()


        enter_button = tk.Button(self,text='Enter',command=history,borderwidth=3,width=22,height=1)
        enter_button.pack(pady=5)



        def menu():
            id.set('')
            for widget in button_frame.winfo_children():
                widget.destroy()
            controller.show_frame('MenuPage')   
        menu_button = tk.Button(self,command=menu,text='Menu',relief='raised',borderwidth=3,width=22,height=1)
        menu_button.pack(pady=5)


        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        visa_photo = tk.PhotoImage(file='visa.png')
        visa_label = tk.Label(bottom_frame,image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.png')
        mastercard_label = tk.Label(bottom_frame,image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.png')
        american_express_label = tk.Label(bottom_frame,image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()