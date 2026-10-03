# IoT Botnet Attack Detection — Group 1 Decision Tree

An academic, reproducible implementation of a **CART-style Decision Tree with Cost-Complexity Pruning** for detecting IoT botnet attacks on commercial smart devices using the benchmark **N-BaIoT** dataset.

---

## 1. Methodological & Algorithmic Context

- **Assigned Algorithm:** Decision Tree (`sklearn.tree.DecisionTreeClassifier`)
- **Research Framework Reference:** *"Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees"*
- **Implementation Distinction:**
  A CART-style Decision Tree was implemented using scikit-learn's `DecisionTreeClassifier`, while the assigned research framework is based on C4.5 Decision Tree methodology. Scikit-learn implements an optimized version of the CART algorithm (Breiman et al., 1984) utilizing strictly binary splits, Gini Impurity, and Minimal Cost-Complexity Pruning ($ccp\_\alpha$). This project represents a CART-style Decision Tree implementation inspired by the assigned C4.5 IoT botnet detection research framework, rather than an exact software reproduction of Quinlan's original C4.5 codebase.
- **Core Requirement:** Hyper-tune the cost-complexity pruning parameter `ccp_alpha` to control tree complexity, evaluate overfitting mitigation, and profile computational latency across single-sample and batch operational regimes.

---

## 2. Dataset & Sampling Methodology

- **Dataset Source:** UCI Machine Learning Repository — N-BaIoT (Meidan et al., 2018).
- **Physical Dataset Path:** `/Users/swapnil/Documents/cns/archive` (Left completely unmodified).
- **Dataset Population:** 7,062,606 packet traffic instances distributed across 89 capture files covering 9 commercial IoT devices authentically infected with **Mirai** and **BASHLITE (Gafgyt)** botnets.
- **Experimental Sampling Strategy:**
  A deterministic systematic sampling strategy with a fixed row step of 55 was employed to obtain a reproducible experimental subset from the full N-BaIoT dataset while respecting the memory constraints of the experimental machine.
  - Full Dataset Population: 7,062,606 packets
  - Experimental Subset: **128,366 packets**
  - Sampling Step: 55
  - Training Set: **102,692 packets** (80.0%)
  - Test Set: **25,674 packets** (20.0%)
  - Train/Test Split: Stratified 80/20 split (`random_state=42`)
  - Representation: All 89 traffic capture files and all 9 IoT devices are fully represented. Class proportions in the sampled subset match the full 7.06M dataset distribution to within $\pm 0.01\%$.
- **Feature Space:** 115 continuous flow features extracted over 5 damped sliding windows ($\lambda \in \{5, 3, 1, 0.1, 0.01\}$) across 5 stream aggregation scopes (`MI_dir`, `H`, `HH`, `HH_jit`, `HpHp`).
- **Port and Protocol Handling:** The N-BaIoT dataset does not contain discrete categorical protocol headers (e.g., "TCP", "UDP") or raw integer port numbers (e.g., 80, 443). Instead, HpHp features represent Host+Port-to-Host+Port communication statistics and therefore capture socket-level behavior without exposing raw port numbers as independent categorical attributes.

---

