import urllib.request,json
from .models import Post

# Getting api key
api_key = None
# Getting the post base url
base_url = None

def configure_request(app):
    global api_key,base_url
    api_key = app.config['POST_API_KEY']
    base_url = app.config['POST_API_BASE_URL']

