from az_devops_items import collect_work_items
from bq import load_df_to_bq
import os

def sync_devops_to_bq(*args):
   work_items_df = collect_work_items(*args)
   load_df_to_bq(work_items_df)


if __name__ == '__main__':
   # _token variable to be assigned from secret.
   _url = 'https://dev.azure.com/Massarius-Adtech'
   _token = os.environ['GITHUB_AZURE_INTEGRATION_READONLY']

   sync_devops_to_bq(_url, _token)