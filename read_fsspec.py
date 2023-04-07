import pyart
import fsspec
import xarray as xr
import xradar as xd
import boto3
import botocore
from botocore.client import Config
from datetime import datetime


def create_query(date, radar_site):
    """
    Creates a query for listing IDEAM radar files stored in AWS bucket
    :param date: date to be queried. e.g datetime(2021, 10, 3, 12). Datetime python object
    :param radar_site: radar site e.g. Guaviare
    :return: string with a
    """
    prefix = f'l2_data/{date:%Y}/{date:%m}/{date:%d}/{radar_site}/{radar_site[:3].upper()}{date:%y%m%d}'
    return prefix


def main():
    str_bucket = 's3://s3-radaresideam/'
    s3 = boto3.resource('s3',
                        config=Config(signature_version=botocore.UNSIGNED, user_agent_extra='Resource'))
    bucket = s3.Bucket('s3-radaresideam')
    query = create_query(date=datetime(2021, 10, 3, 12), radar_site='Guaviare')
    radar_files = [f'{str_bucket}{i.key}' for i in bucket.objects.filter(Prefix=f"{query}")]

    # using context manager for reading radar data from guaviare radar
    of = pyart.io.prepare_for_read(radar_files[2], storage_options={'anon': True})
    with of as f:
        radar = pyart.io.read(f)
        print(radar.range['meters_between_gates'])
        f.close()

    for idx, i in enumerate(radar_files[2:3]):
        file = fsspec.open_local(f'simplecache::{i}', s3={'anon': True}, filecache={'cache_storage': '.'})
        dtree = xd.io.open_iris_datatree(file)
        ds = xr.open_dataset(file, group=1, engine="iris")
        print('done')


if __name__ == "__main__":
    main()
