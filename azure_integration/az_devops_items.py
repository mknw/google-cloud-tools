
from azure.devops.credentials import BasicAuthentication
from azure.devops.connection import Connection
from azure.devops.v5_1.work_item_tracking.models import Wiql

from utils import print_dictionary, print_work_item, pfield
import pandas as pd

from types import SimpleNamespace

__VERSION__ = "0.0.1"

url = 'https://dev.azure.com/Massarius-Adtech'

def collect_work_items(url, auth_token, verbose = False):
   # TO ADD: output_path for loggin option 

   context = SimpleNamespace()
   context.runner_cache = SimpleNamespace()

   # setup the connection
   context.connection = Connection(
      base_url=url,
      creds=BasicAuthentication('PAT', auth_token),
      user_agent='azure-devops-dashboard-sync/' + __VERSION__)

   # hook for debugging can be added to context.connection.get_client

   work_items_iterator = wiql_query(context, verbose=verbose)
   return work_items_to_dataframe(work_items_iterator)




def wiql_query(context, **kwargs):
   wit_client = context.connection.clients.get_work_item_tracking_client()
   wiql = Wiql(
      query=query
   )

   wiql_results = wit_client.query_by_wiql(wiql, top=100).work_items
   print("Results: {0}".format(len(wiql_results)))
   if wiql_results:
      # WIQL query gives a WorkItemReference with ID only 
      work_items = (
         wit_client.get_work_item(int(res.id)) for res in wiql_results
      )
      if kwargs['verbose']:
         for work_item in work_items:
            print_work_item(work_item)
      return work_items
   else:
      return []

def work_items_to_dataframe(work_items, **kwargs):
   # 1. Initialize lists as columns for DataFrame
   work_items = list(work_items)
   # Change dates to pd.Datetime
   list_to_date = lambda l: [pd.to_datetime(x.split('T')[0], format=f"%Y-%m-%d") for x in l]

   ids = [i.id for i in work_items]

   creation_dates = list_to_date([i.fields['System.CreatedDate'] for i in work_items])
   change_dates = list_to_date([i.fields['Microsoft.VSTS.Common.StateChangeDate'] for i in work_items])

   titles = [i.fields['System.Title'] for i in work_items]
   assignees = [i.fields['System.AssignedTo']['displayName'] for i in work_items]
   base_url = 'https://dev.azure.com/Massarius-Adtech/Adtech%20Tasks/_workitems/edit/{}'
   urls = [base_url.format(i.id) for i in work_items]
   states = [i.fields['System.State'] for i in work_items]
   # reasons = [i.fields['System.Reason'] for i in work_items]
   comment_counts = [i.fields['System.CommentCount'] for i in work_items]
   prios = [i.fields['Microsoft.VSTS.Common.Priority'] for i in work_items]

   return pd.DataFrame({'id': ids,
                 'creation_date': creation_dates,
                 'change_date': change_dates, # change dates to pd.Datetoime
                 'title': titles,
                 'assignee': assignees,
                 'url': urls,
                 'state': states,
                 'comment_count': comment_counts,
                 'priority': prios,})



query="""
select [System.Id],
    [System.WorkItemType],
    [System.Title],
    [System.State],
    [System.AreaPath],
    [System.IterationPath],
    [System.Tags]
from WorkItems
order by [System.ChangedDate] desc"""


# if __name__ == "__main__":
#    df = collect_work_items(url, auth_token, verbose = False)