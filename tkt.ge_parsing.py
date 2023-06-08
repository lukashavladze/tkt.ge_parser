import requests
from bs4 import BeautifulSoup
import tkinter as tk
import sqlite3


concerts = 'https://tkt.ge/concerts'
page = requests.get(concerts)
soup = BeautifulSoup(page.text, 'html.parser')
result_koncertebi = soup.find_all(class_='eventItem__EventItemDescTitle-sc-1xt5420-6 geviHq')

koncertebi_header = []
koncertebi_place = []
teatri_header = []
teatri_place = []
opera_header = []
opera_place = []

koncertebi = []
opera = []
teatri = []

# scrapping details
for result in result_koncertebi:
    koncertebi_header.append(result.text)

result_place = soup.find_all(class_='eventItem__EventItemDescLocation-sc-1xt5420-7 elQKfu')
for result in result_place:
    koncertebi_place.append(result.text)


url_teatri = 'https://tkt.ge/theatre'
page2 = requests.get(url_teatri)
soup2 = BeautifulSoup(page2.text, 'html.parser')
result_teatri_header = soup2.find_all(class_='eventItem__EventItemDescTitle-sc-1xt5420-6 geviHq')
for result in result_teatri_header:
    teatri_header.append(result.text)


result_teatri_place = soup2.find_all(class_='eventItem__EventItemDescLocation-sc-1xt5420-7 elQKfu')
for result in result_teatri_place:
    teatri_place.append(result.text)

url_opera = 'https://tkt.ge/opera'
page1 = requests.get(url_opera)
soup1 = BeautifulSoup(page1.text, 'html.parser')
result_opera = soup1.find_all(class_='eventItem__EventItemDescTitle-sc-1xt5420-6 geviHq')
for result in result_opera:
    opera_header.append(result.text)


result_opera_place = soup1.find_all(class_='eventItem__EventItemDescLocation-sc-1xt5420-7 elQKfu')
for result in result_opera_place:
    opera_place.append(result.text)


# scrapping links for events
link_results = soup.find_all(attrs={'data-testid': 'anchor-tag'})
events_links = []
for result in link_results:
    links = result.get('href')
    if links is None:
        pass
    else:
        b3 = ("https://tkt.ge/" + links)
        print(b3)
        events_links.append(b3)
print(len(events_links))
print(len(koncertebi_header))

# scrapping for teatri
link_results_teatri = soup2.find_all(attrs={'data-testid': 'anchor-tag'})
teatri_links = []
for result in link_results_teatri:
    links = result.get('href')
    if links is None:
        pass
    else:
        b2 = ("https://tkt.ge/" + links)
        print(b2)
        teatri_links.append(b2)
print(len(teatri_links))
print(len(teatri_header))

# scrapping links for opera
# scrapping for teatri
link_results_opera = soup1.find_all(attrs={'data-testid': 'anchor-tag'})
opera_links = []
for result in link_results_opera:
    links = result.get('href')
    if links is None:
        pass
    else:
        b1 = ("https://tkt.ge/" + links)
        print(b1)
        opera_links.append(b1)
print(len(opera_links))
print(len(opera_header))

# function for getting links on select

def on_select():
    selected_links = listbox3.curselection()
    if selected_links:
        selected_record = events_links[selected_links[2]]
        for record in events_links:
            listbox4.insert(tk.END, record[2])



# adding our recordes in one list
for a, b in zip(koncertebi_header, koncertebi_place):
    koncertebi.append([a, b])

for a, b in zip(opera_header, opera_place):
    opera.append([a, b])

for a, b in zip(teatri_header, teatri_place):
    teatri.append([a, b])

# function for extracting data from sqlite database
def koncertebi_from_sql():
    connection = sqlite3.connect('koncertebi.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM events')
    data = cursor.fetchall()
    connection.close()
    return data

def opera_from_sql():
    connection = sqlite3.connect('koncertebi.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM opera')
    data = cursor.fetchall()
    connection.close()
    return data

def teatri_from_sql():
    connection = sqlite3.connect('koncertebi.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM teatri')
    data = cursor.fetchall()
    connection.close()
    return data

# creating sql database

