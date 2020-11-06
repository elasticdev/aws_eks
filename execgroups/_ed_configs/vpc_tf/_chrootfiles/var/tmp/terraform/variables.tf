variable "eks_aws_azs" {
  default = "us-west-1a, us-west-1c"
}

variable "eks_az_count" {
  default = 2
}

variable "eks_aws_default_region" {
  default = "us-west-1"
}

variable "eks_vpc_cidr_base" {
  default = "10.15"
}

variable "aws_vpc_name" {
  default = "eks_vpc"
}

variable "eks_cluster" {
  default = "dev-k8"
}
