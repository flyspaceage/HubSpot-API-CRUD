#!/usr/bin/env python3
import config.config as config
import requests
import json
import time
from urllib.request import urlopen

# store credentials
APIKEY = f'?hapikey={config.APIKEY_VALUE}'
HS_API_URL = "http://api.hubapi.com"
PORTAL_ID = 2942250

"""
CRUD (Create, Retrieve, Update, And Delete) HTTP methods for the
ManpowerGroup Employment Outlook Survey hosted in HubSpot
"""

# Define content group IDs as global variables
MEOS_ID = 5664168304  #  ManpowerGroup Employment Outlook Survey
MEOS_GUID = "71df6020-8385-4e2e-9a36-23e708fa4605"

# Lists HubDB table IDs as global variables
# MEOS_Q1_2020 = "2033279"
HUBDB_ID = "3418001"

# Define JSON Actions
PUBLISH = {"action": "schedule-publish"}
CANCEL = {"action": "cancel-publish"}

# Define publication details
PUBLISH_NOW = str(time.time())
DRAFT = 'draft'
LIVE = 'publish'
LIMIT = 152 # Number of rows in table to publish as posts
PASSWORD = ''# Enter password for embargo 'mpgmeos#' - or blank to unlock

def create_batch_posts(table_id):
    """Get table by row
    GET /hubdb/api/v2/tables/:tableId/rows
    """
    
    url = f'{HS_API_URL}/hubdb/api/v2/tables/{table_id}/rows?portalId={PORTAL_ID}'
    response = requests.get(url, params={'portalId': PORTAL_ID})
    table_data = response.json()
    # print(table_data)

    for row in table_data["objects"]:
        name = row["values"]["1"]
        embed = row["values"]["2"]
        title = row["values"]["3"]
        state = row["values"]["4"]
        date = row["values"]["5"]
        year = row["values"]["6"]
        quarter = row["values"]["7"]
        country = row["values"]["9"]
        forecast = row["values"]["10"]
        blog_author_id = row["values"]["11"]
        campaign_id = row["values"]["12"]
        campaign_name = row["values"]["13"]
        content_group_id = row["values"]["14"]
        featured_image = row["values"]["15"]
        year_id = row["values"]["19"]
        quarter_id = row["values"]["20"]
        market_id = row["values"]["21"]
        state_id = row["values"]["22"]
        epoch_date = row["values"]["23"]
        embed_pdf = f'<embed src="https://drive.google.com/viewerng/viewer?embedded=true&amp;url=https://go.manpowergroup.com/hubfs/MEOS/{year}_{quarter}/{embed}.pdf" width="500" height="675">'
        POST = {
            "blog_author_id": blog_author_id,
            "campaign": campaign_id,
            "campaign_name": campaign_name,
            "content_group_id": content_group_id,
            "featured_image": featured_image,
            "topic_ids": [year_id, quarter_id, market_id, state_id],
            "meta_description": f'{quarter} ~ {year} ~ {date} | {forecast} {title} {name} | {state}, {country}',
            "name": f'{date} | {forecast} {title} {name}',
            "post_body": f'{embed_pdf}<br><br><a href="https://go.manpowergroup.com/hubfs/MEOS/{year}_{quarter}/{embed}.pdf" target="_blank">Download Press Release</a>',
            "publish_date": f'{epoch_date}',
            "publish_immediately": False,
            "slug": f'{quarter}_{year}/{embed}',
            "use_featured_image": True
        }
        url = f'{HS_API_URL}/content/api/v2/blog-posts{APIKEY}'
        headers = { "content-type" : "application/json" }
        response = requests.post(url, headers=headers, data=json.dumps(POST))
        # print(response.status_code, response.content, response)


def publish_post(blog_post_id):
    """
    Publish, schedule or unpublish a blog post
    POST /content/api/v2/blog-posts/:blog_post_id/publish-action
    """
    url = f'{HS_API_URL}/content/api/v2/blog-posts/{blog_post_id}/publish-action{APIKEY}'
    response = requests.post(url)
    headers = { "content-type" : "application/json" }
    response = requests.post(url, headers=headers, data=json.dumps(PUBLISH))
    print(response.status_code, response.content, response)


def publish_draft_post_by_id():
    """Get the blog post by ID
    GET /content/api/v2/blog-posts/
    """
    url = f'{HS_API_URL}/content/api/v2/blog-posts/{APIKEY}&content_group_id={MEOS_ID}&state={DRAFT}&limit={LIMIT}'
    response = urlopen(url).read()
    blog_data = json.loads(response)
    for blog_post in blog_data['objects']:
        draft_id = blog_post['id']
        print(draft_id)
        publish_post(draft_id)


def set_password(page_id):
    """
    Update a page
    PUT /content/api/v2/pages/:page_id
    """
    url = f'{HS_API_URL}/content/api/v2/pages/{page_id}{APIKEY}'
    response = requests.put(url, params={'portalId': PORTAL_ID}, json={"password": PASSWORD})
    page = response.json()
    page_password = page['meta']['password']
    print(page_password)


def list_pages(campaign_guid):
    """
    List pages
    GET /content/api/v2/pages
    """
    url = f'{HS_API_URL}/content/api/v2/pages{APIKEY}'
    response = requests.get(url, params={'portalId': PORTAL_ID, 'campaign': campaign_guid})
    pages = response.json()

    for page in pages['objects']:
        page_id = page['id']
        print(page_id)

        page_password = page['meta']['password']
        print(page_password)

        # Calls set_password
        set_password(page_id)


def main():

    # ***Embargo Lock and Unlock***
    print('Changing password...')
    list_pages(MEOS_GUID) # MEOS_GUID - Enter Campaign GUID

    # ***Create draft blog post with content saved in HubDB***
    # create_batch_posts(HUBDB_ID)
    # print('Batch posts created')

    # ***Gets the draft ID and then calls publish_post***
    # publish_draft_post_by_id()
    # print('Draft posts published')


if __name__ == '__main__':
    main()
