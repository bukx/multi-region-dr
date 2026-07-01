"""Multi-Region Disaster Recovery Solution — architecture diagram.
Active-passive across two AWS regions. RPO 5 min / RTO 15 min.
Run: python architecture.py  (outputs architecture.png)
"""
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import Route53, Route53HostedZone
from diagrams.aws.security import IAM
from diagrams.aws.storage import S3
from diagrams.onprem.client import Users
from diagrams.onprem.iac import Terraform

graph_attr = {"fontsize": "18", "bgcolor": "white", "pad": "0.6", "splines": "spline"}

with Diagram(
    "Multi-Region Disaster Recovery (Active-Passive)",
    filename="architecture",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
):
    users = Users("Users")

    with Cluster("Global Routing"):
        dns = Route53("Route 53\nfailover policy")
        hc = Route53HostedZone("Health Checks")
        dns - Edge(style="dotted") - hc

    with Cluster("PRIMARY — us-east-1 (active)"):
        app_p = EC2("App tier")
        ddb_p = Dynamodb("DynamoDB")
        s3_p = S3("S3 bucket")

    with Cluster("SECONDARY — us-west-2 (passive)"):
        app_s = EC2("App tier\n(warm standby)")
        ddb_s = Dynamodb("DynamoDB")
        s3_s = S3("S3 bucket")

    with Cluster("Infra as Code"):
        tf = Terraform("Terraform modules\nS3 · IAM · networking")
        iam = IAM("IAM")
        tf >> Edge(style="dashed") >> iam

    # traffic
    users >> dns
    dns >> Edge(label="active", color="darkgreen") >> app_p
    dns >> Edge(label="failover", color="firebrick", style="dashed") >> app_s
    hc >> Edge(style="dotted", label="probe") >> app_p

    app_p >> ddb_p
    app_p >> s3_p
    app_s >> ddb_s
    app_s >> s3_s

    # replication (RPO 5 min)
    ddb_p >> Edge(label="DynamoDB Global Tables", color="navy") >> ddb_s
    s3_p >> Edge(label="S3 cross-region replication", color="navy") >> s3_s

    # IaC provisions both regions
    tf >> Edge(style="dashed", color="gray") >> s3_p
    tf >> Edge(style="dashed", color="gray") >> s3_s
