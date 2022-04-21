from re import I
from az_devops_items import collect_work_items
from bq import load_df_to_bq
import os
import logging
from flask import Request
import functions_framework

def sync_devops_to_bq(*args):
   work_items_df = collect_work_items(*args)
   load_df_to_bq(work_items_df)

@functions_framework.http
def main(request):
   logging.info(f'====Request====:\n')
   logging.info(f'Request method: {request.method}\n')
   logging.info(f'request json: {request.get_json()}\n')

   _url = 'https://dev.azure.com/Massarius-Adtech'
   _token = os.environ.get('GITHUB_AZURE_INTEGRATION_READONLY')
   sync_devops_to_bq(_url, _token)

   return 'request successful'