output "arn" {
  value = "${element(concat(aws_ecs_task_definition.taskdef.*.arn, list("")), 0)}"
}
