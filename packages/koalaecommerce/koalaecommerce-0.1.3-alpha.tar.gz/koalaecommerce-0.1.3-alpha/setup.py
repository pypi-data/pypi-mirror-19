from distutils.core import setup

setup(
    name='koalaecommerce',
    packages=['koalaecommerce'],  # this must be the same as the name above
    version='0.1.3-alpha',
    description='',
    author='Matt Badger',
    author_email='foss@lighthouseuk.net',
    url='https://github.com/LighthouseUK/koalaecommerce',  # use the URL to the github repo
    download_url='https://github.com/LighthouseUK/koalaecommerce/tarball/0.1.3-alpha',  # I'll explain this in a second
    keywords=['gae', 'lighthouse', 'koala'],  # arbitrary keywords
    classifiers=[],
    install_requires=[
        'koalacore==0.1.4-alpha',
        'blinker',
        'satchless',
        'itsdangerous',
        'prices',
        'pycrypto'
    ],
)
