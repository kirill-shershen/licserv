# -*- coding: utf-8 -*-
import os

def get(name, default = ''):
    return os.environ.get(name, default)

PORT = int(os.environ.get('PORT', 5000))
SQLALCHEMY_DATABASE_URI = get('DATABASE_URL')
