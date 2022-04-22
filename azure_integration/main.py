from re import I
from az_devops_items import collect_work_items
from bq import load_df_to_bq
import os
import logging
from flask import Request
import functions_framework

logging.basicConfig(level=logging.DEBUG)

def sync_devops_to_bq(*args):
   work_items_df = collect_work_items(*args)
   if work_items_df.empty:
      logging.warning('No Fetched Data from Azure DevOps.')
   else:
      logging.info('Data Fetched from Azure DevOps.')

   load_df_to_bq(work_items_df)


@functions_framework.http
def main(request, _token=None):
   logging.info(f'====Request====:\n')
   logging.info(f'Request method: {request.method}\n')

   '''just some boilerplate to test the function working request.'''
   content_type = request.headers['content-type']
   if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
            print(f'name: {name}')
        else:
            logging.warning("JSON is invalid, or missing a 'name' property")
   elif content_type == 'application/octet-stream':
        name = request.data
   elif content_type == 'text/plain':
        name = request.data
   logging.info(f'Request data: {name}')

   _url = 'https://dev.azure.com/Massarius-Adtech'
   if not _token:
      _token = os.environ.get('GITHUB_AZURE_INTEGRATION_READONLY')

   sync_devops_to_bq(_url, _token)
   return f'request successful, {name}'


if __name__ == '__main__':
   class Req():
      method = 'POST'
      def get_json(self):
         return {'mockup':'json'}
   token = ''
   r = Req()
   main(r, token)