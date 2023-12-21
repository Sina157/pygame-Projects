import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
if __name__ == "__main__":
    import RecordsDB as dbApi
else:
    import RecordsDB as dbApi


class SubmitGUI:
    def __init__(self, root, record):
        # setting title
        root.title("Submit Record")
        self.record = record
        self.root = root
        self.Submit = False
        # setting window size
        width = 348
        height = 192
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLineEdit_44 = tk.Entry(root)
        GLineEdit_44["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times', size=15)
        GLineEdit_44["font"] = ft
        GLineEdit_44["fg"] = "#000000"
        GLineEdit_44["justify"] = "center"
        GLineEdit_44["text"] = ""
        GLineEdit_44.place(x=70, y=70, width=253, height=30)

        GLabel_837 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=18)
        GLabel_837["font"] = ft
        GLabel_837["fg"] = "#000000"
        GLabel_837["justify"] = "center"
        GLabel_837["text"] = "Name"
        GLabel_837.place(x=0, y=70, width=70, height=25)

        GLabel_789 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=23)
        GLabel_789["font"] = ft
        GLabel_789["fg"] = "#000000"
        GLabel_789["justify"] = "center"
        GLabel_789["text"] = "Your record was " + str(self.record)
        GLabel_789.place(x=40, y=20, width=269, height=30)

        GButton_223 = tk.Button(root)
        GButton_223["bg"] = "#f0ffff"
        GButton_223["borderwidth"] = "5px"
        GButton_223["cursor"] = "arrow"
        ft = tkFont.Font(family='Times', size=23)
        GButton_223["font"] = ft
        GButton_223["fg"] = "#000000"
        GButton_223["justify"] = "center"
        GButton_223["text"] = "Submit"
        GButton_223["relief"] = "ridge"
        GButton_223.place(x=100, y=120, width=154, height=38)
        GButton_223["command"] = lambda: self.GButton_223_command(
            GLineEdit_44.get())
        showAllDataBTN = tk.Button(root)
        showAllDataBTN["font"] = tkFont.Font(family='Times', size=10)
        showAllDataBTN["bg"] = "#011b26"
        showAllDataBTN["fg"] = "#0bffd6"
        showAllDataBTN["borderwidth"] = "2px"
        showAllDataBTN["text"] = "Show Records"
        showAllDataBTN["cursor"] = "arrow"
        showAllDataBTN["command"] = lambda: ShowRecords()
        showAllDataBTN.place(x=0, y=0, width=100, height=20)

    def GButton_223_command(self, text):
        if text.split() == [] or len(text) > 20:
            messagebox.showerror('Response', 'Invalid Name')
        else:
            dbApi.CreateTable()
            dbApi.AddToRecords(self.record, text)
            self.Submit = True
            self.root.destroy()


class ShowDataGUI:
    def __init__(self, root, Records):
        # setting title
        root.title("Records")
        self.FullRecords = sorted(Records, key=lambda item: item[1])
        self.FirstMaxShow = 10
        self.records = self.FullRecords[-self.FirstMaxShow:]
        # setting window size
        width = 369
        height = 282
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GListBox_20 = tk.Listbox(root)
        GListBox_20["bg"] = "#011b26"
        GListBox_20["borderwidth"] = "2px"
        GListBox_20["cursor"] = "arrow"
        ft = tkFont.Font(family='Times', size=13)
        GListBox_20["font"] = ft
        GListBox_20["fg"] = "#0bffd6"
        GListBox_20["justify"] = "center"
        GListBox_20.place(x=20, y=50, width=331, height=219)
        GListBox_20["exportselection"] = "0"
        GListBox_20["selectmode"] = "extended"
        self.GListBox_20 = GListBox_20
        GButton_137 = tk.Button(root)
        GButton_137["bg"] = "#8ee0ca"
        ft = tkFont.Font(family='Times', size=18)
        GButton_137["font"] = ft
        GButton_137["fg"] = "#000000"
        GButton_137["justify"] = "center"
        GButton_137["text"] = "Show All"
        GButton_137.place(x=20, y=10, width=329, height=31)
        GButton_137["command"] = self.GButton_137_command
        self.Refresh()

    def Refresh(self):
        self.GListBox_20.delete(0, 'end')
        for i in range(len(self.records)):
            self.GListBox_20.insert(
                0, f"{self.records[i][0]} ========> {self.records[i][1]}")

    def GButton_137_command(self):
        self.records = self.FullRecords
        self.Refresh()


def Submit(Record):
    root = tk.Tk()
    app = SubmitGUI(root, Record)
    root.mainloop()
    return app.Submit


def ShowRecords():
    root = tk.Tk()
    Data = []
    dbApi.CreateTable()
    for item in dbApi.GetAllRecords():
        Data.append((item["Name"], int(item["Record"])))
    ShowDataGUI(root, Data)
    root.mainloop()


if __name__ == "__main__":
    # root = tk.Tk()
    # SubmitGUI = SubmitGUI(root, 0)
    # root.mainloop()
    # root = tk.Tk()
    # ShowDataGUI(root, [("sina", 12), ("ali", 2323), ("majid", 1)])
    # root.mainloop()
    # root = tk.Tk()
    # Data = []
    # for item in dbApi.GetAllRecords():
    #     print(item)
    #     Data.append((item["Name"], int(item["Record"])))
    # ShowDataGUI(root, Data)
    # root.mainloop()
    Submit(12)
