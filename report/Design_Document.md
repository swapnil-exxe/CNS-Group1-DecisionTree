# Cryptography and Network Security: Group 1 Design Document
## Complete System Architecture, Subsystem Engineering, and Deployment Specifications for Lightweight IoT Botnet Attack Detection Using Pruned CART Decision Trees

---

**Course / Subject:** Cryptography and Network Security (CNS)  
**Project Group:** Group 1 — Decision Tree  
**Assigned Research Topic:** Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees  
**Actual Machine Learning Implementation:** Classification and Regression Trees (CART) via `sklearn.tree.DecisionTreeClassifier`  
**Dataset:** N-BaIoT — Network-Based Detection of IoT Botnet Attacks (UCI ML Repository)  
**Target Environment:** Resource-Constrained IoT Gateway Appliances and Edge Routers  

---

# 1. Title and System Metadata

This document establishes the comprehensive software and hardware engineering design for the Group 1 Cryptography and Network Security (CNS) laboratory project. The system provides automated, deterministic, and explainable intrusion detection against active IoT botnet infections directly at the local network edge.

### System Specification Summary:
- **System Identifier:** CNS-G1-CART-IDS-v1.0
- **Primary Algorithm:** CART Decision Tree (`sklearn.tree.DecisionTreeClassifier`)
- **Optimization Strategy:** Minimal Cost-Complexity Pruning ($ccp\_\alpha = 1.999753 \times 10^{-5}$)
- **Telemetry Corpus:** N-BaIoT (89 Raw CSV files across 9 commercial IoT appliances, 7,062,606 raw packets)
- **Experimental Sample Partition:** 128,366 packets systematically sampled with deterministic step $k=55$
- **Feature Space:** 115 continuous stream statistics extracted across 5 damped sliding windows ($\lambda \in \{0.01, 0.1, 1, 3, 5\}$)
- **Classification Paradigm:** Dual-mode (11-class granular multi-vector attack taxonomy + binary benign/attack isolation)
- **Target Deployment Platform:** Embedded Linux gateway router (ARM Cortex-A or MIPS architecture)

---

# 2. Executive System Overview

The exponential proliferation of Internet of Things (IoT) hardware—spanning IP surveillance cameras, smart doorbells, home automation hubs, and digital voice assistants—has introduced massive security vulnerabilities into consumer and enterprise networks. Attackers deploy autonomous malware (e.g., Mirai, BASHLITE) that infect vulnerable IoT nodes and organize them into centrally managed botnets.

Existing intrusion detection solutions frequently rely on heavyweight deep learning models (such as Deep Autoencoders or Convolutional Neural Networks) that require substantial RAM and high-power floating-point hardware accelerators. Such models cannot run directly on edge gateways with strict power and memory budgets.

The **Group 1 System** solves this challenge by implementing an optimized, cost-complexity pruned CART decision tree. By operating over continuous behavioral flow statistics and employing structural pruning, the system achieves:
1. **Ultra-Low Classification Latency:** Single-packet evaluation latency of **34.41 $\mu$s**, enabling real-time inline packet filtering.
2. **Line-Rate Throughput:** Batch inference capacity of **12,036,209 packets per second**, exceeding Gigabit Ethernet wire speeds by more than 6x.
3. **Minimal Memory Footprint:** Serialized model disk footprint of **5.44 KB** and operational RAM usage under **100 KB**.
4. **Superior Predictive Accuracy:** **99.6183%** multiclass test accuracy and **99.9649%** binary botnet detection accuracy across 25,674 held-out test packets.

---

# 3. Fundamental Design Principles

The engineering architecture is guided by six foundational design principles:

1. **Deterministic Edge Execution:** The system must execute without probabilistic runtime variation. Branching paths are bounded by a fixed maximum tree depth ($h = 18$), guaranteeing deterministic worst-case latency.
2. **Zero In-Memory Feature Scaling Overhead:** The model operates directly on unscaled continuous floating-point values, eliminating the runtime CPU cycles required for min-max normalization or z-score standardization.
3. **Rigorous Test-Set Isolation:** The optimization and hyperparameter tuning pipeline must maintain strict separation between training and evaluation partitions, preventing data leakage.
4. **White-Box Security Explainability:** Every classification outcome must map to an explicit, human-auditable chain of Boolean inequalities to facilitate manual forensic verification and rapid firewall policy generation.
5. **Architectural Parsimony (Cost-Complexity Regularization):** Unnecessary structural complexity is actively pruned using Breiman's cost-complexity criterion, reducing overfitting while shrinking memory and latency footprints.
6. **Graceful Degradation and Fault Tolerance:** The system must handle unexpected data distribution shifts or network traffic bursts without crashing, buffer overflow, or kernel panics.

