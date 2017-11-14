# -*- coding: utf-8 -*-
import os

def get(name, default = ''):
    return os.environ.get(name, default)

SQLALCHEMY_DATABASE_URI = get('DATABASE_URL')
