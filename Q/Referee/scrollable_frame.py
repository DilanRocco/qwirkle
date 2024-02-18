import tkinter as tk
from tkinter import ttk, HORIZONTAL, N, S, W, E, NW


class AutoScrollbar(tk.Scrollbar):
   # Only works if you use the grid geometry manager
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError("cannot use pack with this widget")

    def place(self, **kw):
        raise tk.TclError("cannot use place with this widget")


class ScrollFrame:
    def __init__(self, master):

        self.vscrollbar = AutoScrollbar(master)
        self.vscrollbar.grid(row=0, column=1, sticky=N+S)
        self.hscrollbar = AutoScrollbar(master, orient=HORIZONTAL)
        self.hscrollbar.grid(row=1, column=0, sticky=E+W)

        self.canvas = tk.Canvas(master, yscrollcommand=self.vscrollbar.set,
                                xscrollcommand=self.hscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)

        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

        # make the canvas expandable
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # create frame inside canvas
        self.frame = tk.Frame(self.canvas)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(1, weight=1)

    def update(self):
        self.canvas.create_window(0, 0, anchor=NW, window=self.frame)
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.frame.winfo_reqwidth())
        if self.frame.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canvas.config(height=self.frame.winfo_reqheight())