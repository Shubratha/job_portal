## Resources needed for AWS serverless deployments


### Non-AWS:
1. A virtual env named `<service-name>-service`
2. A git repo named `<service-name>`
3. [Zappa](https://github.com/Miserlou/Zappa) project name should be `<service-name>`
4. create two settings module: settings_test and settings_prod

### AWS:
`<stage>` can be dev, test or prod


* S3 bucket name: `zappa-<service-name>-<stage>`
* API Gateway name should be `<service-name>`
* Lambda function name should be `<service-name>-<stage>`
* MySQL DB name should be `<service-name>` (dash replaced with underscore)
* Create a policy named: `zappa-deploy-<service-name>-<stage>`
* An IAM user with username `<service-name>-<stage>-deployer`
* IAM Execution role: `<service-name>-ZappaLambdaExecutionRole`

### Zappa settings 
* Add s3_bucket_name
* set manage_roles to false
* add vpc config


## Using Zappa for serverless deployments

### Setup AWS CLI

Configure AWS CLI


* Make sure awscli is installed inside your virtualenv and that your virtualenv is active
* Create a folder inside your home directory .aws (note the dot in front)
* Create two files inside .aws folder: credentials and config
* Sample content of config file (replace cs-fileupload with your service-name)
```
[cs-fileupload-dev-deployer]
output=json
region=ap-southeast-1

```
* Sample content of credentials file (replace cs-fileupload with your `<service-name>`) and use aws access keys provided to you
```
[cs-fileupload-dev-deployer]
region=ap-southeast-1
aws_access_key_id = AKIAIOQPGM2ATYWUWVVA
aws_secret_access_key = vhlFoNoPNzMsfDasw7SzYH3hV55zPsjhSRUS4mVi

```

### Zappa commands
Before running zappa commands, make sure that the cs-utils package is not in develop mode. To remove the develop mode for cs-utils run the following commands:

```
cd <cs-utils-dir>
python setup.py develop --uninstall
python setup.py install
```


* `zappa manage dev migrate`
* `zappa manage dev "reset_db --noinput"`
* `zappa update dev` (use this to update the AWS API Gateway code)
* `zappa deploy dev` (use this carefully, it will change your service endpoint url)
* `zappa undeploy dev`


After deploying to AWS if you want to move back to development mode package, use the following commands, after moving to your service's root directory:

```
pip uninstall cs-utils
python setup.py develop
```