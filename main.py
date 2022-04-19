from az_devops_items import collect_work_items
from bq import load_df_to_bq

def sync_devops_to_bq(*args):
   work_items_df = collect_work_items(*args)
   load_df_to_bq(work_items_df)


if __name__ == '__main__':
   _token = 'ewscnbruzv4jmq4jyy557tosmqipbxnhialrm7bg2euibfqqe4yq'
   _url = 'https://dev.azure.com/Massarius-Adtech'

   sync_devops_to_bq(_url, _token)