import MySQLdb
import tkinter as tk
from tkinter import ttk

import MySQLdb._exceptions


db = None


class LoginGUI:
    host = ""
    user = ""
    password = ""
    login = False
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.title("CRUD Application Login")
        self.root.resizable(False, False)

        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)

        self.frame = tk.Frame(self.root)
        self.frame.grid(column = 1, row = 0)
        self.frame.columnconfigure(0, weight=1)
        for i in range (6):
            self.frame.rowconfigure(i, weight=1)

        self.hostLabel = tk.Label(self.frame, text="Enter Host Name")
        self.hostLabel.grid(column=0, row=0)
        self.hostForm = tk.Entry(self.frame)
        self.hostForm.grid(column=1, row=0, padx=5,pady=5)

        self.userLabel = tk.Label(self.frame, text="Enter User Name")
        self.userLabel.grid(column=0, row=1)
        self.userForm = tk.Entry(self.frame)
        self.userForm.grid(column=1, row=1, padx=5,pady=5)

        self.passLabel = tk.Label(self.frame, text="Enter Password")
        self.passLabel.grid(column=0, row=2)
        self.passForm = tk.Entry(self.frame)
        self.passForm.grid(column=1, row=2, padx = 5, pady = 5)

        self.submitCredentials = tk.Button(self.frame, text="Submit", command=self.attemptLogin)
        self.submitCredentials.grid(column = 0, row = 3, sticky="ew", columnspan = 2)
        
        self.status = tk.Label(self.frame, wraplength=250)
        self.status.grid(column=0,row=4, columnspan = 2, rowspan=2)

    def attemptLogin(self):
        self.host = self.hostForm.get()
        self.user = self.userForm.get()
        self.password = self.passForm.get()
        global db
        try:
            db = MySQLdb.connect(self.host, self.user, self.password)
            self.root.quit()
            self.root.destroy()
        except MySQLdb.OperationalError as err:
            self.status.config(text=err.args[1])
       
    
LoginGUI().root.mainloop()


