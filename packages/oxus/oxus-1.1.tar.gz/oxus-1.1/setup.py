"""
oxus
-----------

oxus is a python package for making stand-alone interactive plots

Link
`````

* Source
  https://github.com/kouroshparsa/oxus

"""
from setuptools import Command, setup, find_packages
import os
from distutils import sysconfig;
inc_path = sysconfig.get_config_vars()['INCLUDEPY']
if not os.path.exists(os.path.join(inc_path, 'Python.h')):
    raise Exception('You must install python headers to install the Paramiko dependency.'\
        '\nExample on ubuntu: sudo apt-get install python-dev'\
        '\nExample on centos: sudo yum install python-dev')

version = '1.1'
import sys
setup(
    name='oxus',
    version=version,
    url='https://github.com/kouroshparsa/oxus',
    download_url='https://github.com/kouroshparsa/oxus/packages/%s' % version,
    license='GNU',
    author='Kourosh Parsa',
    author_email="kouroshtheking@gmail.com",
    description='Interactive plots',
    long_description=__doc__,
    packages=find_packages(),
    install_requires = ['Jinja2>=2.1'],
    include_package_data=True,
    zip_safe=False,
    platforms='Any',
    classifiers=[
        'Operating System :: Unix',
        'Programming Language :: Python'
    ]
)

