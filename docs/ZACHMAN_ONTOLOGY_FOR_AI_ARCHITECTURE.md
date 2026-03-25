# **Architectural Integrity in Socio-Technical Systems: An Ontology-Driven Framework for Zero Trust via the Zachman Matrix and Veridm Discipline**

The contemporary enterprise operates as a complex socio-technical system, where the traditional boundaries of network security and organizational structure have dissolved under the pressure of digital transformation and decentralized operations.1 As organizations transition toward Zero Trust Architecture (ZTA), the challenge shifts from implementing isolated security products to managing a pervasive and dynamic architectural complexity that spans users, devices, networks, applications, and data.3 This report examines the intersection of the Zachman Framework for Enterprise Architecture and an emerging AI-driven discipline called veridm, providing a formal ontology and a systematic approach to scaffolding these complex systems using modern AI agents like Codex within a Visual Studio and Git-based development environment.5

## **The Crisis of Complexity in Modern Socio-Technical Systems**

Enterprises are fundamentally socio-technical in nature, meaning they are comprised of interconnected human actors and technical components that must operate in concert to achieve organizational goals.2 This inherent complexity is exacerbated by the modern threat landscape, where traditional perimeter-based security models have proven inadequate.8 The dissolution of the network edge—driven by remote work, bring-your-own-device (BYOD) policies, and multi-cloud environments—requires a fundamental shift in how trust is managed.9 In this environment, the enterprise cannot be viewed as a static machine; it is a living system requiring a new form of architectural governance.10

The shift toward Zero Trust is not merely a technical upgrade but a strategic response to these trends. Zero Trust operates on the principle of "never trust, always verify," assuming that the network is always hostile and that threats are persistent both inside and outside the environment.3 To manage this, security must be moved from the network perimeter to the individual resource and access request level.4 However, implementing such a granular model across an entire enterprise creates a massive increase in the volume of architectural metadata that must be managed, requiring a systematic classification scheme.13

### **The Emergence of Veridm as an AI-Driven Discipline**

In response to this complexity, the discipline of veridm has emerged. Rooted in the need for "architectural truth" within socio-technical systems, veridm serves as an AI-driven methodology for maintaining alignment between strategic intent and operational reality.11 The term itself suggests a focus on the veracity of the system's state—ensuring that the functioning enterprise remains a faithful instantiation of its design.11 Veridm leverages generative AI and common ontologies to transform linear resource accretion into governed scaling, preventing the "architectural rot" that typically occurs when systems grow without a formal classification framework.14

By utilizing AI agents to mediate the reification process—the transition from abstract idea to concrete implementation—veridm allows organizations to maintain a "single source of truth" across all perspectives of the enterprise.10 This is particularly critical in Zero Trust environments, where a single misconfiguration in an access policy or a gap in identity governance can compromise the entire security posture.3

## **Fundamentals of the Zachman Framework for Enterprise Architecture**

To provide the necessary structure for Zero Trust and veridm, the Zachman Framework offers a comprehensive classification system.13 It is not a methodology but an ontology—a theory of the existence of a structured set of essential components for any object, in this case, the enterprise.5 The framework is depicted as a 6x6 matrix, intersecting six communication interrogatives (the Columns) with six perspectives of reification (the Rows).5

### **The Communication Interrogatives: The Columns**

The columns of the Zachman Framework represent the fundamental questions that must be answered to describe any complex system.13 Each column addresses a distinct aspect of the enterprise and has its own unique basic model.13

| Interrogative | Fundamental Aspect | Description in a Zero Trust Context |
| :---- | :---- | :---- |
| What | Data / Inventory Sets | The protect surface, including sensitive data, applications, assets, and services (DAAS). 1 |
| How | Function / Process Flows | The transactions and workflows that describe how data is accessed and moved. 4 |
| Where | Network / Distribution | The spatial distribution of resources, including cloud, on-prem, and remote nodes. 9 |
| Who | People / Responsibility | The identities (human and machine), roles, and access control permissions. 3 |
| When | Time / Timing Cycles | The temporal aspects of access, session durations, and event logging. 4 |
| Why | Motivation / Intentions | The business rules, security policies, and goals driving access decisions. 12 |

