import requests
from bs4 import BeautifulSoup
import sqlite3
from plyer import notification
conn = sqlite3.connect("database.sqlite3")
cur = conn.cursor()

item_name = ""
url = ""
cost = 0
both = []
soup = ""
response = ""

cur.execute("SELECT * FROM wishlist")
both = cur.fetchall()

for i in both:
    id = i[0]
    id = int(id)
    print(id)
    item_name = i[1]
    url = i[2]
    cost = i[3]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    pp_span = soup.find("span", {"class": "explist_dollars"}).text
    pp_span = pp_span[1:]
    pp_span = pp_span.replace(",", "")
    pp_span = int(pp_span)
    pp_span +=  pp_span * 0.15
    pp_span = round(pp_span)
    
    if cost > pp_span:
        cur.execute("SELECT cost FROM wishlist WHERE id = ?", (id,))
        cur.execute("UPDATE wishlist SET cost = ? WHERE id = ?",(pp_span, id,))
        conn.commit()
        notification.notify(
            title = f"{item_name} Is on SALE!!!",
            message = f"only ${pp_span} now!",
            app_icon = None,
            timeout = 10,
            toast = True,
        )
        
    if cost < pp_span:
         cur.execute("SELECT cost FROM wishlist WHERE id = ?", (id,))
         cur.execute("UPDATE wishlist SET cost = ? WHERE id = ?",(pp_span,id,))
         conn.commit()
         notification.notify(
            title = f"{item_name} Is off sale :(",
            message = f"${pp_span} now",
            app_icon = None,
            timeout = 10,
            toast = True,)
        