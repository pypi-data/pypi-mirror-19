from distutils.core import setup

setup(
    name='Automatedscreenshots',
    version='0.3.4',
    author='Jim Barcelona',
    author_email='barce@me.com',
    packages=['automatedscreenshots', 'automatedscreenshots.tests'],
    install_requires=[
      'future',
    ],
    scripts=[],
    url='http://pypi.python.org/pypi/Automatedscreenshots/',
    license='LICENSE.txt',
    description='Useful screenshots stuff.',
    long_description=open('README.txt').read(),
)
