# Group 1 Decision Tree: Final Academic Master Audit & Quality Control Certification

This document presents the complete final master audit, verification, and quality control report for the **Group 1 (Decision Tree)** IoT botnet attack detection pipeline implemented on the **N-BaIoT** dataset at `/Users/swapnil/Documents/cns/group1_decision_tree/`.

---

## 1. Project Information

- **Project Root Directory:** `/Users/swapnil/Documents/cns/group1_decision_tree`
- **Raw Dataset Location:** `/Users/swapnil/Documents/cns/archive` (Strictly Read-Only)
- **Assigned Research Framework:** *"Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees"*
- **Actual Implementation Algorithm:** CART-style Decision Tree via `sklearn.tree.DecisionTreeClassifier`
- **Audit Date & Local Time:** September 30, 2026, 11:05 AM IST
- **Target Venue / Format:** IEEE Conference / Journal Double-Column Format
- **Submission Readiness Status:** **READY WITH MANUAL CHECKS**

---

## 2. Dataset Verification & Population Integrity

- **Raw Data Directory:** `/Users/swapnil/Documents/cns/archive`
- **Protection & Immutability Status:** **VERIFIED 100% INTACT**. All 92 CSV files retain their original January 18, 2020 filesystem modification timestamps. Zero bytes written, zero files renamed, moved, or deleted.
- **Population Audit:**
  - Total records confirmed from `data_summary.csv`: Exactly **7,062,606 rows**.
  - Traffic capture CSV files: Exactly **89 CSV files**.
  - Commercial IoT devices: Exactly **9 devices** (Danmini Doorbell, Ecobee Thermostat, Enplug Digital Signage, Philips B120N10 Baby Monitor, Provision 737 Security Camera, Provision 838 Security Camera, SimpleHome 1002 Security Camera, SimpleHome 1003 Security Camera, Samsung SNH 1011 N Webcam).
  - Classes: Exactly **11 categories** (1 Benign baseline + 10 malicious attack vectors across Mirai and BASHLITE/Gafgyt).
- **Feature Space:** Exactly **115 continuous flow features** (`features.csv`).
- **Data Integrity:** 0 null values, 0 infinite values, 0 duplicate rows detected.
- **Evidence Files:** `results/tables/dataset_summary.csv`, `results/tables/dataset_files_inspection.csv`.

---

## 3. Sampling Methodology

- **Sampling Strategy:** A deterministic systematic row-step sampling strategy with a fixed step size of 55 was executed across all 89 traffic capture files.
- **Academic Framing:** Systematic row-step sampling was adopted strictly to obtain a reproducible, representative experimental subset of **128,366 samples** while keeping active memory residency safely below 60 MB and respecting the 16.0 GB host RAM limit. It is not claimed to be a mathematically perfect or unbiased random survey, but a reproducible uniform stride across all capture files.
- **Class Representation Fidelity:** Class distributions of the 128,366-sample corpus match the full 7,062,606 population within $\pm 0.01\%$ across all 11 classes:
  - `mirai_udp`: Full 17.42% vs. Sample 17.42%
  - `gafgyt_udp`: Full 13.40% vs. Sample 13.40%
  - `gafgyt_tcp`: Full 12.17% vs. Sample 12.18%
  - `mirai_syn`: Full 10.38% vs. Sample 10.38%
  - `mirai_ack`: Full 9.12% vs. Sample 9.12%
  - `benign`: Full 7.87% vs. Sample 7.87%
  - `mirai_scan`: Full 7.62% vs. Sample 7.62%
  - `mirai_udpplain`: Full 7.41% vs. Sample 7.41%
  - `gafgyt_combo`: Full 7.29% vs. Sample 7.29%
  - `gafgyt_junk`: Full 3.71% vs. Sample 3.70%
  - `gafgyt_scan`: Full 3.61% vs. Sample 3.61%
- **Evidence File:** `results/tables/sampling_distribution_audit.csv`.

---

## 4. Leakage Audit

- **Target Leakage:** Target label columns (`label_11`, `label_bin`), category names, and attack identifiers are completely excluded from the feature matrix $X$.
- **Metadata & Identifier Leakage:** No source/destination IP strings, MAC addresses, port integers, packet timestamps, or device identifiers are present in $X$.
- **Preprocessing Contamination:** Because decision trees are strictly invariant to monotonic feature scaling, no standardization or normalization transformers were fitted across splits. Zero missing values exist, avoiding any data-dependent imputer fitting.
- **Split Disjointness:** Train and test index sets are mutually exclusive ($\text{Train} \cap \text{Test} = \emptyset$).
- **Evidence File:** `results/tables/data_leakage_audit.csv`.

