import json
import requests
import config.config as config

# Add details for new topic below in JSON format
NEW_TOPIC = {
    "name": "2020",
    "description": "Year"
}

def create_topic():
    """
    Create a new blog topic
    POST /blogs/v3/topics
    """
    # and including a request body of:

    xurl = "/blogs/v3/topics/"
    url = config.HS_API_URL + xurl + config.APIKEY
    response = requests.post(url)
    headers = { "content-type" : "application/json" }
    response = requests.post(url, headers=headers, data=json.dumps(NEW_TOPIC))
    print(response.status_code, response.content, response)

create_topic()
