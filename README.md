# tf\_ecs\_task\_definition

[![Build Status](https://travis-ci.org/mergermarket/tf_ecs_task_definition.svg?branch=master)](https://travis-ci.org/mergermarket/tf_ecs_task_definition)

This module creates a basic ECS Task Definition.

## Usage

    module "taskdef" {
        source = "github.com/mergermarket/tf_ecs_task_definition"

        family = "live-service-name"
        container_definitions = [
            <<END
    {
        ...container definition...
    }
    END
        ]

        volume = {
            name = 'data'
            host_path = '/mnt/data'
        }
    }

## API

### Parameters

* `family` - the name of the task definition. For ECS services it is recommended to use the same name as for the service, and for that name to consist of the environment name (e.g. "live"), the comonent name (e.g. "foobar-service"), and an optional suffix (if an environment has multiple services for the component running - e.g. in a multi-tenant setup), separated by hyphens.
* `container_definitions` - list of strings. Each string should be a JSON document describing a single container definition - see https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html.
* `task_role_arn` - The Amazon Resource Name for an IAM role for the task.
* `volume` - Volume block map with 'name' and 'host_path'. See https://www.terraform.io/docs/providers/aws/r/ecs_task_definition.html#volume for more info.

### Outputs

* `arn` - the ARN of the task definition.
