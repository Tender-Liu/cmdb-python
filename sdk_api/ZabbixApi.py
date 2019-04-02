# -*- encoding: utf-8 -*-
import json
import logging
import os
import ssl
import sys


try:
    import urllib2
except ImportError:
    import urllib.request as urllib2


class NullHandler(logging.Handler):
    """Null logger handler.
    :class:`NullHandler` will used if there are no other logger handlers.
    """
    def emit(self, record):
        pass

null_handler = NullHandler()
logger = logging.getLogger(__name__)
logger.addHandler(null_handler)


class ZabbixAPIException(Exception):
    def __init__(self, *args):
        super(Exception, self).__init__(*args)
        if len(args) == 1 and isinstance(args[0], dict):
            self.error = args[0]
            self.message = self.error['message']
            self.code = self.error['code']
            self.data = self.error['data']
            self.json = self.error['json']


class ZabbixAPIObjectClass(object):
    def __init__(self, group, parent):
        self.group = group
        self.parent = parent

    def __getattr__(self, name):


        def fn(*args, **kwargs):
            if args and kwargs:
                raise TypeError("Found both args and kwargs")

            method = '{0}.{1}'.format(self.group, name)
            logger.debug("Call %s method", method)

            return self.parent.do_request(
                method,
                args or kwargs
            )['result']

        return fn


def ssl_context_compat(func):
    def inner(req):
        # We shoul explicitly disable cert verification to support
        # self-signed certs with urllib2 since Python 2.7.9 and 3.4.3

        default_version = (2, 7, 9)
        version = {
            2: default_version,
            3: (3, 4, 3),
        }

        python_version = sys.version_info[0]
        minimum_version = version.get(python_version, default_version)

        if sys.version_info[0:3] >= minimum_version:
            # Create default context to skip SSL cert verification.
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            res = func(req, context=ctx)
        else:
            res = func(req)

        return res

    return inner


@ssl_context_compat
def urlopen(*args, **kwargs):
    return urllib2.urlopen(*args, **kwargs)


class ZabbixAPI(object):
    def __init__(self, url=None, use_authenticate=False, user=None,
                 password=None):

        url = url or os.environ.get('ZABBIX_URL') or 'https://localhost/zabbix'
        user = user or os.environ.get('ZABBIX_USER') or 'Admin'
        password = password or os.environ.get('ZABBIX_PASSWORD') or 'zabbix'

        self.use_authenticate = use_authenticate
        self.auth = None
        self.url = url + '/api_jsonrpc.php'
        self._login(user, password)
        logger.debug("JSON-PRC Server: %s", self.url)

    def __getattr__(self, name):
        """Dynamically create an object class (ie: host).
        :type name: str
        :param name: Zabbix API method group name.
            Example: `apiinfo.version` method it will be `apiinfo`.
        """

        return ZabbixAPIObjectClass(name, self)

    def _login(self, user='', password=''):
        """Do login to zabbix server.
        :type user: str
        :param user: Zabbix user
        :type password: str
        :param password: Zabbix user password
        """

        logger.debug("ZabbixAPI.login({0},{1})".format(user, password))

        self.auth = None

        if self.use_authenticate:
            self.auth = self.user.authenticate(user=user, password=password)
        else:
            self.auth = self.user.login(user=user, password=password)

    def api_version(self):
        """Return version of server Zabbix API.
        :rtype: str
        :return: Version of server Zabbix API.
        """

        return self.apiinfo.version()

    def do_request(self, method, params=None):
        request_json = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'id': '1',
        }

        # apiinfo.version and user.login doesn't require auth token
        if self.auth and (method not in ('apiinfo.version', 'user.login')):
            request_json['auth'] = self.auth

        logger.debug(
            'urllib2.Request({0}, {1})'.format(
                self.url,
                json.dumps(request_json)))

        data = json.dumps(request_json)
        if not isinstance(data, bytes):
            data = data.encode("utf-8")

        req = urllib2.Request(self.url, data)
        req.get_method = lambda: 'POST'
        req.add_header('Content-Type', 'application/json-rpc')

        try:
            res = urlopen(req)
            res_str = res.read().decode('utf-8')
            res_json = json.loads(res_str)
        except ValueError as e:
            raise ZabbixAPIException("Unable to parse json: %s" % e.message)

        res_str = json.dumps(res_json, indent=4, separators=(',', ': '))
        logger.debug("Response Body: %s", res_str)

        if 'error' in res_json:
            err = res_json['error'].copy()
            err.update({'json': str(request_json)})
            raise ZabbixAPIException(err)

        return res_json

    def get_id(self, item_type, item=None, with_id=False, hostid=None, **args):
        result = None
        name = args.get('name', False)

        type_ = '{item_type}.get'.format(item_type=item_type)

        item_filter_name = {
            'mediatype': 'description',
            'trigger': 'description',
            'triggerprototype': 'description',
            'user': 'alias',
            'usermacro': 'macro',
        }

        item_id_name = {
            'discoveryrule': 'item',
            'graphprototype': 'graph',
            'hostgroup': 'group',
            'itemprototype': 'item',
            'map': 'selement',
            'triggerprototype': 'trigger',
            'usergroup': 'usrgrp',
            'usermacro': 'hostmacro',
        }

        filter_ = {
            'filter': {
                item_filter_name.get(item_type, 'name'): item,
            },
            'output': 'extend'}

        if hostid:
            filter_['filter'].update({'hostid': hostid})

        if args.get('templateids'):
            if item_type == 'usermacro':
                filter_['hostids'] = args['templateids']
            else:
                filter_['templateids'] = args['templateids']

        if args.get('app_name'):
            filter_['application'] = args['app_name']

        logger.debug(
            'do_request( "{type}", {filter} )'.format(
                type=type_,
                filter=filter_))
        response = self.do_request(type_, filter_)['result']

        if response:
            item_id_str = item_id_name.get(item_type, item_type)
            item_id = '{item}id'.format(item=item_id_str)
            result = []
            for obj in response:
                # Check if object not belong current template
                if args.get('templateids'):
                    if (not obj.get('templateid') in ("0", None) or
                            not len(obj.get('templateids', [])) == 0):
                        continue

                if name:
                    o = obj.get(item_filter_name.get(item_type, 'name'))
                    result.append(o)
                elif with_id:
                    result.append({item_id: int(obj.get(item_id))})
                else:
                    result.append(int(obj.get(item_id)))

            list_types = (list, type(None))
            if not isinstance(item, list_types):
                result = result[0]

        return result