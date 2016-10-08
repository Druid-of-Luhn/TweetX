from setuptools import setup

setup(
    name='tweetx',
    version='0.0.1',
    description='In space, everyone can hear you tweet.',
    packages=['tweetx', 'tweetx.bot'],
    install_requires=[
        'tweepy',
        'websockets'
    ]
)
