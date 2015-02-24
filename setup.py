from setuptools import setup
from os.path import exists

setup(
    name='pyope',
    version='0.0.2',
    description='Implementation of symmetric order-preserving encryption scheme',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Security :: Cryptography',
    ],
    url='https://github.com/rev112/pyope/',
    author='Anton Ovchinnikov',
    author_email='anton.ovchi2nikov@gmail.com',
    license='MIT',
    packages=['pyope'],
    install_requires=['pytest>=2.6.4', 'pycrypto>=2.6.1'],
    zip_safe=False,
)
