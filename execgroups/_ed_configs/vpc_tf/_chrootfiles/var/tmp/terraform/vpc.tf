module "vpc" {
  source = "git::ssh://git@github.com/reactiveops/terraform-vpc.git?ref=v5.0.1"

  aws_vpc_name = var.aws_vpc_name
  aws_region = var.eks_aws_default_region
  az_count   = var.eks_az_count
  aws_azs    = var.eks_aws_azs

  vpc_cidr_base = var.eks_vpc_cidr_base

  global_tags = {
    "kubernetes.io/cluster/${var.eks_cluster}" = "shared"
  }
}
