module "eks" {
  source       = "git::https://github.com/terraform-aws-modules/terraform-aws-eks.git?ref=v12.1.0"
  cluster_name = var.eks_cluster
  vpc_id       = var.vpc_id
  subnets      = split(",",var.subnet_ids)

  node_groups = {
    eks_nodes = {
      instance_type    = var.instance_type
      desired_capacity = tonumber(var.eks_desired_capacity)
      max_capacity     = tonumber(var.eks_max_capacity)
      min_capacity     = tonumber(var.eks_min_capacity)
    }
  }

  manage_aws_auth = false
}
