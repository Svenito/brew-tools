import appdirs
import os
import configparser

current_config = configparser.ConfigParser()

APPNAME = "brewtools"
FILENAME = "brewtools.conf"

units = ["imperial", "metric"]


def config_file() -> str:
    config_dir = appdirs.user_config_dir(APPNAME)
    return os.path.join(config_dir, FILENAME)


def exists() -> bool:
    return os.path.exists(config_file())


def write_config():
    if not os.path.exists(appdirs.user_config_dir(APPNAME)):
        os.makedirs(appdirs.user_config_dir(APPNAME))
    with open(config_file(), "w") as f:
        current_config.write(f)

    return current_config


def read_config():
    current_config.read(config_file())
