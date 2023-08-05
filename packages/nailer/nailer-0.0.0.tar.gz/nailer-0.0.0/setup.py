from setuptools import find_packages, setup

setup(
    name='nailer',
    version='0.0.0',
    description='Using nailgun reads YAML description and populate a system',
    long_description='Reads definition from YAML file to populate the system using nailgun',
    url='https://github.com/SatelliteQE/nailer',
    author='Bruno Rocha',
    author_email='rochacbruno@gmail.com',
    license='GPLv3',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: GNU General Public License v3 or later '
         '(GPLv3+)'),
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    install_requires=[
        'nailgun',
        'import_string',
        'manage'
    ],
)
