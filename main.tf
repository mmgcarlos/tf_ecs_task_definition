resource "aws_ecs_task_definition" "taskdef" {
    family                = "${var.family}"
    container_definitions = "[${join(",", var.container_definitions)}]"
    task_role_arn         = "${var.task_role_arn}"
}
