# AIX Best Practices for Skytap Environments

This guide covers recommended settings, diagnostics, and best practices for AIX LPARs running in Skytap, especially for environments using Oracle ASM and high I/O workloads.

---

## 1. Network Configuration and Tuning

**Gather current network settings:**

```sh
no -a | grep rex
no -a | grep sack
no -a | grep sb
no -a | grep pmtu_di
no -a | grep pmtu_ex
no -a | grep node
ifconfig en0
lsattr -E -l en0
```

**Recommended settings for optimal network performance:**

```sh
# no -p -o tcprexmtthresh=100
# no -p -o sack=1
# no -p -o sb_max=1048576
# no -p -o tcp_pmtu_discover=1
# no -p -o pmtu_expire=10
# no -p -o tcp_nodelayack=1
# chdev -P -l en0 -a rfc1323=1
# chdev -P -l en0 -a tcp_sendspace=1048576
# chdev -P -l en0 -a tcp_recvspace=1048576
# chdev -P -l en0 -a mtu_bypass=off
# chdev -P -l en0 -a mtu=1240
# chdev -P -l en0 -a remmtu=576
```

> **Note:** After making these changes, validate performance in the guest OS.

**Skytap VPN MSS Recommendation:**\
Set the MSS in Skytap VPNs to `1200` for improved performance. The current N/A value should not cause issues, but setting it to 1200 can enhance performance. Changing this requires disabling the WAN to update.

---

## 2. Disk Tuning: `rw_timeout` and Oracle ASM

**Check current disk devices:**

```sh
lsdev -Cc disk
```

**Check current ****\`\`**** value for each disk:**

```sh
lsattr -El hdiskX -a rw_timeout
# Replace hdiskX with your disk name
```

**Best Practice:**\
Set `rw_timeout = 120` and `queue_depth = 10` for each hdisk.

- [Skytap Power Workload Best Practices](https://support.skytap.com/hc/en-us/articles/25613350980247-Skytap-Power-Workload-Best-Practices)
- [Optimizing AIX Read/Write Operations](https://support.skytap.com/hc/en-us/articles/24718995086743-Optimizing-AIX-Read-Write-Operations-for-Skytap-hosted-Logical-Partitions-LPARs)

---

## 3. Oracle ASM and Disk Layout

- **Example of a Workload profile:**

  - 95% reads with large block size.
  - Majority of workload goes through 5–6 ASM raw disks.
  - 70% of workload passes through a single vscsi adapter (e.g., vscsi1).

- **Best Practice:**\
  Distribute ASM disks more evenly across controllers to increase resilience and reduce bottlenecks. This change requires a maintenance window (LPAR must be powered off). Skytap Support will need to know which hdisks are used by Oracle ASM for each LPAR involved.

---

## 4. Troubleshooting & Follow-up

- Apply network and disk tuning as described.
- Test results in the guest OS after making these changes.
- Document which LPARs and hdisks are affected, and coordinate with Skytap Support for infrastructure-level changes if needed.
- If issues are found on multiple LPARs with different configurations, document each occurrence for analysis.

---

## 5. Additional Recommendations

- Do **not** use manual PVID assignment for Oracle ASM disks—let the system manage disk identifiers.
- Increasing `rw_timeout` and `queue_depth` can decrease the risk of disk disconnections.
- Record all current settings before making any changes.
- Use the tuning values provided as the default unless your workload analysis suggests otherwise.

---

## References

- [Skytap Power Workload Best Practices](https://support.skytap.com/hc/en-us/articles/25613350980247-Skytap-Power-Workload-Best-Practices)
- [Optimizing AIX Read/Write Operations for Skytap-hosted LPARs](https://support.skytap.com/hc/en-us/articles/24718995086743-Optimizing-AIX-Read-Write-Operations-for-Skytap-hosted-Logical-Partitions-LPARs)

---

**For further support or architecture guidance, contact Skytap Support.**

---

