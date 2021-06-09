from urllib.request import urlopen
import json
import requests
from pprint import pprint
import config.config as config

# HubDB Table ID - Data for current quarter
MEOS_HUBDB = 1677491

def create_batch_posts(table_id):
    """Get table by row
    GET /hubdb/api/v2/tables/:tableId/rows
    """
    xurl = "/hubdb/api/v2/tables/" + str(table_id) + "/rows?portalId=" + str(config.PORTAL_ID)
    url = config.HS_API_URL + xurl
    response = urlopen(url).read()
    table_data = json.loads(response)

    for row in table_data['objects']:
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
            "meta_description": str(quarter) + " ~ " + str(year) + " ~ " + str(date) + " | " + str(forecast) + " " + str(title) + " " +  str(name) + " | " + str(state) + ", " + str(country),
            "name": str(date) + " | " + str(forecast) + " " + str(title) + " " +  str(name),
            "post_body": embed_pdf,
            "publish_date": str(epoch_date),
            "publish_immediately": False,
            "slug": str(quarter) + "_" + str(year) + "/" + str(embed),
            "use_featured_image": True
        }
        xurl = "/content/api/v2/blog-posts"
        url = config.HS_API_URL + xurl + config.APIKEY
        headers = { "content-type" : "application/json" }
        response = requests.post(url, headers=headers, data=json.dumps(POST))
        # print(response.status_code, response.content, response)

create_batch_posts(MEOS_HUBDB)
