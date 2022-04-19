from google.cloud import bigquery
from google.oauth2 import service_account

from pathlib import Path



_json_creds_path = Path.home() / "code/cloud/dags/_massarius/credentials/google.json"


def instantiate_client():
    # TODO: This process will have to be rethought for Google Cloud Function.
    list_scopes = ['https://www.googleapis.com/auth/drive', 
                   'https://www.googleapis.com/auth/bigquery'
                   ]

    credentials = service_account.Credentials.from_service_account_file(
        filename = _json_creds_path ,
        scopes = list_scopes,
    )
    bq_client = bigquery.Client(credentials = credentials)
    return bq_client

def load_df_to_bq(df):
    # Load to bigQuery

    job_config = bigquery.LoadJobConfig(
        time_partitioning=bigquery.table.TimePartitioning(field="creation_date"),
        write_disposition='WRITE_TRUNCATE', # if append else 'WRITE_TRUNCATE',
        schema=[],
    )

    bq_client = instantiate_client()
    table_ref = bq_client.dataset('azure_workitems').table('adtech_workitems')
    job = bq_client.load_table_from_dataframe(
        df, table_ref, location="eu", job_config=job_config
    )
    job.result()


if __name__ == '__main__':
    load_df_to_bq(df)