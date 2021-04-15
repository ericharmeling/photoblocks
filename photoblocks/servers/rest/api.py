#!/usr/bin/env python3
import logging
import json
from servers.rest.resources import PackResource, PeerResource, ChainResource, MineResource
import falcon
#import bjoern

def api(pack, db):
    app = falcon.API()
    app.add_route('/pack', PackResource(pack=pack, db=db))
    app.add_route('/nodes', PeerResource(pack=pack, db=db))
    app.add_route('/nodes/{id}', PeerResource(pack=pack, db=db))
    app.add_route('/chain', ChainResource(pack=pack, db=db))
    app.add_route('/mine', MineResource(pack=pack, db=db))
#    bjoern.run(app, node.host, node.port, reuse_port=True)

