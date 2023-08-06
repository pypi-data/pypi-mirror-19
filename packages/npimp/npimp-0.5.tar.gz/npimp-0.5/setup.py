from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='npimp',
    version='0.5',
    description='Notebook regulation daemon',
    long_description=long_description,
    author='Tomáš Kukrál',
    author_email='tomas.kukral@6shore.net',
    license='MIT',
    url='https://github.com/tomkukral/npimp/',
    download_url='https://github.com/tomkukral/npimp/archive/v0.4.tar.gz',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'npimp = npimp:main',
        ],
    },
)
