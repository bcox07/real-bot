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
      subnets = [
        "subnet-038f80f0e098a519b", 
        "subnet-01e1ec72d1e0cb06a", 
        "subnet-0548f0be096cedcdb"
      ]
    }
}

resource "aws_ecs_task_definition" "lineup_bot" {
    family = "lineup-bot"
    requires_compatibilities = ["FARGATE"]
    container_definitions = "${file("task-definitions/lineup-bot.json")}"
    cpu = 256
    memory = 512
    network_mode = "awsvpc"
    execution_role_arn = "arn:aws:iam::160885261208:role/ecsTaskExecutionRole"
}