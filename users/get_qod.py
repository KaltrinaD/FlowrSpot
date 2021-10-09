from django.contrib.sites import requests
import requests
from rest_framework.utils import json


def get_quota(self):
    r = requests.get('https://quotes.rest/qod')
    json_data = json.loads(r.text)
    if 'contents' in json_data:
        return json_data['contents']['quotes'][0]['quote']  # if there is an error, return the last quote of the day from db
    return 'Keep on going and the chances are you will stumble on something, perhaps when you are least expecting it. I have never heard of anyone stumbling on something sitting down.'
