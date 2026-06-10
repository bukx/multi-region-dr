# Multi-Region Disaster Recovery

AWS disaster recovery architecture that models active-passive failover across two regions. The repo combines a local failover simulator with Terraform infrastructure for Route 53 failover routing, DynamoDB Global Tables, S3 cross-region replication, and warm-standby recovery patterns.

![Architecture](./architecture.png)

## Why this repo matters

This project focuses on resilience engineering rather than simple infrastructure provisioning. It shows how DNS failover, replicated data stores, and repeatable regional infrastructure work together to reduce outage impact.

## Recovery objectives

- **RPO:** 5 minutes
- **RTO:** 15 minutes

## What is included

- local CLI simulator for health checks, failover, and DR drills
- Terraform infrastructure under `terraform/`
- example configuration under `config/`
- architecture diagram source in `architecture.py`
- test coverage for the local simulator

## Architecture

The design uses:
- **Route 53 failover routing** to move traffic from the primary region to the secondary region
- **Route 53 health checks** to detect primary-region failure
- **DynamoDB Global Tables** to keep application data replicated across regions
- **S3 cross-region replication** to protect object data
- **Terraform modules** to keep both regional environments consistent

## Run locally

```bash
python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m multi_region_dr.cli --config config/example.json status
PYTHONPATH=src python3 -m multi_region_dr.cli --config config/example.json failover --reason "regional outage"
```

## Deploy the AWS infrastructure

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

Required inputs:
- unique S3 bucket names for both regions
- Route 53 hosted zone ID
- primary and secondary application endpoints for failover DNS

## Repository layout

```text
.
|-- config/             # example simulator configuration
|-- src/                # local DR simulator logic
|-- terraform/          # AWS infrastructure
|-- tests/              # unit tests
|-- architecture.py     # diagram source
`-- architecture.png    # rendered architecture diagram
```

## What this demonstrates

- practical disaster recovery design for AWS workloads
- tradeoffs between warm standby cost and recovery speed
- automated failover using health checks and DNS routing
- repeatable regional infrastructure with Terraform

## Render the diagram

```bash
python architecture.py
```
