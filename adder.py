import requests
from bs4 import BeautifulSoup
import sqlite3
connection = sqlite3.connect("./pbtech_pricescraper/database.sqlite3")
cur = connection.cursor()
userInput = ""
newProd = ""
soup = ""
response = ""
price = 0
parent_span = ""
pp_span = ""
value = ""

class product:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        


cur.execute("CREATE TABLE IF NOT EXISTS wishlist(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, url TEXT NOT NULL, cost INTEGER NOT NULL);")

userInput = input("Would you like to (1)add to the database or (2)view the database?\n> ")

if userInput == "1":
    newProd = product(input("What would you like to call this product?\n>"), input("Url for product?\n> "))
    response = requests.get(newProd.url)
    soup = BeautifulSoup(response.content, "html.parser")
    pp_span = soup.find("span", {"class": "dollars"})

    print(pp_span)
    
