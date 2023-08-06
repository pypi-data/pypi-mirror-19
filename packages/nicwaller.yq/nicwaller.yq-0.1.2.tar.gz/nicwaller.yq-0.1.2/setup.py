# Upgraded from distutils (so old!) to setuptools to support install_requires=[]
# from distutils.core import setup
from setuptools import setup, find_packages
import os

version_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'yq', 'VERSION'))
version = version_file.read().strip()

setup(
    name='nicwaller.yq',
    version=version,
    author='Nic Waller',
    author_email='code@nicwaller.com',
    description='A little wrapper for jq to read YAML files',
    url='https://github.com/nicwaller/yq',
    install_requires=[
        'pyyaml'
    ],
    # scripts=[
        # 'scripts/yq',
    # ],
    entry_points={
        "console_scripts": [
            "yq=yq.yq:main",
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'yq': ['yq/VERSION'],
    },
)
