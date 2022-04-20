
from tkinter import W


def print_dictionary(dic):
   for k, v in dic.items():
      print(k, ': ', v)

def print_work_item(work_item):

   pfield(work_item, 'System.CreatedDate')
   print('{} {}: {}'.format( work_item.fields['System.WorkItemType'],
                            work_item.id,
                            work_item.fields['System.Title']))
   print(f"{work_item.fields['System.AssignedTo']['displayName']}")

   print(f"url: {work_item.url}")
   actual_url = f'https://dev.azure.com/Massarius-Adtech/Adtech%20Tasks/_workitems/edit/{work_item.id}'
   print(f'actual url: {actual_url}')
   pfield(work_item, 'System.State')
   pfield(work_item, 'System.Reason')
   pfield(work_item, 'System.CommentCount')
   pfield(work_item, 'System.BoardColumn')
   pfield(work_item, 'System.BoardColumnDone')
   pfield(work_item, 'Microsoft.VSTS.Common.Priority')
   print('-.-' * 10)


def pfield(work_item, field_name):
   '''
   P(relevate) field,
   but also: P(rint) field.
   '''
   try:
      print(f"{field_name} : {work_item.fields[field_name]}")
      return work_item.fields[field_name]
   except KeyError:
      print(f'{field_name} not found. Returning None.')
      return None