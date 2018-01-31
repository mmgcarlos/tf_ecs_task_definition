resource "aws_ecs_task_definition" "taskdef" {
  family                = "${var.family}"
  container_definitions = "[${join(",", var.container_definitions)}]"
  task_role_arn         = "${var.task_role_arn}"
  network_mode          = "awsvpc"

  volume = {
    name      = "${lookup(var.volume, "name", "dummy")}"
    host_path = "${lookup(var.volume, "host_path", "/tmp/dummy_volume")}"
  }
}