---

# 4. Overall System Architecture

The system is organized into a modular five-layer architecture:

```text
+-------------------------------------------------------------------------+
|                  Layer 1: Data Ingestion & Sampling                     |
|  - Raw N-BaIoT Archive Ingestion (89 CSVs, 7,062,606 raw packets)      |
|  - Deterministic Systematic Sampling (Step k = 55)                      |
|  - Balanced Extraction: 128,366 packets across 9 IoT appliances        |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|               Layer 2: Preprocessing & Data Hygiene Subsystem           |
|  - Verification of 115 continuous features (Zero NaNs, Zero Infs)       |
|  - Multiclass (11 classes) and Binary (Benign vs Malicious) Mapping     |
|  - Stratified Partitioning: 80% Training (102,692) / 20% Test (25,674) |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|            Layer 3: Optimization & Cost-Complexity Pruning              |
|  - Internal 80/20 Train/Validation Split (82,153 Train / 20,539 Val)    |
|  - Pruning Path Generation: 60 unique candidate alpha values           |
|  - Multi-Criteria Selection: Optimal alpha* = 1.999753e-05 isolated    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|              Layer 4: Retraining & Model Serialization Subsystem         |
|  - Full Training Set Fitting (102,692 instances) with alpha*            |
|  - Structural Simplification: Depth=18, Nodes=133, Leaves=67           |
|  - High-Efficiency Model Serialization (5.44 KB joblib payload)         |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|              Layer 5: Edge Inference & Real-Time Inspection             |
|  - Streaming Flow Ingestion & Feature Vector Construction               |
|  - Microsecond Scalar Tree Traversal (Average 34.41 us per packet)      |
|  - Line-Rate Gigabit Batch Processing (12.04M packets/sec)             |
|  - SIEM / Firewall Action Triggering (Alert, Drop, Quarantine)         |
+-------------------------------------------------------------------------+
```

---

# 5. Data Ingestion Subsystem

The Data Ingestion Subsystem interfaces directly with the raw packet telemetry corpus.

### 5.1 Telemetry Source
The system consumes the **N-BaIoT (Network-Based Detection of IoT Botnet Attacks)** dataset curated by Meidan et al. (2018) from the UCI Machine Learning Repository. Telemetry was collected from 9 physical commercial IoT appliances deployed in an isolated testbed:
1. Danmini Doorbell
2. Ecobee Thermostat
3. Ennio Doorbell
4. Philips B120N/10 Baby Monitor
5. Provision 737E PTZ Security Camera
6. Provision 838 PTZ Security Camera
7. SimpleHome XCS7-1002-WHT Security Camera
8. SimpleHome XCS7-1003-WHT Security Camera
9. Samsung SNH 1011 N SmartCam

### 5.2 Deterministic Systematic Sampling Engine
The complete raw dataset contains **7,062,606 rows** distributed across **89 distinct CSV files**, totaling over 9.2 GB of disk storage. To enable rigorous training within the memory constraints of typical development and evaluation hardware while maintaining class and device distributions, a deterministic systematic sampling engine is implemented:
- **Sampling Algorithm:** Systematic row extraction with a fixed period $k = 55$.
- **Offset:** Deterministic start index $0$.
- **Output Sample Size:** Exactly **128,366 packets**.
- **Audit Verification:** The sampling process was verified to preserve device and class proportions with zero random state drift.

---

# 6. Data Preprocessing & Validation Subsystem

The Preprocessing Subsystem transforms raw tabular telemetry into model-ready numerical matrices.

### 6.1 Data Hygiene and Sanitization
Each ingested record is validated against strict integrity rules:
1. **Null / NaN Check:** Complete verification confirms 0 missing entries across all 128,366 rows and 115 features.
2. **Infinite Value Check:** Verification confirms 0 positive or negative infinite values.
3. **Data Type Casting:** All 115 continuous features are validated as IEEE 754 64-bit floating-point numbers (`float64`).

### 6.2 Label Mapping and Class Taxonomy
The system implements an 11-class multi-vector label taxonomy covering benign operations and 10 specific attack vectors across two major IoT botnet families:

