#!/usr/bin/env python3
import logging
import falcon
import bjoern
from photoblocks.exceptions import ConfigurationError
from .resources import PackResource, PeerResource, ChainResource, MineResource, HealthResource

def create_api(pack, db):
    """
    Create and configure the Photoblocks REST API
    
    Args:
        pack (dict): Node configuration package
        db (redis.Redis): Redis connection instance
        
    Returns:
        falcon.API: Configured API instance
        
    Raises:
        ConfigurationError: If required configuration is missing
    """
    try:
        app = falcon.API()
        
        # Add health check
        app.add_route('/health', HealthResource(pack=pack, db=db))
        
        # Register all resources
        app.add_route('/pack', PackResource(pack=pack, db=db))
        app.add_route('/nodes', PeerResource(pack=pack, db=db))
        app.add_route('/nodes/{id}', PeerResource(pack=pack, db=db))
        app.add_route('/chain', ChainResource(pack=pack, db=db))
        app.add_route('/mine', MineResource(pack=pack, db=db))
        
        return app
        
    except Exception as e:
        raise ConfigurationError(f"Failed to create API: {e}") 

def run_server(pack, db, host='0.0.0.0', port=None):
    """Run the API server using the configured web server"""
    try:
        app = create_api(pack, db)
        server_port = port or pack.get('port')
        if not server_port:
            raise ConfigurationError("No port specified")
            
        logging.info(f"Starting server on {host}:{server_port}")
        
        bjoern.run(app, host, server_port, reuse_port=True)
        
    except Exception as e:
        raise ConfigurationError(f"Failed to start server: {e}") 