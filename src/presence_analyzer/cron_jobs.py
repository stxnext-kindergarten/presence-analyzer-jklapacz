# -*- coding: utf-8 -*-
"""
Cron entry points - for example: update remote users xml file
"""
import os
import urllib2
import sys

from presence_analyzer.main import app


def update_users_xml():
    """
    Download/update local xml file with user data
    user can pass url of remote xml file:
    ./cron_jobs_update_xml remote.server.com/path/to/users.xml
    """
    app.config.from_pyfile(
        os.path.join(
            os.path.dirname(__file__), '..', '..', 'parts', 'etc', 'deploy.cfg'
        )
    )

    if len(sys.argv) == 2:
        app.config['REMOTE_USERS_XML_URL'] = sys.argv[1]

    remote = urllib2.urlopen(app.config['REMOTE_USERS_XML_URL'])
    with open(app.config['USERS_XML'], 'w') as local:
        local.write(remote.read())
        print 'file updated'
