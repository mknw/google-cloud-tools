from tkinter import W
import requests
import pandas as pd
import ipdb

# Perform the request as performed from terminal with:
# $ curl -i -u Massarius:$github_token   -H "Accept: application/vnd.github.v3+json" \
# "https://api.github.com/repos/massarius/cloud/issues?per_page=100"

def get_issues(token=None):
   payload = {'per_page': 100}
   headers = {'Accept': 'applications/vnd.github.v3+json'}
   r = requests.get('https://api.github.com/repos/massarius/cloud/issues',
                     params=payload, 
                     headers=headers,
                     auth=('Massarius', token))

   df = pd.DataFrame(clean_issues(r.json()))
   
   # convert to right dtype
   df[['created_at', 'updated_at']] = df[['created_at', 'updated_at']].apply(pd.to_datetime)
   # df[['html_url', 'title', 'user_avatar_url', 'labels_name', 'state', 'assignee_login', 'assignee_avatar_url', 'milestone']] = df[
   #    [ 'html_url', 'title', 'user_avatar_url', 'labels_name', 'state', 'assignee_login', 'assignee_avatar_url', 'milestone']].astype(str)
   return df


def clean_issues(issues):
   keys = ('html_url', 'number', 'title',
            'milestone', 'comments', 'created_at',
            'updated_at', 'state')
   # Dict keys are needed to index dictionary items.
   # For some nested dictionaries, a combination of keys will be necessary
   # to extract intended info. For each value in `dict_keys`, a simple
   # tuple implies a dictionary whose keys will be indexed with values in 
   # the tuple. For lists, each tuple indicates the values to use for 
   # to index a list of dictionaries. See below for an example.
   dict_keys = {'user': ('login', 'avatar_url'), 
                'labels': [('name')], 
                'assignee': ('login', 'avatar_url'),
                'reactions': ('laugh', 'hooray', 'confused', 'heart', 'rocket', 'eyes')}
   out_issues = []
   for i in issues:
      out_issues.append(clean_issue_dimensions(i, keys, dict_keys))
   return out_issues



def clean_issue_dimensions(issue, keys=None, dict_keys=None):
   '''
   Turn dictionaries from the format: 

   '''
   row = dict()
   for k, v in issue.items():
      if k in keys:
         row[k] = v
      if k in dict_keys:
         nested_keys = dict_keys[k]
         # for single dictionaries
         if isinstance(nested_keys, tuple):
               for nested in nested_keys:
                  if v is None:
                     # in case 'assignee' is just None
                     row[f'{k}_{nested}'] = v
                  # otherwise, extract the needed keys
                  else:
                     try:
                        row[f'{k}_{nested}'] = v[nested]
                     except TypeError as te:
                        print('tuple: ', te)

         # for list of dictionar(y|ies)
         if isinstance(nested_keys, list):
            assert isinstance(v, list)
            # Extract sub_keys to repeat for each dict in list
            nested = nested_keys[0]
            if not v:
               # for those instances where v is None
               row[f'{k}_{nested}'] = v
            else:
               list_of_values = []
               for sub_dictionary in v:
                  for kk, v in sub_dictionary.items():
                     if kk in nested:
                        try:
                           list_of_values.append(v)
                        except TypeError as te:
                           print('list of tuples: ', te)
               row[f'{k}_{nested}'] = list_of_values
   return row


def show_issue(issue):
   '''

   Param:
   ------
      issue: dict
      Dictionary containing issue metadata.
   '''
   for k, v in issue.items():
      print('------>', k)
      print(v)


def get_env_vars():
   env_vars = dict()
   with open('.env', 'r') as env:
      for l in env:
         text = l.strip().split('=')
         assert len(text) == 2
         env_vars[text[0]] = text[1]
   return env_vars

if __name__ == '__main__':

   # utility snippet to avoid storing token in plain text on github.
   env_vars = get_env_vars()

   get_issues(**env_vars)