---

## 5. Train / Validation / Test Methodology

- **Three-Way Separation Protocol:**
  - Experimental sample ($N=128,366$) partitioned into **80% Training ($N=102,692$)** and **20% Test ($N=25,674$)** using stratified sampling (`random_state=42`).
  - Full Training partition ($N=102,692$) internally subdivided into **80% Internal Training Subset ($N=82,153$)** and **20% Internal Validation Set ($N=20,539$)**.
- **Isolation of Test Set:** The 25,674-sample test set was strictly held out and never inspected during pruning path extraction, candidate alpha selection, or threshold tuning. It was evaluated **exactly once** on the retrained final model.

---

## 6. Baseline Model Performance

- **Configuration:** Unpruned `DecisionTreeClassifier(criterion='gini', ccp_alpha=0.0, random_state=42)`.
- **Structural Complexity:** Maximum depth = **21 levels**, Total nodes = **181 nodes**, Terminal leaves = **91 leaves**.
- **Predictive Performance ($N=25,674$):**
  - Multiclass Test Accuracy: **99.6144%**
  - Multiclass Macro F1-Score: **99.6487%**
  - Weighted F1-Score: **99.6143%**
  - Binary Detection Accuracy: **99.9649%**
  - Binary Detection F1-Score: **99.9810%**
  - Train-Test Generalization Gap: **0.1022%** ($99.7166\% - 99.6144\%$)
- **Evidence File:** `results/tables/baseline_metrics.csv`.

---

## 7. Cost-Complexity Pruning ($ccp\_\alpha$) Methodology

- **Pruning Path Computation:** Derived using `cost_complexity_pruning_path(X_train_sub, y_train_sub)` on the 82,153-sample internal training subset in 3.99 seconds. Exactly 60 unique effective alpha thresholds were computed.
- **Validation Evaluation:** 20 representative candidate thresholds spanning $[0.0, 0.12135]$ were trained on the internal training subset and evaluated strictly on the internal validation set ($N=20,539$).
- **Selection Rule:** Primary: Validation Macro F1; Secondary: Validation Accuracy; Tie-breaker: Minimal Leaves.
- **Selected Parameter:** **$\alpha = 1.999753 \times 10^{-5} \approx 1.9998 \times 10^{-5}$** (Candidate ID 2).
  - Validation Macro F1: **99.7696%** (peak validation score)
  - Validation Accuracy: **99.7127%**
  - Validation Subtree Leaves: 65
- **Evidence Files:** `results/tables/ccp_pruning_path_raw.csv`, `results/tables/ccp_alpha_results.csv`, `results/tables/selected_alpha.json`.

---

## 8. Final Model Retraining & Evaluation Protocol

- **Retraining:** The final decision tree was retrained on the **full 102,692-sample training set** with the validation-selected parameter $\alpha = 1.999753 \times 10^{-5}$ in 5.8524 s.
- **Evaluation:** Evaluated exactly once on the held-out test partition ($N=25,674$).
- **Final Model File:** Saved to `results/models/final_decision_tree.joblib` (5.44 KB).

---

## 9. Final Verified Metrics

All values are generated programmatically and saved in `results/tables/final_metrics.csv`:

- **Multiclass Test Accuracy:** **99.6183%**
- **Multiclass Macro F1-Score:** **99.6510%**
- **Multiclass Weighted F1-Score:** **99.6182%**
- **Multiclass Macro Precision:** **99.6611%**
- **Multiclass Macro Recall:** **99.6455%**
- **Binary Detection Accuracy:** **99.9649%**
- **Binary Detection Precision:** **99.9746%**
- **Binary Detection Recall:** **99.9873%**
- **Binary Detection F1-Score:** **99.9810%**
- **Generalization Gap:** **0.0769%** (down from 0.1022%, a 24.8% reduction in overfitting)

---

## 10. Complexity & Overhead Comparison

