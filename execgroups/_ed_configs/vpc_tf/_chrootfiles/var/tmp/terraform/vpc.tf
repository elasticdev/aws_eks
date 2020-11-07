module "vpc" {
  source = "git@github.com:reactiveops/terraform-vpc.git?ref=v5.0.1"

  aws_vpc_name    = var.vpc_name
  aws_region      = var.aws_default_region
  aws_azs         = split(",",var.availability_zones)
  az_count        = var.availability_zones_count
  vpc_cidr_base   = var.subnet_base

  global_tags = {
    "kubernetes.io/cluster/${var.eks_cluster}" = "shared"
  }
}
