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
def main(request, _token=None):
   logging.info(f'====Request====:\n')
   logging.info(f'Request method: {request.method}\n')
   logging.info(f'request json: {request.get_json()}\n')

   _url = 'https://dev.azure.com/Massarius-Adtech'
   if _token is None:
      _token = os.environ.get('GITHUB_AZURE_INTEGRATION_READONLY')
   sync_devops_to_bq(_url, _token)

   return 'request successful'


if __name__ == '__main__':
   class Req():
      method = 'POST'
      def get_json(self):
         return {'mockup':'json'}
   token = 'ewscnbruzv4jmq4jyy557tosmqipbxnhialrm7bg2euibfqqe4yq'
   r = Req()
   main(r, token)