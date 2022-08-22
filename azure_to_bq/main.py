from az_devops_items import collect_work_items
from bq import load_df_to_bq
import os
import logging
import functions_framework

# get rid of all those pesky DEBUG level logs. 
logging.basicConfig(level=logging.INFO)

# in its original configuration, this query was performed
# to sync the Yield team to BigQuery (and relative Data Studio dashboard).
query_yield = """
select [System.Id],
    [System.WorkItemType],
    [System.Title],
    [System.State],
    [System.AreaPath],
    [System.IterationPath],
    [System.Tags]
from WorkItems
where (([System.State] contains 'Open' OR [System.State] contains 'Waiting' OR [System.State] contains 'On Hold') OR ([Microsoft.VSTS.Common.ClosedDate] >= @Today-14)) AND ([System.AreaPath] under 'Analysis Tasks')
order by [Microsoft.VSTS.Common.Priority] asc, [System.ChangedDate] desc"""

# in its original configuration, this query was performed
# to sync the Adtech team to BigQuery (and relative Data Studio dashboard).
query_adtech = """
select [System.Id],
    [System.WorkItemType],
    [System.Title],
    [System.State],
    [System.AreaPath],
    [System.IterationPath],
    [System.Tags]
from WorkItems
where [System.State] contains 'Open' OR [System.State] contains 'Waiting' OR [System.State] contains 'On Hold'
order by [Microsoft.VSTS.Common.Priority] asc, [System.ChangedDate] desc"""


def sync_devops_to_bq(*args):
   work_items_df = collect_work_items(*args)
   if work_items_df.empty:
      logging.warning('No Fetched Data from Azure DevOps.')
   else:
      logging.info('Data Fetched from Azure DevOps.')

   load_df_to_bq(work_items_df)


@functions_framework.http
def main(request, _url=None, query=None, _token=None):
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

   if not _url:
      raise ValueError('This ')
      _url = URL
   if not _token:
      _token = os.environ.get('GITHUB_AZURE_INTEGRATION_READONLY')
   if not _query:
      _query = query

   sync_devops_to_bq(_url, query, _token)
   return f'request successful, {name}'


if __name__ == '__main__':
   ''' Placeholder request body. '''
   class Req():
      method = 'POST'
      headers = {'content-type': 'application/json'}
      def get_json(self, **kwargs):
         print(*kwargs)
         return {'name':'Jason'}

   r = Req()

   from utils import read_env
   config = read_env('.venv.yaml')
   # pass: 
   # 1. (AZ) team group (done)
   # 1.b Token (done)
   # 2. query (done)
   # 3. bigquery 
   # main(r, token)
   main(r, _url=f"https://dev.azure.com/{config['azure_team']}",
            _token=config['token'])