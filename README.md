# Overview

This is a Lambda function, triggered by a CloudWatch event. When an EC2 instance is terminated, such as during an auto-scaling event, the network information of the server is sent to the Lambda function and it is de-registered from the directory service.

At Element 84, we use FreeIPA, and we've provided an example CloudFormation stack to deploy the CloudWatch event, IAM role, and Lambda.

Make sure your Lambda has access to your directory server, which probably requires it to run within a VPC and have appropriate network routes available.

The main script can be found under `functions/freeipa/remove_host.py`

# Installation / Setup
As this is Lambda, you need to install the libraries prior to zipping into a Lambda deployment package.

## Install dependencies
`pip install git+https://github.com/Element84/python-freeipa-json.git -t .` 

This will install the dependencies into the project root, necessary for Lambda.  The libraries themselves and `lambda.zip` have been added to `.gitignore`, so make sure to run the `pip` step prior to creating the zip package.

We currently have forked the FreeIPA-JSON repo to work with our Python3 project and plan to contribute back to the upstream [FreeIPA-JSON project](https://github.com/nordnet/python-freeipa-json) for Py3 support.

## Create Lambda zip
`zip -r lambda.zip .` to create the Lambda package.

# TODO

* Cloudformation
* Add tests
