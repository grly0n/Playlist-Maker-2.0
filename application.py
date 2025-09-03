import tkinter as tk
import api
import subprocess
import threading
import os
import time
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from song import Song, InvalidIDException


class DownloadThread(threading.Thread):
    def __init__(self, link: str):
        super().__init__()
        self.result = None
        self.link = link

    def run(self):
        download_command = ['spotdl', 'download', self.link, '--preload', '--output', '{artist} - {title}']
        subprocess.run(download_command)
        self.result = True


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
        duration_var = tk.StringVar()
        progress_var = tk.StringVar()
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
        self.entries_dict = {'link': link_entry, 'artist': artist_entry, 'title': title_entry, 'album': album_entry, 'duration': duration_entry}
        self.variables_dict = {'artist': artist_var, 'title': title_var, 'album': album_var, 'duration': duration_var, 'progress': progress_var}

        # Listbox
        self.song_listbox = tk.Listbox(self.main_frame, width=40)
        self.song_listbox.grid(row=0, column=3, rowspan=5)
        h_scrollbar = ttk.Scrollbar(self.main_frame, orient='horizontal', command=self.song_listbox.xview)
        v_scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.song_listbox.yview)
        h_scrollbar.grid(row=6, column=3, sticky='ew')
        v_scrollbar.grid(row=0, column=4, rowspan=5, sticky='ns')
        self.song_listbox.config(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Event handler bindings
        link_entry.bind('<Return>', self.create_song)
        self.song_listbox.bind('<<ListboxSelect>>', self.select_song)

        # Buttons
        link_button = ttk.Button(self.main_frame, text='Enter', command=self.create_song)
        edit_button = ttk.Button(self.main_frame, text='Submit changes', command=self.edit_song, state=tk.DISABLED)
        delete_button = ttk.Button(self.main_frame, text='Delete song', command=self.delete_song, state=tk.DISABLED)
        export_button = ttk.Button(self.main_frame, text='Export songs', command=self.export_songs)
        link_button.grid(row=0, column=2)
        edit_button.grid(row=5, column=0)
        delete_button.grid(row=5, column=1)
        export_button.grid(row=5, column=2)
        self.buttons_dict = {'link': link_button, 'edit': edit_button, 'delete': delete_button, 'export': export_button}


    def create_progress_bar(self):
        self.progress_bar = ttk.Progressbar(self.main_frame, length=250)
        self.progress_bar.grid(row=7, column=0, columnspan=3)
        self.variables_dict['progress'].set(f'Progress: {self.download_successes}/{self.song_list_length}')
        self.progress_label = ttk.Label(self.main_frame, textvariable=self.variables_dict['progress'])
        self.progress_label.grid(row=8, column=0, sticky='EW')


    # Event handlers
    def create_song(self, *args):
        try:
            new_song = Song(self.entries_dict['link'].get())
        except IndexError:
            messagebox.showerror(title='Error', message='Error: invalid Spotify link provided')
        except InvalidIDException:
            messagebox.showerror(title='Error', message='Error: invalid Spotify track ID provided')
        else:
            self.song_listbox.insert(tk.END, new_song)
            self.song_list.append(new_song)
        finally:
            self.entries_dict['link'].delete(0, tk.END)

    def select_song(self, *args):
        self.get_selected_song()
        self.change_editing_widgets_state(tk.ACTIVE)
        self.variables_dict['artist'].set(self.selected_song.artists)
        self.variables_dict['title'].set(self.selected_song.title)
        self.variables_dict['album'].set(self.selected_song.album)
        self.variables_dict['duration'].set(self.selected_song.duration)

    def edit_song(self, *args):
        self.selected_song.artists = self.variables_dict['artist'].get()
        self.selected_song.title = self.variables_dict['title'].get()
        self.selected_song.album = self.variables_dict['album'].get()
        self.selected_song.duration = self.variables_dict['duration'].get()
        self.clear_editing_entries()
        self.change_editing_widgets_state(tk.DISABLED)
        self.song_listbox.delete(self.selected_index)
        self.song_listbox.insert(self.selected_index, self.selected_song)

    def delete_song(self, *args):
        self.clear_editing_entries()
        self.change_editing_widgets_state(tk.DISABLED)
        self.song_listbox.delete(self.selected_index)
        self.song_list.remove(self.selected_song)

    def export_songs(self, *args):
        dirpath = fd.askdirectory(title='Select song download directory')
        filepath = fd.asksaveasfilename(title='Select playlist save location', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
        self.song_list_length = len(self.song_list)
        self.download_successes = 0
        self.create_progress_bar()
        if dirpath and filepath:
            os.chdir(dirpath)
            with open(f'{filepath}.txt', 'w') as file:
                for song in self.song_list:
                    file.write(f'{song}\n\n')
                    thread = DownloadThread(song.spotify_link)
                    thread.start()
                    self.monitor_thread(thread)
                    
        else:
            messagebox.showerror(title='Error', message='Error: Must provide save locations for songs and playlist')


    def monitor_thread(self, thread: DownloadThread):
        if thread.is_alive():
            self.after(100, lambda: self.monitor_thread(thread))
        else:
            if thread.result is True:
                self.download_successes += 1
                self.variables_dict['progress'].set(f'Progress: {self.download_successes}/{self.song_list_length}')
                self.progress_bar['value'] += 1 / self.song_list_length * 100
    

    # Event handler helpers
    def get_selected_song(self) -> None:
        if len(self.song_listbox.curselection()):
            self.selected_index = self.song_listbox.curselection()[0]
            self.selected_song = self.song_list[self.selected_index]

    def change_editing_widgets_state(self, state) -> None:
        for entry in {'artist', 'title', 'album', 'duration'}:
            self.entries_dict[entry].config(state=state)
        for button in {'edit', 'delete'}:
            self.buttons_dict[button].config(state=state)

    def clear_editing_entries(self):
        for entry in {'artist', 'title', 'album', 'duration'}:
            self.entries_dict[entry].delete(0, tk.END) 



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