class mainGUI:
    databaseList = []
    tableList = ["Select Table"]
    fieldList = []
    recordList = []
    keyNames = []
    keyIndexes = []
    forms = []
    selectedRecord = None
    selectedDBCopy = None
    
    def __init__(self):
        '''MAIN WINDOW'''
        self.selectDatabases()
        self.root = tk.Tk()
        self.root.geometry("1200x600")
        self.root.title("CRUD Application")
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        '''LEFT FRAME'''
        self.lframe = tk.Frame(self.root)
        self.lframe.grid(column=0,row=0, sticky="news")
        self.lframe.grid_propagate(False)

        self.lframe.columnconfigure(0, weight=1)
        self.lframe.rowconfigure(0, weight=1)
        self.lframe.rowconfigure(1, weight=3)
        self.lframe.rowconfigure(2, weight=1)

        self.search = tk.Frame(self.lframe, bg="black")
        self.search.grid(column=0,row=0)
        self.search.grid_propagate(False)

        self.formframe = tk.Frame(self.lframe)
        self.formframe.grid(column=0, row=1, sticky="news")
        self.formframe.rowconfigure(0, weight=1)
        self.formframe.columnconfigure(0, weight=1)
        self.formframe.columnconfigure(1)
        self.formframe.grid_propagate(False)

        self.formCanvas = tk.Canvas(self.formframe)
        self.formCanvas.grid(column=0, row=0, sticky="news")
        self.formCanvasScrollbar = ttk.Scrollbar(self.formframe, orient="vertical", command=self.formCanvas.yview)
        self.formCanvasScrollbar.grid(column=1,row=0,sticky="ns")

        self.formframePH = tk.Label(self.formCanvas, text="Input forms will appear here after selecting a table.")
        self.formframePH.pack(expand=True)
        
        self.controlframe = tk.Frame(self.lframe)
        self.controlframe.grid(column=0, row=2, sticky="news")
        self.controlframe.grid_propagate(False)

    
        self.controlframe.columnconfigure(0, weight=1)
        self.controlframe.columnconfigure(1, weight=1)
        self.controlframe.columnconfigure(2, weight=1)
        self.controlframe.columnconfigure(3, weight=1)
        self.controlframe.rowconfigure(0, weight=1)

        self.addRecBtn = tk.Button(self.controlframe, text="Add Record")
        self.addRecBtn.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.delRecBtn = tk.Button(self.controlframe, text="Delete Record")
        self.delRecBtn.grid(row=0, column=1, padx=10, pady=10, sticky="news")
        self.updateRecBtn = tk.Button(self.controlframe, text="Update Record")
        self.updateRecBtn.grid(row=0, column=2, padx=10, pady=10, sticky="news")
        self.searchRecBtn = tk.Button(self.controlframe, text="Search Record", command=self.debug)
        self.searchRecBtn.grid(row=0, column=3, padx=10, pady=10, sticky="news")
      

        '''RIGHT FRAME'''
        self.rframe = tk.Frame(self.root, bg="blue")
        self.rframe.grid(column=1,row=0, sticky="news")
        self.rframe.grid_propagate(False)

        self.rframe.columnconfigure(0, weight=1)
        self.rframe.rowconfigure(0, weight=1)
        self.rframe.rowconfigure(1, weight=5)

        self.navframe = tk.Frame(self.rframe)
        self.navframe.grid(column=0, row=0, sticky="news")
        self.navframe.grid_propagate(False)
        self.navframe.rowconfigure(0,weight=1)
        for x in range (4):
            self.navframe.columnconfigure(x,weight=1)

        self.addDBBtn = tk.Button(self.navframe, text="Add Database", command = self.popupAddDB)
        self.addDBBtn.grid(column=0, row=0, sticky="ew", padx=5)

        self.delDBBtn = tk.Button(self.navframe, text="Delete Database", command = self.popupDelDB)
        self.delDBBtn.grid(column=1, row=0, sticky="ew", padx=5)

        self.selectedDB = tk.StringVar()
        self.selectedDB.set("Select Database")
        self.dbDrpDwn = ttk.Combobox(self.navframe, textvariable=self.selectedDB, values=self.databaseList, state="readonly")
        self.dbDrpDwn.grid(column=2, row=0, sticky="ew", padx=5)
        self.selectedDB.trace_add('write', self.onDatabaseChange)

        self.selectedTable = tk.StringVar()
        self.selectedTable.set("Select Table")
        self.tableDrpDwn = ttk.Combobox(self.navframe, textvariable=self.selectedTable, values=self.tableList, state="readonly")
        self.tableDrpDwn.grid(column=3, row=0, sticky="ew", padx=5)
        self.selectedTable.trace_add('write', self.onTableChange)

        self.dataframe = tk.Frame(self.rframe, bg="white")
        self.dataframe.grid(column=0, row=1, sticky="news")
        self.dataframe.grid_propagate(False)
        self.dataframe.rowconfigure(0, weight=1)
        self.dataframe.rowconfigure(1)
        self.dataframe.columnconfigure(0, weight=1)
        self.dataframe.columnconfigure(1)

        self.dataframePH = tk.Label(self.dataframe, text="Select a Database and a Table to Start.", bg="white")
        self.dataframePH.place(anchor="center", relx=.5,rely=.5)

    def selectDatabases(self):
        c = db.cursor()
        c.execute("SHOW DATABASES;")
        options = c.fetchall()
        for option in options:
            self.databaseList.append(option[0])
        c.close()

    def onDatabaseChange(self,p1,p2,p3):
        self.destroyDisplay()
        c = db.cursor()
        c.execute("USE {}".format(self.selectedDB.get()))
        c.close()
        self.selectTables()

    def selectTables(self):
        self.tableList = []
        c = db.cursor()
        c.execute("SHOW TABLES;")
        options = c.fetchall()
        for option in options:
            self.tableList.append(option[0])
        c.close()
        self.recreateTableDrp()
    
    def recreateTableDrp(self):
        self.tableDrpDwn.destroy()
        self.tableDrpDwn = ttk.Combobox(self.navframe, textvariable=self.selectedTable, values=self.tableList, state="readonly")
        self.tableDrpDwn.grid(column=3, row=0, sticky="ew")

    def popupAddDB(self):
        try:
            self.winDelDB.destroy()
        except:
            pass
        
        try:
            self.winAddDB.destroy()
        except:
            pass
    
        self.winAddDB = tk.Toplevel(self.root)
        self.winAddDB.title("Add Database")
        self.winAddDB.geometry = ("300x250")
        self.winAddDB.resizable(False, False)
        self.winAddDBL = tk.Label(self.winAddDB, text="Database Name:")
        self.winAddDBL.grid(column=0,row=0,sticky="news", padx=5, pady=5)
        self.winAddDBE = tk.Entry(self.winAddDB)
        self.winAddDBE.grid(column=1,row=0,sticky="news", padx=5, pady=5)
        self.winAddDBBtn = tk.Button(self.winAddDB, command = self.addDB, text="Add")
        self.winAddDBBtn.grid(column=0,row=1, columnspan=2, sticky="news", padx=5, pady=5)
        self.addDBError = tk.Label(self.winAddDB, wraplength=250)
        self.addDBError.grid(column=0, row=2, rowspan=2, columnspan=2, padx=5, pady=5)
        self.winAddDB.mainloop()
   
    def popupDelDB(self):
        try:
            self.winAddDB.destroy()
        except:
            pass
        
        try:
            self.winDelDB.destroy()
        except:
            pass

        self.winDelDB = tk.Toplevel(self.root)
        self.winDelDB.title("Delete Database")
        self.winDelDB.geometry = ("300x250")
        self.winDelDB.resizable(False, False)
        self.winDelDBL = tk.Label(self.winDelDB, text="Choose Database: ")
        self.winDelDBL.grid(column=0, row=0, sticky="news", padx=5,pady=5)
        self.toDel = tk.StringVar()
        self.dbDrpDwn = ttk.Combobox(self.winDelDB, textvariable=self.toDel, values=self.databaseList, state="readonly")
        self.dbDrpDwn.grid(column=1,row=0, padx=5,pady=5,sticky="news")
        self.winDelDBBtn = tk.Button(self.winDelDB, command = self.delDB, text="Delete")
        self.winDelDBBtn.grid(column=0,row=1, columnspan=2, sticky="news", padx=5, pady=5)
        self.delDBError = tk.Label(self.winDelDB, wraplength=250)
        self.delDBError.grid(column=0, row=2, rowspan=2, columnspan=2, padx=5, pady=5)
        self.winDelDB.mainloop()

    def addDB(self):
        c = db.cursor()
        try:
            c.execute("CREATE DATABASE %s;" % (self.winAddDBE.get()))
            c.close()
            self.winAddDB.destroy()
            self.recreateDBDrp()
        except MySQLdb.OperationalError as err:
            c.close()
            self.addDBError.config(text=err.args[1])
        except MySQLdb._exceptions.ProgrammingError as err:
            c.close()
            self.addDBError.config(text=err.args[1])

    def delDB(self):
        c = db.cursor()
        print(self.toDel.get())
        try:
            c.execute("DROP DATABASE %s;" % (self.toDel.get()))
            c.close()
            self.winDelDB.destroy()
            self.recreateDBDrp()
        except MySQLdb.OperationalError as err:
            c.close()
            self.delDBError.config(text=err.args[1])
      
    def recreateDBDrp(self):
        self.databaseList = []
        self.selectDatabases()
        self.dbDrpDwn.destroy()
        self.dbDrpDwn = ttk.Combobox(self.navframe, textvariable=self.selectedDB, values=self.databaseList, state="readonly")
        self.dbDrpDwn.grid(column=2, row=0, sticky="ew", padx=5)

    def getPrimaryKey(self, dbname, tablename):
        self.keyNames = []
        c = db.cursor()
        c.execute("""SELECT k.column_name
        FROM information_schema.table_constraints t
        JOIN information_schema.key_column_usage k
        USING(constraint_name, table_schema, table_name)
        WHERE t.constraint_type="PRIMARY KEY"
        AND t.table_schema= "%s"
        AND t.table_name= "%s";
        """ % (dbname, tablename))
        for key in c.fetchall():
            self.keyNames.append(key[0])
        c.close()

    def onTableChange(self,p1,p2,p3):
        self.getPrimaryKey(self.selectedDB.get(), self.selectedTable.get())
        self.fetchColumns()
        self.fetchRecords()
        self.destroyDisplay()
        self.createDisplay()
        self.createForms()
    
    def fetchColumns(self):
        self.fieldList = []
        self.keyIndexes = []
        c = db.cursor()
        c.execute("""SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = "%s" 
        AND TABLE_NAME = "%s";""" % (self.selectedDB.get(), self.selectedTable.get())) 
        
        for index, column in enumerate(c.fetchall()):
            self.fieldList.append(column[0])
            if column[0] in self.keyNames:
                self.keyIndexes.append(index)
        c.close()

    def fetchRecords(self):
        self.recordList = []
        c = db.cursor()
        c.execute("SELECT * FROM %s;" % (self.selectedTable.get()))
        for data in c.fetchall():
            self.recordList.append(data)
        c.close()
    
    def destroyDisplay(self):
        for child in self.dataframe.winfo_children():
            child.destroy()

    def createDisplay(self):
        self.tree = ttk.Treeview(self.dataframe, columns=self.fieldList, show="headings")
        for column in self.fieldList:
            self.tree.heading(column, text=column)
        for record in self.recordList:
            self.tree.insert('', tk.END, values=record)
        self.tree.grid(row=0, column=0, sticky="news")

        self.treeScrollbarX = tk.Scrollbar(self.dataframe, orient = "horizontal", command=self.tree.xview)
        self.treeScrollbarY = tk.Scrollbar(self.dataframe, orient = "vertical", command=self.tree.yview)
        self.treeScrollbarX.grid(row=1, column = 0, sticky="ew")
        self.treeScrollbarY.grid(row=0, column = 1, sticky="ns")
    
    def createForms(self):
        try:
            self.innerFFrame.destroy()
        except:
            pass
        try:
            self.formframePH.destroy()
        except:
            pass

        self.innerFFrame = ttk.Frame(self.formCanvas)
        self.innerFFrame.bind("<Configure>", lambda e: self.formCanvas.configure(scrollregion=self.formCanvas.bbox("all")))
        self.formCanvas.create_window((0,0), window=self.innerFFrame, anchor="nw")
        self.formCanvas.configure(yscrollcommand=self.formCanvasScrollbar.set)
        self.innerFFrame.columnconfigure(0, weight=1)
        self.innerFFrame.columnconfigure(1, weight=1)
    
        for index, field in enumerate(self.fieldList):
            self.field = tk.Label(self.innerFFrame, text=field, wraplength=150)
            self.field.grid(column=0, row=index, sticky="ew", padx=50, pady=10)
            self.entry = tk.Entry(self.innerFFrame, width=30)
            self.entry.grid(column=1, row=index, sticky="ew", padx=50, pady=10)
            self.forms.append((self.field, self.entry))

    def popupAddRec(self):
        c = db.cursor()

    def debug(self):
        print(self.fieldList)
        print(self.recordList)
        print(self.keyNames)
        print(self.keyIndexes)
        print(self.forms)
        print(self.forms[0][0].cget("text"))
        print(self.forms[0][1].get())

if db != None:       
    win = mainGUI()
    win.root.mainloop()

print("program closed")