#!/usr/bin/env python3
import config.config as config
import requests
import json
from pprint import pprint

# user data 
email = "testingapis@hubspot.com"
firstname = "firstname"
lastname = "lastname"
website = "http://www.manpowergroup.com"
company = "ManpowerGroup"
phone = "414-961-1000"
address = "100 Manpower Pl"
city = "Milwaukee"
state = "WI"
zipCode = "53202"

endpoint = f'http://api.hubapi.com/contacts/v1/contact/{config.APIKEY}'
headers = {}
headers["Content-Type"]="application/json"

data = json.dumps({
  "properties": [
    {
      "property": "email",
      "value": f'{email}'
    },
    {
      "property": "firstname",
      "value": f'{firstname}'
    },
    {
      "property": "lastname",
      "value": f'{lastname}'
    },
    {
      "property": "website",
      "value": f'{website}'
    },
    {
      "property": "company",
      "value": f'{company}'
    },
    {
      "property": "phone",
      "value": f'{phone}'
    },
    {
      "property": "address",
      "value": f'{address}'
    },
    {
      "property": "city",
      "value": f'{city}'
    },
    {
      "property": "state",
      "value": f'{city}'
    },
    {
      "property": "zip",
      "value": f'{zipCode}'
    }
  ]
})


r = requests.post( url = endpoint, data = data, headers = headers )

pprint(r.text)

      