| Class ID | Canonical Label | Botnet Family | Attack Vector Description | Layer / Transport Protocol |
| :---: | :--- | :--- | :--- | :--- |
| **0** | `benign` | Benign Baseline | Normal operational IoT telemetry | Multi-protocol (TCP/UDP/ICMP) |
| **1** | `gafgyt_combo` | BASHLITE / Gafgyt | Telnet brute-force combo attack | TCP / Application Layer |
| **2** | `gafgyt_junk` | BASHLITE / Gafgyt | High-volume junk packet flooding | TCP Flooding |
| **3** | `gafgyt_scan` | BASHLITE / Gafgyt | Horizontal vulnerability scanning | TCP / ICMP Reconnaissance |
| **4** | `gafgyt_tcp` | BASHLITE / Gafgyt | TCP state exhaustion flood | TCP Handshake Flood |
| **5** | `gafgyt_udp` | BASHLITE / Gafgyt | Volumetric UDP bandwidth flood | UDP Transport Flood |
| **6** | `mirai_ack` | Mirai | TCP ACK state table exhaustion | TCP State Table Flood |
| **7** | `mirai_scan` | Mirai | Autonomous IP scanning for open ports | TCP SYN Scanning |
| **8** | `mirai_syn` | Mirai | Synchronize (SYN) connection flood | TCP Handshake Flood |
| **9** | `mirai_udp` | Mirai | High-intensity UDP packet flood | UDP Flooding |
| **10** | `mirai_udpplain`| Mirai | Optimized plain UDP flood (raw payload) | UDP Flooding |

### 6.3 Feature Space Representation
The feature space consists of **115 continuous statistical features** extracted by the upstream Kitsune network capture framework using damped incremental windows. The features capture packet size and inter-arrival timing dynamics across 5 time decay factors ($\lambda \in \{0.01, 0.1, 1, 3, 5\}$) and 4 network traffic scopes:
- **Host (H):** Outbound packet statistics originating from the local device.
- **Host-to-Host (HH):** Bi-directional flow statistics between the local device and specific remote endpoints.
- **Host-to-Host Jitter (HH_jit):** Packet inter-arrival time jitter statistics.
- **Host+Port-to-Host+Port (HpHp):** Fine-grained socket-level interaction statistics.

---

# 7. Tree Construction & Pruning Subsystem

The Tree Construction Subsystem is the algorithmic core of the architecture.

### 7.1 CART Induction Engine
The induction engine uses `sklearn.tree.DecisionTreeClassifier` parameterized as:
- `criterion='gini'`: Gini Impurity minimization for split selection.
- `splitter='best'`: Optimal exhaustive threshold search across all continuous dimensions.
- `random_state=42`: Fixed seed ensuring complete determinism.

### 7.2 Weakest-Link Cost-Complexity Pruner
Structural complexity is regularized via Minimal Cost-Complexity Pruning. The pruner:
1. Calculates the impurity risk $R(t)$ for every internal node and subtree $T_t$.
2. Solves for the critical threshold:
   $$\alpha_{\text{eff}}(t) = \frac{R(t) - R(T_t)}{|T_t| - 1}$$
3. Collapses subtrees sequentially to produce the sequence of candidate pruned trees.

---

# 8. Inference & Evaluation Subsystem

The Inference Subsystem provides dual evaluation pathways tailored for both real-time inline packet inspection and offline security reporting.

### 8.1 Dual-Mode Inference Engine
1. **Multiclass Engine:** Evaluates the input feature vector across the 18-level decision tree and outputs the exact attack vector classification (e.g., `mirai_ack`, `gafgyt_tcp`).
2. **Binary Anomaly Flag:** Projects the 11 multiclass labels into a binary indicator:
   $$\hat{y}_{\text{binary}} = \begin{cases} 0 \ (\text{Benign}), & \text{if } \hat{y}_{\text{multi}} = 0 \\ 1 \ (\text{Malicious Botnet}), & \text{if } \hat{y}_{\text{multi}} \in \{1, \dots, 10\} \end{cases}$$

### 8.2 Real-Time Metrics Pipeline
During test evaluation, the subsystem generates:
- Full 11x11 Multiclass Confusion Matrix
- Per-class Precision, Recall, and F1-score
- Macro, Micro, and Weighted Average F1-scores
- Binary Detection Accuracy, Precision, Recall, and F1-score

