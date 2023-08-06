from distutils.core import setup

setup(
    name='IPStreet',
    packages=['IPStreet'],  # this must be the same as the name above
    version='v0.2',
    description='A Python SDK for interacting with the IP Street API',
    author='Reed Jessen',
    author_email='Reed@IPStreet.com',
    url='https://github.com/IPStreet/PythonSDK',  # use the URL to the github repo
    download_url='https://github.com/IPStreet/PythonSDK/archive/v0.2.tar.gz',  # I'll explain this in a second
    install_requires=['requests'],
    keywords=['patent', 'SDK', 'IP Street', 'API', 'wrapper'],  # arbitrary keywords
    classifiers=[],
)
