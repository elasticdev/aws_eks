def run(stackargs):

    import json

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_required(key="eks_cluster")
    stack.parse.add_optional(key="insert_env_vars",default='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]')
    stack.parse.add_optional(key="aws_default_region",default="us-west-1")
    stack.parse.add_optional(key="eks_min_capacity",default="1")
    stack.parse.add_optional(key="eks_max_capacity",default="2")
    stack.parse.add_optional(key="eks_desired_capacity",default="1")

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
    env_vars["CLOBBER"] = True
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["STATEFUL_ID"] = stateful_id
    env_vars["METHOD"] = "create"

    env_vars["TF_VAR_vpc_id"] = vpc_info["vpc_id"]

    # zones need to include a , and a space
    env_vars["TF_VAR_eks_min_capacity"] = stack.eks_min_capacity
    env_vars["TF_VAR_eks_max_capacity"] = stack.eks_max_capacity
    env_vars["TF_VAR_eks_desired_capacity"] = stack.eks_desired_capacity
    env_vars["TF_VAR_eks_cluster"] = stack.eks_cluster

    env_vars["RESOURCE_TYPE"] = "eks"
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
