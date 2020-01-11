import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = '-^%osj2asg*)+b$ucqx5p=&fj)l630&o96hqmhy#l*-ps_&(3q'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bsharing',
        'USER': 'postgres',
        'PASSWORD': 'burak123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

