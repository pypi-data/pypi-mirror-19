"""

Установочный файл библиотеки

Created: 09.01.17 18:26
Author: Ivan Soshnikov, e-mail: ivan@wtp.su
"""

from setuptools import setup

setup(
    name='zeonapi',
    packages=['zeonapi'],  # this must be the same as the name above
    version='0.0.1',
    description='ZEON PBX API library',
    author='Ivan Soshnikov',
    author_email='ivan@wtp.su',
    url='https://github.com/soshnikov/zeonapi',
    download_url='https://github.com/soshnikov/zeonapi/archive/master.zip',
    keywords=[],
    classifiers=[],
    install_requires=[
        'progressbar-latest',
        'beautifulsoup4',
        'pydub',
        'pymongo',
        'simplejson',
    ]
)
