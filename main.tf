resource "aws_ecs_task_definition" "taskdef" {
    family                = "${var.family}"
    container_definitions = "[${join(",", var.container_definitions)}]"
    task_role_arn         = "${var.task_role_arn}"

    volume = {
        name      = "${lookup(var.volume, "name", "dummy")}",
        host_path = "${lookup(var.volume, "host_path", "/tmp/dummy_volume")}"
    }
}

variable volumes {
    default = [
        {
            "name"= "aaa",
            "host_path"= "/tmp"
        }
    ]
}

output volumes {
    value = "${var.volumes}"
}
