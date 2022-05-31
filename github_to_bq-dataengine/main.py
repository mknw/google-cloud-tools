import os
import logging
import functions_framework

from bq import load_df_to_bq
from github_issues import get_open_issues
from github_issues import get_env_vars


logging.basicConfig(level=logging.INFO)

def issues_to_bq(_token):
   
   if not _token:
      env_vars = get_env_vars()
   else:
      env_vars = {'token': _token}
      
   df = get_open_issues(**env_vars) 
   if df.empty:
      logging.warning('No Fetched Data from Github.')
   else:
      logging.info('Data Fetched from Github.')
   
   load_df_to_bq(df)

@functions_framework.http
def main(request, _token=None):
   req_str = '====Request====:\nRequest method: {}\n'
   logging.info(req_str.format(request.method))

   '''just some boilerplate to test the function working request.'''
   content_type = request.headers['content-type']
   if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
            print(f'name: {name}')
        else:
            logging.warning("JSON is invalid, or missing a 'name' property")
            logging.error(f'Payload: {request_json}')
   elif content_type == 'application/octet-stream':
        name = request.data
   elif content_type == 'text/plain':
        name = request.data
   logging.info(f'Request data: {name}')

   if not _token:
      _token = os.environ.get('GITHUB_MASSARIUS_PAT')

   issues_to_bq(_token)
   return f'request successful, {name}'



if __name__ == '__main__':
   class Req():
      method = 'POST'
      headers = dict()
      headers['content-type'] = 'application/json'
      def get_json(self, **kwargs):
         return {'mockup':'json', 'name': 'johnny'}
   r = Req()
   main(r)