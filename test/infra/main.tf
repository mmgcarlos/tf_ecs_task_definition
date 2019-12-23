provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_get_ec2_platforms      = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  max_retries                 = 1
  access_key                  = "a"
  secret_key                  = "a"
  region                      = "eu-west-1"
}

variable "task_role_arn_param" {
  description = "The test can set this var to be passed to the module"
  type        = "string"
  default     = ""
}

variable "task_volume_param" {
  description = "The test can set this var to be passed to the module"
  type        = "map"
  default     = {}
}

variable "execution_role_arn" {
  description = "The Amazon Resource Name for an execution role for the task"
  type        = "string"
  default     = ""
}

module "taskdef" {
  source = "../.."

  family             = "tf_ecs_taskdef_test_family"
  task_role_arn      = "${var.task_role_arn_param}"
  execution_role_arn = "${var.execution_role_arn}"
  volume             = "${var.task_volume_param}"

  container_definitions = [
    <<END
{
  "name": "web",
  "image": "hello-world:latest",
  "cpu": 10,
  "memory": 128,
  "essential": true
}
END
    ,
  ]
}

module "taskdef_with_invalid_name" {
  source = "../.."

  family             = "tf_ecs_taskdef_test_family.something"
  task_role_arn      = "${var.task_role_arn_param}"
  execution_role_arn = "${var.execution_role_arn}"
  volume             = "${var.task_volume_param}"

  container_definitions = [
    <<END
{
  "name": "web",
  "image": "hello-world:latest",
  "cpu": 10,
  "memory": 128,
  "essential": true
}
END
    ,
  ]
}

output "taskdef_arn" {
  value = "${module.taskdef.arn}"
}
