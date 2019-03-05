import urllib.request,json
from .models import Post

# Getting api key
api_key = None
# Getting the post base url
base_url = None

def configure_request(app):
    global api_key,base_url
    base_url = app.config['POST_API_BASE_URL']

def get_posts():

   with urllib.request.urlopen(base_url) as url:
       get_posts_data = url.read()
       get_posts_response = json.loads(get_posts_data)

       post_object = None

       if get_posts_response:
           id=get_posts_response.get('id')
           author=get_posts_response.get('author')
           post=get_posts_response.get('post')
           post_object = Post(id,author,post)

   return post_object

