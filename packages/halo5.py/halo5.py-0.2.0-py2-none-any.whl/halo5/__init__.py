""" Halo 5: Guardians API Wrapper """

__version__ = '0.2.0'
__all__ = ['Client']

USER_AGENT = 'Halo 5: Guardians API Wrapper %s' % __version__

from halo5.client import Client
