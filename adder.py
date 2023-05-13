
# 5/13/23 Completed Add to database working well but no input validation yet.


import requests
from bs4 import BeautifulSoup
import sqlite3
import tkinter as tk
from tkinter import ttk
connection = sqlite3.connect("database.sqlite3")
cur = connection.cursor()
userInput = ""
newProd = ""
soup = ""
response = ""
price = 0
parent_span = ""
pp_span = ""
value = ""
data = []

class product:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        


cur.execute("CREATE TABLE IF NOT EXISTS wishlist(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, url TEXT NOT NULL, cost INTEGER NOT NULL);")

class mainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("PBTECH Wishlister!")
        self.root.geometry("+{}+{}".format(int(self.root.winfo_screenwidth()/2 - 250), int(self.root.winfo_screenheight()/2 - 250)))
        
        
        self.text_welcome = tk.Label(self.root, text="Welcome to Pbtech Wishlister!")
        self.text_welcome.pack(padx=10,pady=10)
        
        self.button_adddb = tk.Button(self.root, text="Add to Database", command=self.addToDatabase)
        self.button_adddb.pack(padx=10,pady=10)
        
        self.button_viewdb = tk.Button(self.root, text="View the entire Database", command=self.viewDatabase)
        self.button_viewdb.pack(padx=10,pady=10)
        
        
        
        self.root.mainloop()

    def addToDatabase(self):
        self.root.destroy()
        addGUI()
    def viewDatabase(self):
        self.root.destroy()
        viewGUI()

class addGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Add To Wishlist!")
        self.root.geometry("+{}+{}".format(int(self.root.winfo_screenwidth()/2 - 250), int(self.root.winfo_screenheight()/2 - 250)))
        
        self.item_name_label = tk.Label(self.root, text="Please Enter The name of the product below")
        self.item_name =  tk.Text(self.root, height=1,width=30)
        self.item_name_label.pack(padx=5,pady=5)
        self.item_name.pack(padx=5, pady=5)
        
        
        self.item_url_label = tk.Label(self.root, text="Please Enter the Url Below")
        self.item_url = tk.Text(self.root, height=1, width= 50)
        self.item_url_label.pack(padx=5,pady=5)
        self.item_url.pack(padx=5,pady=5)
        
        self.add_to_db_button = tk.Button(self.root, text="Enter!", command=self.appendToDB)
        self.add_to_db_button.pack(padx=5,pady=5)
        
        
        
        
        self.back_button = tk.Button(self.root, text="Back", command=self.backToMain)
        self.back_button.pack(padx=10,pady=10)
        
        self.root.mainloop()
    def backToMain(self):
        self.root.destroy()
        mainGUI()
    def appendToDB(self):
        newProd = product(self.item_name.get("1.0", tk.END), self.item_url.get("1.0", tk.END))
        if not newProd.url.startswith('http://') and not newProd.url.startswith('https://'):
            newProd.url = 'https://' + newProd.url
        response = requests.get(newProd.url)
        soup = BeautifulSoup(response.content, "html.parser")
        pp_span = soup.find("span", {"class": "explist_dollars"}).text
        pp_span = pp_span[1:]
        pp_span = pp_span.replace(",", "")
        pp_span = int(pp_span)
        pp_span +=  pp_span * 0.15
        pp_span = round(pp_span)
        cur.execute("INSERT INTO wishlist(name, url, cost) VALUES(?,?,?);",(newProd.name, newProd.url,pp_span))
        connection.commit()
        self.backToMain()
    
class viewGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wishlist!")
        self.root.geometry("+{}+{}".format(int(self.root.winfo_screenwidth()/2 - 250), int(self.root.winfo_screenheight()/2 - 250)))

        self.tree = ttk.Treeview(self.root, columns=("#0", "#1", "#2"))
        self.tree.column("#0")
        self.tree.heading("#0",text='ID', anchor=tk.W)
        
        self.tree.column("#1")
        self.tree.heading("#1", text="Name", anchor=tk.E)
        
        self.tree.column("#2")
        self.tree.heading("#2", text="URL", anchor=tk.E)
        
        self.tree.pack()
        
        cur.execute("SELECT * FROM wishlist")
        rows = cur.fetchall()
        for row in rows:
            print(row)
            self.tree.insert("",tk.END, values=row)
           
        self.backButton = tk.Button(self.root, text="Back To Menu", command=self.backToMenu)
        self.backButton.pack(pady=10)
        self.root.mainloop()
    def backToMenu(self):
        self.root.destroy()
        mainGUI()
          
           
mainGUI()





# while True:
#     userInput = input("Would you like to (1)add to the database or (2)view the database (3) wipe database? (4) end program\n> ")
#     if userInput == "1":
#         newProd = product(input("What would you like to call this product?\n>"), input("Url for product?\n> "))
#         response = requests.get(newProd.url)
#         soup = BeautifulSoup(response.content, "html.parser")
#         pp_span = soup.find("span", {"class": "explist_dollars"}).text
#         pp_span = pp_span[1:]
#         pp_span = pp_span.replace(",", "")
#         pp_span = int(pp_span)
#         pp_span +=  pp_span * 0.15
#         pp_span = round(pp_span)
#         cur.execute("INSERT INTO wishlist(name, url, cost) VALUES(?,?,?);",(newProd.name, newProd.url,pp_span))
#         connection.commit()
        
        
#     if userInput == "2":
#         cur.execute("SELECT * FROM wishlist;")
#         data = cur.fetchall()
#         for row in data:
#             print(f"id: {row[0]} Name: {row[1]} URL: {row[2]} Price: ${row[3]}")
            
            
#     if userInput == "3":
#         userInput = input("1. Wipe\n2. Remove 1 item\n> ")
#         if userInput == "1":
#             cur.execute("DROP TABLE IF EXISTS wishlist")
#             connection.commit()
            
            
#         else:
#             userInput = input("What is the id of the item you would like to remove?\n> ")
#             cur.execute("DELETE FROM wishlist WHERE id = ?", (userInput))
#             connection.commit()
#     if userInput == "4":
#         break