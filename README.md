# lambda-spot-instance-operation

This repository is AWS Lambda function's upload files.

## Language

- python3.6.2

## Package

- botocore
- boto3
- datetime
- os

## How To Use

### 1.clone git repository

```
git clone https://github.com/mkawabata-linkbal/lambda-instance-operation.git
```

### 2.prepare upload zip file

```
pip install botocore -t ./ --upgrade
pip install boto3 -t ./ --upgrade
zip -r ../lambda-spot-instance-operation.zip .
```
### 3.set environment variables on AWS Console

```
TAG_NAME : <TAG NAME>
```

### see also
- http://dev.classmethod.jp/cloud/aws/launch-spotblock-with-lambda/

