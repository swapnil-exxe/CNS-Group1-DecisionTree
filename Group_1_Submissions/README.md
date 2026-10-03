# CNS A.Y. 2026–27: Group 1 Performance Benchmark Tournament Submission
## Collaborative R&D Manifest: Comparative Algorithmic Analysis for Advanced Cybersecurity Domains

**Faculty:** Prof. Renuka Pawar  
**Institution:** Sardar Patel Institute of Technology (Autonomous Affiliated to University of Mumbai)  
**Subject:** Cryptography and Network Security (CNS)  
**Group:** Group 1 — Decision Tree  
**Assigned Research Topic:** Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees  
**Actual Implementation:** CART Decision Tree (`sklearn.tree.DecisionTreeClassifier`)  
**Regularization Strategy:** Minimal Cost-Complexity Pruning ($ccp\_\alpha = 1.999753 \times 10^{-5}$)  
**Dataset:** N-BaIoT (UCI Machine Learning Repository, 9 Commercial IoT Devices, 11 Classes)  

---

## 1. Executive Summary & Research Problem
Edge IoT devices lack defensive agent software and possess widespread firmware vulnerabilities. Attackers compromise these nodes using self-propagating worm binaries (Mirai and BASHLITE/Gafgyt families) to execute multi-vector volumetric and state-table exhaustion attacks. Traditional deep learning anomaly detectors (e.g., Deep Autoencoders) require high floating-point compute and hundreds of megabytes of RAM, rendering them unsuitable for deployment on low-cost edge gateway routers.

Group 1 evaluates a **CART-style Decision Tree** regularized via **Minimal Cost-Complexity Pruning ($ccp\_\alpha$)**. Operating over continuous flow statistics, our model delivers:
- **Multiclass Test Accuracy:** 99.6183% across 11 granular traffic categories
- **Macro F1-Score:** 99.6510%
- **Binary Botnet Detection Accuracy:** 99.9649% (F1-score: 99.9810%)
- **ROC-AUC (One-vs-Rest Macro):** 0.999410
- **Model Storage Footprint:** 5.44 KB
- **Single-Packet Latency:** 34.41 $\mu$s (real-time inline inspection)
- **Batch Processing Throughput:** 12,036,209 packets/sec (exceeding Gigabit Ethernet wire speeds by 8x)

---

## 2. Methodological Clarification: CART vs. C4.5
- **Assigned Framework:** *"Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees"* serves as the conceptual motivation.
- **Actual Implementation:** Python's `sklearn.tree.DecisionTreeClassifier` implements Breiman et al.'s **Classification and Regression Trees (CART)** algorithm.
- **Key Distinctions:**
  1. CART enforces strictly **binary splits** ($x_j \le \theta$) on continuous variables, whereas C4.5 supports multi-way nominal branching.
  2. CART uses **Gini Impurity** (eliminating logarithmic overhead during tree induction), whereas C4.5 uses Shannon Entropy and Gain Ratio.
  3. CART employs **Minimal Cost-Complexity Pruning ($ccp\_\alpha$)**, whereas C4.5 uses pessimistic error-based pruning.

---