---

# 9. Computational Profiling Subsystem

To validate operational viability on resource-constrained embedded network appliances, the system incorporates a dedicated hardware benchmarking harness.

### 9.1 Latency and Throughput Profiler
The profiler evaluates runtime execution across multiple packet batch sizes:
- Single-packet real-time evaluation ($B = 1$)
- Small burst buffers ($B = 10$, $B = 100$)
- High-throughput flow buffers ($B = 1,000$, $B = 10,000$)
- Complete test partition evaluation ($B = 25,674$)

For each batch configuration, the profiler executes repeated runs to record mean execution time, per-sample latency ($\mu$s), and packet processing throughput (packets/second).

---

# 10. Security & Threat Modeling

The system is designed to defend against the primary threats facing IoT edge infrastructures.

### 10.1 Threat Taxonomy and Attack Vectors
1. **Volumetric Denial of Service (UDP Floods):** Mirai UDP and BASHLITE UDP floods exhaust network bandwidth by transmitting randomized high-rate datagrams. The system detects these attacks via high packet rates (`MI_dir_L0.01_weight`) and low socket-level weights (`HpHp_L1_weight`).
2. **State Table Exhaustion (SYN/ACK Floods):** Mirai SYN and ACK attacks flood target servers with half-open TCP connections, exhausting OS transmission control blocks. The system identifies these attacks through asymmetric host-to-host packet counts and abnormal packet size means (`H_L0.01_mean`).
3. **Automated Reconnaissance (IP and Port Scanning):** Infected bots scan IP ranges to locate vulnerable devices. The system flags this behavior through elevated connection variances and host-to-host jitter metrics.
4. **Telnet / SSH Brute-Force Probing (`gafgyt_combo`):** Multi-stage automated credential attacks exhibit periodic request bursts captured by short-window statistical weights.

---

# 11. Data Flow Architecture

The data flow architecture is structured hierarchically across three standard Data Flow Diagram (DFD) levels.

### 11.1 Level 0 Context Diagram
The Level 0 context diagram models the boundary between the external environment and the intrusion detection system:
- **Inputs:** Raw packet telemetry from IoT edge appliances.
- **System:** Group 1 Decision Tree Intrusion Detection Engine.
- **Outputs:** Real-time threat alerts, packet filtering actions (forward/drop), and SIEM forensic logs.

### 11.2 Level 1 Data Flow Diagram (Subsystem Level)
The Level 1 DFD decomposes the system into its primary processes:
1. Process 1.0: Ingestion & Systematic Sampling
2. Process 2.0: Hygiene Verification & Stratified Splitting
3. Process 3.0: Cost-Complexity Pruning & Optimization
4. Process 4.0: Retraining & Model Persistence
5. Process 5.0: Edge Inference & Real-Time Traffic Classification

### 11.3 Level 2 Component Flow Diagram
The Level 2 diagram specifies internal data transformations within Process 3.0 (Pruning Engine):
- Step 3.1: Internal 80/20 train/validation partitioning
- Step 3.2: Extraction of effective alpha pruning sequence
- Step 3.3: Systematic validation scoring
- Step 3.4: Selection of optimal regularization parameter $\alpha^*$

---

# 12. Component Interface Specifications

All subsystems communicate through strictly typed, standardized data interfaces:

```text
+-----------------------------------+-----------------------------------+
| Interface ID                      | Specification                     |
+-----------------------------------+-----------------------------------+
| IF-INGEST-01                      | Output: pandas.DataFrame          |
|                                   | Schema: 128,366 rows x 117 cols   |
|                                   | (115 features + device_id + class)|
+-----------------------------------+-----------------------------------+
| IF-PREPROC-02                     | Output: numpy.ndarray             |
|                                   | Matrices: X_train (102,692 x 115)  |
|                                   |           y_train (102,692,)      |
|                                   |           X_test  (25,674 x 115)   |
|                                   |           y_test  (25,674,)       |
|                                   | Dtype: float64 / int64            |
+-----------------------------------+-----------------------------------+
| IF-PRUNE-03                       | Output: Python dict (JSON format) |
|                                   | Keys: selected_ccp_alpha,         |
|                                   |       val_macro_f1, val_acc,      |
|                                   |       tree_depth, leaf_count      |
+-----------------------------------+-----------------------------------+
| IF-MODEL-04                       | Output: joblib serialized binary  |
|                                   | Payload: Trained DecisionTree     |
|                                   | Target: results/models/model.pkl  |
|                                   | Size: 5.44 KB                     |
+-----------------------------------+-----------------------------------+
| IF-INFER-05                       | Input: X_packet (B x 115)         |
|                                   | Output: Tuple(y_multi, y_binary,  |
|                                   |              latency_ms)          |
+-----------------------------------+-----------------------------------+
```

