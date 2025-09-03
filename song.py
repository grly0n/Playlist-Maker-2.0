import api


class InvalidIDException(Exception):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)


class Song:
  def __init__(self, link: str):
    self.spotify_link = link
    response = api.request_song_info(self.spotify_link)
    
    if response.status_code == 200:
      response = response.json()
      self.album = response['album']['name']
      self.artists = ', '.join(artist['name'] for artist in response['artists'])
      self.title = response['name']
      self.duration = self.calculate_duration(response['duration_ms'])
    elif response.status_code == 400:
      raise InvalidIDException('Invalid Spotify ID')
    else:
      print(response.status_code, response.text)
    

  def __repr__(self):
    return f'{self.artists} - {self.title} - {self.album} ({self.duration})'
  

  def calculate_duration(self, duration: float):
    total_duration_seconds = round(duration / 1000)
    duration_minutes = int(total_duration_seconds / 60)
    duration_seconds = total_duration_seconds % 60
    return f'{duration_minutes}:{duration_seconds:02d}'
  