class DataSetModel:
  def __init__(self, json):
    self.json = json

  def name(self):
    return self.json['name']

  def filename(self):
    return self.json['filename']

  def md5(self):
    return self.json['md5']

  def download_url(self):
    return self.json['download_url']
