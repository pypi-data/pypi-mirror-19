"""
Script to perform various ops against TC API
"""

from setuptools import setup, find_packages

setup(
    name='tctalker',
    version='0.1.0',
    description='Script to perform various ops against TC API',
    url='https://github.com/MihaiTabara/tctalker',
    author='Mihai Tabara',
    author_email='mtabara@mozilla.com',
    license='MPL',
    classifiers=[],
    keywords='taskcluster api cli tool',
    install_requires=['taskcluster'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'tctalker': ['*.sample'],
    },
    entry_points={
        'console_scripts': [
            'tctalker=tctalker.tctalker:main',
        ],
    },
)
