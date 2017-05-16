import re
import unittest
import os
import time
from subprocess import check_call, check_output

import boto3

REGION = 'eu-west-1'

cwd = os.getcwd()

class TestCreateTaskdef(unittest.TestCase):

    def setUp(self):
        check_call([ 'terraform', 'get', 'test/infra' ])

    
    def test_create_taskdef(self):
        # ms since epoch
        name = 'test-' + str(int(time.time() * 1000))

        output = check_output([
            'terraform',
            'apply',
            '-var', 'name={}'.format(name),
            '-var', 'region={}'.format(REGION),
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        taskdef_arn = re.search(r'taskdef_arn = (\S+)', output).group(1)

        ecs = boto3.Session(region_name=REGION).client('ecs')

        taskdef = ecs.describe_task_definition(
            taskDefinition=taskdef_arn
        )['taskDefinition']

        assert taskdef['containerDefinitions'][0]['name'] == name


    def tearDown(self):
        check_call([
            'terraform', 'destroy',
            '-var', 'name=meh',
            '-var', 'region={}'.format(REGION),
            '-force',
            'test/infra'
        ])
