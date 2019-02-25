import os
import shutil
import tempfile
import unittest
from subprocess import check_call, check_output
from textwrap import dedent


class TestCreateTaskdef(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.module_path = os.path.join(os.getcwd(), 'test', 'infra')

        check_call(['terraform', 'get', self.module_path], cwd=self.workdir)
        check_call(['terraform', 'init', self.module_path], cwd=self.workdir)

    def tearDown(self):
        if os.path.isdir(self.workdir):
            shutil.rmtree(self.workdir)

    def test_create_taskdef(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            self.module_path],
            cwd=self.workdir
        ).decode('utf-8')
        assert dedent("""
+ module.taskdef.aws_ecs_task_definition.taskdef
      id:                                              <computed>
      arn:                                             <computed>
      container_definitions:                           "[{\\"cpu\\":10,\\"essential\\":true,\\"image\\":\\"hello-world:latest\\",\\"memory\\":128,\\"name\\":\\"web\\"}]"
      family:                                          "tf_ecs_taskdef_test_family"
      network_mode:                                    <computed>
      revision:                                        <computed>
      volume.#:                                        "1"
      volume.3039886685.docker_volume_configuration.#: "0"
      volume.3039886685.host_path:                     "/tmp/dummy_volume"
      volume.3039886685.name:                          "dummy"
Plan: 1 to add, 0 to change, 0 to destroy.
        """).strip() in output

    def test_task_role_arn_is_included(self):
        output = check_output([
            'terraform',
            'plan',
            '-var', 'task_role_arn_param=arn::iam:123',
            '-no-color',
            self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        assert dedent("""
+ module.taskdef.aws_ecs_task_definition.taskdef
      id:                                              <computed>
      arn:                                             <computed>
      container_definitions:                           "[{\\"cpu\\":10,\\"essential\\":true,\\"image\\":\\"hello-world:latest\\",\\"memory\\":128,\\"name\\":\\"web\\"}]"
      family:                                          "tf_ecs_taskdef_test_family"
      network_mode:                                    <computed>
      revision:                                        <computed>
      task_role_arn:                                   "arn::iam:123"
      volume.#:                                        "1"
      volume.3039886685.docker_volume_configuration.#: "0"
      volume.3039886685.host_path:                     "/tmp/dummy_volume"
      volume.3039886685.name:                          "dummy"
Plan: 1 to add, 0 to change, 0 to destroy.
        """).strip() in output

    def test_task_execution_role_arn_is_included(self):
        output = check_output([
            'terraform',
            'plan',
            '-var', 'execution_role_arn=arn::iam:123',
            '-no-color',
            self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        assert dedent("""
+ module.taskdef.aws_ecs_task_definition.taskdef
      id:                                              <computed>
      arn:                                             <computed>
      container_definitions:                           "[{\\"cpu\\":10,\\"essential\\":true,\\"image\\":\\"hello-world:latest\\",\\"memory\\":128,\\"name\\":\\"web\\"}]"
      execution_role_arn:                              "arn::iam:123"
      family:                                          "tf_ecs_taskdef_test_family"
      network_mode:                                    <computed>
      revision:                                        <computed>
      volume.#:                                        "1"
      volume.3039886685.docker_volume_configuration.#: "0"
      volume.3039886685.host_path:                     "/tmp/dummy_volume"
      volume.3039886685.name:                          "dummy"
Plan: 1 to add, 0 to change, 0 to destroy.
        """).strip() in output

    def test_task_volume_is_included(self):
        output = check_output([
            'terraform',
            'plan',
            '-var', 'task_volume_param={name="data_volume",host_path="/mnt/data"}',
            '-no-color',
            self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        assert dedent("""
+ module.taskdef.aws_ecs_task_definition.taskdef
      id:                                            <computed>
      arn:                                           <computed>
      container_definitions:                         "[{\\"cpu\\":10,\\"essential\\":true,\\"image\\":\\"hello-world:latest\\",\\"memory\\":128,\\"name\\":\\"web\\"}]"
      family:                                        "tf_ecs_taskdef_test_family"
      network_mode:                                  <computed>
      revision:                                      <computed>
      volume.#:                                      "1"
      volume.27251535.docker_volume_configuration.#: "0"
      volume.27251535.host_path:                     "/mnt/data"
      volume.27251535.name:                          "data_volume"
Plan: 1 to add, 0 to change, 0 to destroy.
        """).strip() in output
