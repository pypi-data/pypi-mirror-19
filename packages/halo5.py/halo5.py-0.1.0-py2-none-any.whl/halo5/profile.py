from halo5.base import Base
from urllib import quote_plus

class Profile(Base):
  """ For fetching the `Profile` info from the Halo 5 API """

  def __init__ (self, sub_key):
    super (Profile, self).__init__('profile/h5/profiles/', sub_key)

  def emblem_image (self, player, size=256):
    return self.get (
      params = { 'size' : size },
      url    = self.base_url + quote_plus (player) + '/emblem?').raw

  def spartan_image (self, player, size=256, crop='full'):
    return self.get (
      params = { 'size' : size, 'crop' : crop },
      url    = self.base_url + quote_plus (player) + '/spartan?').raw
