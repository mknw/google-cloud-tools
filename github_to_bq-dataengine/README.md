# Github Issues to BigQuery 

## Intro

This readme will be written in a procedural manner. That is, listing the action I perform as I solve the subject of interest. 
The latter involves fetching issues from github and loading them to github. 

Before you start, make sure you obtain a [PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for your account / application.

## Github REST API

RESTful API's allow us to fetch information without needing to record previous information on a system state. It's that simple. 
REST stands for REpresentational State Transfer, and implies that the data we gather is not tied to specific resources or method. 

This said, we can look at the [Github REST API page](https://docs.github.com/en/rest) to figure out which request we need to perform first. Since our request 

From the examples under [List repository issues](https://docs.github.com/en/rest/issues/issues#list-repository-issues), we learn that a simple `curl` HTTP (GET) request with OWNER and REPO path parameters gets the job done:

```
curl \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/issues
```

Since the our repo of interest is private, user authentication needs to be performed by means of the `-u` or `--user` flag. This is explained in the [Authentication](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api) section of the Getting Started guide.

Additionally, we want to make sure that all the default parameters correspond to the desired request, or change them if they aren't.

We can read through the list of parameters by checking the [issues section](https://docs.github.com/en/rest/issues/issues) of the API documentation. 

```
curl -i -u Massarius:$github_token   -H "Accept: application/vnd.github.v3+json" \
"https://api.github.com/repos/massarius/cloud/issues?per_page=100"
```

We add the query parameters by adjusting the field and value of the desired parameter as follows: the `https://api.request.com/endpoint?field=value&other_field=other_value`.

## Python 

### Fetch the Issues from the API
Lookup the [requests](https://docs.python-requests.org) library. It will explain how to implement [custom headers](https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers) for the version definition, providing [parameters](https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers) for the `per_page` field and [basic authentication](https://2.python-requests.org/en/master/user/authentication/#basic-authentication).

Once implemented <!-- add link to repo >
we can focus on data wrangling. The json payload needs to be formatted in a way that Pandas understand. This enables us to:

1. ensure the structure of data is homogeneous across data points.
2. check wether data types for each dimensions / metric are correct, and
3. use the `load_table_from_dataframe` method of the bigquery client.

### Load the data to BigQuery

[Create a BigQuery Dataset](https://cloud.google.com/bigquery/docs/datasets#create-dataset) to store the data:

```
CREATE SCHEMA `dev-era-184513.github_issues`
OPTIONS(
  description="Open Github issues from the `massarius/cloud` repository updated weekly.",
  labels=[('org_unit', 'devops'), ('team', 'data')]
)
```

Then the table: 

```
CREATE TABLE  `dev-era-184513.github_sync.dataengine_issues`
(html_url                          STRING,
number                             INT64,
title                              STRING,
user_login                         STRING,
user_avatar_url                    STRING,
labels_name                        STRING,
state                              STRING,
assignee_login                     STRING,
assignee_avatar_url                STRING,
milestone                          STRING,
comments                           INT64,
created_at                         DATETIME,
updated_at                         DATETIME,
reactions_laugh                    INT64,
reactions_hooray                   INT64,
reactions_confused                 INT64,
reactions_heart                    INT64,
reactions_rocket                   INT64,
reactions_eyes                     INT64
)
OPTIONS(
  description = 'Contains open tickets from repository Massarius/cloud on Github.'
)
```

## Google Cloud Functions

In this section it will be explained:

0. Testing the GCF locally.
1. Save the Github Personal Access Token (PAT) that you previously used in Google Cloud Console with the appropriate Google Secret Manager.
2. Load the Google Cloud Function with gcloud-cli tools, making the PAT (secret token) available.
3. Testing the function.

### Testing

In order to test the function, one way is to provide credentials for a service account which performs the operation through the Python API. In order to do this, we can simply provide the Environment Variable `GOOGLE_APPLICATION_CREDENTIALS` setting to the path of the json file for the desired service account.

Simply type `export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"` in your terminal. At massarius, a json configuration file is already used in the cloud repo configuration (dags/_massarius/credentials) for the ms-method service account, so you can use that one. 

This enables your code to avoid inline authentication, allowing it to be unchanged in the version uploaded as Cloud Function on GCP.

After setting the path, activate the virtual environment where the necessary packages are installed. Run `python main.py` to start the process. Once the script has run, make sure to check on BigQuery to ensure the data was uploaded.

If everything was performed correctly, we can save dependencies for the GCF as requirements.txt with: `pip freeze > requirements.txt`. This file will be used by GCP to import the appropriate set of libraries.


### Deploying

Once the secret is saved, a bucket needs to be created to store the source code. 
Make sure the right project is selected on gcloud with `gcloud config get project`. A list of available projects can be obtained with `gcloud list projects`, while setting the right project can be done with `gcloud config set project <project_name>`. 

Create the bucket with `gcloud mb -l europe-west2 gs://<bucket-name>`.

While in your working directory, run: 

```
 gcloud functions deploy NAME --region=europe-west2 \
--entry-point=main --memory=256MB --runtime=python38 \
--stage-bucket=gs://BUCKET_NAME \
--set-secrets=GITHUB_MASSARIUS_PAT=github-massarius-account-pat:latest --trigger-http
```

This will upload the code in the `pwd` to GCP.
Next, a scheduler job needs to be setup in order to call the GCF when needed. 



