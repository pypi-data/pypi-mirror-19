from __future__ import print_function
from __future__ import unicode_literals

import re
import argparse
import requests
from requests.auth import HTTPBasicAuth

try:
    from devpi_server.auth import AuthException
    from devpi_server.log import threadlog

except ImportError:  # No devpi_server available
    class AuthException(Exception):
        pass

    import logging
    threadlog = logging

gitlab_url = None


def devpiserver_auth_user(userdict, username, password):
    """Attempt login to gitlab registry with the provided details."""

    global registry_url

    status = "unknown"
    if registry_url and username == 'gitlab-ci-token':
        status = "reject"
        try:
            if not registry_url.startswith('http'):
                registry_url = 'https://' + registry_url

            # Start communication with base registry url
            rsp = requests.get(registry_url+'/v2/', verify=False)
            # This will return the url to request a login ticket from
            parts = re.findall('realm="(.*?)",service="(.*?)"', rsp.headers['Www-Authenticate'])[0]
            authurl = '{realm}?service={service}'.format(realm=parts[0], service=parts[1])
            # login to the provided url with the passed in authentication
            rsp = requests.get(authurl, auth=HTTPBasicAuth(username, password), verify=False)
            # If they're accepted we get a 200 and a ticket!
            if rsp.status_code == 200 and b'token' in rsp.content:
                status = 'ok'
                threadlog.info("devpi-auth_gitlab accepting gitlab ci login")
        except:
            threadlog.exception("devpi-auth_gitlab failed to authenticate")

    return {'status': status}


class GitlabConfigAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        global registry_url
        registry_url = values
        setattr(namespace, self.dest, registry_url)


def devpiserver_add_parser_options(parser):
    gitlab = parser.addgroup("Gitlab auth")
    gitlab.addoption(
        "--gitlab-registry-url", action=GitlabConfigAction,
        help="Gitlab Registry URL")

