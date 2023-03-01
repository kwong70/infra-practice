from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_ecs as ecs,
    aws_ecr_assets as ecr_assets,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_s3_assets as s3_assets,
    aws_ssm as ssm,
    aws_route53 as route53,
    aws_cloudfront as cloudfront,
    Stack,
    aws_secretsmanager as sm,
)
import aws_cdk
import json

class InfraStack(Stack):

    def __init__(self, scope: aws_cdk.App,  construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Templated secret with username and password fields
        # templated_secret = sm.Secret(self, "TemplatedSecret",
        #     generate_secret_string=sm.SecretStringGenerator(
        #         secret_string_template=json.dumps({"username": "postgres"}),
        #         generate_string_key="password"
        #     )

        secret = sm.Secret(self, "Secret")


        # create VPC
        vpc = ec2.Vpc(self, "MyAppVPC", max_azs=2)

        
        db = rds.DatabaseInstance(self, "PostgresInstance1",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            credentials=rds.Credentials.from_secret(secret),
            vpc=vpc
        )
        # create Flask app task definition
        # flask_task_definition = ecs.FargateTaskDefinition(self, "MyAppFlaskTaskDefinition")
        # flask_container = flask_task_definition.add_container("MyAppFlaskContainer",
        #     image=ecs.ContainerImage.from_asset("path/to/flask/app"),
        #     environment={
        #         "DATABASE_HOST": db.instance_endpoint,
        #         "DATABASE_NAME": "MyAppDatabase",
        #         "DATABASE_USER": templated_secret.secret_value_from_json("username").to_string(),
        #         "DATABASE_PASSWORD": templated_secret.secret_value_from_json("password") 
        #     }
        # )
        # flask_container.add_port_mappings(ecs.PortMapping(container_port=5000))

        # # create ECS service for Flask app
        # flask_service = ecs.FargateService(self, "MyAppFlaskService",
        #     task_definition=flask_task_definition,
        #     cluster=ecs.Cluster(self, "MyAppCluster", vpc=vpc),
        #     desired_count=1,
        #     assign_public_ip=False,
        #     security_group=ec2.SecurityGroup(
        #         self, "MyAppFlaskSecurityGroup", vpc=vpc, allow_all_outbound=True),
        #     health_check=ecs.HealthCheck(
        #         path="/health",
        #         interval=aws_cdk.Duration.seconds(30),
        #         timeout=aws_cdk.Duration.seconds(10),
        #         retries=3
        #     ),
        #     platform_version=ecs.FargatePlatformVersion.VERSION1_4
        # )
           