| Architecture Metric | Baseline Model ($\alpha = 0.0$) | Final Pruned Model ($\alpha = 1.9998 \times 10^{-5}$) | Delta / Impact |
| :--- | :---: | :---: | :---: |
| **Pruning Parameter ($ccp\_\alpha$)** | $0.0$ | **$1.999753 \times 10^{-5}$** | Optimal validation threshold |
| **Maximum Tree Depth** | 21 levels | **18 levels** | **-3 levels (-14.3%)** |
| **Total Node Count** | 181 nodes | **133 nodes** | **-48 nodes (-26.5%)** |
| **Terminal Leaves ($|T|$)** | 91 leaves | **67 leaves** | **-24 leaves (-26.4%)** |
| **Multiclass Test Accuracy** | 99.6144% | **99.6183%** | **+0.0039% (Maintained / slight gain)** |
| **Multiclass Macro F1-Score** | 99.6487% | **99.6510%** | **+0.0023% (Maintained / slight gain)** |
| **Generalization Overfitting Gap**| 0.1022% | **0.0769%** | **-0.0253% (Overfitting reduced)** |
| **Serialized Model Size** | 6.16 KB | **5.44 KB** | Microcontroller flash compatible (-11.7%) |

- **Evidence File:** `results/tables/baseline_vs_pruned_comparison.csv`.

---

## 11. Feature Importance Analysis

- **Verification:** Feature importances extracted directly from `final_decision_tree.feature_importances_`.
  - Feature count: Exactly 115 features.
  - Sum of importances: Exactly 1.0000.
- **Top 5 Predictive Features (Gini Impurity Reduction):**
  1. `H_L0.01_mean` ($0.181074$): Mean packet size of outbound traffic from host over 100ms decay window.
  2. `MI_dir_L0.01_mean` ($0.172377$): Direct source IP flow mean packet size over 100ms window.
  3. `HH_jit_L1_mean` ($0.170079$): Mean packet jitter between communicating hosts over 1s window.
  4. `MI_dir_L0.01_weight` ($0.136502$): Packet arrival frequency/weight from source IP over 100ms window.
  5. `MI_dir_L0.1_weight` ($0.086472$): Packet arrival weight from source IP over 10ms window.
- **Evidence Files:** `results/tables/feature_importance.csv`, `results/figures/feature_importance.png`.

---

## 12. Latency & Computational Overhead Benchmark

- **Single-Sample Inference Latency ($N=1$):** **$34.41\ \mu\text{s}$ per packet** ($29,062\ \text{packets/s}$) for pruned model vs. $39.74\ \mu\text{s}$ ($25,162\ \text{packets/s}$) for unpruned model (+13.4% latency speedup). Dominated by Python interpreter call overhead and NumPy array type validation.
- **Batch Amortized Latency ($N=25,674$):** **$0.083\ \mu\text{s}$ per sample** (**$12,036,209\ \text{packets/s}$**). Reflects amortized pure C-tree traversal speed in bulk memory buffer mode.
- **Academic Caution:** Batch throughput must **not** be presented as real-world single-packet sequential online inspection latency. Sequential processing incurs per-packet operating system and API overhead.
- **Evidence Files:** `results/tables/batch_inference_latency.csv`, `results/figures/batch_latency_throughput.png`.

---

## 13. Hardware & Software Environment

- **Operating System:** Darwin 27.0.0 (macOS, Darwin Kernel 27.0.0: Tue Aug 11 2026)
- **Hardware Architecture:** `arm64` (Apple Silicon)
- **CPU Cores:** 10 Physical / 10 Logical Cores
- **System Memory:** 16.0 GB Total RAM (4.90 GB available during test execution)
- **Software Stack:** Python 3.13.9, scikit-learn 1.7.2, NumPy 2.3.5, Pandas 2.3.3, Matplotlib 3.10.8, Seaborn 0.13.2, Joblib 1.5.3
- **Evidence File:** `results/tables/hardware_environment.csv`.

---

## 14. CART vs. C4.5 Methodological Distinction

- **Assigned Framework:** Quinlan's C4.5 Decision Tree algorithm (multiway categorical splits, Gain Ratio criterion, pessimistic subtree error pruning).
- **Experimental Implementation:** Breiman's CART algorithm via `sklearn.tree.DecisionTreeClassifier` (strictly binary recursive splitting, Gini Impurity, minimal cost-complexity pruning with parameter $ccp\_\alpha$).
- **Academic Justification:** On continuous numerical feature spaces like N-BaIoT, CART's binary threshold evaluations $\mathbb{I}(X_j \le \theta)$ provide functionally equivalent non-linear partition boundaries to C4.5's continuous splits, while $ccp\_\alpha$ provides a mathematically formalized complexity regularization framework.

---

## 15. Port and Socket-Level Behavioral Analysis

