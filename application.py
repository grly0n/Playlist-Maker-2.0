import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title('Playlist Maker')
        self.geometry('300x200')
        self.resizable(True, True)

        # Main frame configuration
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0)

        # Widget configuration
        self.create_widgets()


    def create_widgets(self):
        self.welcome_label = ttk.Label(self.main_frame, text='Playlist Maker 2.0', font=('Arial', 14))
        self.welcome_label.grid(row=0, column=0, sticky='n')
