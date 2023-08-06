from setuptools import setup, find_packages
import os

import gitql


def extra_dependencies():
    import sys
    ret = []
    if sys.version_info < (2, 7):
        ret.append('argparse')
    if sys.version_info < (3, 4):
        ret.append('enum34')
    if sys.platform == 'win32':
        ret.append('pyreadline')
        ret.append('colorama')
    return ret


def read(*names):
    values = dict()
    extensions = ['txt', 'rst']
    for name in names:
        value = ''
        for ext in extensions:
            filename = name + ext
            if os.path.isfile(filename):
                value = open(filename).read()
                break
        values[name] = value
    return values


long_description = """
%(README)s
""" % read('README')

url = 'https://github.com/mackong/gitql'

setup(
    name='gitql',
    version=gitql.__version__,
    description='A git query language',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation',
    ],
    keywords='git gitql',
    author='MacKong',
    author_email='mackonghp@gmail.com',
    maintainer='MacKong',
    maintainer_email='mackonghp@gmail.com',
    url=url,
    download_url=url + '/tarball/' + gitql.__version__,
    license='MIT',
    packages=find_packages(),
    entry_points={'console_scripts': ['gitql = gitql.main:main', ]},
    install_requires=[
        'GitPython',
        'termcolor',
    ] + extra_dependencies(),
    include_package_data=True)