## 3. Dataset, Preprocessing, and Sampling
- **Raw Population:** 7,062,606 packets across 89 CSV files covering 9 commercial IoT appliances.
- **Systematic Sampling:** Deterministic row step $k = 55$ yielded **128,366 packets**, preserving exact device and class proportions.
- **Feature Space:** 115 continuous stream statistics extracted across 5 damped sliding windows (decay factors $\lambda \in \{0.01, 0.1, 1, 3, 5\}$) and 4 traffic scopes: Host (H), Host-to-Host (HH), Host-to-Host Jitter (HH_jit), and Host+Port-to-Host+Port (HpHp).
- **Transport Dynamics:** Raw discrete port numbers are absent; socket behaviors are modeled through continuous `HpHp_*` aggregates (with `HpHp_L1_weight` ranking #8 in importance).
- **Data Hygiene:** 0 missing values, 0 infinite values, 100% verified continuous float64 features.

---

## 4. Strict Train / Validation / Test Methodology
To prevent test-set contamination and model-selection bias:
1. **Stratified Split (80/20):**
   - Training Partition (80%): 102,692 packets
   - Held-Out Test Partition (20%): 25,674 packets (sealed until final evaluation)
2. **Internal Train / Validation Partition (80/20 on Training Set):**
   - Internal Training Subset: 82,153 packets
   - Internal Validation Subset: 20,539 packets
3. **Pruning Path Discovery:** 60 candidate alphas discovered solely on the internal training subset.
4. **Validation Selection:** 20 representative candidates evaluated against the 20,539-sample validation set.
5. **Optimal Alpha:** Candidate 2 with **$\alpha^* = 1.9997530739682578 \times 10^{-5}$** isolated based on peak validation Macro F1 (99.7696%) and leaf reduction.
6. **Final Retraining:** Retrained on all 102,692 training samples and evaluated **exactly once** on the held-out 25,674 test samples.

---

## 5. Structural Impact of Cost-Complexity Pruning

| Structural Metric | Baseline (Unpruned, $\alpha=0$) | Final Pruned Model ($\alpha=1.9998e-5$) | Net Change |
| :--- | :---: | :---: | :---: |
| **Tree Depth** | 21 levels | **18 levels** | **-3 levels (-14.3%)** |
| **Total Node Count** | 181 nodes | **133 nodes** | **-48 nodes (-26.5%)** |
| **Terminal Leaves ($|T|$)** | 91 leaves | **67 leaves** | **-24 leaves (-26.4%)** |
| **Multiclass Test Accuracy** | 99.6144% | **99.6183%** | **+0.0039%** |
| **Multiclass Macro F1** | 99.6487% | **99.6510%** | **+0.0023%** |
| **Generalization Gap** | 0.1022% | **0.0769%** | **-24.8% Overfitting Reduction** |
| **Serialized Model Size** | 6.16 KB | **5.44 KB** | **-11.7% Storage Reduction** |

---

## 6. Standardized Tournament Leaderboard Metrics (`results.csv`)

These metrics were generated directly by calling the faculty notice's `evaluate_tournament_model()` benchmarking function on our test partition:

| Leaderboard Parameter | Measured Value | Standardized Format |
| :--- | :---: | :--- |
| **Accuracy** | **99.6183%** | Percentage (Macro) |
| **Precision** | **99.6611%** | Percentage (Macro Average) |
| **Recall** | **99.6455%** | Percentage (Macro Average) |
| **F1-Score** | **99.6510%** | Percentage (Macro Average) |
| **ROC-AUC** | **0.999410** | Probability Area (One-vs-Rest Macro) |
| **Training Time (s)** | **5.8563 s** | Single-Core Wall-Clock Seconds |
| **Inference Latency (ms/sample)** | **0.000187 ms** | Batch-Vectorized Latency per Sample |

*(Note: Single-sample unbatched real-time latency is **0.0344 ms/sample** / 34.41 $\mu$s, providing inline inspection capacity).*

---

## 7. Submission Package Inventory

```text
Group_1_Submissions/
│
├── model_script.py            # Standalone, runnable tournament script
├── confusion_matrix.png       # High-res 11x11 multiclass confusion matrix
├── feature_importance.png     # Top-10 Gini feature importance plot
├── model_comparison.png       # Baseline vs Pruned structural comparison
├── results.csv                # Standardized faculty tournament metrics
├── README.md                  # Comprehensive group technical documentation
├── technical_summary.pdf      # Concise 6-page academic summary report (PDF)
├── technical_summary.docx     # Editable Word format of technical summary
│
├── papers/
│   └── 2_research_papers.pdf  # Synthesized Scopus review of 2 IEEE IoTJ papers
│
└── report/
    ├── Section_3.2.docx       # Algorithm and CART methodology section
    └── Section_5.2.docx       # Computational and hardware latency section
```

---

## 8. Instructions for Faculty Execution

### Prerequisites
Install standard data science packages:
```bash
pip install numpy pandas scikit-learn joblib matplotlib
```

### Running the Standalone Benchmark
Execute `model_script.py` from the submission directory:
```bash
cd Group_1_Submissions
python model_script.py
```

### Expected Output
The script automatically locates `preprocessed_data.joblib`, trains the pruned CART model, generates all 7 tournament metrics via `evaluate_tournament_model()`, prints the leaderboard block, displays structural tree parameters, and writes `results.csv`.