- **Dataset Reality:** N-BaIoT contains 115 continuous sliding-window statistical features. It does **not** contain discrete integer port fields (e.g., port 80, 443) or categorical protocol flags.
- **Socket Stream Representation:** Transport dynamics are captured statistically via `HpHp_*` (Host+Port-to-Host+Port) sliding-window aggregates.
- **Key Finding:** Feature `HpHp_L1_weight` ranks #8 overall with Gini importance of $0.056838$ (5.68%). It represents the socket packet count weight at decay factor $\lambda=1$. In the decision tree, Node 107 utilizes `HpHp_L1_weight` to distinguish structured Mirai UDP floods from randomized-port Mirai UDP-plain attacks.

---

## 16. Reproducibility & Pipeline Workflow

The complete experimental workflow is packaged into 8 standalone, sequentially executable Python scripts in `src/`:
1. `01_inspect_dataset.py`: Inspects 89 files, verifies 7,062,606 rows and 115 features.
2. `02_preprocess.py`: Performs systematic step-55 sampling and stratified splitting.
3. `03_baseline_decision_tree.py`: Fits and evaluates baseline unpruned tree.
4. `04_ccp_alpha_tuning.py`: 3-way validation-isolated cost-complexity pruning sweep.
5. `05_final_model.py`: Retrains final model on full train set; single test evaluation.
6. `06_tree_visualization.py`: Renders tree diagrams, exports DOT/text, and traces decision paths.
7. `07_computational_analysis.py`: Benchmarks multi-batch latency, throughput, and training overhead.
8. `08_final_consistency_audit.py`: Automated quality control and consistency audit.

---

## 17. Artifact & File System Manifest

- **Scripts:** `src/01_inspect_dataset.py` through `src/08_final_consistency_audit.py`
- **Reports:**
  - `report/section_3_2_decision_tree.md`
  - `report/section_5_2_computational_analysis.md`
  - `report/literature_review_group1.md`
  - `report/decision_path_analysis.md`
  - `report/final_audit_report.md`
- **Tables (`results/tables/`):** 19 verified CSV/JSON tables covering data summary, leakage audit, metrics, pruning path, latency, and hardware specs.
- **Models (`results/models/`):** `baseline_decision_tree.joblib` (6.16 KB), `final_decision_tree.joblib` (5.44 KB).
- **Figures (`results/figures/`):** 11 high-resolution figures covering class distribution, 5 pruning tradeoff curves, feature importance, confusion matrix, complete tree structure, readable tree structure, and multi-batch latency.

---

## 18. Automated Consistency Audit Result

The automated quality control script `src/08_final_consistency_audit.py` was executed:

```
================================================================================
GROUP 1 DECISION TREE: AUTOMATED FINAL CONSISTENCY AUDIT
================================================================================
[Check 1/7] Verifying file system manifest...
  -> File system manifest: PASS (all required deliverables exist)
[Check 2/7] Verifying preprocessed dataset integrity...
  -> Dataset integrity: PASS (115 features, 11 classes, 128,366 samples, 0 nulls, 0 leakage)
[Check 3/7] Verifying models and tabular metrics consistency...
  -> Model & tabular consistency: PASS (Alpha=1.999753e-05, Nodes=133, Leaves=67, Depth=18)
[Check 4/7] Verifying feature importance table...
  -> Feature importance: PASS (115 features ranked, sum=1.0000, top='H_L0.01_mean')
[Check 5/7] Scanning active codebase for obsolete/stale references...
  -> Obsolete token scan: PASS (Zero stale alpha references in active files)
[Check 6/7] Verifying raw dataset directory isolation...
  -> Raw dataset isolation: PASS (Archive intact with 92 CSV files)
[Check 7/7] Verifying report and README numerical consistency...
  -> Report consistency: PASS (README and reports match verified model metrics)
================================================================================
FINAL AUDIT: PASS
All consistency, integrity, and methodological checks passed successfully.
================================================================================
```

---

## 19. Remaining Manual Tasks (Action Items for User)

The project status is certified as **READY WITH MANUAL CHECKS**. Three manual external actions must be executed prior to final submission:

1. **Institutional Scopus Verification:** Confirm indexed status of Shafiq et al. (2021) and Moubayed et al. (2020) via institutional library portal before submission.
2. **Peer Group Integration:** When Groups 2–5 complete their evaluations, populate the comparative benchmarks in `results/tables/comparative_algorithms_benchmark_template.csv` and Table II in Section 5.2.
3. **Overleaf / LaTeX Ingestion:** Copy Markdown sections from `report/section_3_2_decision_tree.md` and `report/section_5_2_computational_analysis.md` into the group paper LaTeX template.
