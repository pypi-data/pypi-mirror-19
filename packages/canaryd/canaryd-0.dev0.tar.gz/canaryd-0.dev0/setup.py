# canaryd
# File: setup.py
# Desc: canaryd package setup

from setuptools import setup, find_packages


setup(
    name='canaryd',
    version='0dev0',
    description='Client for System Canary',
    author='Oxygem',
    author_email='hello@oxygem.com',
    license='MIT',
    url='http://systemcanary.com',
    packages=find_packages(),
    scripts=(
        'bin/canaryctl',
        'bin/canaryd',
    ),
    extras_require={
        'dev': (
            'ipdb',
        ),
    },
)
