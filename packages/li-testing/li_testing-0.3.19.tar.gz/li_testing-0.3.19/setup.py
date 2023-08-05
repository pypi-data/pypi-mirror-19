# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def get_version_from_file():
    # get version number from __init__ file
    # before module is installed

    fname = 'li_testing/__init__.py'
    with open(fname) as f:
        fcontent = f.readlines()
    version_line = [l for l in fcontent if 'VERSION' in l][0]
    return version_line.split('=')[1].strip().strip("'").strip('"')


VERSION = get_version_from_file()

DESCRIPTION = """
Package containing stuff usefull for testing purposes.
""".strip()


setup(name='li_testing',
      version=VERSION,
      author='Juca Crispim',
      author_email='juca@lojaintegrada.com.br',
      url='',
      description=DESCRIPTION,
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=['selenium>=3.0.1', 'boto>=2.38.0',
                        'li-repo==1.9.31'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Testing',
      ],
      test_suite='tests',
      provides=['li_testing'],)
