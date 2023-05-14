import requests
from bs4 import BeautifulSoup
import sqlite3
from plyer import notification
import winreg
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


def create_key(name: str="default", path: ""=str)->bool:
    # initialize key (create) or open
    reg_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, # path current user
                                 r'Software\Microsoft\Windows\CurrentVersion\Run', # sub path startup
                                 0, # reserved (must be zero, default is 0)
                                 winreg.KEY_WRITE) # set permission to write

    # CreateKey returns a handle
    # if null it failed
    if not reg_key:
        return False

    # set the value of created key
    winreg.SetValueEx(reg_key, # key
        name,                  # value name
        0,                     # reserved (must be zero, default is 0)
        winreg.REG_SZ,     # REG_SZ - null-terminated string (for file path)
        path) # set file path

    # close key (think of it as opening a file)
    reg_key.Close()
    return True

if create_key("startup_batch", r"C:\Users\admin\Desktop\test.bat"):
    print("Added startup key.")
else:
    print("Failed to add startup key.")

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
        