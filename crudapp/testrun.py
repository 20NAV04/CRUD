import MySQLdb
import tkinter as tk
import datetime
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
    fieldTypes = []
    recordList = []
    keyNames = []
    keyIndexes = []
    forms = []
    selectedEntry = None
    selectedRecord = None
    selectedDBCopy = None
    typeMapping = {
        'bigint': int,
        'bit': bool,
        'char': str,
        'date': datetime,
        'datetime': datetime,
        'decimal': float,
        'float': float,
        'int': int,
        'longtex': str,
        'mediumint': int,
        'mediumtext': str,
        'smallint': int,
        'text': str,
        'time': datetime,
        'tinyint': int,
        'tinytext': str,
        'varchar': str,
    }
    
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

        self.header = tk.Frame(self.lframe)
        self.header.grid(column=0,row=0, sticky = "news")
        self.header.grid_propagate(False)
        self.header.rowconfigure(0, weight = 3)
        self.header.rowconfigure(1, weight = 1)
        self.header.columnconfigure(0, weight = 0)

        self.title = tk.Label(self.header, text = "CRUD APPLICATION", font = ("TKDefaultFont", 25))
        self.title.grid(row = 0, column = 0)

        self.note = tk.Label(self.header, text = "For adding and updating values, blank fields are interpreted as NULL.  For searching values, blank fields are not included; type NULL for filtering NULL values. Select a record on the right to update and delete", wraplength=550)
        self.note.grid(column = 0, row = 1, sticky = "news", padx = 5)

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

        self.addRecBtn = tk.Button(self.controlframe, text="Add Record", command =self.addRec)
        self.addRecBtn.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.delRecBtn = tk.Button(self.controlframe, text="Delete Record", command=self.delRec)
        self.delRecBtn.grid(row=0, column=1, padx=10, pady=10, sticky="news")
        self.updateRecBtn = tk.Button(self.controlframe, text="Update Record", command=self.updateRec)
        self.updateRecBtn.grid(row=0, column=2, padx=10, pady=10, sticky="news")
        self.searchRecBtn = tk.Button(self.controlframe, text="Search Record", command=self.selectRec)
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
        try:
            self.innerFFrame.destroy()
        except:
            pass
        try:
            self.formframePH.destroy()
        except:
            pass
        self.formframePH = tk.Label(self.formCanvas, text="Input forms will appear here after selecting a table.")
        self.formframePH.pack(expand=True)
        
        self.destroyDisplay()
        self.dataframePH = tk.Label(self.dataframe, text="Select a Database and a Table to Start.", bg="white")

        self.dataframePH.place(anchor="center", relx=.5,rely=.5)
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
        self.selectedTable.set("Select Table")
        self.tableDrpDwn = ttk.Combobox(self.navframe, textvariable=self.selectedTable, values=self.tableList, state="readonly")
        self.tableDrpDwn.grid(column=3, row=0, sticky="ew")

    def popupAddDB(self):
        try:
            self.winDelDB.destroy()
        except:
            pass
        
        try:
            self.alertPopup.destroy()
        except:
            pass
    
        self.alertPopup = tk.Toplevel(self.root)
        self.alertPopup.title("Add Database")
        self.alertPopup.geometry = ("300x250")
        self.alertPopup.resizable(False, False)
        self.alertPopupL = tk.Label(self.alertPopup, text="Database Name:")
        self.alertPopupL.grid(column=0,row=0,sticky="news", padx=5, pady=5)
        self.alertPopupE = tk.Entry(self.alertPopup)
        self.alertPopupE.grid(column=1,row=0,sticky="news", padx=5, pady=5)
        self.alertPopupBtn = tk.Button(self.alertPopup, command = self.addDB, text="Add")
        self.alertPopupBtn.grid(column=0,row=1, columnspan=2, sticky="news", padx=5, pady=5)
        self.addDBError = tk.Label(self.alertPopup, wraplength=250)
        self.addDBError.grid(column=0, row=2, rowspan=2, columnspan=2, padx=5, pady=5)
        self.alertPopup.mainloop()
   
    def popupDelDB(self):
        try:
            self.alertPopup.destroy()
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
            c.execute("CREATE DATABASE %s;" % (self.alertPopupE.get()))
            c.close()
            self.alertPopup.destroy()
            self.recreateDBDrp()
        except MySQLdb.OperationalError as err:
            c.close()
            self.addDBError.config(text=err.args[1])
        except MySQLdb._exceptions.ProgrammingError as err:
            c.close()
            self.addDBError.config(text=err.args[1])

    def delDB(self):
        c = db.cursor()
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
        if(self.selectedTable.get() != "Select Table"):
            self.getPrimaryKey(self.selectedDB.get(), self.selectedTable.get())
            self.fetchColumns()
            self.fetchRecords()
            self.fetchDataType()
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

    def fetchDataType(self):
        self.fieldTypes = []
        c = db.cursor()
        c.execute("""SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = "%s" AND TABLE_NAME = "%s";""" % (self.selectedDB.get(), self.selectedTable.get()))

        for datatype in c.fetchall():
            self.fieldTypes.append(datatype[0])
        c.close()
    
    def destroyDisplay(self):
        self.selectedRecord = None
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
        self.tree.bind("<<TreeviewSelect>>", self.getEntryId)

    def getEntryId(self, target):
        self.selectedEntry = self.tree.focus() 
        self.onSelectChange()
    
    def createForms(self):
        try:
            self.innerFFrame.destroy()
        except:
            pass
        try:
            self.formframePH.destroy()
        except:
            pass

        self.forms = []

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

    def delRec(self):
        if self.selectedTable.get() != "Select Table" and self.selectedEntry is not None:
            self.toDeleteVal = []
            self.query = ""
            for index in self.keyIndexes:
                self.toDeleteVal.append(self.tree.item(self.selectedEntry)['values'][index])
            for index, key in enumerate(self.toDeleteVal):
                if index == 0:
                    self.query += "DELETE FROM %s WHERE %s = %s" % (self.selectedTable.get(), self.keyNames[index], self.toDeleteVal[index])
                else:
                    self.query += " AND %s = %s" % (self.keyNames[index], self.toDeleteVal[index])
            self.query += ";"
            
            try:
                c = db.cursor()
                print(self.query)
                c.execute(self.query)
                c.close()
                self.tree.delete(self.selectedEntry)
            except MySQLdb.Error as e:
                self.alertMessage(e.args[1])
    
    def onSelectChange(self):
        for i in range(len(self.fieldList)):
            self.forms[i][1].delete(0, tk.END)
            self.forms[i][1].insert(0, self.tree.item(self.selectedEntry)['values'][i])

    def updateRec(self):
        if self.selectedTable.get() != "Select Table" and self.selectedEntry is not None:
            self.newVal = []
            self.newValCpy = []
            self.query = ""
            for i in range(len(self.fieldList)):
                if self.forms[i][1].get() == '':
                    self.newVal.append('NULL')
                    self.newValCpy.append(self.forms[i][1].get())
                elif type(self.tree.item(self.selectedEntry)['values'][i]) == int:
                    self.newVal.append(int(self.forms[i][1].get()))
                    self.newValCpy.append(int(self.forms[i][1].get()))
                elif type(self.tree.item(self.selectedEntry)['values'][i]) == float:
                    self.newVal.append(float(self.forms[i][1].get()))
                    self.newValCpy.append(float(self.forms[i][1].get()))
                elif type(self.tree.item(self.selectedEntry)['values'][i]) == str:
                    self.newVal.append("\""+str(self.forms[i][1].get())+"\"")
                    self.newValCpy.append(str(self.forms[i][1].get()))
                else: 
                    self.newVal.append(self.forms[i][1].get())
                    self.newValCpy.append(self.forms[i][1].get())

            self.query += "UPDATE %s SET " % (self.selectedTable.get())
            for i in range(len(self.fieldList)):
                self.query += "%s = %s" % (self.fieldList[i], self.newVal[i])
                if i != (len(self.fieldList)-1):
                    self.query += ", "
            for i, key in enumerate(self.keyNames):
                if i == 0:
                    self.query += " WHERE %s = %s" % (key, self.tree.item(self.selectedEntry)['values'][self.keyIndexes[i]])
                else:
                    self.query += " AND %s = %s" % (key, self.tree.item(self.selectedEntry)['values'][self.keyIndexes[i]])
            self.query += ";"

            try:
                c = db.cursor()
                c.execute(self.query)
                self.tree.item(self.selectedEntry, values=self.newValCpy)
                c.close()
                self.alertMessage()
            except MySQLdb.Error as e:
                self.alertMessage(e.args[1])
    
    def addRec(self):
        if self.selectedTable.get() != "Select Table":
            self.query=""
            self.toAddVal = []
            self.toAddValCopy = []
            for i in range(len(self.fieldList)):
                if self.forms[i][1].get() == '':
                    self.toAddVal.append('NULL')
                    self.toAddValCopy.append(self.forms[i][1].get())
                elif (self.typeMapping[self.fieldTypes[i]]) is str:
                    self.toAddVal.append("\""+self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get())+"\"")
                    self.toAddValCopy.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
                else:
                    self.toAddVal.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
                    self.toAddValCopy.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
            self.query += "INSERT INTO %s (" % (self.selectedTable.get())
            for i in range(len(self.fieldList)):
                self.query += "%s" % (self.fieldList[i])
                if (i != (len(self.fieldList)-1)):
                    self.query += ", "
                else:
                    self.query += ") VALUES ("
            for i in range(len(self.fieldList)):
                self.query += "%s" % (self.toAddVal[i])
                if (i != (len(self.fieldList)-1)):
                    self.query += ", "
                else:
                    self.query += ");"
            
            try:
                c = db.cursor()
                c.execute(self.query)
                c.close()
                self.tree.insert('', tk.END, values=self.toAddValCopy)
                self.alertMessage()
            except MySQLdb.Error as e:
                self.alertMessage(e.args[1])

    def selectRec(self):
        if self.selectedTable.get() != "Select Table":
            self.toFilterVal = []
            self.recordList = []
            self.query = ""
            for i in range (len(self.fieldList)):
                if self.forms[i][1].get() == 'NULL':
                    self.toFilterVal.append('NULL')
                elif self.forms[i][1].get() == '':
                    self.toFilterVal.append(self.fieldList[i])
                elif (self.typeMapping[self.fieldTypes[i]]) is str:
                    self.toFilterVal.append("\""+self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get())+"\"")
                else:
                    self.toFilterVal.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
            self.query = "SELECT * FROM %s WHERE " % (self.selectedTable.get())
            for i in range (len(self.fieldList)):
                if i == 0:
                    self.query += "%s = %s " % (self.fieldList[i], self.toFilterVal[i])
                else:
                    self.query += "AND %s = %s " % (self.fieldList[i], self.toFilterVal[i])
            
            c = db.cursor()
            c.execute(self.query)
            for data in c.fetchall():
                self.recordList.append(data)
            self.destroyDisplay()
            self.createDisplay()
        
    def alertMessage(self, message = "Action Successful!"):
        try:
            self.alertAction.destroy()
        except:
            pass

        self.alertAction = tk.Toplevel(self.root)
        self.alertAction.title("Alert")
        self.alertAction.geometry = ("300x250")
        self.alertAction.resizable(False, False)
        self.alertActionM = tk.Label(self.alertAction, text = message)
        self.alertActionM.grid(column=0,row=0,sticky="news", padx=5, pady=5)
        self.alertAction.mainloop()

if db != None:       
    win = mainGUI()
    win.root.mainloop()

print("Program Terminated.")