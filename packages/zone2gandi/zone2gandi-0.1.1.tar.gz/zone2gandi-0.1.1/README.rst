zone2gandi
==========

This is a tool for pushing simple zone files (skip the SOA and NS
records) up to Gandi.

Install by running: pip install zone2gandi

Getting API Credentials
~~~~~~~~~~~~~~~~~~~~~~~

http://doc.rpc.gandi.net/

Config
~~~~~~

The config file needs to be in the current directory and look like this:

.. code:: yaml
  apiendpoint: 'https://rpc.ote.gandi.net/xmlrpc/'
  apikey: 'm4ljWR8zQdSQUMhE03GJCv5p'
