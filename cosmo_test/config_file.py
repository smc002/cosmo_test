import time, ctypes, shutil, stat
import os, os.path, sys
import configparser, logging
from constant_utility import config_file, removeall, config_path
from constant_utility import default_server, default_username, default_password, default_project_area, default_adapter_name, default_resource_folder, default_log_folder 
import encrypt


def change_option(section, option, value):
    assert os.path.exists(config_file), 'Configuration file: {} not found! Please run EA first.'.format(config_file)
    logger = logging.getLogger("COSMO.ea.config_file")
    logger.info('Configuration file {} changed'.format(config_file))
    logger.info('Section: {}; option: {}; value: {}'.format(section, option, value))
    config = configparser.ConfigParser()
    config.read(config_file)
    if section not in config.sections():
        config.add_section(section)
    if option == 'password':
        pass
        # value = "{}".format(ea.encrypt.encrypt(value[1:-1])) # the password in config file is enctrypted. Would be failed if the result is not in gbk.
    else:
        config.set(section, option, value)
        f = open(config_file, 'w')
        config.write(f)
        f.close()

def initialize(
        server = default_server,
        username = default_username,
        password = default_password,
        project_area = default_project_area,
        adapter_name = default_adapter_name,
        resource_folder = default_resource_folder,
        log_folder = default_log_folder,
        remove_original_file = False
        ):

    if not os.path.exists(config_path):
        os.makedirs(config_path)
    if not os.path.exists(config_file):
        f = open(config_file, 'w')
        f.close()
    shutil.copy('Configuration.ini', config_file)
    os.chmod( config_file, stat.S_IREAD | stat.S_IWRITE )
    if remove_original_file:
        removeall(config_file)
        with open(config_file, 'w') as f:
            pass


    change_option('Server', 'server address', '"{}"'.format(server))
    change_option('Server', 'username', '"{}"'.format(username))
    change_option('Server', 'password', '"{}"'.format(password)) # this is the 'test' with encryption
    change_option('Server', 'projectarea', '"{}"'.format(project_area))

    change_option('Client', 'name', '"{}"'.format(adapter_name))
    change_option('Client', 'rootresourcefolder', '"{}"'.format(resource_folder))
    change_option('Client', 'systemlogfolder', '"{}"'.format(log_folder))
    change_option('Client', 'systemlognamestyle', '"StaticName"')
    change_option('Client', 'connectatstartup', 'TRUE')
# use the same adapter id to avoid adapter choose in webpage
    change_option('Do not touch items in this section', 'adapterid', '"_hYzYFDFYEeOfmKniIK943w"')


if __name__ == "__main__":
    initialize(remove_original_file = True)
    # change_option('Client', 'ConnectAtStartup', 'FALSE')
