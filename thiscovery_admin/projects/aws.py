import os
import sys
import json
import logging
from pythonjsonlogger import jsonlogger
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

# region Logging

logger = None


def get_logger():
    global logger
    if logger is None:
        logger = logging.getLogger('thiscovery')
        # print('creating logger')
        log_handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter('%(asctime)s %(module)s %(funcName)s %(lineno)d %(name)-2s %(levelname)-8s %(message)s')
        formatter.default_msec_format = '%s.%03d'
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger

# endregion


DEFAULT_AWS_REGION = 'eu-west-1'


def get_aws_region():
    try:
        region = os.environ['AWS_REGION']
    except:
        region = DEFAULT_AWS_REGION
    return region


def get_aws_namespace():
    try:
        secrets_namespace = settings.SECRETS_NAMESPACE
    except:
        secrets_namespace = '*** NOT SET ***'
    return secrets_namespace


def get_secret(secret_name, namespace_override=None):
    logger = get_logger()
    # need to prepend secret name with namespace...
    if namespace_override is None:
        namespace = get_aws_namespace()
    else:
        namespace = namespace_override

    if namespace is not None:
        secret_name = namespace + secret_name

    region = get_aws_region()
    endpoint_url = "https://secretsmanager." + region + ".amazonaws.com"

    logger.info('get_secret: ' + secret_name)

    session = boto3.session.Session()
    # logger.info('get_aws_secret:session created')
    client = session.client(
        service_name='secretsmanager',
        region_name=region,
        endpoint_url=endpoint_url
    )

    secret = None

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        # logger.info('get_aws_secret:secret retrieved')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            logger.error("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            logger.error("The request was invalid due to:" + str(e))
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            logger.error("The request had invalid params:" + str(e))
        raise
    except:
        logger.error(sys.exc_info()[0])
    else:
        # logger.info('get_aws_secret:secret about to decode')
        # Decrypted secret using the associated KMS CMK
        # Depending on whether the secret was a string or binary, one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
        # logger.info('get_aws_secret:secret decoded')
        # logger.info('secret:' + secret)

        secret = json.loads(secret)
    finally:
        return secret

# endregion
