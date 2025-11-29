# Backup Solutions for AIX in Skytap

This document provides a technical overview of the backup solutions available for AIX in Skytap, including feature comparisons, architectural considerations, and operational recommendations.

---

## 1. Overview of Backup Solutions

| Tool Name                | Backup & Restore | High Availability | DR Solution | Limitations                                  |
|--------------------------|------------------|-------------------|-------------|----------------------------------------------|
| CommVault                | YES              | Yes               | Yes         | Issues with some AIX 7.2 versions            |
| Storix                   | YES              | No                | Partial     | No HA, DR is not full                        |
| Veeam                    | YES              | Yes               | Yes         | JFS2 not snapshot backup (some LPARs)        |
| Skytap Snapshot          | Limited          | N/A               | N/A         | Limited, not file-level or granular          |
| FalconStor StorSafe VTL  | YES              | Yes               | Yes         | None significant, Skytap certified           |
| Mimix for AIX            | YES              | Yes               | Yes         | Requires configuration, licensed product     |

---

## 2. Detailed Solution Descriptions

### 2.1. **FalconStor StorSafe VTL**

#### **Key Features**
- **Certified by Skytap** for Power (AIX, IBM i, Linux) workloads.
- **Virtual Tape Library (VTL)** replaces or complements tape libraries with disk/cloud.
- **Global deduplication and advanced compression**: Up to 95% reduction in backup storage costs.
- **Multi-OS support**: IBM i, AIX, Linux.
- **Encryption at-rest and in-flight** for data security.
- **Seamless hybrid-cloud and DR**: Replicate to Skytap, Azure Blob, PowerVS, or even on-premises.
- **Pay-as-you-grow scalability**: From 1TB to PBs.
- **Non-disruptive**: Reuse existing backup software and processes; no need for forklift upgrades.
- **Multi-cloud support**: Azure, AWS, Google Cloud, Skytap.
- **Long-term retention and tape consolidation**.

#### **How It Works**
- Deploy StorSafe VTL as a virtual appliance in Skytap (or on-prem).
- Use existing backup software (e.g., BRMS, Spectrum Protect, Veeam, or native AIX/IBM i utilities) to back up AIX data to the VTL.
- Data is deduplicated/compressed before landing on primary disk or cloud (e.g., Azure Blob).
- Supports 3-2-1 backup architectures (multiple offsite copies for DR).
- Enables both operational backup and migration scenarios (on-prem to Skytap, or Skytap-to-Skytap DR).
- Management via StorSight console for unified operations and monitoring.

#### **Technical Use Cases**
1. **On-Prem Backup Optimization**: Use StorSafe VTL to speed up and deduplicate on-prem AIX backups, replicating to Skytap for DR.
2. **Hybrid Cloud Backup**: Deduplicate backups on-prem, then send only optimized data to Skytap for archive or DR.
3. **Migration**: Back up AIX workloads on-prem, replicate to Skytap, and restore to Skytap LPARs. Legacy tape data can also be migrated.
4. **Skytap Resident Backup**: Directly protect AIX running in Skytap; backup to VTL, deduplicate to Azure Blob for cost savings.
5. **Disaster Recovery**: Replicate AIX backups across Skytap regions for region-to-region DR; also supports air-gapped ransomware protection.

#### **Advantages**
- Proven at large scale (multiple enterprise Skytap customers).
- Dramatic storage and cost savings.
- No need to disrupt existing backup strategies; complements legacy processes.
- Multi-cloud, scalable, secure, and supports advanced compliance and long-term retention scenarios.

---

### 2.2. **Mimix for AIX**

**Product Page:** <a href="https://www.precisely.com/product/precisely-assure/assure-mimix-for-aix" target="_blank" rel="noopener noreferrer">Assure Mimix for AIX</a>

#### **Key Features**
- **Real-time data replication and continuous availability** for AIX environments.
- **Automated failover and failback**: Enables rapid DR testing and response for planned or unplanned events.
- **Granular file system and volume group protection:** Protects mission-critical data (e.g., DB2, application filesystems, user data).
- **GUI/AUI and command-line control:** Easy management, monitoring, and role swaps.
- **Snapshot/point-in-time recovery:** Virtual failover and fast testing for DR scenarios.
- **Integration with AIX and Skytap:** Certified and runbook-driven deployment for Skytap environments.

#### **How It Works**
- Mimix for AIX is installed on both production and recovery AIX LPARs.
- Real-time replication of protected filesystems and volume groups.
- GUI/AUI or CLI used to manage start/stop, planned/unplanned failover, and failback.
- Snapshots allow virtual failover and testing at any recovery point.
- Integrated scripts support application (e.g., DB2) start/stop around backup/failover events.
- Automated or manual DR workflows, with logging and monitoring via web UI and CLI.

#### **Operational Workflows (from runbook)**
- **Planned/Unplanned Switch:** Easily roleswap between production and recovery.
- **Failover/Failback:** Multiple workflows supported (GUI and CLI) with precise steps.
- **Monitoring:** Replication lag, status, and log file monitoring via UI or CLI (`tail -f /var/log/EchoStream/scrt_lca-1.out`).
- **Snapshot Automation:** Scripted DB/application stop, snapshot creation, restart, and automated transfer to DR.
- **Recovery Testing:** Mount/umount filesystems at DR, snapshot rollback, PIT restore, and validation workflows.

