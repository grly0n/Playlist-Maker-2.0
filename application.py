import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from song import Song


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title('Playlist Maker')
        self.geometry('300x200')
        self.resizable(True, True)

        # Main frame configuration
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky='NSWE')

        # Song list configuration
        self.song_list = []

        # Widget configuration
        self.create_widgets()


    def create_widgets(self):
        # Labels
        label1 = ttk.Label(self.main_frame, text='Spotify link:')
        label2 = ttk.Label(self.main_frame, text='Artist:')
        label3 = ttk.Label(self.main_frame, text='Title:')
        label4 = ttk.Label(self.main_frame, text='Album:')
        label5 = ttk.Label(self.main_frame, text='Duration:')
        label1.grid(row=0, column=0, padx=10, pady=10, sticky='NSWE')
        label2.grid(row=1, column=0, padx=10, sticky='E')
        label3.grid(row=2, column=0, padx=10, sticky='E')
        label4.grid(row=3, column=0, padx=10, sticky='E')
        label5.grid(row=4, column=0, padx=10, sticky='E')

        # Entries
        link_entry = ttk.Entry(self.main_frame)
        artist_entry = ttk.Entry(self.main_frame, state=tk.DISABLED)
        title_entry = ttk.Entry(self.main_frame, state=tk.DISABLED)
        album_entry = ttk.Entry(self.main_frame, state=tk.DISABLED)
        duration_entry = ttk.Entry(self.main_frame, state=tk.DISABLED)
        link_entry.grid(row=0, column=1)
        artist_entry.grid(row=1, column=1)
        title_entry.grid(row=2, column=1)
        album_entry.grid(row=3, column=1)
        duration_entry.grid(row=4, column=1)


        # Event handlers
        def create_song(event):
            self.song_list.append(Song(link_entry.get()))
            link_entry.delete(0, tk.END)
        
        # Event handler bindings
        link_entry.bind('<Return>', create_song)

        # Buttons


class API_key_prompt(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title('Playlist Maker')
        self.geometry('300x200')
        self.resizable(width=False, height=False)

        # Frame configuration
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=1, sticky='NSEW')

        # Widget configuration
        self.create_widgets()


    def create_widgets(self):
        # Labels
        title = ttk.Label(self.main_frame, text='Playlist Maker 2.0', font=('Ariel', 20, 'bold'))
        label1 = ttk.Label(self.main_frame, text='Spotify API Client ID:')
        label2 = ttk.Label(self.main_frame, text='Spotify API Client Secret:')
        title.grid(row=0, column=1, pady=10, columnspan=2)
        label1.grid(row=1, column=1, padx=5, pady=5, sticky='NSEW')
        label2.grid(row=2, column=1, padx=5, pady=5, sticky='NSEW')

        # Entries
        client_id_entry = ttk.Entry(self.main_frame)
        client_secret_entry = ttk.Entry(self.main_frame)
        client_id_entry.grid(row=1, column=2)
        client_secret_entry.grid(row=2, column=2)

        # Event handlers
        def submit_credentials():
            with open('.env', 'w') as file:
                file.write(f'SPOTIFY_CLIENT_ID={client_id_entry.get()}\n')
                file.write(f'SPOTIFY_CLIENT_SECRET={client_secret_entry.get()}')

        # Buttons
        enter_button = ttk.Button(self.main_frame, text='Enter', command=submit_credentials)
        enter_button.grid(row=3, column=1, pady=10, columnspan=2)
