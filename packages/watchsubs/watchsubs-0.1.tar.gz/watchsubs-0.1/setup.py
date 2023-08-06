#!/usr/bin/env python

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='watchsubs',
    version='0.1',
    packages=['watchsubs'],
    description='Joint magic from watchdog and subliminal',
    author='Enrique',
    author_email='enrique.manjavacas@gmail.com',
    url='https://www.github.com/emanjavacas/watchsubs',
    download_url='https://api.github.com/repos/emanjavacas/watchsubs/tarball',
    install_requires=[
        'watchdog>=0.8.3',
        'subliminal>=2.0.5'
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'watchsubs = watchsubs.watchsubs:main'
        ]
    }
)


try:
    from distutils import sysconfig

    def get_bin_path():
        lib = sysconfig.get_python_lib()
        bin_path = os.path.dirname(os.path.dirname(lib))[:-3] + 'bin'
        return bin_path

    print(("\n***\n" +
           "`watchsubs` should've been installed to [%s].\n" +
           "Unless you've used a different location," +
           "make sure to include that directory into your PATH\n" +
           "***\n") % get_bin_path())
    print("To permanently watch a directory for movies, add the following" +
          " line to your crontab file:\n  @reboot watchsubs --path PATH\n")

except ImportError:
    pass
