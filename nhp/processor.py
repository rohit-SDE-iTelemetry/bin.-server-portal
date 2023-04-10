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
from nhp_app.models import site, readings_2023
from datetime import datetime
import pytz
import shutil
import logging

tz = pytz.timezone('Asia/Kolkata')
now = datetime.now(tz)


# file_path = "/home/ubuntu/aaxisnano/devices.json"
# data_base_path = "/home/ubuntu/binsrv/data/"
processed_data_folder = "/home/rohit/Desktop/nhp_projects/nhp/git/bin.-server-portal/nhp/processed_data_folder/"
data_files = "/home/rohit/Desktop/nhp_projects/nhp/git/bin.-server-portal/nhp/data_folder/"
all_adata_files = glob.glob(data_files + "*.adata")


# check for site in DB
def _check4site(fprefix):
    print(f'[PREFIX CHECK] ... checking {fprefix.upper()} for existance')
    if(site.objects.filter(prefix=fprefix)):
        print(f'[WARNING] ... {fprefix.upper()} device already exist')
        siteObj = site.objects.get(prefix=fprefix)
        # siteObj.device_config = deviceCong
        siteObj.total_params = ['timestamp', 'count']
        siteObj.save()

        params_labels = _get_param_labels(siteObj)
        return site.objects.filter(prefix=fprefix)[0], params_labels
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
            print(f'[OK] ... {fprefix.upper()}  device created successfully')
            params_labels = _get_param_labels(siteObj)
        except Exception as err:
            print(f'[ERROR] ... Error occured while add new device : {err}')
            return None, []
        return siteObj, params_labels


# upload data to DB
def _upload2db(site_obj, dic_readings):
    try:
        print(f'[READINGS STARTS] ... {fprefix.upper()}  readings starts')
        for new_readings in dic_readings:
            param_read = new_readings
            ts = new_readings['timestamp']
            del param_read['timestamp']
            print(ts, ' ---> ' ,new_readings)
            try:
                reading_obj = readings_2023(site_id=site_obj,
                                        timestamp = ts,
                                        readings = new_readings)
                reading_obj.save()
                site_obj.last_reading_received_at = ts
                site_obj.last_readings = new_readings
                site_obj.save()

            except Exception as err:
                print(f'[ERROR] ... Error on adding new reading to db : {err}')
        print(f'[READINGS ENDS] ... {fprefix.upper()}  readings ends')
        return True
    except Exception as err:
        return False


# get params label
def _get_param_labels(siteObj):
    data = siteObj.device_config['sensor_position']
    context_list = []
    for k, v in data.items():
        if v:
            context_list.append(v)
    return context_list


print("+"*100)
for f in all_adata_files[:]:
    fprefix = f.split('/')[-1].split('.')[0].lower()
    print(f'[STATION PREFIX] ... {fprefix.upper()}')
    site_obj, df_labels = _check4site(fprefix)
    if site_obj and df_labels:
        print(f'[STATION NAME] ... {site_obj}')
        print(f'[DATAFRAME LABELS] ... {df_labels}')
        filepath = os.path.join(data_files, os.path.basename(f))
        '''
        print("filepath ---> ",filepath)
        '''
        print(f'[FILEPATH] ... {filepath}')
        time.sleep(0.1)
        try:
            sample_df = pd.read_csv(filepath)
            df = pd.read_csv(filepath, names=df_labels)
        except pd.errors.EmptyDataError as err:
            print(f'[ERROR] ... File is empty \n{err}')
        except pd.errors.ParserError as err:
            print(f'[ERROR] ... No columns to parse from file \n{err}')
        else:
            df_col_count = len(df.columns)
            sample_df_col_count = len(sample_df.columns)
            '''
            print('df >>> \n',sample_df.head(1))
            '''
            if (df_col_count == sample_df_col_count):
                df = df.drop('count', axis=1)
                '''
                print('df >>> \n',df.head())
                print('sample_df_col_count >>> ',sample_df_col_count)
                '''
                readings_df = df.to_dict(orient='records')
                if readings_df:
                    _upload2db(site_obj, readings_df)
                else:
                    print("[WARNING] ... Empty dataframe")
            else:
                print("+-"*50)
                print('[ERROR] ... Site params not configured properly! .... plss configure it to process data.')
                print("+-"*50)
    else:
        print(f'[ERROR] ... Unable to process data. [site_obj:{site_obj} and df_labels:{df_labels}]')
    print("+"*100)
print("PROCESS COMPLETED :)")