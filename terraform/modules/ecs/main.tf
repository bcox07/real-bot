provider "aws" {
  region  = "us-east-2"
  profile = "superuser"
}

resource "aws_ecs_cluster" "lineup_bot" {
    name = "lineup-bot"
}

resource "aws_ecs_service" "lineup_bot" {
    name = "lineup-bot"
    cluster = aws_ecs_cluster.lineup_bot.id
    task_definition = aws_ecs_task_definition.lineup_bot.arn
    desired_count = 1
    launch_type = "FARGATE"
    network_configuration {
      assign_public_ip = true
      subnets = [
        "subnet-09ec76bcb82192abe"
      ]
    }
}

resource "aws_ecs_task_definition" "lineup_bot" {
    family = "lineup-bot"
    requires_compatibilities = ["FARGATE"]
    container_definitions = "${file("modules/ecs/task-definitions/lineup-bot.json")}"
    cpu = 256
    memory = 512
    network_mode = "awsvpc"
    execution_role_arn = "arn:aws:iam::160885261208:role/ecsTaskExecutionRole"
}