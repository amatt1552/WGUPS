import tkinter as tk
from tkinter import ttk
from turtle import width

#https://tkdocs.com/tutorial/widgets.html
#https://realpython.com/python-gui-tkinter/#building-your-first-python-gui-application-with-tkinter

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.targetHour = tk.StringVar(value="12")
        self.targetMinute = tk.StringVar(value="00")
        self.timeOfDay = tk.StringVar(value="PM")
        self.data = tk.StringVar(value="Welcome.")
        self.lookupType = tk.StringVar(value="ID")
        self.lookupValue = tk.StringVar(value="")
        self.pack(side=tk.TOP, anchor='w', fill='x')
        self.init_main_menu()

    def init_main_menu(self):
        self.clear_frame()
        #target time
        targetTimeLabel = tk.Label(master=self,text="Target Time: ")
        targetTimeLabel.pack(side=tk.LEFT)
        targetHour = tk.Entry(master=self,textvariable=self.targetHour)
        targetHour.pack(side=tk.LEFT)
        colonLabel = tk.Label(master=self,text=":")
        colonLabel.pack(side=tk.LEFT)
        targetMinute = tk.Entry(master=self,textvariable=self.targetMinute)
        targetMinute.pack(side=tk.LEFT)
        targetTimeOfDay = ttk.Combobox(master=self,textvariable=self.timeOfDay)
        targetTimeOfDay["values"] = ["AM","PM"]
        targetTimeOfDay["width"] = 5
        targetTimeOfDay.state(["readonly"])
        targetTimeOfDay.pack(side=tk.LEFT)
        #Run Button
        self.runBtn = tk.Button(master=self, text="Run")
        self.runBtn.pack(side=tk.LEFT, fill=tk.BOTH)
        #Optimize Button
        self.optimizeBtn = tk.Button(master=self, text="Optimize")
        self.optimizeBtn.pack(side=tk.LEFT, fill=tk.BOTH)
        #Reset Button
        self.resetBtn = tk.Button(master=self, text="Reset")
        self.resetBtn.pack(side=tk.LEFT, fill=tk.BOTH)
        #Lookup Label
        lookupLabel = tk.Label(master=self,text="  Find Package(s): ")
        lookupLabel.pack(side=tk.LEFT)
        #Lookup Entry
        lookupEntry = tk.Entry(master=self,textvariable=self.lookupValue)
        lookupEntry.pack(side=tk.LEFT)
        #Lookup Type        
        lookupCombo = ttk.Combobox(master=self,textvariable=self.lookupType)
        lookupCombo["values"] = ["ID","All"]
        lookupCombo["width"] = 10
        lookupCombo.state(["readonly"])
        lookupCombo.pack(side=tk.LEFT)
        #Lookup Button
        self.lookupBtn = tk.Button(master=self, text="Search")
        self.lookupBtn.pack(side=tk.LEFT, fill=tk.BOTH)
        #Close Button
        self.closeBtn = tk.Button(master= self, text="Close", command = self.close_application)
        self.closeBtn.pack(side=tk.RIGHT,anchor="ne")
        #Data
        dataFrame = tk.Frame(master=self).pack()
        data = tk.Label(master=dataFrame, textvariable=self.data,justify=tk.LEFT)
        data.pack(side=tk.LEFT,anchor="nw")

    def set_cell(self, column, row, newBorderWidth=1, sticky=""):
        self.columnconfigure(column, weight=1)
        self.rowconfigure(row, weight=1)
        frame = tk.Frame(
            master=self,
            relief=tk.RAISED,
            borderwidth=newBorderWidth
        )
        frame.grid(column=column, row=row, sticky = sticky)
        return frame

    def close_application(self):
        print("Closing")
        self.clear_frame()
        self.master.destroy()
    
    def clear_frame(self):
        for widgets in self.winfo_children():
             widgets.destroy()
    
    def set_time(self, hour, minute, timeOfDay):
        self.targetHour.set(value=hour)
        self.targetMinute.set(value=minute)
        self.timeOfDay.set(value=timeOfDay)

    def get_time(self):
        time = self.targetHour.get() +":"+ self.targetMinute.get() + " " + self.timeOfDay.get()
        return time

    def get_lookup(self):
        """
        Gets lookup value based on lookup type\n
        Return: returns -1 if using lookup type id and value is not an integer or empty.\n
                returns None if using invalid lookup.
        """
        if(self.lookupType.get() == "ID"):
            try:
                return int(self.lookupValue.get())
            except:
                return -1
        elif(self.lookupType.get() == "All"):
            return self.lookupValue.get()
        else:
            return None

    def set_data(self, newData):
        self.data.set(newData)

    def set_command(self, buttonName, command):
        if(buttonName == "run"):
            self.runBtn["command"] = command
        elif(buttonName == "optimize"):
            self.optimizeBtn["command"] = command
        elif(buttonName == "reset"):
            self.resetBtn["command"] = command
        elif(buttonName == "lookup"):
            self.lookupBtn["command"] = command
        elif(buttonName == "close"):
            pass

def get_window(runCommand, optimizeCommand, resetCommand, lookupCommand):
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = Application(master = root)
    app.set_time("11", "59", "PM")
    app.set_command("run",runCommand)
    app.set_command("optimize",optimizeCommand)
    app.set_command("reset",resetCommand)
    app.set_command("lookup",lookupCommand)
    return app


