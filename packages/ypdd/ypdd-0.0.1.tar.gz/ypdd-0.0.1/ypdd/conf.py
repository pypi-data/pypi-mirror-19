# coding: utf-8

import os
import json


class Config:
    def __init__(self, path=None):
        if path:
            conf_path = path
        else:
            home_dir = os.getenv('HOME')
            conf_path = os.path.join(home_dir, '.pdd.conf')

        self.conf = {}

        with open(conf_path) as f:
            self.conf = json.load(f)

    def __getattr__(self, item):
        try:
            return self.conf[item]
        except AttributeError:
            return None
