"""
Openedoo-Script
--------------

Flask support for writing external scripts.

Links
`````

* `documentation <http://flask-script.readthedocs.org>`_


"""
import sys
from setuptools import setup

version='0.1.1'

# Hack to prevent stupid TypeError: 'NoneType' object is not callable error on
# exit of python setup.py test # in multiprocessing/util.py _exit_function when
# running python setup.py test (see
# https://github.com/pypa/virtualenv/pull/259)
try:
    import multiprocessing
except ImportError:
    pass

install_requires = ['Flask']

setup(
    name='Openedoo-Script-Test',
    version=version,
    url='https://github.com/openedoo/openedoo-script',
	download_url = 'https://github.com/openedoo/openedoo-script/archive/master.zip',
    license='MIT',
    author='rendiya',
    author_email='ligerrendy@gmail.com',
    maintainer='rendiya',
    maintainer_email='ligerrendy@gmail.com',
    description='Scripting support for Flask',
    long_description='hello',
    packages=[
        'openedoo_script'
    ],
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[
        'pytest',
    ],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
