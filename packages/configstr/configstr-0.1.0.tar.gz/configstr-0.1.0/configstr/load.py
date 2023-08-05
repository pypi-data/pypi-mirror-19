import os
import argparse
import logging
import requests

from .exceptions import ConfigstrSetupError

logger = logging.getLogger(__name__)

logger.debug("reading configuration from environment")
CONFIGSTR_ENV = os.environ.get("CONFIGSTR_ENV")
CONFIGSTR_KEY = os.environ.get("CONFIGSTR_KEY")
CONFIGSTR_HOST = os.environ.get("CONFIGSTR_HOST") or "https://api.configstr.io"


def cs_headers(key):
    return {'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + key}


def cs_env(env):
    return CONFIGSTR_HOST + '/api/v1/environment/' + env


def cs_creds(env, key):
    env = env or CONFIGSTR_ENV
    key = key or CONFIGSTR_KEY
    # TODO load from file here if needed
    if env is None:
        raise ConfigstrSetupError("environment id required")
    if key is None:
        raise ConfigstrSetupError("access key required")
    return env, key


def load_config(env=None, key=None):
    env, key = cs_creds(env, key)
    logger.info("loading environment %s", env)
    r = requests.get(cs_env(env), headers=cs_headers(key))
    r.raise_for_status()
    response = r.json()
    env_name = response['name']
    config_id = response['config']['id']
    data = response['config']['data']
    namespace = argparse.Namespace(**data)
    logger.info("loaded %s configuration: %s", env_name, namespace)
    return namespace
