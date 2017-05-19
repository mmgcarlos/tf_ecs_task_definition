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
