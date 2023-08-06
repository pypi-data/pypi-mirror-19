AUTHOR = 'Vsevolod Novikov'
AUTHOR_EMAIL = 'nnseva@gmail.com'
URL = 'https://github.com/nnseva/django-jsoneditor'

import jsoneditor

from setuptools import setup, find_packages

description = 'Django JSON Editor'

try:
	with open('README.md') as f:
	    long_description = f.read()
except FileNotFoundError:
	long_description = ""

setup(
    name = 'django-jsoneditor-ng',
    version = jsoneditor.__version__,
    description = description,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    long_description = long_description,
    packages = ['jsoneditor','jsoneditor.fields'],
    package_data = {'jsoneditor':['static/jsoneditor/*.js','static/jsoneditor/*.css','static/jsoneditor/img/*','static/django-jsoneditor/*.js']},
    include_package_data = True,
    zip_safe = False,
)
