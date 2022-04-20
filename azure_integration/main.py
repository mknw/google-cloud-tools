from az_devops_items import collect_work_items
from bq import load_df_to_bq
import os
import logging

def sync_devops_to_bq(*args):
   work_items_df = collect_work_items(*args)
   load_df_to_bq(work_items_df)



def main(**kwargs):
   logging.info(f'Arguments provided to main: ')
   for k, v in kwargs.items():
      logging.info(f'{k}: {v}')
   _url = 'https://dev.azure.com/Massarius-Adtech'
   _token = os.environ.get('GITHUB_AZURE_INTEGRATION_READONLY')
   sync_devops_to_bq(_url, _token)