## 3. Project Directory Structure
```
group1_decision_tree/
│
├── README.md                                    # Comprehensive project guide and replication instructions
├── requirements.txt                             # Exact Python dependencies
│
├── src/                                         # Executable Python pipeline scripts
│   ├── 01_inspect_dataset.py                    # Phase 1: Raw dataset inspection and metadata extraction
│   ├── 02_preprocess.py                         # Phase 4: Systematic sampling and stratified train/test split
│   ├── 03_baseline_decision_tree.py             # Phase 5: Baseline unpruned Decision Tree induction
│   ├── 04_ccp_alpha_tuning.py                   # Phase 6: Pruning path extraction and ccp_alpha hyper-tuning
│   ├── 05_final_model.py                        # Phase 7 & 8: Optimal model selection and test evaluation
│   ├── 06_tree_visualization.py                 # Phase 9, 10, 11: Tree diagrams, feature ranking, decision paths
│   └── 07_computational_analysis.py             # Phase 12: Hardware profiling, multi-batch latency benchmarking
│
├── data/                                        # Preprocessed artifacts & documentation
│   ├── README.md                                # Reference to raw dataset path and licensing
│   └── preprocessed_data.joblib                 # Serialized preprocessed dataset bundle (128,366 samples, 115 features)
│
├── results/                                     # Output tables, publication figures, and serialized models
│   ├── tables/
│   │   ├── dataset_files_inspection.csv         # Physical file size and metadata mapping for 89 files
│   │   ├── dataset_class_distribution_all.csv   # Class distribution across 7.06M instances
│   │   ├── sampling_distribution_audit.csv      # Audit table comparing full dataset vs. sample vs. splits
│   │   ├── baseline_metrics.csv                 # Baseline unpruned model metrics
│   │   ├── ccp_alpha_results.csv                # Complete grid of 20 tested ccp_alpha configurations
│   │   ├── final_metrics.csv                    # Final pruned model metrics
│   │   ├── classification_report.csv            # Per-class precision, recall, and F1 on test set
│   │   ├── baseline_vs_pruned_comparison.csv    # Side-by-side performance and complexity comparison
│   │   ├── feature_importance.csv               # Ranked 115 features with stream scope analysis
│   │   ├── batch_inference_latency.csv          # Single-packet vs batch latency and throughput
│   │   ├── hardware_environment.csv             # Host hardware, CPU, RAM, and OS specifications
│   │   └── decision_tree_structure.txt          # Complete ASCII text representation of final tree
│   │
│   ├── figures/
│   │   ├── class_distribution.png               # Stratified class balance across train/test splits
│   │   ├── ccp_alpha_vs_f1.png                  # Macro and Weighted F1-Score vs ccp_alpha
│   │   ├── ccp_alpha_vs_accuracy.png            # Train vs Test Accuracy showing overfitting reduction
│   │   ├── ccp_alpha_vs_tree_depth.png          # Tree depth reduction curve
│   │   ├── ccp_alpha_vs_leaves.png              # Terminal leaf count (|T|) reduction curve
│   │   ├── ccp_alpha_vs_computational_time.png  # Training time and latency vs ccp_alpha
│   │   ├── feature_importance.png               # Top 15 features bar plot with socket HpHp highlighted
│   │   ├── confusion_matrix.png                 # Normalized 11-class confusion matrix heatmap
│   │   ├── batch_latency_throughput.png         # Multi-batch latency and throughput log-scale plot
│   │   ├── decision_tree_complete.png           # Complete structural tree diagram (via sklearn plot_tree)
│   │   └── decision_tree_readable.png           # Readable upper 3-level decision tree diagram
│   │
│   └── models/
│       ├── baseline_decision_tree.joblib        # Serialized unpruned baseline model (6.16 KB)
│       └── final_decision_tree.joblib           # Serialized optimal pruned model (5.44 KB)
│
├── CNS_Group1_Decision_Tree_Submission_Report.pdf # Publication-ready 10-page Submission Report PDF
│
└── report/                                      # Academic report deliverables
    ├── section_3_2_decision_tree.md             # Section 3.2 Methodology, formulation, and tuning report
    ├── section_5_2_computational_analysis.md    # Section 5.2 Computational overhead and hardware profiling
    ├── decision_path_analysis.md                # Decision paths traced for benign vs botnet packets
    ├── literature_review_group1.md              # Scopus-relevant research review on Decision Trees
    └── final_audit_report.md                    # Comprehensive audit, verification, and QC report
```

---

## 4. Dependencies & Execution Instructions

### Dependencies:
```bash
cd /Users/swapnil/Documents/cns/group1_decision_tree
pip install -r requirements.txt
```
Tested on Python 3.13 on Apple Silicon macOS (`arm64`).

### Execution:
Execute each pipeline stage sequentially:
```bash
python3 src/01_inspect_dataset.py
python3 src/02_preprocess.py
python3 src/03_baseline_decision_tree.py
python3 src/04_ccp_alpha_tuning.py
python3 src/05_final_model.py
python3 src/06_tree_visualization.py
python3 src/07_computational_analysis.py
python3 src/08_final_consistency_audit.py
python3 src/09_generate_submission_pdf.py
```

*Visualization Note:* The system did not have the standalone Graphviz `dot` executable available; therefore the visualization was generated using scikit-learn's native tree plotting functionality (`plot_tree`) alongside complete DOT and textual tree exports.

---

## 5. Verified Empirical Results

All reported values originate directly from execution on the test partition (25,674 packets):

| Metric | Baseline (Unpruned, $\alpha = 0.0$) | Final Pruned Model ($\alpha = 1.9998 \times 10^{-5}$) | Delta / Impact |
| :--- | :---: | :---: | :---: |
| **Pruning Parameter ($ccp\_\alpha$)** | $0.0$ | **$1.9998 \times 10^{-5}$** | Validation-selected optimal trade-off point |
| **Maximum Tree Depth** | 21 levels | **18 levels** | **-3 levels (-14.3%)** |
| **Total Tree Nodes** | 181 nodes | **133 nodes** | **-48 nodes (-26.5%)** |
| **Terminal Leaves ($|T|$)** | 91 leaves | **67 leaves** | **-24 leaves (-26.4%)** |
| **Multiclass Test Accuracy** | 99.6144% | **99.6183%** | **+0.0039% (Maintained / slight gain)** |
| **Multiclass Macro F1-Score** | 99.6487% | **99.6510%** | **+0.0023% (Maintained / slight gain)** |
| **Binary Detection Accuracy** | 99.9649% | **99.9649%** | Identical |
| **Binary Detection F1-Score** | 99.9810% | **99.9810%** | Identical |
| **Generalization Gap (Train - Test Acc)** | 0.1022% | **0.0769%** | **-0.0253% (Overfitting reduced)** |
| **Single-Sample Inference Latency ($N=1$)** | 39.74 $\mu$s | **34.41 $\mu$s** | +13.4% speedup (29,062 pkts/s) |
| **Batch Amortized Latency (Batch 25k)** | 0.089 $\mu$s | **0.083 $\mu$s** | Pure C-tree traversal speed |
| **Batch Inference Throughput** | 11.18M pkts/s | **12.04M pkts/s** | High throughput buffered inspection |
| **Serialized Model File Size** | 6.16 KB | **5.44 KB** | Microcontroller flash compatible (-11.7%) |

*Latency Note:* Batch throughput and amortized per-sample latency should not be interpreted as equivalent to single-packet online latency.
