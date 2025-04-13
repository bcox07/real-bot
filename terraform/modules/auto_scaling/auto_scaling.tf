resource "aws_autoscaling_group" "lineup_bot_group" {
  name                      = "terraform-test-foobar5"
  max_size                  = 1
  min_size                  = 1
  force_delete              = true
  termination_policies      = ["OldestInstance"]
}

resource "aws_autoscaling_schedule" "lineup_bot_schedule_stop" {
  scheduled_action_name  = "lineup_bot_scheduled_action_stop"
  min_size               = 0
  max_size               = 0
  desired_capacity       = 0
  start_time             = "2016-12-11T18:00:00Z"
  recurrence             = "30 23 * * *"
  time_zone              = "America/Denver"
  autoscaling_group_name = aws_autoscaling_group.lineup_bot_group.name
}


resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = 4
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.example.name}/${aws_ecs_service.example.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}