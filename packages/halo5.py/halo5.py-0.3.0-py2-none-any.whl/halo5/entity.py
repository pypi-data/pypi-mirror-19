class Entity(object):
  """ Wrapper for response from Halo 5 API """

  @staticmethod
  def create_entity (obj):
    if type(obj) is dict:
      for k in obj.keys():
        obj[k] = Entity.create_entity(obj[k])
      return Entity(obj)
    elif type(obj) is list:
      for i in range(0, len(obj)):
        obj[i] = Entity.create_entity(obj[i])
      return obj
    else: return obj

  def __init__(self, obj):
    self.obj = obj

  def __getattr__(self, name):
    if name in self.obj:
      return self.obj.get(name)
    raise AttributeError
