variable "family" {
    description = "A unique name for your task defintion."
    type = "string"
}

variable "container_definitions" {
    description = "A list of valid container definitions provided as a single valid JSON document."
    type = "list"
}

variable "task_role_arn" {
    description = "The Amazon Resource Name for an IAM role for the task"
    type = "string"
    default = ""
}

variable "volume" {
    description = "Volume block map with 'name' and 'host_path'. 'name': The name of the volume as is referenced in the sourceVolume. 'host_path' The path on the host container instance that is presented to the container."
    type = "map"
    default = {}
}
