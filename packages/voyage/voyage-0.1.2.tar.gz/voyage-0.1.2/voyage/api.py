import requests

from voyage.models import DataSetModel

VOYAGE_URL = 'https://s3.amazonaws.com/voyage-datasets/list.json'

class VoyageCore(object):
  def get_datasets_list(self):
    request = requests.get(VOYAGE_URL)
    json = request.json()
    datasets_json = json['datasets']
    datasets = []
    for datasets_json in datasets_json:
        datasets.append(DataSetModel(datasets_json))
    return datasets

class Voyage(VoyageCore):
  pass
