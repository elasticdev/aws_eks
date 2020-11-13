def _get_subnet_ids(vpc_info):

    data = vpc_info["raw"]["terraform"]

    subnet_ids = []

    for resource in data["resources"]:
        for instance in resource["instances"]:
            _type = resource["type"]
            _name = resource["name"]
            _mode = resource.get("mode")
    
            # this is the main category for the terraform template
            if _type != "aws_subnet": continue
            if _name != "private_prod": continue
            if _mode != "managed": continue
    
            _results = instance["attributes"]
            subnet_ids.append(_results["id"])
    
    return ",".join(subnet_ids)

def run(stackargs):

    import json

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_required(key="eks_cluster")

    # docker image to execute terraform with
    stack.parse.add_optional(key="docker_exec_env",default="elasticdev/terraform-run-env")

    stack.parse.add_optional(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')
    stack.parse.add_optional(key="aws_default_region",default="us-west-1")
    stack.parse.add_optional(key="eks_min_capacity",default="1")
    stack.parse.add_optional(key="eks_max_capacity",default="2")
    stack.parse.add_optional(key="eks_desired_capacity",default="1")
    stack.parse.add_optional(key="resource_type",default="eks")

    # Add execgroup
    stack.add_execgroup("elasticdev:::aws_eks::eks_tf")

    # Initialize 
    stack.init_variables()

    # Initialize execgroups
    stack.init_execgroups()

    vpc_info = stack.get_resource(name=stack.vpc_name,
                                  resource_type="vpc",
                                  must_exists=True)[0]

    # Execute execgroup for creating vpc
    stateful_id = stack.random_id()

    env_vars = {"NAME":stack.eks_cluster}
    env_vars["K8_NAME"] = stack.eks_cluster
    env_vars["EKS_NAME"] = stack.eks_cluster
    env_vars["EKS_CLUSTER"] = stack.eks_cluster
    env_vars["CLOBBER"] = True
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["STATEFUL_ID"] = stateful_id
    env_vars["METHOD"] = "create"

    env_vars["TF_VAR_vpc_id"] = vpc_info["vpc_id"]
    env_vars["TF_VAR_subnet_ids"] = _get_subnet_ids(vpc_info)

    # zones need to include a , and a space
    env_vars["TF_VAR_eks_min_capacity"] = stack.eks_min_capacity
    env_vars["TF_VAR_eks_max_capacity"] = stack.eks_max_capacity
    env_vars["TF_VAR_eks_desired_capacity"] = stack.eks_desired_capacity
    env_vars["TF_VAR_eks_cluster"] = stack.eks_cluster

    env_vars["RESOURCE_TYPE"] = stack.resource_type
    env_vars["RESOURCE_TAGS"] = "{},{},{},{},{},{}".format("vpc","eks", "aws_eks", stack.eks_cluster, stack.vpc_name, stack.aws_default_region)
    env_vars["USE_DOCKER"] = True
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env

    _docker_env_fields_keys = env_vars.keys()
    _docker_env_fields_keys.append("AWS_ACCESS_KEY_ID")
    _docker_env_fields_keys.append("AWS_SECRET_ACCESS_KEY")
    _docker_env_fields_keys.remove("METHOD")

    env_vars["DOCKER_ENV_FIELDS"] = ",".join(_docker_env_fields_keys)

    inputargs = {"insert_env_vars":stack.insert_env_vars}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["name"] = stack.vpc_name
    inputargs["stateful_id"] = stateful_id
    stack.eks_tf.insert(**inputargs)

    return stack.get_results()
