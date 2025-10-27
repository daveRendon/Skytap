# 🚀 Skytap Landing Zones on Azure

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Azure](https://img.shields.io/badge/Azure-Skytap%20on%20Azure-0078D4?logo=microsoft-azure)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)
![Made with Bicep](https://img.shields.io/badge/IaC-Bicep-5C2D91?logo=azuredevops)
![GitHub Stars](https://img.shields.io/github/stars/daverendon/skytap?style=social)

Welcome to the **Skytap Landing Zones on Azure** repository!
This project provides a **structured approach** for deploying **Skytap environments** on Azure, making it easier to migrate **AIX** and **IBM i** systems into the cloud.

[🌟 Star this repo](https://github.com/daverendon/skytap) to stay updated and show your support!

---

## 📖 Overview

**Skytap on Azure** enables organizations to run **IBM Power** and **x86 workloads** in the cloud with a **lift-and-shift migration**—no major application or architecture changes required.

A **Skytap Landing Zone** is a **pre-configured environment** following best practices to help you deploy, secure, and scale workloads on Azure.

### 🔑 Key Components

1. **Pre-configured Infrastructure**
   Virtual networks, storage, and compute resources optimized for performance, security, and compliance.

2. **Security & Compliance**
   Built with controls and standards to meet organizational and regulatory requirements.

3. **Connectivity**
   Support for **VPNs** and **ExpressRoute** to connect on-premises data centers securely and reliably.

4. **Scalability & Flexibility**
   Grow and adapt resources dynamically with scalable storage and compute allocation.

5. **Automation & Orchestration**
   Leverage **Bicep templates** and **Skytap APIs** to automate deployment and management.

---

## 🎯 Why Use a Landing Zone?

* ✅ **Risk Mitigation** – A secure and controlled environment reduces migration risk.
* ⚡ **Accelerated Migration** – Ready-to-use templates shorten setup and configuration time.
* 🛠 **Best Practices Built-in** – Security, compliance, and performance guidelines are pre-integrated.
* 📏 **Consistency** – Standardized deployments across multiple projects and teams.

---

## 🚦 Getting Started

### 1️⃣ Prerequisites

* Active **Azure subscription**
* **Skytap on Azure** subscription ([how to set it up](https://blog.azinsider.net/deploy-skytap-on-azure-using-bicep-language-to-run-your-ibm-power-workloads-a245e7c3287e?source=friends_link&sk=a863322248b8aba5288da813d569afdc))
* Knowledge of **Azure VNets, Blob Storage, ExpressRoute**
* Basic understanding of Skytap

### 2️⃣ Select a Landing Zone

| OS        | Description                                                        |
| --------- | ------------------------------------------------------------------ |
| **AIX**   | [Deploy the Skytap AIX Landing Zone](docs/aix/aix-landing-zone.md) |
| **IBM i** | IBM i Landing Zone (🚧 work in progress)                           |

### 3️⃣ Configure

* Adjust networking to match organizational requirements.
* Set up **ExpressRoute** or **VPN** for hybrid connectivity.

### 4️⃣ Deploy

* Use the provided **Bicep templates** and automation scripts.

### 5️⃣ Explore Additional Guides

* 📘 [Backup Strategy](./docs/backup-strategy/backup-solutions.md)
* 📘 [AIX Best Practices](./docs/aix-best-practices/aix-best-practices.md)
* 📘 [Performance Navigator Guides](./docs/performance-navigator/)

---

## 🤝 Contributing

We welcome contributions!
You can help by:

* 💬 Providing **feedback** on templates and scripts
* 💡 Suggesting **new features** or enhancements
* 📝 Improving **documentation**

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🆘 Support

For help, please [open an issue](https://github.com/daverendon/skytap/issues).

