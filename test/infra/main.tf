variable "name" {
    description = "used to ensure taskdef updates"
}

variable "region" {
    description = "AWS region"
}

provider "aws" {
  region = "${var.region}"
}

module "taskdef" {
  source = "../.."

  family = "tf_ecs_taskdef_test_family"
  container_definitions = [
    <<END
{
  "name": "${var.name}",
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
