# Integration Azure Devops - Google bigQuery

This repo directory contains code to be deployed as a Google Cloud Function synchronising Azure DevOps work items to BigQuery. 

The function can be deployed as follows:

```
gcloud functions deploy NAME --region=europe-west1 --allow-unauthenticated --entry-point=main --memory=256MB --runtime=python38  --stage-bucket=devops_workitems_to_bigquery --set-secrets=GITHUB_AZURE_INTEGRATION_READONLY=github-azure-integration-readonly:latest --trigger-http
```

As of now, the 100 most recently changed items are fetched and loaded to bigQuery. If needed, these parameters can be changed in the appropriate python files.


To test the function, you can run something like: 

```
curl -X POST "http://europe-west1-dev-era-184513.cloudfunctions.net/azure_bq_integration" -H "Content-Type:application/json"
```
