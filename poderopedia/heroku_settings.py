import os

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ASSETS_DEBUG = os.environ.get('ASSET_DEBUG', 'False') == 'True'
ASSETS_AUTO_BUILD = False

GRANO_HOST = os.environ.get('GRANO_HOST', 'http://beta.grano.cc/')
GRANO_APIKEY = os.environ.get('GRANO_APIKEY')
GRANO_PROJECT = os.environ.get('GRANO_PROJECT', 'poderopedia')
