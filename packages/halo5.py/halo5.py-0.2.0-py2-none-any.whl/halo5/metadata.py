from halo5.base import Base

class Metadata(Base):
  """ For fetching the `Metadata` info from the Halo 5 API """

  def __init__(self, sub_key):
    super (Metadata, self).__init__('metadata/h5/metadata/', sub_key)

  def campaign_missions (self):
    return self.get (url = self.base_url + 'campaign-missions')

  def commendations (self):
    return self.get (url = self.base_url + 'commendations')

  def csr_designations (self):
    return self.get (url = self.base_url + 'csr-designations')

  def enemies (self):
    return self.get (url = self.base_url + 'enemies')

  def flexible_stats (self):
    return self.get (url = self.base_url + 'flexible-stats')

  def game_base_variants (self):
    return self.get (url = self.base_url + 'game-base-variants')

  def game_variants (self, id):
    return self.get (url = self.base_url + 'game-variants/' + id)

  def impulses (self):
    return self.get (url = self.base_url + 'impulses')

  def map_variants (self, id):
    return self.get (url = self.base_url + 'map-variants/' + id)

  def maps (self):
    return self.get (url = self.base_url + 'maps')

  def medals (self):
    return self.get (url = self.base_url + 'medals')

  def playlists (self):
    return self.get (url = self.base_url + 'playlists')

  def requisition_packs (self, id):
    return self.get (url = self.base_url + 'requisition-packs/' + id)

  def requisitions (self, id):
    return self.get (url = self.base_url + 'requisitions/' + id)

  def seasons (self):
    return self.get (url = self.base_url + 'seasons')

  def skulls (self):
    return self.get (url = self.base_url + 'skulls')

  def spartan_ranks (self):
    return self.get (url = self.base_url + 'spartan-ranks')

  def team_colors (self):
    return self.get (url = self.base_url + 'team-colors')

  def vehicles (self):
    return self.get (url = self.base_url + 'vehicles')

  def weapons (self):
    return self.get (url = self.base_url + 'weapons')
