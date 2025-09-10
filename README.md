# Playlist Maker 2.0
This project is an update to an older (playlist project)[https://github.com/grly0n/playlist-maker] I made last year.

Upon launching the executable, you will need to enter a Spotify API Client ID and Secret (not provided). The API authentication information is written in a .env file in the current working directory. After supplying a valid ID and Secret, the main app will launch.

The main workflow of the Playlist Maker is:
1. Enter a link to a song on Spotify.
2. Select the entered song and edit information (artist, title, album, or duration).
3. Repeat 1-2 for as many songs as desired.
4. Export the playlist and select locations to download the music and save the playlist.

Spotify song information is fetched using the Spotify API, and songs are converted to MP3 using (spotdl)[https://github.com/spotDL/spotify-downloader].

Playlists are saved in a `.txt` file, and entries are in the form "Artist - Title - Album (Duration)".
