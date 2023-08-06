# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='django-react-cms',
    version='0.1.0',
    author=u'Leonardo Arroyo',
    author_email='contato@leonardoarroyo.com',
    packages=find_packages(),
    url='https://github.com/leonardoarroyo/django-react-cms',
    download_url = 'https://github.com/leonardoarroyo/django-react-cms/tarball/0.1.0',
    license='MIT',
    description='Manage and export react components to the client.',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires=reqs
)
