from az_devops_items import collect_work_items
from bq import load_df_to_bq
import os

def sync_devops_to_bq(*args):
   work_items_df = collect_work_items(*args)
   load_df_to_bq(work_items_df)



def main():
   _url = 'https://dev.azure.com/Massarius-Adtech'
   _token = os.environ.get('GITHUB_AZURE_INTEGRATION_READONLY')
   sync_devops_to_bq(_url, _token)