# -*- coding:utf-8 -*-
import os

import lib_fabric_dreamhost


def get_templates_folder():
    return os.path.join(os.path.dirname(lib_fabric_dreamhost.__file__), 'templates')


def get_filepath(filename):
    return os.path.join(get_templates_folder(), filename)