conn = sqlite3.connect('koncertebi.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                    header_event TEXT,
                    place_event TEXT
                    )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS teatri (
                    header_teatri TEXT,
                    place_teatri TEXT
                    )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS opera (
                    header_opera TEXT,
                    place_opera TEXT
                    )''')
conn.commit()
cursor.execute('SELECT * FROM events')
conn.commit()
data = cursor.fetchall()
koncertebi_items = [item for item in data]

for item in koncertebi:
    if tuple(item) not in list(koncertebi_items):
        # print("found new record")
        cursor.execute('INSERT INTO events VALUES (?, ?)', (item[0], item[1]))
        conn.commit()
    else:
        # print("no new records")
        break

# teatri
cursor.execute('SELECT * FROM teatri')
conn.commit()
data = cursor.fetchall()
teatri_items = [item for item in data]

for item in teatri:
    if tuple(item) not in list(teatri_items):
        # print("found new record")
        cursor.execute('INSERT INTO teatri VALUES (?, ?)', (item[0], item[1]))
        conn.commit()
    else:
        # print("no new records")
        break

# opera
cursor.execute('SELECT * FROM opera')
conn.commit()
data = cursor.fetchall()
opera_items = [item for item in data]

for item in opera:
    if tuple(item) not in list(opera_items):
        # print("found new record")
        cursor.execute('INSERT INTO opera VALUES (?, ?)', (item[0], item[1]))
        conn.commit()
    else:
        # print("no new records")
        break



# tkinter window
mainWindow = tk.Tk()
mainWindow.title('TKT.GE')
# mainWindow.geometry('1024x768')
mainWindow.state('zoomed')

# 1 frame for koncerts
names_frame = tk.Frame(mainWindow)
names_frame.grid(column=1, row=2)
koncert_label = tk.Label(mainWindow, text="კონცერტები", foreground='red')
koncert_label.grid(column=1, row=1)
scrollbar = tk.Scrollbar(names_frame)
scrollbar.pack(side='right', fill='y')
listbox = tk.Listbox(names_frame, yscrollcommand=scrollbar.set, width=80, height=30)
listbox.pack(side='left', fill='both', expand=True)
scrollbar.config(command=listbox.yview)

# 2 frame for teatri
teatri_frame = tk.Frame(mainWindow)
teatri_frame.grid(column=2, row=2)
teatri_label = tk.Label(mainWindow, text="თეატრი", foreground='red')
teatri_label.grid(column=2, row=1)
scrollbar1 = tk.Scrollbar(teatri_frame)
scrollbar1.pack(side='right', fill='y')
listbox1 = tk.Listbox(teatri_frame, yscrollcommand=scrollbar1.set, width=80, height=30)
listbox1.pack(side='left', fill='both', expand=True)
scrollbar1.config(command=listbox1.yview)

# 3 frame for opera
opera_frame = tk.Frame(mainWindow)
opera_frame.grid(column=3, row=2)
opera_label = tk.Label(mainWindow, text="ოპერა", foreground='red')
opera_label.grid(column=3, row=1)
scrollbar2 = tk.Scrollbar(opera_frame)
scrollbar2.pack(side='right', fill='y')
listbox2 = tk.Listbox(opera_frame, yscrollcommand=scrollbar2.set, width=80, height=30)
listbox2.pack(side='left', fill='both', expand=True)
scrollbar2.config(command=listbox2.yview)

# for search bar frame
search_frame = tk.Frame(mainWindow)
search_frame.place(x=200, y=550)
scrollbar3 = tk.Scrollbar(search_frame)
scrollbar3.pack(side='right', fill='y')
listbox3 = tk.Listbox(search_frame, yscrollcommand=scrollbar3.set, width=150)
listbox3.pack(side='left', fill='both', expand=True)
scrollbar3.config(command=listbox3.yview)


# links frame
link_frame = tk.Frame(mainWindow)
link_frame.place(x=1150, y=550)
listbox4 = tk.Listbox(link_frame, width=40)
listbox4.pack(side='left', fill='both', expand=True)



# adding items from sql into tkinter window
koncertebi_sql = koncertebi_from_sql()
opera_sql = opera_from_sql()
teatri_sql = teatri_from_sql()

def show_events():
    listbox.delete(0, tk.END)
    for i in koncertebi_sql:
        listbox.insert('end', i)

def show_teatri():
    listbox1.delete(0, tk.END)
    for i in teatri_sql:
        listbox1.insert('end', i)

def show_opera():
    listbox2.delete(0, tk.END)
    for i in opera_sql:
        listbox2.insert('end', i)



event_button = tk.Button(mainWindow, text='events', command=show_events, width=20, background="yellow")
event_button.place(x=150, y=510)
teatri_button = tk.Button(mainWindow, text='teatri', command=show_teatri, width=20, background="yellow")
teatri_button.place(x=650, y=510)
opera_button = tk.Button(mainWindow, text='opera', command=show_opera, width=20, background="yellow")
opera_button.place(x=1150, y=510)




def search_word():
    find = entry.get()
    connection = sqlite3.connect('koncertebi.db')
    table_names = ["teatri", "events", "opera"]
    cursor = connection.cursor()
    matching_records = []
    for table in table_names:
        cursor.execute(f"SELECT * FROM {table}")
        records = cursor.fetchall()
        for record in records:
            if find.lower() in str(record).lower():
                matching_records.append(record)
        listbox3.delete(0, tk.END)
        for result in matching_records:
            listbox3.insert(tk.END, result)




entry = tk.Entry(mainWindow, width=20)
entry.place(x=600, y=720)

button_search = tk.Button(mainWindow, text='Search', command=search_word,  background="green")
button_search.place(x=725, y=720)




conn.close()


mainWindow.mainloop()
