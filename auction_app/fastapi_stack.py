from aws_cdk import Stack
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct
import os

class FastApiStack(Stack):
    def __init__(self, scope: Construct, id: str,
                 items_table: dynamodb.Table,
                 bids_table: dynamodb.Table,
                 **kwargs):
        super().__init__(scope, id, **kwargs)

        docker_image = ecr_assets.DockerImageAsset(self, "FastApiImage",
            directory=os.path.abspath(".")
        )

        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FastApiService",
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            public_load_balancer=True,
            task_image_options={
                "image": ecs.ContainerImage.from_docker_image_asset(docker_image),
                "container_port": 8000  
            }
        )

        items_table.grant_read_write_data(service.task_definition.task_role)
        bids_table.grant_read_write_data(service.task_definition.task_role)

        self.api_url = service.load_balancer.load_balancer_dns_name
