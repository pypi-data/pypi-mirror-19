from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='aiocall',
    packages=['aiocall'],
    version='0.2',
    description='The missing call methods for python asyncio',
    long_description=readme(),
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: Public Domain',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    ],
    author='Holger Waldmann',
    author_email='holger.waldmann@web.de',
    url='http://github.com/waldhol/aiocall',
    license='Public Domain',
    include_package_data=True,
    zip_safe=False,
    )
