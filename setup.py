from setuptools import setup

setup(
    name='kai-python',
    version='0.1',
    packages=['KaiSDK'],
    install_requires=[
        'websocket_client',
    ],
    url='https://github.com/vicara-hq/kai-python',
    license='MIT',
    author='Vicara',
    author_email='dev@vicara.co',
    description='Python Client Library for the KaiSDK'
)
