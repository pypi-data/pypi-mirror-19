import os, sys
try:
    from setuptools import setup, find_packages
    use_setuptools = True
except ImportError:
    from distutils.core import setup
    use_setuptools = False

try:
    with open('README.md', 'rt') as readme:
        description = '\n' + readme.read()
except IOError:
    # maybe running setup.py from some other dir
    description = ''

install_requires = [
    'crossbar>=16.10.1',
    'scikit-learn>=0.18.1'
]

setup(
    name="edkit-server",
    version='0.3.1',
    url='https://github.com/edkit/edkit-server',
    license='MIT',
    description="edkit server package for local usage",
    long_description=description,
    author='Romain Picard',
    author_email='romain.picard@oakbits.com',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Debuggers'
    ],
    scripts=['edkit-server'],
)
