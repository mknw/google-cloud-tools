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

Lookup the [requests](https://docs.python-requests.org) library. It will explain how to implement [custom headers](https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers) for the version definition, providing [parameters](https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers) for the `per_page` field and [basic authentication](https://2.python-requests.org/en/master/user/authentication/#basic-authentication).

Once implemented <!-- add link to repo >
we can focus on data wrangling.
