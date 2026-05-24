# Multi-Region Disaster Recovery Solution — Architecture

> Active-passive disaster recovery across two AWS regions. **RPO 5 min · RTO 15 min.**
> Repo: [github.com/bukx/multi-region-dr](https://github.com/bukx/multi-region-dr)

![Architecture](./architecture.png)

## Mermaid view

```mermaid
flowchart LR
    U(["👥 Users"])
    DNS["Route 53<br/>failover routing"]
    HC["Health Checks"]
    DNS -.-> HC

    subgraph P["PRIMARY — us-east-1 (active)"]
        APP_P["App tier"]
        DDB_P[("DynamoDB")]
        S3_P["S3 bucket"]
    end

    subgraph S["SECONDARY — us-west-2 (passive)"]
        APP_S["App tier<br/>warm standby"]
        DDB_S[("DynamoDB")]
        S3_S["S3 bucket"]
    end

    subgraph IAC["Infra as Code"]
        TF["Terraform modules<br/>S3 · IAM · networking"]
    end

    U --> DNS
    DNS -- active --> APP_P
    DNS -. failover .-> APP_S
    HC -. probe .-> APP_P
    APP_P --> DDB_P & S3_P
    APP_S --> DDB_S & S3_S
    DDB_P == Global Tables ==> DDB_S
    S3_P == cross-region replication ==> S3_S
    TF -. provisions .-> S3_P & S3_S
```

## Components & data flow

| Concern | Service | Responsibility |
|---------|---------|----------------|
| Routing | **Route 53** | Failover routing policy directs traffic to primary; reroutes to secondary on health-check failure. |
| Detection | **Route 53 health checks** | Probe the primary endpoint; trigger automated DNS failover. |
| Data — DB | **DynamoDB Global Tables** | Active-active table replication keeps the passive region within the 5-min RPO. |
| Data — objects | **S3 Cross-Region Replication** | Asynchronously replicates objects to the secondary bucket. |
| Provisioning | **Terraform modules** | Reusable modules build S3, IAM, and networking identically in both regions. |

## DR targets

| Metric | Target | How it's met |
|--------|--------|--------------|
| **RPO** | 5 minutes | Continuous Global Tables + S3 CRR keep data loss window small. |
| **RTO** | 15 minutes | Route 53 health-check failover + warm standby tier in the secondary region. |

## Design notes
- **Active-passive:** secondary runs as a warm standby — data replicates continuously, compute scales up on promotion.
- **Automated failover:** no manual DNS edits; health checks flip the record set.
- **Repeatable regions:** Terraform modules guarantee the passive region matches the active one.

## Render the PNG
```bash
python architecture.py   # requires: pip install diagrams  +  graphviz binary
```
