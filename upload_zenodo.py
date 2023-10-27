import os

import requests
from tqdm import tqdm  # pip install tqdm
from tqdm.utils import CallbackIOWrapper

params = {"access_token": "8dNcAQuZMrT7DwiubiKwb2H7xZI6r04BCn5T2q2cmMdpYpxE604J5H9ZUhbf"}

# Get bucket URL
res = requests.get(
    "https://zenodo.org/api/deposit/depositions/8374470", 
    json={},
    params=params,
)
# print(res.json())
bucket_url = res.json()["links"]["bucket"]

# Upload file
file_path = "/data/keeling/a/alfonso8/projects/notebooks/data/Tablazo.tar.gz"
file_size = os.stat(file_path).st_size
with open(file_path, "rb") as f:
    with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
        wrapped_file = CallbackIOWrapper(t.update, f, "read")
        requests.put(
            bucket_url + "/" + os.path.basename(file_path),
            data=wrapped_file,
            params=params,
        )
