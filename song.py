import api


class Song:
  def __init__(self, link: str):
    self.spotify_link = link
    print('Pulling Spotify information for link', self.spotify_link)

  def __repr__(self):
    return f'{self.spotify_link}'