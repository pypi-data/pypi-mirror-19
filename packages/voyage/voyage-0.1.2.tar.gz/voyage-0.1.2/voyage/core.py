from voyage import data_utils
from voyage.dataset import DataSet
from voyage.api import Voyage

def load_dataset(name, shuffle=False, percentage=1.0, resize=False, streaming=False):
  datasets = Voyage().get_datasets_list()
  dataset = None
  for i in datasets:
    if i.name() == name:
      dataset = i

  if not dataset is None:
    path = data_utils.get_dataset(dataset.filename(), dataset.download_url(), dataset.md5())
    return DataSet(path)
