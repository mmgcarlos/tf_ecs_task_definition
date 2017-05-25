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
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')
        print(output)

        assert dedent("""
            + module.taskdef.aws_ecs_task_definition.taskdef
                arn:                         "<computed>"
                container_definitions:       "a173db30ec08bc3c9ca77b5797aeae40987c1ef7"
                family:                      "tf_ecs_taskdef_test_family"
                network_mode:                "<computed>"
                revision:                    "<computed>"
                volume.#:                    "1"
                volume.3039886685.host_path: "/tmp/dummy_volume"
                volume.3039886685.name:      "dummy"
            Plan: 1 to add, 0 to change, 0 to destroy.
        """).strip() in output

    def test_task_role_arn_is_included(self):
        output = check_output([
            'terraform',
            'plan',
            '-var', 'task_role_arn_param=arn::iam:123',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        assert dedent("""
            + module.taskdef.aws_ecs_task_definition.taskdef
                arn:                         "<computed>"
                container_definitions:       "a173db30ec08bc3c9ca77b5797aeae40987c1ef7"
                family:                      "tf_ecs_taskdef_test_family"
                network_mode:                "<computed>"
                revision:                    "<computed>"
                task_role_arn:               "arn::iam:123"
                volume.#:                    "1"
                volume.3039886685.host_path: "/tmp/dummy_volume"
                volume.3039886685.name:      "dummy"
            Plan: 1 to add, 0 to change, 0 to destroy.
        """).strip() in output

    def test_task_volume_is_included(self):
        output = check_output([
            'terraform',
            'plan',
            '-var', 'task_volume_param={name="data_volume",host_path="/mnt/data"}',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        print(output)

        assert dedent("""
            + module.taskdef.aws_ecs_task_definition.taskdef
                arn:                       "<computed>"
                container_definitions:     "a173db30ec08bc3c9ca77b5797aeae40987c1ef7"
                family:                    "tf_ecs_taskdef_test_family"
                network_mode:              "<computed>"
                revision:                  "<computed>"
                volume.#:                  "1"
                volume.27251535.host_path: "/mnt/data"
                volume.27251535.name:      "data_volume"
            Plan: 1 to add, 0 to change, 0 to destroy.
        """).strip() in output
