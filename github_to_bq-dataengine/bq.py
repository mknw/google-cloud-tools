from google.cloud import bigquery
from google.oauth2 import service_account

from pathlib import Path
import logging


_json_creds_path = Path.home() / "code/cloud/dags/_massarius/credentials/google.json"


def instantiate_client():
    # scopes = ['https://www.googleapis.com/auth/drive', 
    #                'https://www.googleapis.com/auth/bigquery'
    #                ]
    bq_client = bigquery.Client()
    return bq_client

def load_df_to_bq(df):
    # Load to bigQuery
    n_entries = df.shape[0]

    job_config = bigquery.LoadJobConfig(
        # time_partitioning=bigquery.table.TimePartitioning(field="creation_date"),
        write_disposition='WRITE_TRUNCATE',
        schema=[],
    )

    bq_client = instantiate_client()
    job = bq_client.load_table_from_dataframe(
        df,
        'dev-era-184513.github_sync.dataengine_issues', 
        job_config=job_config
    )
    r = job.result()
    if r.done():
        if n_entries == r.output_rows:
            logging.info(f'{r.output_rows} Data Points Correctly Loaded to BigQuery')
        else:
            logging.warning(f'DataFrame with {n_entries} entries, but loaded {r.output_rows} to BigQuery.')
        return 1
    else:
        logging.warning('BigQuery Load Job Was Not Validated.')
        return 0

# if __name__ == '__main__':
#     from az_devops_items import collect_work_items, auth_token, url
#     df = collect_work_items(url, auth_token)
#     load_df_to_bq(df)