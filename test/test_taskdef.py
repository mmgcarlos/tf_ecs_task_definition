import re
import unittest
import os
import docker
import time

import boto3

REGION = 'eu-west-1'

cwd = os.getcwd()

class TestCreateTaskdef(unittest.TestCase):
    
    def test_create_taskdef(self):
        
        docker_client = docker.from_env()

        docker_client.containers.run(
            'hashicorp/terraform:light',
            command=['get', 'test/infra'],
            remove=True,
            detach=False,
            volumes={ cwd: { 'bind': cwd, 'mode': 'rw' } },
            working_dir=cwd
        )

        # ms since epoch
        name = 'test-' + str(int(time.time() * 1000))

        output = docker_client.containers.run(
            'hashicorp/terraform:light',
            command=[
                'apply',
                '-var', 'name={}'.format(name),
                '-var', 'region={}'.format(REGION),
                '-no-color',
                'test/infra'
            ],
            remove=True,
            detach=False,
            volumes={ cwd: { 'bind': cwd, 'mode': 'rw' } },
            environment={
                'AWS_ACCESS_KEY_ID': os.environ['AWS_ACCESS_KEY_ID'],
                'AWS_SECRET_ACCESS_KEY': os.environ['AWS_SECRET_ACCESS_KEY'],
                'AWS_SESSION_TOKEN': os.environ['AWS_SESSION_TOKEN'],
            },
            working_dir=cwd
        ).decode('utf-8')

        taskdef_arn = re.search(r'taskdef_arn = (\S+)', output).group(1)

        ecs = boto3.Session(region_name=REGION).client('ecs')

        taskdef = ecs.describe_task_definition(
            taskDefinition=taskdef_arn
        )['taskDefinition']

        assert taskdef['containerDefinitions'][0]['name'] == name
