import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nhp.settings")
import django
django.setup()

import sys
import anndata
import pandas as pd
import pysftp, os, random
import glob, shutil
from datetime import datetime
import time
from nhp_app.models import site



# file_path = "/home/ubuntu/aaxisnano/devices.json"
# data_base_path = "/home/ubuntu/binsrv/data/"
data_files = '/home/rohit/Desktop/nhp_projects/nhp/nhp_project/nhp/data_folder/'
all_adata_files = glob.glob(data_files + "*.adata")


# check for site in DB
def _check4site(fprefix):
    if(site.objects.filter(prefix=fprefix)):
        print('device already exist')
        deviceCong = {
                            "device" : fprefix,
                            "location" : "",
                            "sensor_position" : {
                                "0" : "timestamp",
                                "1" : "count",
                                "2" : "",
                                "3" : "",
                                "4" : "",
                                "5" : "",
                                "6" : "",
                                "7" : "",
                                "8" : "",
                                "9" : "",
                                "10" : "",
                                "11" : "",
                            }
                        }
        siteObj = site.objects.get(prefix=fprefix)
        siteObj.device_config = deviceCong
        siteObj.total_params = ['timestamp', 'count']
        siteObj.save()
        return site.objects.filter(prefix=fprefix)[0]
    else:
        try:
            deviceCong = {
                            "device" : fprefix,
                            "location" : "",
                            "sensor_position" : {
                                "0" : "timestamp",
                                "1" : "count",
                                "2" : "",
                                "3" : "",
                                "4" : "",
                                "5" : "",
                                "6" : "",
                                "7" : "",
                                "8" : "",
                                "9" : "",
                                "10" : "",
                                "11" : "",
                            }
                        }

            siteObj = site(name = "",
                            device_location = "",
                            prefix = fprefix,
                            tpro_prefix = "",
                            site_lattitude = "",
                            sit_longitude = "",
                            device_config = deviceCong,
                            total_params = ['timestamp', 'count']
                            )
            siteObj.save()
            print('new device created successfully')
        except Exception as err:
            print(f'Error occured while add new device : {err}')

        return siteObj


# upload data to DB
def _upload2db():
    pass


for f in all_adata_files[:]:
    fprefix = f.split('/')[-1].split('.')[0].lower()
    print('f name >>>> ',fprefix)
    _check4site(fprefix)
    filepath = os.path.join(data_files, os.path.basename(f))
    print("filepath ---> ",filepath)
    time.sleep(0.1)

    try:
        # df = pd.read_csv(filepath)
        df = pd.read_csv(filepath, names=['timestamp', 'count', 'analog1', 'analog2', 'battery', 'pulse'])
    except pd.errors.EmptyDataError as err:
        print(f'Error: File is empty \n{err}')
    except pd.errors.ParserError as err:
        print(f'Error: No columns to parse from file \n{err}')
    else:
        # Do something with the parsed data
        col_count = len(df.columns)
        print('col_count >>> ',col_count)
        print(df.head(20))
    print("+"*100)



print("PROCESS COMPLETED :)")