---

# 13. Storage and Artifact Directory Schema

The project structure maintains clean separation between source code, raw data, processed models, and academic reports:

```text
/Users/swapnil/Documents/cns/group1_decision_tree/
├── archive/                     # READ-ONLY raw N-BaIoT dataset (7M rows, 89 CSVs)
├── src/                         # Production Python Pipeline Scripts
│   ├── 01_inspect_dataset.py    # Raw dataset audit & sampling verification
│   ├── 02_preprocess.py         # Systematic sampling, hygiene, train/test split
│   ├── 03_baseline_decision_tree.py # Unpruned tree induction & baseline metrics
│   ├── 04_ccp_alpha_tuning.py   # Pruning path extraction & validation tuning
│   ├── 05_final_model_evaluation.py # Final model fitting & test set evaluation
│   ├── 06_decision_path_analysis.py # Feature importance & tree path extraction
│   ├── 07_computational_benchmarks.py # Hardware latency & throughput profiling
│   ├── 08_final_consistency_audit.py # Pipeline verification & metric consistency
│   ├── 09_generate_submission_pdf.py # Academic PDF report compilation
│   └── 10_generate_design_diagrams.py # Architectural diagram generation
├── results/
│   ├── tables/                  # Verified CSV & JSON benchmark metrics
│   ├── figures/                 # High-resolution PNG architectural figures
│   └── models/                  # Serialized trained decision tree models
└── report/                      # Comprehensive academic documentation
```

---

# 14. Hyperparameter Optimization Pipeline

The hyperparameter optimization engine implements an automated grid search over the cost-complexity pruning path:

1. **Isolation of Internal Validation Partition:** 20% of the training partition (20,539 packets) is held out exclusively for validation.
2. **Path Discovery:** The pruning path discovers 60 critical alpha thresholds.
3. **Candidate Subsampling:** 20 representative alpha candidates spanning 6 orders of magnitude ($0.0$ to $0.12135$) are evaluated.
4. **Optimal Selection:** Candidate 2 with **$\alpha^* = 1.999753 \times 10^{-5}$** is selected based on maximum validation Macro F1 (99.7696%) and leaf reduction (74 to 65).

---

# 15. Verification, Validation & Integrity Framework

To ensure publication-grade integrity, the pipeline executes automated verification checks:
- **Zero Test Leakage Audit:** Confirms that neither test features nor test labels were exposed to the pruning path discovery or candidate selection routines.
- **Reproducibility Verification:** All stochastic operations utilize fixed seeds (`random_state=42`).
- **Matrix Dimension Verification:** Strict matrix dimension assertions verify that feature counts and record totals match across training and testing partitions.

---

# 16. Deployment Architecture for Edge Gateways

The system is designed for deployment on residential routers and commercial IoT edge gateways:

```text
+--------------------------------------------------------------------------+
|                  IoT Gateway Appliance (e.g., OpenWrt / Linux)           |
|                                                                          |
|  +--------------------+      +--------------------+      +-------------+ |
|  | Network Interface  | ---> |  Kitsune Feature   | ---> | Group 1     | |
|  | Card (Promiscuous) |      |  Extractor (FPGA/C)|      | CART Model  | |
|  +--------------------+      +--------------------+      +-------------+ |
|                                                                 |        |
|                                                                 v        |
|  +--------------------+      +--------------------+      +-------------+ |
|  | Linux iptables /   | <--- | Real-Time Decision | <--- | Fast Tree   | |
|  | Netfilter Engine   |      | (Forward or Drop)  |      | Walk (34 us)| |
|  +--------------------+      +--------------------+      +-------------+ |
+--------------------------------------------------------------------------+
```

Because the compiled model occupies only **5.44 KB** and evaluates in **34.41 $\mu$s**, it can be embedded directly into kernel netfilter modules or run as a lightweight user-space daemon without saturating gateway CPU resources.

---

# 17. Operational Constraints & Assumptions

