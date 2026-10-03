# IoT Botnet Detection Using Cost-Complexity Pruned CART Decision Trees

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Accuracy](https://img.shields.io/badge/Accuracy-99.62%25-brightgreen.svg)]()
[![Macro F1](https://img.shields.io/badge/Macro%20F1-99.65%25-brightgreen.svg)]()
[![Model Size](https://img.shields.io/badge/Model%20Size-5.44%20KB-orange.svg)]()

> **Course:** Cryptography and Network Security (CNS A.Y. 2026–2027)  
> **Institution:** Bhartiya Vidya Bhavan's Sardar Patel Institute of Technology (SPIT), Mumbai  
> **Group:** Group 1 — Decision Tree  
> **Assigned Research Framework:** *Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees*  
> **Implemented Algorithm:** Minimal Cost-Complexity Pruned CART (`sklearn.tree.DecisionTreeClassifier`)  
> **Benchmark Dataset:** N-BaIoT Telemetry Dataset (UCI Machine Learning Repository #442)  

---

## ⚡ Quick Start (1-Click Replication)

You can replicate the entire training, pruning evaluation, and generate test metrics in under **6 seconds**:

```bash
# 1. Clone the repository
git clone https://github.com/swapnil-exxe/CNS-Group1-DecisionTree.git
cd CNS-Group1-DecisionTree

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the standalone replication script
python3 model_script.py
```

**Expected Console Output:**
```text
===========================================================================
SARDAR PATEL INSTITUTE OF TECHNOLOGY | CNS COLLABORATIVE R&D
GROUP 1 — DECISION TREE: OPTIMIZED BENCHMARK PIPELINE
===========================================================================
[+] Successfully loaded preprocessed dataset from: data/preprocessed_data.joblib
[+] Ingestion Summary: Train=102692 | Test=25674 | Features=115 | Classes=11

--- Evaluating Baseline Decision Tree (ccp_alpha=0.0) ---
  Baseline Depth  : 21 levels
  Baseline Nodes  : 181 nodes
  Baseline Leaves : 91 leaves
  Baseline Test Acc: 99.6144% | Macro F1: 99.6487%

--- Evaluating Final Pruned Decision Tree (ccp_alpha=1.999753e-05) ---

 --- TOURNAMENT BENCHMARK RESULTS --- 
Accuracy                      : 99.618291%
Precision                     : 99.661076%
Recall                        : 99.645542%
F1-Score                      : 99.650961%
ROC-AUC                       : 0.999410
Training Time (s)             : 5.85 s
Inference Latency (ms/sample) : 0.000095 ms

Final Pruned Structural Impact:
  - Tree Depth    : 18 levels (-14.3%)
  - Total Nodes   : 133 nodes (-26.5%)
  - Terminal Leaves: 67 leaves (-26.4%)
[+] High-resolution confusion matrix saved to: confusion_matrix.png
[+] Tournament metrics exported to results.csv successfully.
===========================================================================
```

---

## 📌 Project Overview

This project implements an ultra-lightweight, high-throughput network intrusion detection system (NIDS) designed specifically for resource-constrained Internet of Things (IoT) edge appliances (routers, IP cameras, doorbells, smart hubs).

By applying **Minimal Cost-Complexity Pruning (MCCP)** to a CART Decision Tree:
1. **Tree depth decreases from 21 to 18 levels** (-14.3%).
2. **Total node count drops from 181 to 133 nodes** (-26.5%).
3. **Model memory footprint shrinks to just 5.44 KB** (easily fitting in microcontroller SRAM/Flash).
4. **Generalization error gap drops from 0.1022% to 0.0769%** without sacrificing detection accuracy (99.62%).

---

## 🧠 How the Project Works (End-to-End System Flow)

The system transforms raw, high-velocity network packet streams into real-time threat classifications through a 5-stage pipeline:

```
[ Raw Network Traffic ] ───► [ 115-D Feature Extraction ] ───► [ Stratified Sampling ]
  89 CSV files (7.06M)        Kitsune Damped Windows            Stride S=55 (128,366)
                                                                        │
                                                                        ▼
[ Deployment / Detection ] ◄── [ Cost-Complexity Pruning ] ◄─── [ CART Induction ]
  34.41 µs / packet             Optimal Alpha: 1.999753e-5       Binary Gini Splits
  5.44 KB flash footprint       Depth: 18 | Leaves: 67           Depth: 21 | Leaves: 91
```

### Stage 1: Continuous Behavioral Feature Extraction
Raw network packets are summarized using Kitsune-style damped incremental statistics. For every arriving packet, statistics are updated across **5 sliding time windows** with decay factors $\lambda \in \{5, 3, 1, 0.1, 0.01\}$ over **5 aggregation scopes**:
- `MI_dir`: Packet volume and directionality from the source MAC and IP.
- `H`: Host traffic dynamics from the source IP address.
- `HH`: Interactive dynamics between a source-destination host pair.
- `HH_jit`: Inter-arrival packet jitter between a host pair (critical for detecting botnet heartbeat loops).
- `HpHp`: Host+Port-to-Host+Port socket-level interaction statistics.
This yields **115 continuous features** capturing rate, variance, and covariance without needing plaintext payload inspection.

### Stage 2: Systematic Deterministic Sampling
The raw N-BaIoT population comprises **7,062,606 packet records** across 89 files. To achieve complete reproducibility and respect memory constraints without introducing random sampling bias, a **systematic sampling row stride of $S = 55$** is applied. This extracts exactly **128,366 samples** while preserving true device and class proportions to within $\pm 0.01\%$.

### Stage 3: Strict 3-Way Data Partitioning (Zero Leakage)
To ensure complete mathematical integrity and prevent data snooping:
- **Test Set ($N = 25,674$, 20%):** Kept strictly isolated in a vault until the final audit.
- **Train Set ($N = 102,692$, 80%):** Subdivided into:
  - *Internal Sub-train ($N = 82,153$, 80% of Train)*: Used to grow candidate trees.
  - *Internal Validation ($N = 20,539$, 20% of Train)*: Used exclusively to score candidate pruning parameters ($\alpha$).

### Stage 4: Minimal Cost-Complexity Pruning (MCCP)
An unconstrained tree overfits on continuous IoT telemetry noise (growing to depth 21 with 181 nodes). Minimal Cost-Complexity Pruning minimizes the regularized cost objective:
$$R_\alpha(T) = R(T) + \alpha |T|$$
Where $R(T)$ is the total leaf impurity, $|T|$ is the number of terminal leaves, and $\alpha \ge 0$ is the complexity penalty parameter.
- The cost-complexity pruning path generates candidate $\alpha$ thresholds.
- Each candidate is evaluated solely on the **internal validation set**.
- The optimal parameter **$\alpha^* = 1.9997530739682578 \times 10^{-5}$** is selected because it maximizes validation Macro F1 ($99.7696\%$) while eliminating 48 redundant nodes.

### Stage 5: Final Model Retraining & Deployment Evaluation
With $\alpha^*$ frozen, the tree is retrained on the entire 102,692 training samples and evaluated once on the untouched held-out 25,674 test samples.

---

## 🔍 How Each File Works in Particular

Here is an exact, detailed breakdown of every file in the repository:

### 1. Root Execution Files

#### `model_script.py` (Standalone Master Script)
- **Purpose:** A self-contained, 1-click Python script that anyone can execute to train, prune, and test the model in seconds.
- **How it works:**
  1. *Loads Data:* Automatically locates and unpacks `data/preprocessed_data.joblib` containing $X_{train}, X_{test}, y_{train}, y_{test}$.
  2. *Trains Baseline:* Builds an unpruned `DecisionTreeClassifier(random_state=42, ccp_alpha=0.0)` and logs depth (21) and nodes (181).
  3. *Applies Optimal Pruning:* Builds the optimized tree with `ccp_alpha=1.9997530739682578e-05`, reducing depth to 18 and nodes to 133.
  4. *Evaluates Performance:* Predicts test samples, computes Multiclass Accuracy (99.62%), Precision, Recall, Macro F1, and multiclass ROC-AUC (0.9994).
  5. *Exports Deliverables:* Generates `confusion_matrix.png` and writes tournament benchmark results to `results.csv`.

#### `requirements.txt`
- Specifies the exact, minimal Python libraries needed (`scikit-learn`, `numpy`, `pandas`, `joblib`, `matplotlib`, `seaborn`).

#### `results.csv`
- A single-line comma-separated summary containing the verified test set metrics for direct automated aggregation into collaborative tournament leaderboards.

#### `confusion_matrix.png`
- A publication-grade 11x11 normalized confusion matrix visualizing exact classification across all 11 target classes (1 benign + 10 botnet attack sub-classes).

---

### 2. The Modular Pipeline (`src/`)

For researchers wishing to inspect each phase step-by-step, the `src/` folder provides individual, sequential execution modules:

#### `src/01_inspect_dataset.py` (Raw Inspection & Audit)
- **Role:** Examines the raw dataset files before any processing occurs.
- **Internal Mechanics:**
  - Scans all 89 CSV files across the 9 IoT devices in `/archive`.
  - Calculates exact physical file sizes, row counts, and verifies header integrity across all 115 features.
  - Outputs `results/tables/dataset_files_inspection.csv` and `dataset_class_distribution_all.csv`, proving that the raw dataset contains 7,062,606 packet rows.

#### `src/02_preprocess.py` (Systematic Sampling & Stratification)
- **Role:** Extracts the representative experimental sample and partitions it without data leakage.
- **Internal Mechanics:**
  - Implements the deterministic row step $S = 55$ across all 89 files.
  - Verifies that zero NaN or infinite values exist in the 115 feature columns.
  - Stratifies samples into 80% train (102,692) and 20% test (25,674).
  - Serializes the entire verified dataset package into `data/preprocessed_data.joblib` (16 MB).
  - Generates `sampling_distribution_audit.csv` proving that every class is preserved within $\pm 0.01\%$.

#### `src/03_baseline_decision_tree.py` (Unpruned Tree Induction)
- **Role:** Fits the unconstrained baseline CART model.
- **Internal Mechanics:**
  - Trains a tree using Gini impurity with `ccp_alpha=0.0`.
  - Records maximum complexity: depth 21, 181 nodes, 91 leaves.
  - Saves the unpruned baseline model to `results/models/baseline_decision_tree.joblib` (6.16 KB).
  - Exports `results/tables/baseline_metrics.csv`.

#### `src/04_ccp_alpha_tuning.py` (Pruning Path & Grid Search)
- **Role:** Determines the mathematically optimal regularization strength ($\alpha^*$).
- **Internal Mechanics:**
  - Splits the 102,692 training samples into internal sub-train (82,153) and internal validation (20,539).
  - Extracts the exact cost-complexity pruning path using `tree.cost_complexity_pruning_path()`.
  - Evaluates candidate $\alpha$ values across tree depth, leaf count, and validation Macro F1 score.
  - Selects $\alpha^* = 1.9997530739682578 \times 10^{-5}$ as the global validation optimum ($99.7696\%$ Macro F1).
  - Exports `results/tables/ccp_alpha_results.csv`, `selected_alpha.json`, and 5 pruning trajectory plots.

#### `src/05_final_model.py` (Final Model & Test Verification)
- **Role:** Retrains on full training data and performs final held-out test evaluation.
- **Internal Mechanics:**
  - Trains the final tree on all 102,692 samples using $\alpha^*$.
  - Evaluates on the held-out test set ($N = 25,674$).
  - Computes detailed multiclass and binary metrics, per-class classification reports, and saves the final serialized model to `results/models/final_decision_tree.joblib` (5.44 KB).
  - Outputs `results/tables/final_metrics.csv`, `classification_report.csv`, and `final_confusion_matrix.csv`.

#### `src/06_tree_visualization.py` (Tree Structure & Feature Ranking)
- **Role:** Extracts human-interpretable rules and feature importances from the tree.
- **Internal Mechanics:**
  - Computes total Gini impurity reduction for all 115 features.
  - Identifies that socket-level interaction features (`HpHp_L0.1_covariance`, `HpHp_L0.01_weight`, etc.) dominate top decision splits.
  - Generates `results/tables/feature_importance.csv`, `results/tables/decision_tree_structure.dot`, and high-resolution tree visualization images.

#### `src/07_computational_analysis.py` (Latency & Hardware Profiling)
- **Role:** Measures production inference speed and resource consumption.
- **Internal Mechanics:**
  - *Single-Sample Latency:* Measures $N=1$ packet classification time across 10,000 warm iterations, recording **34.41 $\mu$s/packet** (throughput: 29,062 packets/s).
  - *Batch Latency:* Measures vectorized batch inference across all 25,674 test samples, recording **0.083 $\mu$s/packet** (throughput: 12,036,209 packets/s).
  - Profiles training time ($5.9111 \pm 0.1017$ s) and memory footprint.
  - Outputs `results/tables/batch_inference_latency.csv` and `hardware_environment.csv`.

#### `src/08_final_consistency_audit.py` (Integrity & Leakage Check)
- **Role:** Automated quality-assurance script verifying dataset integrity.
- **Internal Mechanics:**
  - Performs intersection checks between train and test row indices to ensure 100% disjoint isolation.
  - Verifies that zero feature values leaked from test into training.
  - Validates all numbers against official project reports and outputs `results/tables/data_leakage_audit.csv`.

#### `src/10_generate_design_diagrams.py` & `src/12_generate_model_comparison_plot.py`
- Generate publication-ready visual architectures, Data Flow Diagrams (DFDs), and baseline-versus-pruned comparison charts stored in `results/figures/`.

---

### 3. Data Directory (`data/`)

- `data/preprocessed_data.joblib` (16 MB):
  A compressed dictionary containing the preprocessed arrays ready for immediate machine learning:
  - `X_train`: shape `(102692, 115)`, float32 matrix of normalized continuous traffic features.
  - `X_test`: shape `(25674, 115)`, float32 matrix of test features.
  - `y_train`: shape `(102692,)`, integer class labels (0 to 10).
  - `y_test`: shape `(25674,)`, integer class labels.
  - `feature_names`: list of 115 feature header strings.
  - `class_names`: list of 11 target category strings (`benign`, `gafgyt_combo`, `gafgyt_junk`, `gafgyt_scan`, `gafgyt_tcp`, `gafgyt_udp`, `mirai_ack`, `mirai_scan`, `mirai_syn`, `mirai_udp`, `mirai_udpplain`).

---

### 4. Results Directory (`results/`)

- `results/models/`:
  - `final_decision_tree.joblib` (5.44 KB): The optimal pruned decision tree model.
  - `baseline_decision_tree.joblib` (6.16 KB): The unpruned baseline model.
  - `candidate_models.joblib`: Checkpoint trees evaluated during hyperparameter search.
- `results/tables/`:
  - 14 comprehensive CSV and JSON tables containing exact raw numerical metrics, feature importances, latency measurements, and audit logs.
- `results/figures/`:
  - 16 high-resolution PNG plots including cost-complexity curves, confusion matrices, latency vs. batch size plots, and decision tree diagrams.

---

### 5. Research & Documentation Reports (`report/`)

Contains complete, formal scientific monographs formatted in GitHub-flavored Markdown:
- `Algorithm_Document.md`: Mathematical formulation of CART, Gini Impurity, split criteria, and Minimal Cost-Complexity Pruning.
- `Design_Document.md`: Architectural specifications, Data Flow Diagrams, and IoT deployment considerations.
- `Implementation_Research_Document.md`: Theoretical comparison between the assigned C4.5 framework and CART.
- `decision_path_analysis.md`: Line-by-line inspection of decision rules and feature threshold splits that separate benign packets from botnet attacks.
- `section_5_2_computational_analysis.md`: Detailed analysis of edge hardware constraints, CPU cycles, cache locality, and Python-to-C traversal overheads.
- `final_audit_report.md`: Verification report demonstrating zero data leakage and exact numerical consistency.

---

## 📊 Summary of Experimental Results

Evaluated on the strict held-out test partition ($N = 25,674$ samples):

| Metric | Unpruned Baseline ($\alpha = 0$) | Optimal Pruned Model ($\alpha^* = 2.0 \times 10^{-5}$) | Net Change / Impact |
| :--- | :---: | :---: | :---: |
| **Pruning Parameter ($ccp\_\alpha$)** | `0.0` | **`1.999753 × 10⁻⁵`** | *Optimal validation choice* |
| **Maximum Tree Depth** | 21 levels | **18 levels** | **-3 levels (-14.3%)** |
| **Total Tree Nodes** | 181 nodes | **133 nodes** | **-48 nodes (-26.5%)** |
| **Terminal Leaves ($|T|$)** | 91 leaves | **67 leaves** | **-24 leaves (-26.4%)** |
| **Multiclass Test Accuracy** | 99.6144% | **99.6183%** | **+0.0039% (Maintained)** |
| **Multiclass Macro F1** | 99.6487% | **99.6510%** | **+0.0023% (Maintained)** |
| **Binary Detection Accuracy** | 99.9649% | **99.9649%** | Identical |
| **Binary Detection F1** | 99.9810% | **99.9810%** | Identical |
| **Generalization Gap (Train - Test)** | 0.1022% | **0.0769%** | **-24.8% (Overfitting mitigated)** |
| **Single-Packet Latency ($N=1$)** | 39.74 $\mu$s | **34.41 $\mu$s** | **+13.4% faster** (29,062 pkts/s) |
| **Batch Amortized Latency** | 0.089 $\mu$s | **0.083 $\mu$s** | Pure C-tree traversal speed |
| **Batch Throughput** | 11.18M pkts/s | **12.04M pkts/s** | +7.7% throughput improvement |
| **Model Size (Joblib serialized)** | 6.16 KB | **5.44 KB** | **-11.7%** (Embedded flash ready) |

---

## 🛠️ Step-by-Step Pipeline Execution

If you prefer to run the modular pipeline step by step:

```bash
# Step 1: Baseline model induction
python3 src/03_baseline_decision_tree.py

# Step 2: Cost-complexity alpha tuning (selects alpha* on internal validation set)
python3 src/04_ccp_alpha_tuning.py

# Step 3: Train final model & evaluate on untouched test set
python3 src/05_final_model.py

# Step 4: Generate visual decision tree diagrams and path traces
python3 src/06_tree_visualization.py

# Step 5: Benchmark single-sample and batch inference latency
python3 src/07_computational_analysis.py

# Step 6: Verify data integrity and zero leakage
python3 src/08_final_consistency_audit.py
```

---

## 💻 Hardware Environment

Benchmarks were evaluated on an **Apple Silicon (M-series, ARM64)** host workstation:
- **Processor:** Apple Silicon (8 cores, up to 3.2 GHz)
- **Memory:** 8.0 GB Unified RAM
- **Operating System:** macOS (Darwin arm64)
- **Python Version:** 3.10+
- **Primary Libraries:** `scikit-learn==1.7.dev0`, `numpy`, `pandas`, `joblib`, `matplotlib`, `seaborn`

---

## 👥 Authors & Academic Attribution

- **Contributing Student:** Swapnil Patil (`swapnil.patil24@spit.ac.in`)
- **Institution:** Sardar Patel Institute of Technology (SPIT), Autonomous Institute Affiliated with the University of Mumbai
- **Course:** Cryptography and Network Security (CNS), Academic Year 2026–2027
- **Faculty Mentor:** Prof. Renuka Pawar
