
resource "aws_ecs_task_definition" "taskdef" {
    family = "${var.family}"
    container_definitions = "${var.container_definitions}"
}

