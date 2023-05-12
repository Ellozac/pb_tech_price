import requests
from bs4 import BeautifulSoup
import sqlite3
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
while True:
    userInput = input("Would you like to (1)add to the database or (2)view the database (3) wipe database? (4) end program\n> ")
    if userInput == "1":
        newProd = product(input("What would you like to call this product?\n>"), input("Url for product?\n> "))
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
        
        
    if userInput == "2":
        cur.execute("SELECT * FROM wishlist;")
        data = cur.fetchall()
        for row in data:
            print(f"id: {row[0]} Name: {row[1]} URL: {row[2]} Price: ${row[3]}")
            
            
    if userInput == "3":
        userInput = input("1. Wipe\n2. Remove 1 item\n> ")
        if userInput == "1":
            cur.execute("DROP TABLE IF EXISTS wishlist")
            connection.commit()
            
            
        else:
            userInput = input("What is the id of the item you would like to remove?\n> ")
            cur.execute("DELETE FROM wishlist WHERE id = ?", (userInput))
            connection.commit()
    if userInput == "4":
        break