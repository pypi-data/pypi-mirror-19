from halo5.base import Base
from halo5.metadata import Metadata
from halo5.profile import Profile
from halo5.stats import Stats
from halo5.ugc import UGC

class Client(object):
  """ The client for interacting with Halo 5 resources """

  def __init__(self, sub_key):
    self.sub_key  = sub_key
    self.metadata = Metadata (self.sub_key)
    self.profile  = Profile (self.sub_key)
    self.stats    = Stats (self.sub_key)
    self.ugc      = UGC (self.sub_key)
