variable "aws_default_region" {
  default = "us-west-1"
}

variable "instance_type" {
  default = "t2.small"
}

variable "vpc_id" {
  default = "vpc-08c62f67d9efab21d"
}

variable "subnet_ids" {
  default = "subnet-0306784a13f526985,subnet-0a0f43144a1e591c5"
}

variable "eks_cluster" {
  default = "dev-k8"
}

variable "eks_min_capacity" {
  default = "1"
}

variable "eks_max_capacity" {
  default = "1"
}

variable "eks_desired_capacity" {
  default = "1"
}

