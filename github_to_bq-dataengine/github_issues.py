import requests
import ipdb

# Perform the request as performed from terminal with:
# $ curl -i -u Massarius:$github_token   -H "Accept: application/vnd.github.v3+json" \
# "https://api.github.com/repos/massarius/cloud/issues?per_page=100"

def get_issues(user=None, token=None):
   payload = {'per_page': 100}
   headers = {'Accept': 'applications/vnd.github.v3+json'}
   r = requests.get('https://api.github.com/repos/massarius/cloud/issues',
                     params=payload, 
                     headers=headers,
                     auth=('Massarius', token))
   data = r.json()
   for i in data[:3]:
      print('-'*30)
      show_issue(i)

   out_data = clean_issues(data)

   # 
   return out_data
   


def clean_issues(issues):
   keys = ('html_url', 'number', 'title',
            'milestone', 'comments', 'created_at',
            'updated_at', 'reactions', 'state')
   # Dict keys are needed to index dictionary items.
   # For some nested dictionaries, a combination of keys will be necessary
   # to extract intended info. For each value in `dict_keys`, a simple
   # tuple implies a dictionary whose keys will be indexed with values in 
   # the tuple. For lists, each tuple indicates the values to use for 
   # to index a list of dictionaries. See below for an example.
   dict_keys = {'user': ('login', 'avatar_url'), 
                'labels': [('name')], 
                'assignee': ('login', 'avatar_url')}
   out_issues = []
   for i in issues:
      out_issues.append(clean_issue_dimensions(i, keys, dict_keys))
   return out_issues


def clean_issue_dimensions(issue, keys=None, dict_keys=None):
   '''
   Turn dictionaries from the format: 

   '''
   ipdb.set_trace()
   row = []
   for k, v in issue.items():
      if k in keys:
         row.append(v)
      if k in dict_keys:
         nested_keys = dict_keys[k]
         if isinstance(nested_keys, tuple):
            for nested_k in nested_keys:
               row.append(v[nested_k])

         if isinstance(nested_keys, list):
            assert isinstance(v, list)
            # Extract sub_keys to repeat for each dict in list
            nested = nested_keys[0]
            for sub_dictionary in v:
               for k, v in sub_dictionary:
                  if k in nested:
                     row.append(v)
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



if __name__ == '__main__':

   # utility snippet to avoid storing token in plain text on github.
   env_vars = dict()
   with open('.env', 'r') as env:
      for l in env:
         text = l.strip().split('=')
         assert len(text) == 2
         env_vars[text[0]] = text[1]

   get_issues(**env_vars)