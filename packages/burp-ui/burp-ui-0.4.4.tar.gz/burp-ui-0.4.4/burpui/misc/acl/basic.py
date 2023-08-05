# -*- coding: utf8 -*-
from .interface import BUIacl, BUIaclLoader

import json


class ACLloader(BUIaclLoader):
    """See :class:`burpui.misc.acl.interface.BUIaclLoader`"""
    def __init__(self, app=None):
        """See :func:`burpui.misc.acl.interface.BUIaclLoader.__init__`

        :param app: Application context
        :type app: :class:`burpui.server.BUIServer`
        """
        self.app = app
        self.admins = [
            'admin'
        ]
        self.clients = {}
        self.servers = {}
        self.standalone = self.app.standalone
        conf = self.app.conf
        adms = []
        if 'BASIC:ACL' in conf.options:
            adms = conf.safe_get('admin', 'force_list', section='BASIC:ACL')
            for opt in conf.options.get('BASIC:ACL').keys():
                if opt == 'admin':
                    continue
                lit = conf.safe_get(opt, section='BASIC:ACL')
                rec = []
                try:
                    rec = json.loads(lit)
                    if isinstance(rec, dict):
                        self.servers[opt] = rec.keys()
                except Exception as e:
                    self.logger.error(str(e))
                    rec = [lit]
                self.clients[opt] = rec

        if adms and adms != [None]:
            self.admins = adms
        self._acl = BasicACL(self)
        self.logger.debug('admins: ' + str(self.admins))
        self.logger.debug('clients: ' + str(self.clients))
        self.logger.debug('servers: ' + str(self.servers))

    @property
    def acl(self):
        """Property to retrieve the backend"""
        if self._acl:
            return self._acl
        return None  # pragma: no cover


class BasicACL(BUIacl):
    """See :class:`burpui.misc.acl.interface.BUIacl`"""
    def __init__(self, handler=None):
        """:func:`burpui.misc.acl.interface.BUIacl.__init__` instanciate ACL
        engine.

        :param handler: ACL handler
        :type handler: :class:`burpui.misc.acl.interface.BUIaclLoader`
        """
        if not handler:  # pragma: no cover
            return
        self.handler = handler
        self.standalone = handler.standalone
        self.admins = handler.admins
        self.cls = handler.clients
        self.srv = handler.servers

    def is_admin(self, username=None):
        """See :func:`burpui.misc.acl.interface.BUIacl.is_admin`"""
        if not username:  # pragma: no cover
            return False
        return username in self.admins

    def clients(self, username=None, server=None):
        """See :func:`burpui.misc.acl.interface.BUIacl.clients`"""
        if not username:  # pragma: no cover
            return []
        if username in self.cls:
            cls = self.cls[username]
            if server and isinstance(cls, dict):
                if server in cls:
                    return cls[server]
                return []
            # No server defined whereas we have an extended ACL
            if not server and self.servers(username):
                return []
            return cls
        return [username]

    def servers(self, username=None):
        """See :func:`burpui.misc.acl.interface.BUIacl.servers`"""
        if username and username in self.srv:
            return self.srv[username]
        return []

    def is_client_allowed(self, username=None, client=None, server=None):
        """See :func:`burpui.misc.acl.interface.BUIacl.is_client_allowed`"""
        if not username or not client:  # pragma: no cover
            return False
        # No server defined whereas we have an extended ACL
        if not server and self.servers(username):
            return False
        cls = self.clients(username, server)
        return (cls and client in cls) or self.is_admin(username)
