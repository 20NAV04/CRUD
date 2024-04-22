import tkinter as tk
import MySQLdb
from tkinter import ttk

db = MySQLdb.connect("localhost", "root", "ace", "TEST")
c = db.cursor()
keyNames = []
keyIndexes = []


c.execute("""SELECT k.column_name
        FROM information_schema.table_constraints t
        JOIN information_schema.key_column_usage k
        USING(constraint_name, table_schema, table_name)
        WHERE t.constraint_type="PRIMARY KEY"
        AND t.table_schema="TEST"
        AND t.table_name="PERSON";
        """)

for key in c.fetchall():
    keyNames.append(key[0])

c.execute("""
          SELECT COLUMN_NAME 
          FROM INFORMATION_SCHEMA.COLUMNS 
          WHERE TABLE_SCHEMA = "TEST" 
          AND TABLE_NAME = "PERSON";""")

result = c.fetchall()
columnList = []

for index, column in enumerate(result):
    columnList.append(column[0])
    if column[0] in keyNames:
        keyIndexes.append(index)


c.execute("""SELECT * FROM PERSON;""")
result2 = c.fetchall()
print(result2)

root = tk.Tk()
root.geometry("600x500")

tree = ttk.Treeview(root, columns=columnList, show='headings')
for column in columnList:
    tree.heading(column, text=column)

data= []
for i in range (len(result2)):
    data.append(result2[i])

for record in data:
    tree.insert('', tk.END, values=record)

tree.grid(row = 0, column = 0, sticky="news")

root.mainloop()

print(keyNames)
print(keyIndexes)
