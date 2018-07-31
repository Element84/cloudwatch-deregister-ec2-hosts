#!/usr/bin/env python

import setuptools

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name='cloudwatch-deregister-ec2-hosts',
    version='0.1',
    author='Element 84 Engineering Team',
    author_email='opensource@element84.com',
    url='https://github.com/Element84/cloudwatch-deregister-ec2-hosts',
    description='Cloudwatch events trigger this Lambda function when instances are terminated to remove from FreeIPA',
    long_description=readme,
    license='Apache License 2.0',
    install_requires=['FreeIPA-JSON==0.1'],
    dependency_links=['git+https://github.com/Element84/python-freeipa-json.git#egg=FreeIPA-JSON-0.1']
)
