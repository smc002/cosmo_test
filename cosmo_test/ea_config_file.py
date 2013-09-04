import time, ctypes
import os, os.path, sys
import configparser, logging
from constant_utility import config_file 
from constant_utility import default_server, default_username, default_password, default_project_area, default_adapter_name, default_resource_folder, default_log_folder 


def change_option(section, option, value):
    assert os.path.exists(config_file), 'Configuration file: {} not found! Please run EA first.'.format(config_file)
    logger = logging.getLogger("COSMO.ea.config_file")
    logger.info('Configuration file {} changed'.format(config_file))
    logger.info('Section: {}; option: {}; value: {}'.format(section, option, value))
    config = configparser.ConfigParser()
    config.read(config_file)
    config.set(section, option, value)
    config.write(open(config_file, 'w'))

def initialize(
        server = default_server,
        username = default_username,
        project_area = default_project_area,
        adapter_name = default_adapter_name,
        resource_folder = default_resource_folder,
        log_folder = default_log_folder):
    change_option('Server', 'server address', '"{}"'.format(server))
    change_option('Server', 'Address', '"{}"'.format(server))
# todo: not finished. Changed configuration file could not be recognized by EA.






if __name__ == "__main__":
    initialize()
