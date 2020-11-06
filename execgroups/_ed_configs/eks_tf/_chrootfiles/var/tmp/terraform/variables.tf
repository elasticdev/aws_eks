variable "eks_cluster" {
  default = "dev-env"
}

variable "eks_min_capacity" {
  default = "1"
}

variable "eks_max_capacity" {
  default = "2"
}

variable "eks_desired_capacity" {
  default = "1"
}

variable "eks_instance_type" {
  default = "t2.small"
}

variable "availability_zones" {
  default = "us-west-1a, us-west-1c"
}

variable "availability_zones_count" {
  default = 2
}

variable "aws_default_region" {
  default = "us-west-1"
}

variable "subnet_base" {
  default = "10.15"
}

variable "vpc_name" {
  default = "eks_vpc"
}
