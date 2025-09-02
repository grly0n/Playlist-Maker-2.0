import tkinter as tk
import api
from tkinter import ttk
from tkinter import messagebox
from song import Song


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title('Playlist Maker')
        self.geometry('600x300')
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
        artist_var = tk.StringVar()
        title_var = tk.StringVar()
        album_var = tk.StringVar()
        duration_var = tk.DoubleVar()
        link_entry = ttk.Entry(self.main_frame)
        artist_entry = ttk.Entry(self.main_frame, state=tk.DISABLED, textvariable=artist_var)
        title_entry = ttk.Entry(self.main_frame, state=tk.DISABLED, textvariable=title_var)
        album_entry = ttk.Entry(self.main_frame, state=tk.DISABLED, textvariable=album_var)
        duration_entry = ttk.Entry(self.main_frame, state=tk.DISABLED, textvariable=duration_var)
        link_entry.grid(row=0, column=1)
        artist_entry.grid(row=1, column=1)
        title_entry.grid(row=2, column=1)
        album_entry.grid(row=3, column=1)
        duration_entry.grid(row=4, column=1)

        # Listbox
        song_listbox = tk.Listbox(self.main_frame, width=40)
        song_listbox.grid(row=0, column=3, rowspan=5)
        h_scrollbar = ttk.Scrollbar(self.main_frame, orient='horizontal', command=song_listbox.xview)
        v_scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=song_listbox.yview)
        h_scrollbar.grid(row=6, column=3, sticky='ew')
        v_scrollbar.grid(row=0, column=4, rowspan=5, sticky='ns')
        song_listbox.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

        # Event handlers
        def create_song(*args):
            new_song = Song(link_entry.get())
            song_listbox.insert(tk.END, new_song)
            self.song_list.append(new_song)
            link_entry.delete(0, tk.END)

        def select_song(*args):
            self.get_selected_song(song_listbox)
            artist_entry.config(state=tk.ACTIVE)
            title_entry.config(state=tk.ACTIVE)
            album_entry.config(state=tk.ACTIVE)
            duration_entry.config(state=tk.ACTIVE)
            artist_var.set(self.selected_song.artists)
            title_var.set(self.selected_song.title)
            album_var.set(self.selected_song.album)
            duration_var.set(self.selected_song.duration)
            edit_button.config(state=tk.ACTIVE)

        def edit_song(*args):
            self.selected_song.artists = artist_var.get()
            self.selected_song.title = title_var.get()
            self.selected_song.album = album_var.get()
            self.selected_song.duration = duration_var.get()
            artist_entry.delete(0, tk.END)
            title_entry.delete(0, tk.END)
            album_entry.delete(0, tk.END)
            duration_entry.delete(0, tk.END)
            edit_button.config(state=tk.DISABLED)
            song_listbox.delete(self.selected_index)
            song_listbox.insert(self.selected_index, self.selected_song)

        
        # Event handler bindings
        link_entry.bind('<Return>', create_song)
        song_listbox.bind('<<ListboxSelect>>', select_song)

        # Buttons
        link_button = ttk.Button(self.main_frame, text='Enter', command=create_song)
        edit_button = ttk.Button(self.main_frame, text='Submit changes', command=edit_song, state=tk.DISABLED)
        link_button.grid(row=0, column=2)
        edit_button.grid(row=5, column=0)

    def get_selected_song(self, song_listbox: tk.Listbox) -> None:
        if len(song_listbox.curselection()):
            self.selected_index = song_listbox.curselection()[0]
            self.selected_song = self.song_list[self.selected_index]


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
            client_id = client_id_entry.get()
            client_secret = client_secret_entry.get()
            access_token, expiration = api.request_access_token(client_id, client_secret)

            if not access_token:
                print('Error: invalid Client ID and/or Client Secret')
                messagebox.showerror(message='Error: Invalid Client ID and/or Client Secret')
            else:
                api.write_to_env(client_id, client_secret, access_token, expiration)
                self.destroy()

        # Buttons
        enter_button = ttk.Button(self.main_frame, text='Enter', command=submit_credentials)
        enter_button.grid(row=3, column=1, pady=10, columnspan=2)
