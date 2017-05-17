import re
import unittest
import os
import time
from textwrap import dedent
from subprocess import check_call, check_output

cwd = os.getcwd()

class TestCreateTaskdef(unittest.TestCase):

    def setUp(self):
        check_call([ 'terraform', 'get', 'test/infra' ])

    
    def test_create_taskdef(self):
        # ms since epoch
        name = 'test-' + str(int(time.time() * 1000))

        output = check_output([
            'terraform',
            'plan',
            '-var', 'name={}'.format(name),
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        assert dedent("""
            + module.taskdef.aws_ecs_task_definition.taskdef
                arn:                   "<computed>"
                container_definitions: "a173db30ec08bc3c9ca77b5797aeae40987c1ef7"
                family:                "tf_ecs_taskdef_test_family"
                network_mode:          "<computed>"
                revision:              "<computed>"
            Plan: 1 to add, 0 to change, 0 to destroy.
        """).strip() in output
