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

## 🔬 Methodological Framework

### 1. Assigned Theme vs Implemented CART
- **Assigned Theoretical Theme:** *C4.5 Decision Trees* (J. Ross Quinlan, 1993). Uses Information Gain Ratio and multi-way categorical splits.
- **Implemented Model:** *CART Decision Tree* (`sklearn.tree.DecisionTreeClassifier`, Breiman et al., 1984). Employs recursive binary partitioning, Gini Impurity, and Minimal Cost-Complexity Pruning.
- *Rationale:* Production data science environments standardly utilize CART. The continuous-valued statistical features (115 dimensions) of the N-BaIoT dataset are optimally partitioned via univariate binary thresholding.

### 2. Dataset & Sampling Strategy
- **Source:** N-BaIoT Telemetry Dataset (UCI Machine Learning Repository ID #442).
- **Raw Population:** 7,062,606 packets across 89 capture files covering 9 commercial IoT devices infected with **Mirai** and **BASHLITE (Gafgyt)**.
- **Systematic Sampling:** To maintain exact statistical representation within standard RAM, a systematic row stride ($S = 55$) was applied:
  - Total Sampled: **128,366 packets**
  - Train Set (80%): **102,692 packets** (Internal sub-train: 82,153 | Internal validation: 20,539)
  - Held-out Test Set (20%): **25,674 packets** (Untouched until final evaluation)

### 3. Feature Representation (115 Continuous Features)
Features are extracted using Kitsune damped incremental statistics across 5 temporal decay factors ($\lambda \in \{5, 3, 1, 0.1, 0.01\}$) over 5 network stream scopes:
1. `MI_dir`: Source IP packet traffic statistics
2. `H`: Source host network activity
3. `HH`: Source-to-Destination host pair statistics
4. `HH_jit`: Inter-arrival packet jitter for host pairs
5. `HpHp`: Host+Port-to-Host+Port socket-level interaction statistics

---

## 📂 Repository Structure

```
CNS-Group1-DecisionTree/
├── README.md                           # This documentation guide
├── requirements.txt                    # Python package dependencies
├── model_script.py                     # Standalone replication script (1-click run)
├── results.csv                         # Master benchmark metrics summary
├── confusion_matrix.png                # High-res 11x11 normalized confusion matrix
│
├── data/
│   ├── preprocessed_data.joblib        # 128,366-sample dataset matrix (16 MB)
│   └── README.md                       # Data provenance and licensing notes
│
├── src/                                # Step-by-step modular pipeline scripts
│   ├── 01_inspect_dataset.py           # Dataset metadata, distribution, and file verification
│   ├── 02_preprocess.py                # Systematic sampling and train/validation/test partitioning
│   ├── 03_baseline_decision_tree.py    # Baseline unpruned tree induction
│   ├── 04_ccp_alpha_tuning.py          # Pruning path extraction & optimal alpha grid search
│   ├── 05_final_model.py               # Retraining on full train set & held-out test evaluation
│   ├── 06_tree_visualization.py        # Visual tree diagrams and decision path exports
│   ├── 07_computational_analysis.py    # Latency, throughput, and hardware profiling benchmarks
│   ├── 08_final_consistency_audit.py   # Strict data-leakage and numerical integrity audit
│   ├── 10_generate_design_diagrams.py  # System architecture & DFD flowchart generators
│   └── 12_generate_model_comparison_plot.py # Baseline vs Pruned comparative visualizer
│
├── results/
│   ├── models/                         # Serialized models (.joblib)
│   │   ├── final_decision_tree.joblib  # Optimal pruned tree (5.44 KB)
│   │   └── baseline_decision_tree.joblib
│   ├── tables/                         # Raw CSV & JSON data files (metrics, audits, reports)
│   └── figures/                        # 16 publication figures (curves, diagrams, confusion matrix)
│
└── report/                             # In-depth Markdown monographs and technical analyses
    ├── Algorithm_Document.md           # Mathematical formulation of CART & MCCP
    ├── Design_Document.md              # System design, DFD, and pipeline architecture
    ├── Implementation_Research_Document.md # C4.5 vs CART theoretical contrast
    ├── decision_path_analysis.md       # Traced feature threshold rules for attack classification
    ├── section_5_2_computational_analysis.md # Detailed latency, throughput & hardware report
    └── final_audit_report.md           # Final numerical consistency and integrity sign-off
```

---

## 🛠️ Step-by-Step Pipeline Execution

If you prefer to run the pipeline phase by phase:

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
