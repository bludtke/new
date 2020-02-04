import tkinter as tk
from tkinter import ttk, filedialog, Text
import os

class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    def __init__(self, parent, label=' ', input_class=ttk.Entry,
                 input_var=None, input_args=None, label_args=None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var


root = tk.Tk()

apps = []

def addApp():

    for widget in frame.winfo_children():
        widget.destroy()

    filename = filedialog.askopenfilename(initialdir = "/", title = "Select File",
                                          filetypes = (("Flare Data", "*.xls"), ("all files", "*.*")))

    apps.append(filename)
    
    for filename in apps:
        label = tk.Label(frame, text=filename, bg="gray")
        label.pack()
    
canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

openFile = tk.Button(root, text = "Open File", padx = 10,
                     pady = 5, fg = "black", bg = "#263D42", command = addApp)
openFile.pack()

runApps = tk.Button(root, text = "Process Data", padx = 10,
                    pady = 5, fg = "black", bg = "#263D42")
runApps.pack()

root.mainloop()
