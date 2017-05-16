variable "family" {
    description = "A unique name for your task defintion."
    type = "string"
}

variable "container_definitions" {
    description = "A list of valid container definitions provided as a single valid JSON document."
    type = "list"
}