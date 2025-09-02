import api


class Song:
  def __init__(self, link: str):
    self.spotify_link = link
    response = api.request_song_info(self.spotify_link).json()
    
    self.album = response['album']['name']
    self.artists = ', '.join(artist['name'] for artist in response['artists'])
    self.title = response['name']
    self.duration = response['duration_ms'] / 1000
    

  def __repr__(self):
    return f'{self.artists} - {self.title} - {self.album} ({self.duration})'