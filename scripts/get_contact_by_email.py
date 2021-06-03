#!/usr/bin/env python3

import config.config as config
import requests
# import json 
from pprint import pprint

userEmail = "flyspaceage@gmail.com"
headers = {}

single_contact_url = f'{config.HS_API_URL}/contacts/v1/contact/email/{userEmail}/profile{config.APIKEY}'

# try:
#   response = requests.get(url = single_contact_url, headers = headers)
# except requests.ConnectionError as error:
#   print(error)

# TODO add verify=False <- override SSL certificate error DANGEROUS!
response = requests.get(url = single_contact_url, headers = headers)

pprint(response.text)