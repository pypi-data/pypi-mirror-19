# Copyright (c) 2016 Jiocloud.com, Inc. or its affiliates.  All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import os
"""
  The following endpoints can be overridden using environment variable
  The environment variable should be in the form of SERVICE_URL, where
  SERVICE is the service keyword in captial.

  Also, user has to export his access and secret key as environment
  variables. Without this, UnknownCredentials exception is thrown
"""

import argparse
import exception

config_handler = None

def setup_config_handler(url, access_key, secret_key, secure, debug):
    """
    Create global object of ConfigHandler based on the arguments
    passed to cli.

    This is to handle the arguments like --debug and --secure
    which are not specific to any command.

    param args: command line arguments passed.

    return: None
    """
    global config_handler
    if not config_handler:
        config_handler = ConfigHandler(url, access_key, secret_key, secure, debug)

def get_config_handler():
    """Fetch the global object of ConfigHandler."""
    global config_handler
    # This is to ensure that incase the initial setup
    # of config handler failed,
    return config_handler

def get_secret_key():
    """Return the secret key for the account user."""
    return get_config_handler().get_secret_key()

def get_access_key():
    """Return the access key for the account user."""
    return get_config_handler().get_access_key()

def get_service_url():
    """
    Return the access key for the account user.

    param service: service name whose url needed

    return: string containing the url
    """
    return get_config_handler().get_service_url()

def check_secure():
    """Check whether to use certificates for connection"""
    return get_config_handler().check_secure()

def check_debug():
    """Check whether trace is requested if exception occurs"""
    # This would become a chicken and egg situation if config
    # setup fails. So just return False if config_handler
    # wasnt created till this point
    return config_handler and get_config_handler().check_debug()

class ConfigHandler(object):
    """
    Object to handle all the config related tasks for the cli

    This deals with:
    1. Providing service specific endpoints
    2. Access/Secret Key values
    3. Processing general arguments given by user
    """
    def __init__(self, endpoint, acsK, secK, secure, debug):
        self.endpoint = endpoint
        self.secure = secure
        self.debug = debug
        self.access_key = acsK
        self.secret_key = secK
        if not self.access_key or not self.secret_key:
            raise exception.UnknownCredentials()

    def get_service_url(self):
        return self.endpoint

    def get_access_key(self):
        return self.access_key

    def get_secret_key(self):
        return self.secret_key

    def check_secure(self):
        return self.secure

    def check_debug(self):
        return self.debug


