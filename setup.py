from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='pyope',
    version='0.1.1',
    description='Implementation of symmetric order-preserving encryption scheme',
    long_description=readme + '\n\n' + history,
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
    install_requires=[
        'cryptography>=1.1',
    ],
)
