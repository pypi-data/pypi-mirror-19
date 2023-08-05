from halo5.base import Base

class Metadata(Base):
  """ For fetching the `Metadata` info from the Halo 5 API """

  def __init__(self, sub_key):
    super (Metadata, self).__init__('metadata/h5/metadata/', sub_key)

  def campaign_missions (self):
    return self.get (url = self.base_url + 'campaign-missions').json()

  def commendations (self):
    return self.get (url = self.base_url + 'commendations').json()

  def csr_designations (self):
    return self.get (url = self.base_url + 'csr-designations').json()

  def enemies (self):
    return self.get (url = self.base_url + 'enemies').json()

  def flexible_stats (self):
    return self.get (url = self.base_url + 'flexible-stats').json()

  def game_base_variants (self):
    return self.get (url = self.base_url + 'game-base-variants').json()

  def game_variants (self, id):
    return self.get (url = self.base_url + 'game-variants/' + id).json()

  def impulses (self):
    return self.get (url = self.base_url + 'impulses').json()

  def map_variants (self, id):
    return self.get (url = self.base_url + 'map-variants/' + id).json()

  def maps (self):
    return self.get (url = self.base_url + 'maps').json()

  def medals (self):
    return self.get (url = self.base_url + 'medals').json()

  def playlists (self):
    return self.get (url = self.base_url + 'playlists').json()

  def requisition_packs (self, id):
    return self.get (url = self.base_url + 'requisition-packs/' + id).json()

  def requisitions (self, id):
    return self.get (url = self.base_url + 'requisitions/' + id).json()

  def seasons (self):
    return self.get (url = self.base_url + 'seasons').json()

  def skulls (self):
    return self.get (url = self.base_url + 'skulls').json()

  def spartan_ranks (self):
    return self.get (url = self.base_url + 'spartan-ranks').json()

  def team_colors (self):
    return self.get (url = self.base_url + 'team-colors').json()

  def vehicles (self):
    return self.get (url = self.base_url + 'vehicles').json()

  def weapons (self):
    return self.get (url = self.base_url + 'weapons').json()