1. **Upstream Feature Availability:** The model assumes network packets are converted into 115-dimensional statistical vectors by an upstream packet extractor.
2. **Fixed Feature Taxonomy:** The 115 features must match the exact damped sliding-window statistical schema defined by the N-BaIoT corpus.
3. **RAM Ceiling:** Designed to operate on devices with as little as 128 MB of system RAM.
4. **Single-Threaded Execution:** The latency benchmarks reflect single-core CPU execution without multi-threaded or GPU acceleration.

---

# 18. Fault Tolerance & Edge Case Handling

1. **Zero-Variance Features:** Features with zero variance are safely handled by the tree induction algorithm; they yield zero Gini gain and are ignored.
2. **Extreme Outliers:** Because decision trees perform monotonic interval thresholding ($x_j \le \theta$), extreme numerical values do not distort split boundaries.
3. **Missing Features:** In real-time inference, missing features are imputed using training-set medians.

---

# 19. Scalability Analysis

- **Inference Scaling:** Decision tree evaluation scales logarithmically with respect to leaf count: $\mathcal{O}(\log |T|)$. Pruning reduced tree depth from 21 to 18, ensuring bounded latency even as traffic volume scales.
- **Throughput Scaling:** Vectorized batch inference processes **12.04 million packets/sec**, demonstrating capacity to handle multi-gigabit line-rate traffic on standard multi-core hardware.

---

# 20. Security Audit & Explainability Interface

The white-box structure of the CART decision tree provides complete auditability:
- **Decision Path Extraction:** The exact decision path for any classified packet can be printed as a sequence of logical predicates.
- **Firewall Rule Generation:** High-confidence malicious branches can be automatically translated into static firewall rules (`iptables`).
- **Feature Importance Audit:** Security analysts can verify which statistical features drive detection decisions.

---

# 21. Mapping to Implementation Scripts

Each architectural subsystem corresponds directly to a modular implementation script:

| Script Name | Architectural Subsystem | Key Outputs / Artifacts |
| :--- | :--- | :--- |
| `01_inspect_dataset.py` | Data Ingestion Audit | `dataset_summary.csv`, file inventory |
| `02_preprocess.py` | Preprocessing & Partitioning | `X_train.npy`, `y_train.npy`, train/test splits |
| `03_baseline_decision_tree.py` | Baseline Tree Induction | Baseline unpruned model, baseline metrics |
| `04_ccp_alpha_tuning.py` | Pruning & Optimization | Pruning path CSV, `selected_alpha.json` |
| `05_final_model_evaluation.py` | Retraining & Evaluation | `final_metrics.csv`, confusion matrix CSV |
| `06_decision_path_analysis.py` | Explainability & Audit | Feature importances, decision path rules |
| `07_computational_benchmarks.py`| Hardware Latency Profiling | Latency CSV, throughput benchmark curves |
| `08_final_consistency_audit.py` | Verification Framework | Comprehensive audit report, consistency checks |
| `10_generate_design_diagrams.py`| Visualization Subsystem | 5 High-resolution architectural diagram PNGs |

---

# 22. Architectural Flowcharts & Diagrams

The following five architectural diagrams specify the design and operational workflows of the system:

### 22.1 Overall System Architecture
![Overall System Architecture](results/figures/design_architecture.png)

### 22.2 Data Flow Diagram (DFD Level 1)
![Data Flow Diagram Level 1](results/figures/design_dfd.png)

### 22.3 Supervised CART Training Workflow
![Supervised CART Training Workflow](results/figures/design_training_workflow.png)

### 22.4 Validation & Cost-Complexity Pruning Workflow
![Validation and Pruning Workflow](results/figures/design_pruning_workflow.png)

### 22.5 Real-Time and Batch Edge Inference Workflow
![Edge Inference Workflow](results/figures/design_inference_workflow.png)

---

# 23. Architectural Summary and Conclusion

The Group 1 System demonstrates that a principled, cost-complexity pruned CART decision tree meets the demanding performance and efficiency requirements of IoT edge intrusion detection. By reducing tree depth by 14.3% and node count by 26.5%, minimal cost-complexity pruning regularizes the model against structural overfitting while preserving peak test accuracy (99.6183%) and sub-microsecond batch inference latency. The resulting architecture provides an optimal combination of predictive performance, explainability, and hardware efficiency for real-world deployment on resource-constrained IoT gateways.
