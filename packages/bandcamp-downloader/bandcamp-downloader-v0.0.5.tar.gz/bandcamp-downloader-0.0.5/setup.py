from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bandcamp-downloader',
    version='0.0.5',
    description='bandcamp-dl downloads albums and tracks from Bandcamp for you',
    long_description=long_description,
    url='https://github.com/iheanyi/bandcamp-dl',
    author='Iheanyi Ekechukwu',
    author_email='iekechukwu@gmail.com',
    license='Unlicense',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Sound/Audio',
        'License :: Public Domain',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['bandcamp', 'downloader', 'music', 'cli', 'albums', 'dl'],
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'docopt',
        'mutagen',
        'ply',
        'requests',
        'slimit',
        'unicode-slugify',
    ],
    entry_points={
        'console_scripts': [
            'bandcamp-dl=bandcamp_dl.bandcamp_dl:main',
        ],
    },
)
