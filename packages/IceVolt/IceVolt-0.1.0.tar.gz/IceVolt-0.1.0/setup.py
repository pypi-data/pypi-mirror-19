from distutils.core import setup

setup(
    # Application name:
    name='IceVolt',

    # Version number (initial):
    version='0.1.0',

    # Application author details:
    author='Clint Moyer',
    author_email='contact@clintmoyer.com',

    # Packages
    packages=['icevolt'],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url='http://pypi.python.org/pypi/icevolt_v010/',

    #
    license='LICENSE.txt',
    description='A mini blog with minimal architecture',

    long_description=open('README.md').read(),

    # Dependent packages (distributions)
    install_requires=[
        'flask',
        'sqlalchemy',
        'csscompressor'
    ],
)