#### **Advantages**
- Real-time DR with minimal RPO/RTO.
- Frequent DR testing, validation, and granular recovery.
- Well-documented and certified for Skytap environments.
- Integrated support for DB/application quiesce before backup/failover.

#### **Limitations/Considerations**
- Requires configuration and licensing per AIX LPAR.
- Operational best practices (network, storage, DR planning) must be followed for reliable protection.

---

### 2.3. **CommVault**

- **Full backup/restore, HA, DR** for AIX in Skytap.
- Integration and new features depend on vendor support.
- **Limitation:** Issues with certain AIX 7.2 versions—always validate compatibility.
- Operates with agent-based architecture.
- Policy-driven backups, automation, ad-hoc restore supported.
- Supported by Skytap and CommVault teams.

---

### 2.4. **Storix**

- **Backup and restore support** for AIX.
- No built-in HA; DR is partial.
- Backup via SBAdmin (Storix Backup Administrator).
- Can recover to same/different hardware.
- Feature and compliance improvements dependent on vendor.
- File and system-level backup supported.

---

### 2.5. **Veeam**

- **Backup, restore, HA, and DR** for AIX.
- Integrates with Kyndryl's business model and multi-cloud targets.
- Supports JFS; **JFS2 snapshot backup not available on some LPARs**—validate before deploying.
- Supports customer-driven enhancements (CR requests).
- Veeam IP and tools can be reused for Google/Amazon cloud targets.

---

### 2.6. **Skytap Snapshot**

- **Limited functionality**: Only supports ad-hoc disk/VM snapshots.
- No file/folder, geo-redundancy, or policy-based backup.
- Basic audit and restore test capabilities.
- Best used as a rapid rollback/quick recovery tool, not as primary backup for critical workloads.

---

## 3. Feature Comparison Table

| Function Requirement                   | Skytap Snapshot | CommVault | Storix | FalconStor StorSafe VTL | Mimix for AIX      |
|-----------------------------------------|-----------------|-----------|--------|------------------------|--------------------|
| Disk/Volume Snapshot Backup             | Limited         | YES       | YES    | YES                    | YES (with DR/HA)   |
| File/Folder Backup                      | Limited         | YES       | YES    | YES (via backup app)   | YES (replication)  |
| Geo-Redundancy                          | Limited         | YES       | YES    | YES                    | YES                |
| Policy-Based Backups (daily/weekly/etc) | To be developed | YES       | YES    | YES                    | YES (schedule)     |
| Ad-hoc Backups                          | YES             | YES       | Limited| YES                    | YES                |
| Backup Failure Alerts/Notifications     | Skytap Support  | TBD       | YES    | YES                    | YES (monitoring)   |
| Backup KPIs Monitoring                  | Skytap Support  | Limited   | Limited| YES (StorSight)        | YES (UI/CLI)       |
| Backup Dashboard                        | No              | Limited   | Limited| YES (StorSight)        | YES (web UI)       |
| Backup Audit Logs                       | Limited         | YES       | Limited| YES                    | YES (logs/CLI)     |
| Archival/Long-Term Retention            | YES             | YES       | YES    | YES (Cloud/Tape)       | Limited            |
| Restore to Same/Different VM            | No Capability   | YES       | YES    | YES                    | YES                |
| Partial Recovery of Volume/Disk         | No Capability   | YES       | YES    | YES                    | YES (snapshot)     |
| Recovery Audit Logs                     | Limited         | YES       | Limited| YES                    | YES                |
| Restore Test Plans                      | Limited         | Limited   | Limited| YES                    | YES (testing)      |

---

## 4. Architectural Recommendations

- **For mission-critical AIX workloads:**  
  Use **FalconStor StorSafe VTL**, **Mimix for AIX**, or **CommVault** for enterprise-grade, policy-based, geo-redundant backups and DR.
- **For continuous availability and frequent DR testing:**  
  Mimix for AIX provides real-time replication, seamless role swap, and robust failover/failback for production environments in Skytap.
- **For quick rollback, dev/test, or supplementary protection:**  
  Skytap Snapshots are fast and easy but not a substitute for enterprise backup.
- **If migrating from tape or modernizing backup strategy:**  
  StorSafe VTL offers seamless integration and deduplication/compression benefits, enabling long-term retention and migration to cloud storage (Azure Blob).
- **For cloud-native or multi-cloud needs:**  
  Veeam provides a reusable asset, especially if targeting Google, Azure, or AWS.

---

## 5. References

- <a href="https://skytap.github.io/well-architected-framework/" target="_blank" rel="noopener noreferrer">Skytap Well-Architected Framework</a>
- <a href="https://help.skytap.com/" target="_blank" rel="noopener noreferrer">Skytap Help & Documentation</a>
- <a href="https://support.skytap.com/hc/en-us/articles/25613350980247-Skytap-Power-Workload-Best-Practices" target="_blank" rel="noopener noreferrer">Kyndryl Skytap Power Workload Best Practices</a>
- <a href="https://www.falconstor.com/" target="_blank" rel="noopener noreferrer">FalconStor StorSafe VTL Overview (from Q1 2025 deck)</a>
- <a href="https://www.precisely.com/product/precisely-assure/assure-mimix-for-aix" target="_blank" rel="noopener noreferrer">Assure Mimix for AIX Product Page</a>

---

**For more information or architectural guidance, contact Skytap, FalconStor, or Precisely support. Validate all backup strategies in pre-production before rolling out to mission-critical AIX workloads.**

---

