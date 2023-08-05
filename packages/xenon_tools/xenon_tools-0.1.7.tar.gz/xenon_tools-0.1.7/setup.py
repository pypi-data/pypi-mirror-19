from distutils.core import setup

'''python setup.py sdist upload -r pypi'''

setup(
    name='xenon_tools',
    packages=['xenon_tools'],  # this must be the same as the name above
    version='0.1.7',
    description='Tools for Xenon',
    author='minus79',
    author_email='gergely06@gmail.com',
    url='https://github.com/minus79/xenon_tools',  # use the URL to the github repo
    download_url='https://github.com/minus79/xenon_tools/tarball/0.1',  # I'll explain this in a second
    keywords=['xenon', 'xenon-tools', 'xenon_tools'],  # arbitrary keywords
    classifiers=[],
)