### **The Reification Perspectives: The Rows**

The rows of the framework represent the different viewpoints of the stakeholders involved in the development and operation of the enterprise.13 The top-down order of the rows is significant, representing the transformation from abstract concepts to physical reality.16

1. **Scope (Planner's View)**: Defines the context and external environment, focusing on high-level objectives and the boundaries of the system.13  
2. **Business Model (Owner's View)**: Describes the business concepts, processes, and organizational structures as the owner sees them.13  
3. **System Model (Designer's View)**: Translates business requirements into logical information system architectures and data models.13  
4. **Technology Model (Builder's View)**: Concentrates on the physical technology infrastructure and the implementation of logical models.13  
5. **Detailed Representations (Sub-contractor's View)**: Contains the specific configurations, code snippets, and deployment details.13  
6. **Functioning Enterprise (User's View)**: The actual operation of the system, including live data and active processes.13

### **The Rules of the Zachman Ontology**

For the framework to be effective as an ontology, it must follow strict rules of normalization.17 Rule 1 mandates that rows and columns must not be added, as the six interrogatives are sufficient to describe any subject.17 Rule 2 states that each column has a simple generic model, and Rule 3 specifies that each cell must be unique, specializing its column's model to its row's perspective.17 Rule 4 requires that the basic model of each column be unique to avoid redundancy, while Rule 5 prohibits diagonal relationships between cells to maintain clarity.17 Finally, Rule 7 asserts that the logic is recursive, meaning it can be applied to describe a whole enterprise or a single component.17

## **Zero Trust Architecture: From Implicit to Explicit Verification**

Zero Trust is a response to the reality that traditional perimeter security is no longer viable in a world of pervasive connectivity and sophisticated threats.8 The core tenets of Zero Trust, as defined by NIST SP 800-207 and industry leaders, emphasize the elimination of implicit trust based on network location.3

### **Core Principles and Tenets**

The Zero Trust security model is built on several non-negotiable principles 3:

* **Never Trust, Always Verify**: No user, device, or workload is trusted by default, even if they are already connected to the corporate network.3 Every access request must be authenticated, authorized, and validated against dynamic policies.1  
* **Least Privilege Access**: Users and devices are granted only the minimum level of access required to perform their specific tasks, reducing the potential blast radius of a breach.3  
* **Assume Breach**: Security teams must operate under the assumption that an attacker is already present in the environment, shifting the focus to internal monitoring, containment, and rapid response.3  
* **Context-Aware Access Policies**: Access decisions are informed by a variety of contextual data points, including identity, device health, location, and the sensitivity of the data being requested.3

### **The Five Pillars of Zero Trust**

Implementation of ZTA typically focuses on five core pillars, each of which must be integrated into the broader architectural framework 3:

1. **Identity**: Securing all human and machine identities through robust authentication (MFA) and continuous monitoring of trustworthiness.4  
2. **Devices**: Assessing the real-time security posture of every device attempting to access the network.3  
3. **Network**: Controlling the network through microsegmentation and software-defined perimeters to restrict lateral movement.3  
4. **Applications**: Verifying access at the application layer and monitoring application behavior at runtime.3  
5. **Data**: Classifying sensitive information and applying stringent access controls to protect it at rest and in transit.3

## **Mapping Zero Trust to the Zachman Framework Cells**

To manage the complexity of a Zero Trust implementation, it is necessary to map its components to the 36 cells of the Zachman matrix.13 This mapping ensures that every security control is aligned with business goals and that there are no gaps in the architectural representation.13

### **Row 1: The Planner's Perspective (Scope of the Protect Surface)**

In the Planner view, the focus is on identifying the high-level scope of the Zero Trust initiative.13 This involves defining the "protect surface"—the critical data, assets, applications, and services (DAAS) that the organization must defend.18

| Aspect | Zero Trust Artifact in the Planner Perspective |
| :---- | :---- |
| What (Data) | Lists of High-Value Assets (HVAs) and critical data categories (e.g., PII, IP). 8 |
| How (Function) | High-level mission and business processes that depend on protected assets. 13 |
| Where (Network) | Geographic and logical locations of business operations (e.g., regions, cloud zones). 13 |
| Who (People) | Major organizational units and stakeholder groups (e.g., departments, partners). 13 |
| When (Time) | Major business cycles and timing requirements for security posture reporting. 13 |
| Why (Motivation) | Strategic goals, compliance mandates (e.g., Executive Order 14028), and risk appetite. 8 |

### **Row 2: The Owner's Perspective (Business Modeling for Access)**

The Owner view describes how the business operates and the rules that govern those operations.13 In a Zero Trust model, this is where business policies are translated into conceptual access rules.3

| Aspect | Zero Trust Artifact in the Owner Perspective |
| :---- | :---- |
| What (Data) | Conceptual data models and business entities (e.g., Customer, Financial Transaction). 13 |
| How (Function) | Workflow models and business activity diagrams showing how tasks are performed. 13 |
| Where (Network) | Business locations and nodes where assets are accessed (e.g., office, home, mobile). 13 |
| Who (People) | Organizational roles and responsibility assignments (e.g., role-based access control units). 2 |
| When (Time) | Business events and schedules that trigger access (e.g., payroll processing time). 13 |
| Why (Motivation) | Business rules and access policies derived from security mandates. 12 |

### **Row 3: The Designer's Perspective (Logical System Modeling)**

The Designer view translates business models into logical system designs.13 This is where the specific logic of the Zero Trust Policy Decision Point (PDP) and Policy Enforcement Point (PEP) is defined.9

| Aspect | Zero Trust Artifact in the Designer Perspective |
| :---- | :---- |
| What (Data) | Logical data models, schemas, and attribute definitions for ABAC. 4 |
| How (Function) | Application architecture and logical process flows for access requests. 4 |
| Where (Network) | Logical network architecture, microsegmentation boundaries, and SDP definitions. 3 |
| Who (People) | User interfaces for identity management and role definitions for access. 2 |
| When (Time) | Processing cycles, session time-out logic, and event-driven triggers. 13 |
| Why (Motivation) | Logical rule models and conditional access logic (e.g., "If risk \> X, then deny"). 3 |

### **Row 4: The Builder's Perspective (Technology Modeling and Infrastructure)**

The Builder view focuses on the actual technology used to implement the logical designs.13 This includes the specific products and services used to enforce Zero Trust.19

| Aspect | Zero Trust Artifact in the Builder Perspective |
| :---- | :---- |
| What (Data) | Physical data models and database schemas for asset and user metadata. 6 |
| How (Function) | System architecture diagrams and configurations for PEPs and PDPs. 13 |
| Where (Network) | Physical network configurations, firewall rules, and VPC lattice settings. 13 |
| Who (People) | Identity management system configurations (e.g., Okta, Azure AD, Ping Identity). 3 |
| When (Time) | Scheduling specifications and timing definitions for security scans and audits. 13 |
| Why (Motivation) | Implementation strategies for applying policies across different technology stacks. 9 |

### **Row 5: The Sub-contractor's Perspective (Detailed Representations)**

The Sub-contractor view provides the detailed specifications and code necessary to build individual components.13 In a veridm-driven approach, this is where AI agents generate the scaffolding and configuration files.15

| Aspect | Zero Trust Artifact in the Sub-contractor Perspective |
| :---- | :---- |
| What (Data) | Data definitions, JSON schemas, and field-level encryption requirements. 13 |
| How (Function) | Code snippets, scripts, and configurations for specific security tools. 13 |
| Where (Network) | Detailed network node addresses, endpoint configurations, and interface specs. 13 |
| Who (People) | Specific security and access control lists (ACLs) and API keys. 13 |
| When (Time) | Precise timing definitions and log format specifications. 13 |
| Why (Motivation) | Detailed business rules expressed as code (e.g., Rego for OPA). 13 |

### **Row 6: The Functioning Enterprise (Operational Reality)**

The final row represents the actual functioning enterprise, where the architecture is instantiated and the security policies are enforced in real-time.13

| Aspect | Zero Trust Artifact in the Functioning Enterprise |
| :---- | :---- |
| What (Data) | Actual data transactions, records, and the real-time state of the protect surface. 13 |
| How (Function) | Running processes, active application sessions, and executed workflows. 13 |
| Where (Network) | Operational network traffic, active connections, and deployed nodes. 13 |
| Who (People) | Active users, authenticated sessions, and real-time operator actions. 13 |
| When (Time) | Event logs, time-stamped access records, and audit trails. 4 |
| Why (Motivation) | Real-time performance metrics and policy enforcement outcomes. 13 |

## **Veridm: The AI-Driven Discipline of Architectural Truth**

The discipline of veridm is essential for managing the recursive and multi-dimensional nature of the Zachman Framework within a Zero Trust environment.14 Veridm acknowledges that in complex socio-technical systems, the "truth" of the architecture is often obscured by rapid change and organizational siloes.10 By leveraging AI as a primary tool for architectural representation, veridm ensures that every change to the system is architecturally valid.15

### **The Role of Generative AI in Architectural Governance**

Generative AI agents, such as Codex, are not just code generators; they are "reasoning engines" that can be programmed to understand and enforce architectural ontologies.21 In the veridm discipline, the AI agent is given the role of a "Sub-contractor" that must operate within the constraints set by the "Designer" and "Owner".13 This is achieved through the use of an "AI Contract"—a set of non-negotiable rules checked into the repository that the AI must follow.15

The AI Contract might specify, for example, that all business logic for access control must reside in a specific domain layer and never in the user interface, or that every database change must be accompanied by an update to the logical data model.15 This prevents the "local hacks" that often occur when AI is used without a formal framework.15

### **Governed Scaling vs. Linear Accretion**

Traditional systems development often relies on linear resource accretion—adding more servers, more code, and more security products as needs grow.14 This leads to fragmented architectures and "technical debt." Veridm replaces this with governed scaling, where the AI ensures that new components are integrated into the existing Zachman matrix according to established patterns.14

This is particularly useful in Zero Trust deployments, which often involve a "crawl, walk, run" approach.19 As an organization moves from basic identity management to advanced microsegmentation, veridm ensures that the new capabilities are mapped to the correct cells in the Zachman Framework, maintaining the integrity of the overall system.19

## **Constructing the Concise Ontology for the Codex Prompt**

To enable Codex to scaffold a 6x6 visual web page backed by a database, we must first define the ontology that will guide its reasoning.5 This ontology provides the metadata and the structural rules that ensure the resulting system is not just a collection of code but a systematic architectural representation.15

### **Ontological Entities and Relationships**

The ontology for the ZT-Zachman visualizer includes the following primary entities:

1. **Perspective (Row)**: One of the six viewpoints (Planner, Owner, Designer, Builder, Sub-contractor, User).  
2. **Interrogative (Column)**: One of the six aspects (What, How, Where, Who, When, Why).  
3. **Cell**: The intersection of a Perspective and an Interrogative, representing a unique architectural artifact.5  
4. **ZT-Pillar**: The security domain (Identity, Device, Network, Application, Data) that the artifact addresses.3  
5. **Artifact-Type**: The format of the representation (e.g., List, Model, Code, Log).  
6. **Constraint**: The rules that govern the cell's creation and its relationship to other cells (e.g., Rule 1-7 of Zachman).17

### **The Reification Rules for the AI Agent**

The ontology must also include the rules of reification that Codex must follow when scaffolding the system 15:

* **Top-Down Alignment**: A change in a higher-row cell (e.g., a new business policy in Row 2, Why) must trigger a requirement for the AI to propose changes in the corresponding lower-row cells (e.g., Row 3, Why logic and Row 5, Why code).15  
* **Columnar Independence**: The AI must treat each column as a distinct descriptive focus, ensuring that data (What) and process (How) are not conflated in the same code module.13  
* **Zero Trust Consistency**: Every artifact in every cell must be evaluated against the "Never Trust, Always Verify" principle.3 For example, a cell in Row 5, Who (Security and Access Control) must use standard identity protocols rather than proprietary hacks.13

## **Prompt Engineering for Codex: Scaffolding the 6x6 Visual Interface**

With the ontology defined, the next step is to develop the prompt for Codex. This task is approached as a multi-step workflow in Visual Studio Code, utilizing Git for version control and persistent architectural documentation.6

### **Step 0: Initial Environment Setup**

The goal is to build a Minimum Viable Product (MVP) of an enterprise architectural visualizer. This involves creating a single web page (using a tool like Streamlit or React) backed by a relational database (like DuckDB or SQLite).6

**Environment Preparation**:

1. Initialize a Git repository.  
2. Launch VS Code.  
3. Install the Codex/GitHub Copilot extension.6  
4. Create a folder structure that separates documentation from implementation:  
   * /docs: For AI\_CONTRACT.md, ARCHITECTURE.md, and DECISIONS.md.15  
   * /src: For the web page and database logic.  
   * /data: For initial CSV data ingestion representing the Zachman matrix.6

### **Step 1: Establishing the AI Contract**

Before generating any code, the AI must be given its "contract".15 This prompt instructs Codex to read the rules and acknowledge them.

**Prompt Snippet**: "You are a Veridm Architectural Lead. Before writing any code, read the following files: AI\_CONTRACT.md and ARCHITECTURE.md. Your goal is to scaffold a 6x6 visual web page that represents the Zachman Framework for a Zero Trust enterprise. Every component you build must align with the 'Never Trust, Always Verify' principle and the structural rules of the Zachman Framework. You are forbidden from creating one-off hacks; all logic must be rule-based and modular." 15

### **Step 2: Defining the Database Scaffolding**

The next step is to prompt Codex to create the database schema that will store the 36 cells and their corresponding ZT artifacts.6

**Prompt Snippet**: "Generate a DuckDB schema for the ZT-Zachman-Matrix. Create a table named zachman\_cells with columns for perspective, interrogative, zt\_pillar, artifact\_name, and artifact\_content. Also, create supporting tables for assets, identities, and access\_policies. Populate the database with initial metadata representing the Row 1 and Row 2 perspectives of a Zero Trust protect surface." 6

### **Step 3: Generating the Visual Dashboard**

Finally, the prompt instructs Codex to build the web interface—a 6x6 grid where each cell is interactive and displays its architectural content from the database.6

**Prompt Snippet**: "Using Streamlit, create a 6x6 visual grid representing the Zachman Matrix. Each cell in the grid should be clickable. When clicked, it should fetch the corresponding artifact from the zachman\_cells table in DuckDB and display it in a sidebar. Ensure the UI differentiates between the perspectives (Rows) and the interrogatives (Columns) using clear labeling. Implement a search function that allows the user to filter cells by Zero Trust pillar (e.g., Identity, Data)." 6

## **Technical Blueprint for the 6x6 Web-Based Architectural Orchestrator**

The resulting system is more than a dashboard; it is an orchestrator that enables the veridm discipline within the enterprise.10

### **The Data Layer: Multi-Perspective Modeling**

The use of DuckDB allows for high-performance querying of the complex relationships between the Zachman cells.6 Each row in the database represents a unique intersection that has been "verified" by the veridm process.5

| Table | Purpose | Relationship to Zachman |
| :---- | :---- | :---- |
| cell\_metadata | Stores the primary artifact for each of the 36 cells. | 1:1 with the Zachman Matrix. 17 |
| protect\_surface | Detailed inventory of DAAS (What). | Maps to What column, Rows 1-4. 18 |
| identity\_governance | Identity registry and role maps (Who). | Maps to Who column, Rows 1-5. 3 |
| policy\_logic | Executable business rules (Why). | Maps to Why column, Rows 2-5. 12 |
| event\_logs | Operational telemetry (When). | Maps to When column, Row 6\. 4 |

### **The Logic Layer: AI-Mediated Reification**

In a veridm-enabled system, the logic layer does not just execute code; it validates changes against the ontology.15 When a developer (the "Sub-contractor") updates a piece of security code in Row 5, the veridm AI checks the AI\_CONTRACT.md and the Designer models in Row 3 to ensure the change is authorized and consistent with the intended ZT posture.15

This creates a "self-healing" architecture where inconsistencies are flagged automatically.15 For example, if a new network route (Where) is added without a corresponding access policy (Why), the system will flag the cell in the visual dashboard as "Invalid" or "Unverified".13

### **The UI Layer: The 6x6 Visual Grid**

The visual interface provides a common language for all enterprise stakeholders.23

* **Planner (Strategic View)**: Shows the progress of ZT maturity across the protect surface.  
* **Architect (System View)**: Visualizes the logical flow of data between zones and layers.  
* **Security Analyst (Operation View)**: Displays real-time threats and access denials mapped to the specific organizational units they affect.3

## **Governing the Transition: A Vertical Slice Methodology**

Implementing a full Zero Trust architecture across 36 Zachman cells is an enormous undertaking.20 The veridm discipline recommends building in "vertical slices"—completing one functional path from the Planner perspective down to the Functioning Enterprise.15

### **Implementing the First Vertical Slice: Identity Verification**

A common first slice is the identity pillar.12 In this slice, the organization would:

1. **Planner (Row 1, Who)**: Identify all critical user groups.13  
2. **Owner (Row 2, Who)**: Define the conceptual roles for those groups.2  
3. **Designer (Row 3, Who)**: Design the MFA and SSO logical architecture.3  
4. **Builder (Row 4, Who)**: Configure the identity provider (e.g., Azure AD).19  
5. **Sub-contractor (Row 5, Who)**: Deploy the specific API integrations and access control lists.13  
6. **Enterprise (Row 6, Who)**: Monitor live login events and anomalies.4

By completing this vertical slice, the organization demonstrates the value of the Zachman-ZT approach and establishes a repeatable pattern for subsequent pillars like Network and Data.19

## **Synthesizing Socio-Technical Integrity and Architectural Governance**

The combination of the Zachman Framework, Zero Trust, and the veridm discipline addresses the core challenges of modern enterprise complexity.2 By treating the enterprise as a socio-technical system that requires systematic representation, organizations can move beyond ad hoc security measures to a state of architectural resilience.10

The role of AI in this process is transformative. Agents like Codex, when guided by a concise ontology and a strict AI contract, can automate the tedious aspects of architectural documentation and scaffolding, allowing architects to focus on strategic alignment and risk management.15 The 6x6 visual orchestrator serves as the nexus of this collaboration, providing a unified view of the enterprise's "architectural truth".11

Ultimately, the goal of these systematic architectural representations is not just to build a secure system, but to manage complexity successfully.14 In an era of pervasive threats and rapid technological change, the ability to maintain a clear, consistent, and verified architecture is the ultimate competitive advantage for the modern enterprise.7

## **Detailed Analysis of Zachman Rule Application in AI Scaffolding**

Applying the seven rules of the Zachman Framework to the AI-driven scaffolding process ensures that the generated code is normalized and robust.17

**Rule 1: Completeness through the Interrogatives** The AI agent must be instructed that the six columns (What, How, Where, Who, When, Why) are exhaustive.17 When scaffolding the database, Codex should generate tables that correspond precisely to these six categories, ensuring that no aspect of the Zero Trust protect surface is omitted.13

**Rule 2: Generic Modeling** Each column must follow its basic model. For the "How" column, this means the AI must focus on process transformations; for the "What" column, it must focus on data objects.17 This prevents the "spaghetti code" that occurs when functions and data are tightly coupled without an architectural reason.15

**Rule 3: Perspective Specialization** The AI must understand that a "Logical Data Model" in the Designer row (Row 3\) is different from a "Physical Database Schema" in the Builder row (Row 4).13 The scaffolding prompt must include instructions for the AI to generate different representations for the same data entity as it moves down the rows of the matrix.6

**Rule 4: Semantic Uniqueness** To avoid redundancy, the AI is forbidden from replicating data in multiple columns.17 For example, the "Who" column manages identities, while the "Where" column manages network locations.13 The AI Contract must enforce this separation, ensuring that access policies (Why) refer to identities and locations without redefining them.15

**Rule 5: Vertical Cohesion** While diagonal relationships are prohibited, vertical relationships (reification) are mandatory.17 The veridm discipline uses AI to check that every piece of code in Row 5 can be traced back through Rows 4 and 3 to a specific business requirement in Row 2\.15

**Rule 7: Recursive Logic** The Zachman ontology is recursive, allowing the 6x6 matrix to be applied to a single microservice or the entire global enterprise.17 This is critical for microsegmentation in Zero Trust, where each segment can be treated as its own "enterprise" with its own protect surface, identities, and policies.3

## **Conclusion: The Convergence of AI and Architecture**

The development of a 6x6 visual web page backed by a database is more than a technical exercise; it is the implementation of a new architectural paradigm.5 By leveraging the Zachman Framework as an ontology and veridm as a discipline, organizations can navigate the complexities of Zero Trust and socio-technical systems with confidence.2

The use of AI agents like Codex to scaffold these systems provides the necessary speed and precision, provided they are governed by a rigorous framework.15 The resulting architectural orchestrator becomes the "single source of truth" for the enterprise, ensuring that every access decision is verified, every asset is protected, and every stakeholder has a clear view of the architectural state.3 This convergence of AI and architecture represents the future of enterprise design, where complexity is managed not through avoidance, but through systematic representation and governed scaling.14

#### **Works cited**

1. What is Zero Trust Architecture (ZTA)? \- CrowdStrike.com, accessed March 10, 2026, [https://www.crowdstrike.com/en-us/cybersecurity-101/zero-trust-security/zero-trust-architecture/](https://www.crowdstrike.com/en-us/cybersecurity-101/zero-trust-security/zero-trust-architecture/)  
2. A Formalized Zoned Role‑Based Framework for the Analysis, Design, Implementation, Maintenance and Access Control of Integrated \- Preprints.org, accessed March 10, 2026, [https://www.preprints.org/manuscript/202602.0025/v1/download](https://www.preprints.org/manuscript/202602.0025/v1/download)  
3. What Is Zero Trust Architecture? Key Elements and Use Cases \- Palo Alto Networks, accessed March 10, 2026, [https://www.paloaltonetworks.com/cyberpedia/what-is-a-zero-trust-architecture](https://www.paloaltonetworks.com/cyberpedia/what-is-a-zero-trust-architecture)  
4. Zero trust architecture \- Wikipedia, accessed March 10, 2026, [https://en.wikipedia.org/wiki/Zero\_trust\_architecture](https://en.wikipedia.org/wiki/Zero_trust_architecture)  
5. About the Zachman Framework \- Zachman International \- FEAC Institute, accessed March 10, 2026, [https://zachman-feac.com/zachman/about-the-zachman-framework](https://zachman-feac.com/zachman/about-the-zachman-framework)  
6. GPT-5.2 Codex Tutorial: Build a Data Pipeline in VSCode | DataCamp, accessed March 10, 2026, [https://www.datacamp.com/tutorial/gpt-5-2-codex-tutorial](https://www.datacamp.com/tutorial/gpt-5-2-codex-tutorial)  
7. (PDF) A Practical Framework for Advancing Cybersecurity, Artificial Intelligence and Technological Ecosystems to Support Regional Economic Development and Innovation \- ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/389198144\_A\_Practical\_Framework\_for\_Advancing\_Cybersecurity\_Artificial\_Intelligence\_and\_Technological\_Ecosystems\_to\_Support\_Regional\_Economic\_Development\_and\_Innovation](https://www.researchgate.net/publication/389198144_A_Practical_Framework_for_Advancing_Cybersecurity_Artificial_Intelligence_and_Technological_Ecosystems_to_Support_Regional_Economic_Development_and_Innovation)  
8. Zero Trust Architecture (ZTA) \- GSA, accessed March 10, 2026, [https://buy.gsa.gov/api/system/files/documents/zta\_buyers\_guide\_v3.0\_20240221.pdf](https://buy.gsa.gov/api/system/files/documents/zta_buyers_guide_v3.0_20240221.pdf)  
9. Zero Trust Architecture \- NIST Technical Series Publications, accessed March 10, 2026, [https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf)  
10. Human Systems Engineering and Design (IHSED2025): Future Trends and Applications, accessed March 10, 2026, [https://openaccess.cms-conferences.org/publications/book/978-1-964867-74-8](https://openaccess.cms-conferences.org/publications/book/978-1-964867-74-8)  
11. A/ 633\_, accessed March 10, 2026, [http://csds.cz/cs/4785-DS/version/15/part/15/data/Havel%20Ivan%20-%20Gratulovn%C3%ADk1998.pdf](http://csds.cz/cs/4785-DS/version/15/part/15/data/Havel%20Ivan%20-%20Gratulovn%C3%ADk1998.pdf)  
12. Zero Trust & Zero Trust Network Architecture (ZTNA), Explained \- Splunk, accessed March 10, 2026, [https://www.splunk.com/en\_us/blog/learn/zero-trust.html](https://www.splunk.com/en_us/blog/learn/zero-trust.html)  
13. What is the Zachman Framework? A Definitive Guide to this EA Standard \- Ardoq, accessed March 10, 2026, [https://www.ardoq.com/knowledge-hub/zachman-framework](https://www.ardoq.com/knowledge-hub/zachman-framework)  
14. December 2025 \- American Journals, accessed March 10, 2026, [https://www.american-journals.com/december2025](https://www.american-journals.com/december2025)  
15. How to Build Real Software with VS Code \+ Codex (Without Letting AI Rot Your Codebase), accessed March 10, 2026, [https://medium.com/@mohsenny/how-to-build-real-software-with-vs-code-codex-without-letting-ai-rot-your-codebase-b4486579d6c4](https://medium.com/@mohsenny/how-to-build-real-software-with-vs-code-codex-without-letting-ai-rot-your-codebase-b4486579d6c4)  
16. Zachman Framework \- Wikipedia, accessed March 10, 2026, [https://en.wikipedia.org/wiki/Zachman\_Framework](https://en.wikipedia.org/wiki/Zachman_Framework)  
17. The Zachman Framework – A Definitive Guide \- SAP LeanIX, accessed March 10, 2026, [https://www.leanix.net/en/wiki/ea/zachman-framework](https://www.leanix.net/en/wiki/ea/zachman-framework)  
18. How to implement zero trust: A step-by-step roadmap \- Diligent, accessed March 10, 2026, [https://www.diligent.com/resources/blog/how-to-implement-zero-trust](https://www.diligent.com/resources/blog/how-to-implement-zero-trust)  
19. Mappings — Implementing a Zero Trust Architecture Project documentation \- NIST Pages, accessed March 10, 2026, [https://pages.nist.gov/zero-trust-architecture/VolumeE/Mappings.html](https://pages.nist.gov/zero-trust-architecture/VolumeE/Mappings.html)  
20. When Zachman Works: a Digital Transformation Guide | askCraig, accessed March 10, 2026, [https://askcraig.ai/articles/architecture/when-zachman-works-for-digital-transformation](https://askcraig.ai/articles/architecture/when-zachman-works-for-digital-transformation)  
21. Best practices \- OpenAI for developers, accessed March 10, 2026, [https://developers.openai.com/codex/learn/best-practices](https://developers.openai.com/codex/learn/best-practices)  
22. Use prompt files in VS Code, accessed March 10, 2026, [https://code.visualstudio.com/docs/copilot/customization/prompt-files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)  
23. Unpacking the Zachman Framework: A Compass for Enterprise Architecture \- Oreate AI Blog, accessed March 10, 2026, [http://oreateai.com/blog/unpacking-the-zachman-framework-a-compass-for-enterprise-architecture/2e99a98fca45c7a4852165f20dc33d06](http://oreateai.com/blog/unpacking-the-zachman-framework-a-compass-for-enterprise-architecture/2e99a98fca45c7a4852165f20dc33d06)