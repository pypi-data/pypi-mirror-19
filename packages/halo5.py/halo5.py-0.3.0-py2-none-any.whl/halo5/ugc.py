from halo5.base import Base
from urllib import quote_plus

class UGC(Base):
  """ For fetching the `UGC` info from the Halo 5 API """

  def __init__ (self, sub_key):
    super (UGC, self).__init__('ugc/h5/players/', sub_key)

  # Private
  def _get_variant (self, v_type, player, variant):
    full_url = self.base_url + quote_plus (player) + '/' + v_type + '/' + variant
    return self.get (url = full_url)

  # Private
  def _list_variants (self, v_type, player, start = 0, count = 25,
  sort = 'modified', order = 'desc'):
    full_url = self.base_url + quote_plus (player) + '/' + v_type + '?'
    params = { 'start' : start, 'count' : count, 'sort' : sort, 'order' : order }
    return self.get (params = params, url = full_url)

  def get_game_variant (self, player, variant):
    return self._get_variant('gamevariants', player, variant)

  def get_map_variant (self, player, variant):
    return self._get_variant('mapvariants', player, variant)

  def list_game_variants (self, player, start = 0, count = 25,
  sort = 'modified', order = 'desc'):
    return self._list_variants('gamevariants', player, start, count, sort, order)

  def list_map_variants (self, player, start = 0, count = 25,
  sort = 'modified', order = 'desc'):
    return self._list_variants('mapvariants', player, start, count, sort, order)
