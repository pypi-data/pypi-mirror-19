# Essential for interacting with REST API
import requests
from entity import Entity

# For encoding requests
try:
  from urllib import urlencode
except ImportError:
  from urllib.parse import urlencode

class Base(object):
  """ Base class w/all essentials inside """

  def __init__(self, url_ext, sub_key):
    self.base_url = 'https://www.haloapi.com/' + url_ext
    self.sub_key = sub_key
    self.debug = False

  def get(self, **kwargs):
    # Prepare request
    param_str = urlencode (kwargs.get('params', {}))
    url = kwargs.get('url')
    headers = kwargs.get('headers', {})
    headers['Ocp-Apim-Subscription-Key'] = self.sub_key
    total_url = url + param_str
    if (self.debug): print 'Requested: ' + total_url

    # Process response
    r = requests.get(total_url, headers=headers)
    return (
      Entity.create_entity(r.json()) if 'json' in r.headers['Content-Type']
      else Entity.create_entity(r.raw)
    )
