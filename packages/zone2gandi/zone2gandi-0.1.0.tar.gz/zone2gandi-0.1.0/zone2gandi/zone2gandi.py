# -*- coding: utf-8 -*-

"""zone2gandi.zone2gandi: provides entry point main()."""

import sys
import yaml
import xmlrpclib

__version__ = "0.1.0"

def main():
  try:
    config = yaml.safe_load(open('config', 'r').read())
  except:
    print 'Create config like "config.sample".'
    sys.exit(1)
  apiendpoint = config['apiendpoint']
  apikey = config['apikey']

  api = xmlrpclib.ServerProxy(apiendpoint)
  gzones = api.domain.zone.list(apikey)
  for zonepath in sys.argv[1:]:
    with open(zonepath, 'r') as zonefd:
      zone = zonefd.read()
    zonefile = zonepath[zonepath.rfind('/') + 1:]
    gzone = {}
    for gzone_needle in gzones:
      if gzone_needle['name'] == zonefile:
        gzone = gzone_needle
        break
    if not gzone:
      gzone = api.domain.zone.create(apikey, { 'name': zonefile })
    version = api.domain.zone.version.new(apikey, gzone['id'])
    api.domain.zone.record.set(apikey, gzone['id'], version, zone)
    api.domain.zone.version.set(apikey, gzone['id'], version)
    api.domain.zone.version.delete(apikey, gzone['id'], gzone['version'])
    print 'Zonefile %s updated (gandi version %d)' % (zonefile, version)
