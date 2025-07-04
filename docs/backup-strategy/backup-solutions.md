
# Backup Solutions for AIX and IBM i in Skytap – Index & Introduction

## Introduction

IBM Power workloads in Skytap require robust, reliable, and scalable backup solutions that align with enterprise SLAs for data protection, business continuity, and compliance. This documentation set provides a technical overview, detailed comparison, and architectural guidance for the most common backup and disaster recovery solutions available for both **AIX** and **IBM i** environments in Skytap.

You will find separate, in-depth documents covering:
- **AIX Backup Solutions**: Details on Commvault, Storix, Veeam, Skytap Snapshot, FalconStor StorSafe VTL, and Mimix for AIX, including pros, cons, architectures, and operational workflows.
- **IBM i Backup Solutions**: Focus on Live Clone, Commvault, FalconStor StorSafe VTL (BRMS integration), BRMS+ICC, and Mimix for IBM i, including unique features, HA/DR, and tape and cloud integration scenarios.

---

## How to Use This Documentation

- **Start here** to understand the available options and their positioning.
- Follow the links below to view the detailed backup solution guides for each platform:
    - [AIX Backup Solutions](aix-backup.md)
    - [IBM i Backup Solutions](ibmi-backup.md)
- Each guide includes comparison tables, architectural diagrams, and reference links to vendor documentation, Skytap Help, and best practice runbooks.

---

## Solution Summary Table

| Platform | Solution Options                                             | Highlights                        |
|----------|-------------------------------------------------------------|------------------------------------|
| AIX      | Commvault, Storix, Veeam, Skytap Snapshot, FalconStor VTL, Mimix | HA/DR, Deduplication, Real-time Replication, Tape Emulation, Cloud-native |
| IBM i    | Live Clone, Commvault, FalconStor VTL, BRMS+ICC, Mimix      | BRMS Integration, VTL, Real-time Replication, Cloud/Hybrid, Tape Migration |

---

## Key References

- [Skytap Well-Architected Framework](https://skytap.github.io/well-architected-framework/)
- [Skytap Help & Documentation](https://help.skytap.com/)
- [FalconStor StorSafe for IBM Power](https://www.falconstor.com/)
- [Assure Mimix for AIX Product Page](https://www.precisely.com/product/precisely-assure/assure-mimix-for-aix)
- [MIMIX for IBM i Overview](https://help.skytap.com/pwr-mimix-overview.html)

---

## About These Guides

These materials are designed for system architects, administrators, and technical teams planning, implementing, or modernizing backup strategies for Power workloads in Skytap.  
For deeper implementation help, contact Skytap Support or your backup solution vendor.

---
