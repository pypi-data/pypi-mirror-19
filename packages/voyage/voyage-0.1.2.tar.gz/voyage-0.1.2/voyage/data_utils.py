from tqdm import tqdm
import requests
import hashlib
import os
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def validate_hash(dataset_path, md5_hash):
  hasher = hashlib.md5()
  with open(dataset_path, 'rb') as f:
    buf = f.read()
    hasher.update(buf)
  if str(hasher.hexdigest()) == str(md5_hash):
    return True
  else:
    return False

def get_dataset(file_name, download_url, md5_hash):
  cache_dir = os.path.expanduser(os.path.join('~', '.voyage'))
  if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
  dataset_path = os.path.join(cache_dir, file_name)

  download = False
  if os.path.exists(dataset_path):
    # Verify file integrity
    if md5_hash is not None:
      if not validate_hash(dataset_path, md5_hash):
        print('The local cache is incomplete or outdated, Downloading...')
        download = True
  else:
    download = True

  if download:
    response = requests.get(download_url, stream=True)
    with open(dataset_path, 'wb') as f:
      for data in tqdm(response.iter_content(), desc="Downloading from Voyage", unit='bytes', unit_scale='kilo'):
        f.write(data)

  return  dataset_path