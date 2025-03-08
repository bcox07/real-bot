resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/24"
  instance_tenancy = "default"
  tags = {
    Name = "main"
  }
}

resource "aws_subnet" "main_subnet" {
    vpc_id = aws_vpc.main_vpc.id
    cidr_block = "10.0.0.0/28"

    tags = {
        Name = "main"
    }
}

resource "aws_internet_gateway" "main_gateway" {
    vpc_id = aws_vpc.main_vpc.id
}

resource "aws_default_route_table" "main" {
  default_route_table_id = aws_vpc.main_vpc.default_route_table_id

  route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.main_gateway.id
    }

  tags = {
    Name = "main"
  }
}

resource "aws_main_route_table_association" "a" {
  vpc_id         = aws_vpc.main_vpc.id
  route_table_id = aws_default_route_table.main.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.main_subnet.id
  route_table_id = aws_default_route_table.main.id
}

output "aws_subnet_id" {
  value = aws_subnet.main_subnet.id
}