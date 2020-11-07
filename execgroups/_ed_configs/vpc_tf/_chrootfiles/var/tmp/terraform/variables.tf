variable "availability_zones" {
  default = "us-west-1a,us-west-1c"
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

variable "eks_cluster" {
  default = "dev-k8"
}
