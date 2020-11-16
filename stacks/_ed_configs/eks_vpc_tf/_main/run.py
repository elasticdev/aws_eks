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
    stack.parse.add_optional(key="availability_zones",default='us-west-1a,us-west-1c')
    stack.parse.add_optional(key="subnet_base",default="10.14")

    # Add execgroup
    stack.add_execgroup("elasticdev:::aws_eks::vpc_tf")

    # Initialize 
    stack.init_variables()

    # Initialize execgroups
    stack.init_execgroups()

    # Execute execgroup for creating vpc
    stateful_id = stack.random_id()

    env_vars = {"NAME":stack.eks_cluster}
    env_vars["CLOBBER"] = True
    env_vars["EKS_CLUSTER"] = stack.eks_cluster
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["STATEFUL_ID"] = stateful_id
    env_vars["METHOD"] = "create"

    # zones need to include a , and a space
    env_vars["TF_VAR_availability_zones"] = ", ".join([ zone.strip() for zone in stack.availability_zones.split(",") ])
    env_vars["TF_VAR_availability_zones_count"] = str(len([ zone.strip() for zone in stack.availability_zones.split(",")]))
    env_vars["TF_VAR_aws_default_region"] = stack.aws_default_region
    env_vars["TF_VAR_subnet_base"] = stack.subnet_base
    env_vars["TF_VAR_eks_cluster"] = stack.eks_cluster

    env_vars["RESOURCE_TYPE"] = "vpc"
    #env_vars["RESOURCE_TAGS"] = "{},{},{},{},{}".format("vpc","eks", "aws_eks", stack.vpc_name, stack.aws_default_region)

    env_vars["USE_DOCKER"] = True
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env

    _docker_env_fields_keys = env_vars.keys()
    _docker_env_fields_keys.append("AWS_ACCESS_KEY_ID")
    _docker_env_fields_keys.append("AWS_SECRET_ACCESS_KEY")
    _docker_env_fields_keys.remove("METHOD")

    env_vars["DOCKER_ENV_FIELDS"] = ",".join(_docker_env_fields_keys)

    inputargs = {"insert_env_vars":stack.insert_env_vars}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["name"] = stack.eks_cluster
    inputargs["stateful_id"] = stateful_id
    stack.vpc_tf.insert(**inputargs)

    return stack.get_results()
