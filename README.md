# Skytap Landing Zones

Welcome to the **Skytap Landing Zones on Azure** repository! This project provides a structured approach to deploying Skytap environments on Azure, facilitating the migration of AIX and IBM i systems to Azure.

<!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>
<a class="github-button" href="https://github.com/daverendon/skytap" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-star" data-size="large" aria-label="Star daverendon/skytap on GitHub">🌟 **Star** this repository to stay updated and show your support!</a>

## Overview

**Skytap on Azure** provides a unique solution for running IBM Power and x86 workloads in the cloud, enabling lift-and-shift migrations without the need to modify the applications or architectures significantly. Skytap Landing Zones are pre-configured environments that follow best practices and guidelines to optimize the deployment of these workloads on Azure.

### Key Components of a Skytap Landing Zone

1. **Pre-configured Infrastructure**:
   - Includes necessary virtual network settings, storage configurations, and computing resources tailored to security, compliance, and operational requirements.

2. **Security and Compliance**:
   - Built with security controls and compliance guidelines in mind to ensure that the migrated applications adhere to organizational policies and regulatory standards.

3. **Connectivity**:
   - Ensures robust connectivity options, including VPNs and ExpressRoute connections, for secure and reliable communication between the Skytap environment and on-premises data centers or other cloud services.

4. **Scalability and Flexibility**:
   - Designed to be scalable and flexible to accommodate growth and changes in the workload requirements. This includes scalable storage options and dynamic allocation of computing resources.

5. **Automation and Orchestration**:
   - Incorporates automation tools and scripts to simplify the migration process. This might involve using Bicep Language and Skytap APIs for automation.

### Purpose of a Skytap Landing Zone

- **Risk Mitigation**: Reduces the risk associated with cloud migrations by providing a controlled and secure environment to deploy applications.
- **Accelerate Migration**: Speeds up the migration process by offering a ready-to-use environment that reduces the setup time and complexity involved in configuring cloud resources from scratch.
- **Best Practices Integration**: Integrates best practices for cloud deployment, management, and security, ensuring a robust and efficient cloud environment.
- **Consistency and Standardization**: Provides a standardized approach to deploying workloads in the cloud, ensuring consistency across various projects and teams within an organization.

Skytap Landing Zones are part of a strategic approach to cloud adoption, ensuring that organizations can leverage the full benefits of the cloud while addressing the challenges of migration.

## Getting Started

Follow these steps to start with Skytap Landing Zones:

1. **Prerequisites**:
   - An active Azure subscription.
   - A basic understanding of Skytap and its functionalities.
   - Basic knowledge of Azure services like VNets, Blob Storage, and ExpressRoute.
   - An active Skytap on Azure subscription. You can create one by following these [instructions](https://blog.azinsider.net/deploy-skytap-on-azure-using-bicep-language-to-run-your-ibm-power-workloads-a245e7c3287e?source=friends_link&sk=a863322248b8aba5288da813d569afdc)

2. **Select a Landing Zone (IBMi or AIX)**:
   - Utilize the provided Bicep Language templates and scripts to set up your initial Skytap environment in Azure.

| OS  | Description                                                                                               |
|-----|-----------------------------------------------------------------------------------------------------------|
| AIX | Deploy the **[Skytap AIX Landing Zone](docs/aix/aix-landing-zone.md)**                                                          |
| IBM | IBM i Landing Zone (work in progress) 


3. **Configuration**:
   - Configure the network settings according to your organizational needs.
   - Set up the connection between your on-premises data center and Azure using ExpressRoute or VPNs.

4. **Deployment**:
   - Deploy the Skytap Landing Zones using the guidelines provided in the deployment scripts.

5. **📘 Additional Guides & Resources**
- [Backup Strategy](./docs/backup-strategy/backup-solutions.md)
- [AIX Best Practices](./docs/aix-best-practices/aix-best-practices.md)
- [Performance Navigator Guides](./docs/performance-navigator/readme.MD)


## Contributing

We welcome contributions! You can help by:
- **Providing Feedback** on templates and scripts.
- **Suggesting Features** or enhancements.
- **Improving Documentation**.

## License

This project is licensed under the MIT license.

## Support

For assistance, please [open an issue](https://github.com/daveRendon/skytap/issues) in this repository.
