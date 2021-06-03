#!/usr/bin/env python3

# This example displays how to get all contacts from a HubID and paginate through them using the 'offset' parameter.
# The end result is a python list containing all parsed contacts. 
import config.config as config
import requests
import json
import urllib
from pprint import pprint


max_results = 3000
count = 5 
contact_list = []
property_list = []
get_all_contacts_url = "/contacts/v1/lists/all/contacts/all"
parameter_dict = {'hapikey': config.APIKEY, 'count': count}
headers = {}

# Paginate your request using offset
has_more = True
while has_more:
	parameters = urllib.parse.urlencode(parameter_dict)
	get_url = config.HS_API_URL + get_all_contacts_url + config.APIKEY
	r = requests.get(url = get_url, headers = headers)
	response_dict = json.loads(r.text)
	has_more = response_dict['has-more']
	contact_list.extend(response_dict['contacts'])
	parameter_dict['vidOffset'] = response_dict['vid-offset']
	if len(contact_list) >= max_results: # Exit pagination, based on whatever value you've set your max results variable to. 
		print('maximum number of results exceeded')
		break
print('loop finished')

print("--- All Contacts ---")
print_contacts = contact_list
pprint(print_contacts)
print("--- end all contacts ---")

list_length = len(contact_list)
print("You've succesfully parsed through {} contact records and added them to a list".format(list_length))
      