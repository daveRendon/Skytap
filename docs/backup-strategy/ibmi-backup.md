
# Backup Solutions for IBM i in Skytap

This guide provides an overview and technical comparison of the leading backup solutions for IBM i running in Skytap, including integration points, benefits, drawbacks, and architecture options.

---

## 1. Key Backup Solutions for IBM i

| Solution                | Benefits                                     | Drawbacks                              |
|-------------------------|----------------------------------------------|----------------------------------------|
| **Live Clone**          | Fast environment clone; no extra cost        | RPO is last clone time                 |
| **Commvault**           | Multi-platform; compression & deduplication  | No native BRMS integration             |
| **VTL/DSI/FalconStor**  | BRMS integration; emulates physical tape     | Additional config/license required     |
| **BRMS + ICC**          | BRMS integration; included in Skytap         | Needs extra space; best for small VMs  |

---

## 2. FalconStor StorSafe VTL for IBM i

FalconStor StorSafe is a **certified solution for IBM i in Skytap**. It delivers backup and DR by providing a virtual tape library (VTL) that integrates with BRMS and supports modern and legacy tape workflows.

**Key features:**
- **Patented deduplication & compression**: Up to 95% storage savings.
- **BRMS and tape process compatibility**: Emulates physical tape, supports BRMS/SAVE21/BRMS-ICC/Spectrum Protect, and other software.
- **Cloud-native**: Backs up directly to Azure Blob, block storage, or object storage.
- **Multi-cloud and hybrid**: Replicate backups between on-prem, Skytap, Azure, AWS, and Google Cloud.
- **Disaster recovery**: Full region-to-region DR in Skytap.
- **Single management pane**: StorSight console for all environments.
- **Non-disruptive**: Reuse current backup apps and tape processes.
- **Secure**: Encryption at-rest and in-flight.

**Use cases:**
- On-premise backup optimization and DR.
- Hybrid cloud backup: Deduplicate and copy on-prem IBM i backups to Skytap.
- Migration: Move workloads and tape data to Skytap/Azure.
- Skytap-resident backup: Cloud-native backup and long-term retention for IBM i workloads.
- Skytap disaster recovery: Region-to-region replication for DR and ransomware protection.

---

## 3. MIMIX for IBM i

<a href="https://help.skytap.com/pwr-mimix-overview.html" target="_blank" rel="noopener noreferrer">MIMIX for IBM i</a> is a leading **real-time logical replication and HA/DR solution** for IBM i, fully supported in Skytap.

**Key features:**
- **Continuous, real-time replication** at the object or journaled level (minimal RPO/RTO).
- **Automated failover/failback**, planned or unplanned.
- **Supports both OS and user data** (delta sync for production LPARs).
- **Delta sync to NFS or cloud for DR/backup scenarios**.
- **Full support for Skytap-to-Skytap, on-prem-to-Skytap, and multi-cloud** architectures.
- **Integrated monitoring, role swap, and scripting for managed DR**.

**Resources:**
- <a href="https://help.skytap.com/pwr-mimix-overview.html" target="_blank" rel="noopener noreferrer">MIMIX for IBM i Overview</a>
- <a href="https://help.skytap.com/pwr-mimix-installation.html" target="_blank" rel="noopener noreferrer">Installation Guide</a>

---

## 4. Commvault for IBM i

Commvault delivers multi-platform backup and restore with advanced deduplication and compression, and supports sending data to cloud targets.  
**Note:** No direct BRMS integration—often paired with other tools for granular IBM i backup.

---

## 5. Skytap Live Clone

- Clone a running IBM i VM/environment in Skytap with a few clicks.
- No additional cost (except storage).
- **Limitation:** Recovery point is last clone operation (not continuous).

---

## 6. BRMS + ICC

- **BRMS integration**: Leverage Skytap-included BRMS licensing for IBM i.
- **Best for small VMs** or for use with incremental capacity cards.
- **Limitation:** Requires extra VM space for temporary backup images.

---

## 7. High Availability and DR Patterns

- **Live Clone**: Simple VM copy for rapid recovery (RPO = last clone).
- **Logical Replication (MIMIX)**: Continuous, low-RPO HA and DR.
- **Geo-Mirroring**: IASP-based replication for lower data change rates.

---

## 8. Reference Architectures

**A. On-premises → Skytap over VPN or ExR**  
- Use VPN or ExpressRoute Global Reach for secure connectivity between your datacenter and Skytap.
- Backup/replication can be routed over this private link.
- <a href="https://help.skytap.com/wan-create-vpn.html" target="_blank" rel="noopener noreferrer">Skytap VPN Setup</a>  
- <a href="https://help.skytap.com/wan-create-self-managed-expressroute.html" target="_blank" rel="noopener noreferrer">ExpressRoute Setup</a>

**B. Skytap to Skytap (DR)**  
- Leverage region-to-region replication with FalconStor or MIMIX for robust DR, ransomware protection, and regulatory compliance.

**C. Hybrid Cloud**  
- Use FalconStor or Commvault to deduplicate and send IBM i backup data to Skytap or Azure Blob for long-term retention and recovery.

---

## 9. Summary Table: IBM i Backup Solution Features

| Solution        | BRMS Integration | Deduplication/Compression | Tape Emulation | Real-time Replication | Cloud/Hybrid Support | Disaster Recovery |
|-----------------|------------------|--------------------------|----------------|----------------------|---------------------|------------------|
| FalconStor VTL  | YES              | YES                      | YES            | No                   | YES                 | YES              |
| MIMIX for IBM i | Partial*         | No                       | No             | YES                  | YES                 | YES              |
| Commvault       | No               | YES                      | No             | No                   | YES                 | YES              |
| Live Clone      | No               | No                       | No             | No                   | No                  | Partial          |
| BRMS + ICC      | YES              | No                       | No             | No                   | No                  | Partial          |

> *MIMIX for IBM i replicates at the OS/journal/object level and works alongside BRMS for tape/archive operations.

---

## 10. References

- <a href="https://help.skytap.com/" target="_blank" rel="noopener noreferrer">Skytap IBM i Documentation</a>
- <a href="https://help.skytap.com/pwr-mimix-overview.html" target="_blank" rel="noopener noreferrer">MIMIX for IBM i Overview</a>
- <a href="https://help.skytap.com/pwr-mimix-installation.html" target="_blank" rel="noopener noreferrer">MIMIX for IBM i Installation</a>
- <a href="https://www.falconstor.com/" target="_blank" rel="noopener noreferrer">FalconStor StorSafe for IBM Power</a>

---

**For detailed implementation guides, best practices, or further technical assistance, contact Skytap, FalconStor, Precisely, or your managed service provider.**
