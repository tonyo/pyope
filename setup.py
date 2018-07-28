import os
from setuptools import setup

setup_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(setup_dir, 'README.rst')) as readme_file:
    readme = readme_file.read()

with open(os.path.join(setup_dir, 'HISTORY.rst')) as history_file:
    history = history_file.read()

setup(
    name='pyope',
    version='0.2.2',
    description='Implementation of symmetric order-preserving encryption scheme',
    long_description=readme + '\n\n' + history,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Security :: Cryptography',
    ],
    url='https://github.com/tonyo/pyope/',
    author='Anton Ovchinnikov',
    author_email='anton.ovchi2nikov@gmail.com',
    license='MIT',
    packages=['pyope'],
    install_requires=[
        'cryptography>=1.1',
        'six>=1.5.0',
    ],
)
