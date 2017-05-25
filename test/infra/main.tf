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
    description = "Allow the test to pass this in"
    type = "string"
    default = ""
}

variable "task_volume_param" {
    description = "Allow the test to pass this in"
    type = "map"
    default = {}
}

module "taskdef" {
  source = "../.."

  family = "tf_ecs_taskdef_test_family"
  task_role_arn = "${var.task_role_arn_param}"
  volume = "${var.task_volume_param}"
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
  ]
}

output "taskdef_arn" {
    value = "${module.taskdef.arn}"
}
