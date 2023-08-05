from distutils.core import setup

setup(
    name='SeansUtils',
    version='0.6',
    author='Sean Wade',
    author_email='seanwademail@gmail.com',
    packages=['seansUtils', 'seansUtils.research'],
    scripts=['bin/seansUtils-test', 'bin/research-dnn'],
    license='Apache-2.0',
    description='Seans usefull things',
    long_description=open('README.txt').read(),
)
