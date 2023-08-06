import os
import microcache
import tempfile
import ruamel.yaml as yaml
from . import snippets

try:
    import ConfigParser as configparser
except ImportError:
    import configparser


class ConfigError(RuntimeError):
    pass


CONFIG_LOCATIONS = [
    '~/.hatchery/hatchery.yaml', '~/.hatchery/hatchery.yml', '.hatchery.yaml', '.hatchery.yml'
]


@microcache.this
def from_yaml():
    """ Load configuration from yaml source(s), cached to only run once """
    default_yaml_str = snippets.get_snippet_content('hatchery.yml')
    ret = yaml.load(default_yaml_str, Loader=yaml.RoundTripLoader)
    for config_path in CONFIG_LOCATIONS:
        config_path = os.path.expanduser(config_path)
        if os.path.isfile(config_path):
            with open(config_path) as config_file:
                config_dict = yaml.load(config_file, Loader=yaml.RoundTripLoader)
                if config_dict is None:
                    continue
                for k, v in config_dict.items():
                    if k not in ret.keys():
                        raise ConfigError(
                            'found garbage key "{}" in {}'.format(k, config_path)
                        )
                    ret[k] = v
    return ret


PYPIRC_LOCATIONS = ['~/.pypirc']


@microcache.this
def from_pypirc(pypi_repository):
    """ Load configuration from .pypirc file, cached to only run once """
    ret = {}
    pypirc_locations = PYPIRC_LOCATIONS
    for pypirc_path in pypirc_locations:
        pypirc_path = os.path.expanduser(pypirc_path)
        if os.path.isfile(pypirc_path):
            parser = configparser.SafeConfigParser()
            parser.read(pypirc_path)
            if 'distutils' not in parser.sections():
                continue
            if 'index-servers' not in parser.options('distutils'):
                continue
            if pypi_repository not in parser.get('distutils', 'index-servers'):
                continue
            if pypi_repository in parser.sections():
                for option in parser.options(pypi_repository):
                    ret[option] = parser.get(pypi_repository, option)
    if not ret:
        raise ConfigError(
            'repository does not appear to be configured in pypirc ({})'.format(pypi_repository) +
            ', remember that it needs an entry in [distutils] and its own section'
        )
    return ret


PYPIRC_TEMP_INDEX_NAME = 'hatchery_tmp'
PYPIRC_TEMPLATE = '''
[distutils]
index-servers =
    {index_name}

[{index_name}]
repository = {index_url}
username = anonymous
password = nopassword
'''


@microcache.this
def pypirc_temp(index_url):
    """ Create a temporary pypirc file for interaction with twine """
    pypirc_file = tempfile.NamedTemporaryFile(suffix='.pypirc', delete=False)
    print(pypirc_file.name)
    with open(pypirc_file.name, 'w') as fh:
        fh.write(PYPIRC_TEMPLATE.format(index_name=PYPIRC_TEMP_INDEX_NAME, index_url=index_url))
    return pypirc_file.name
