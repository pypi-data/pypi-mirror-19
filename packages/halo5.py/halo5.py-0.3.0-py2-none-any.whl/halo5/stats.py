from halo5.base import Base
from urllib import quote_plus

class Stats(Base):
  """ For fetching the `Stats` info from the Halo 5 API """

  def __init__ (self, sub_key):
    super (Stats, self).__init__('stats/h5/', sub_key)

  # Private
  def _post_game (self, game_type, match_id):
    full_url = self.base_url + game_type + '/matches/' + match_id
    return self.get (url = full_url)

  # Private
  def _service_record (self, game_type, players = [], season_id = None):
    full_url = self.base_url + 'servicerecords/' + game_type + '?'
    params = { 'players' : ','.join([quote_plus(p) for p in players]) }
    if season_id is not None: params['seasonId'] = season_id
    return self.get (params = params, url = full_url)

  def events_for_match (self, match_id):
    return self.get (
      url = self.base_url + 'matches/' + match_id + '/events')

  def matches_for_player (self, player, modes = None, start = 0, count = 25):
    params = { 'start' : start, 'count' : count }
    if modes is not None: params['modes'] = modes
    full_url = self.base_url + 'players/' + quote_plus (player) + '/matches?'
    return self.get (params = params, url = full_url)

  def player_leaderboard (self, season_id, playlist_id, count=200):
    params = { 'count' : count }
    full_url = ''.join ([self.base_url, 'player-leaderboards/csr/',
      season_id, '/', playlist_id, '?'])
    return self.get (params = params, url = full_url)

  def post_game_arena (self, match_id):
    return self._post_game('arena', match_id)

  def post_game_campaign (self, match_id):
    return self._post_game('campaign', match_id)

  def post_game_custom (self, match_id):
    return self._post_game ('custom', match_id)

  def post_game_warzone (self, match_id):
    return self._post_game('warzone', match_id)

  def service_record_arena (self, players = [], season_id = None):
    return self._service_record('arena', players, season_id)

  def service_record_campaign (self, players = []):
    return self._service_record('campaign', players)

  def service_record_custom (self, players = []):
    return self._service_record('custom', players)

  def service_record_warzone (self, players = []):
    return self._service_record('warzone', players)
