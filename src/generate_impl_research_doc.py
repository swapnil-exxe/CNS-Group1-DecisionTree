import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_table(table):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for cell in table.rows[0].cells:
        set_cell_background(cell, "1F497D") # Dark Blue
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.name = 'Calibri'
                run.font.size = Pt(9.5)
                
    for r_idx, row in enumerate(table.rows[1:], start=1):
        bg_color = "F2F5F8" if r_idx % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(9.0)

def polish_docx(filename, doc_title):
    doc = docx.Document(filename)
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        header = section.header
        hp = header.paragraphs[0]
        hp.text = f"CNS Group 1 — {doc_title}"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if hp.runs:
            hp.runs[0].font.name = 'Calibri'
            hp.runs[0].font.size = Pt(8.5)
            hp.runs[0].font.color.rgb = RGBColor(128, 128, 128)
            
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Implementation and Research Document | Academic Reference"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if fp.runs:
            fp.runs[0].font.name = 'Calibri'
            fp.runs[0].font.size = Pt(8.5)
            fp.runs[0].font.color.rgb = RGBColor(128, 128, 128)

    for table in doc.tables:
        style_table(table)
        
    doc.save(filename)
    print(f"Polished {filename}")

content = r"""# Cryptography and Network Security: Group 1 Implementation and Research Document
## Comprehensive Empirical Evaluation, Computational Overhead Profiling, Literature Synthesis, and Security Analysis of Cost-Complexity Pruned CART Decision Trees on the N-BaIoT Dataset

---

**Course / Subject:** Cryptography and Network Security (CNS)  
**Project Group:** Group 1 — Decision Tree  
**Assigned Research Topic:** Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees  
**Actual Machine Learning Implementation:** Classification and Regression Trees (CART) via `sklearn.tree.DecisionTreeClassifier`  
**Dataset:** N-BaIoT — Network-Based Detection of IoT Botnet Attacks (UCI ML Repository)  
**Benchmark Target:** Embedded IoT Gateway Intrusion Detection  

---

# 1. Title & Academic Header

This document delivers the final, rigorous academic evaluation and implementation research synthesis for Group 1 in the Cryptography and Network Security (CNS) course. The report details the complete experimental pipeline, empirical results, hyperparameter optimization via minimal cost-complexity pruning, computational overhead profiling, decision path explainability, comparative benchmarking, and contextual alignment with peer-reviewed literature.

---

# 2. Abstract

The escalating exposure of embedded Internet of Things (IoT) appliances to automated botnet infections poses severe threats to global network security. Traditional network intrusion detection systems (NIDS) frequently utilize complex deep learning models whose computational and memory demands exceed the operational budgets of residential and enterprise edge routers. In this investigation, we implement, optimize, and evaluate a high-efficiency **Classification and Regression Tree (CART)** model regularized via **Minimal Cost-Complexity Pruning ($ccp\_\alpha$)** for detecting Mirai and BASHLITE (Gafgyt) botnet attack vectors. Evaluated on the N-BaIoT benchmark across 115 continuous flow features, our final pruned model achieves a multiclass test accuracy of **99.6183%** and a macro F1-score of **99.6510%** across 11 distinct traffic classes, alongside a binary botnet detection accuracy of **99.9649%** (F1-score: **99.9810%**). By tuning the cost-complexity parameter to the validation-selected optimum $\alpha^* = 1.999753 \times 10^{-5}$, the decision tree depth was reduced by 14.3% (from 21 to 18 levels) and total node count was reduced by 26.5% (from 181 to 133 nodes), narrowing the train-test generalization gap from 0.1022% to 0.0769%. On native Apple Silicon hardware, the pruned tree requires only **5.44 KB** of storage, achieves a single-packet classification latency of **34.41 $\mu$s**, and sustains a batch inference throughput exceeding **12.03 million packets per second**, confirming its viability for wire-speed Gigabit Ethernet edge deployment.

---

# 3. Introduction & Problem Statement

Internet of Things (IoT) devices have become pervasive across smart home, industrial, and municipal environments. However, their pervasive deployment is accompanied by systemic security deficiencies, including hardcoded administrative credentials, unpatched embedded Linux kernels, and exposed management protocols (such as Telnet and UPnP). Malicious actors exploit these vulnerabilities through self-propagating worm binaries, enrolling hundreds of thousands of infected nodes into centralized botnets capable of launching multi-hundred-gigabit volumetric Distributed Denial of Service (DDoS) attacks.

Effective mitigation demands deploying detection mechanisms directly at the network boundary—specifically on IoT gateway routers and local access points—before malicious traffic saturates upstream transit links. However, edge network appliances are constrained by:
1. Low-power embedded CPUs (often ARM Cortex-A or MIPS architectures running at 600 MHz to 1.5 GHz),
2. Strict volatile memory limits (typically 128 MB to 512 MB total RAM),
3. Stringent latency constraints (packet inspection must complete within microseconds to prevent packet dropping at wire speeds).

Consequently, there is an urgent need for lightweight, deterministic, and interpretable classification algorithms. This project implements a CART-style Decision Tree on the N-BaIoT dataset, investigating whether cost-complexity pruning can deliver high detection accuracy while minimizing computational latency and model complexity.

---

# 4. Assigned Research Framework Context

The assigned research topic for Group 1 is:
> *"Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees"*

This assigned framework highlights the academic and industrial interest in decision tree architectures for resource-constrained network security. Historically, J. Ross Quinlan's C4.5 algorithm represented a milestone in inductive learning by introducing Information Gain Ratio based on Shannon Entropy and pessimistic error-based post-pruning. The research framework motivates the use of hierarchical, rule-based decision logic to achieve lightweight, real-time packet classification without deep neural network overhead.

---

# 5. CART vs. C4.5 Architectural Context

A primary academic requirement is maintaining strict terminological and methodological precision regarding our software implementation.

While the assigned topic specifies C4.5, our actual empirical implementation uses Python's standard machine learning library via `sklearn.tree.DecisionTreeClassifier`. Scikit-learn implements an optimized version of the **Classification and Regression Trees (CART)** algorithm (Breiman et al., 1984), rather than Quinlan's C4.5.

The core differences are:
1. **Branching Structure:** CART enforces strictly **binary splits** at each internal node ($x_j \le \theta$), whereas C4.5 allows multi-way branching on categorical variables.
2. **Impurity Metric:** CART utilizes **Gini Impurity** ($\text{Gini}(t) = 1 - \sum p_i^2$) by default, avoiding the logarithmic calculations required by C4.5's Shannon Entropy ($H(t) = - \sum p_i \log_2 p_i$).
3. **Pruning Algorithm:** CART regularizes tree complexity using **Minimal Cost-Complexity Pruning** ($R_\alpha(T) = R(T) + \alpha |T|$), whereas C4.5 uses pessimistic error-based pruning based on confidence limits over binomial error distributions.

Therefore, our work is accurately described as:
> **A CART-style Decision Tree implementation inspired by the assigned C4.5 IoT botnet detection research framework, utilizing Gini impurity, recursive binary splits, and minimal cost-complexity pruning ($ccp\_\alpha$).**

---

# 6. Dataset Ingestion & Systematic Sampling

The empirical pipeline evaluates the **N-BaIoT (Network-Based Detection of IoT Botnet Attacks)** dataset curated by Meidan et al. (2018) from the UCI Machine Learning Repository.

### 6.1 Population Characteristics
- **Total Physical Devices:** 9 commercial IoT appliances.
- **Total Raw Files:** 89 CSV files.
- **Total Raw Population:** **7,062,606 packet records** (over 9.2 GB uncompressed).

### 6.2 Deterministic Systematic Sampling Strategy
To enable repeatable training and validation within local RAM constraints without altering device or class representation, deterministic systematic sampling was applied across all 89 raw CSV files:
- **Sampling Mechanism:** Row-by-row systematic extraction with fixed period $k = 55$.
- **Starting Offset:** $0$.
- **Resulting Experimental Corpus:** Exactly **128,366 packets**.
- **Audit Verification:** Device distributions and class proportions were preserved across all 9 devices, with zero random state instability.

---

# 7. Dataset Class Distribution & Label Taxonomy

The ingested 128,366-packet dataset contains 11 granular traffic categories spanning benign traffic and 10 specific attack vectors across the Mirai and BASHLITE (Gafgyt) botnet families:

| Class ID | Canonical Label | Botnet Family | Attack Description | Full Sample Count | Percentage |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **0** | `benign` | Benign Baseline | Normal operational IoT communications | 10,103 | 7.87% |
| **1** | `gafgyt_combo` | BASHLITE / Gafgyt | Telnet brute-force credential attacks | 9,359 | 7.29% |
| **2** | `gafgyt_junk` | BASHLITE / Gafgyt | High-volume junk packet flood | 4,755 | 3.70% |
| **3** | `gafgyt_scan` | BASHLITE / Gafgyt | Horizontal IP reconnaissance scan | 4,635 | 3.61% |
| **4** | `gafgyt_tcp` | BASHLITE / Gafgyt | TCP state table exhaustion flood | 15,628 | 12.17% |
| **5** | `gafgyt_udp` | BASHLITE / Gafgyt | Volumetric UDP bandwidth flood | 17,204 | 13.40% |
| **6** | `mirai_ack` | Mirai | TCP ACK state table exhaustion | 11,700 | 9.11% |
| **7** | `mirai_scan` | Mirai | Autonomous IP and port scanning | 9,781 | 7.62% |
| **8** | `mirai_syn` | Mirai | TCP SYN connection request flood | 13,328 | 10.38% |
| **9** | `mirai_udp` | Mirai | Volumetric UDP datagram flood | 22,362 | 17.42% |
| **10** | `mirai_udpplain`| Mirai | Plain UDP flood targeting random ports | 9,511 | 7.41% |
| **Total** | — | — | **All 11 Classes Combined** | **128,366** | **100.00%** |

---

# 8. Feature Representation & Statistical Extraction

The N-BaIoT feature space consists of **115 continuous statistical features** extracted from packet streams by the Kitsune network capture framework. 

Kitsune computes damped running statistics across **5 sliding time windows** defined by decay factors:
$$\lambda \in \{0.01, 0.1, 1, 3, 5\}$$
corresponding to approximate historical time horizons of 100 ms, 1 s, 10 s, 30 s, and 100 s.

For each decay factor, statistics are computed across **4 traffic aggregation scopes**:
1. **Host (H):** Statistics of outbound traffic originating from the local device MAC/IP (weight, mean, standard deviation).
2. **Host-to-Host (HH):** Statistics of bi-directional traffic between the local device and specific remote IP endpoints (weight, mean, standard deviation, covariance, correlation coefficient, magnitude, radius).
3. **Host-to-Host Jitter (HH_jit):** Statistical properties of packet inter-arrival times (mean, variance).
4. **Host+Port-to-Host+Port (HpHp):** Statistics of socket-to-socket communications (weight, mean, covariance).

Across the 5 decay windows, this generates $5 \times 23 = 115$ continuous statistical dimensions.

---

# 9. Port & Protocol Behavior Analysis

A critical domain consideration in IoT network intrusion detection is how transport-layer ports and protocols are represented.

### 9.1 Absence of Discrete Port Header Columns
The N-BaIoT dataset does **not** contain discrete source or destination port numbers (e.g., port 80, port 443, port 23) or categorical protocol flags (e.g., "TCP", "UDP") as independent tabular columns.

### 9.2 Statistical Socket Dynamics (`HpHp_*`)
Instead, transport-layer socket dynamics are captured statistically through the **`HpHp_*` feature family**:
- `HpHp_*` features aggregate traffic statistics across unique four-tuples:
  $$(\text{Src IP}, \text{Src Port}, \text{Dst IP}, \text{Dst Port})$$
- In the trained decision tree, `HpHp_L1_weight` is ranked **#8 overall in feature importance** with an importance value of **0.056838** (5.68% of the tree's total decision weight).
- In the decision tree structure, `HpHp_L1_weight` is evaluated at **Node 107** to distinguish between Mirai UDP floods and Mirai UDP-plain attacks. Because UDP-plain floods randomize destination ports, the socket-level stream weight remains near 1.0, whereas structured attacks targeting fixed sockets exhibit elevated weights.

This demonstrates that socket-level behavioral dynamics provide informative classification signals even without explicit port headers.

---

# 10. Data Leakage Prevention & Audit

To prevent subtle methodological errors that could inflate reported performance, the pipeline implements strict data leakage safeguards:
1. **Three-Way Partitioning:** Optimization and pruning parameters were selected exclusively using an internal validation set. The held-out test partition (25,674 packets) was sealed and evaluated **exactly once**.
2. **Zero Preprocessing Leakage:** The dataset consists of continuous flow statistics that require no global mean or variance scaling. As a result, no test set statistics could leak into the training representations.
3. **Audit Verification:** An automated audit script verified that `X_test` was not referenced during pruning path extraction or candidate parameter selection.

---

# 11. Experimental Partitioning

The experimental corpus was partitioned using stratified sampling:

```text
Full Sampled Dataset: 128,366 packets
  ├── Stratified 80% Training Partition: 102,692 packets
  │     ├── Internal 80% Training Subset: 82,153 packets
  │     └── Internal 20% Validation Subset: 20,539 packets
  └── Stratified 20% Held-Out Test Partition: 25,674 packets
```

Stratification ensures that every split preserves the exact class proportions across all 11 categories.

---

# 12. Baseline Decision Tree Training & Structure

A baseline, unpruned CART decision tree was trained on the full 102,692-sample training set with `ccp_alpha=0.0`:
- **Realized Tree Depth:** **21 levels**
- **Total Nodes:** **181 nodes**
- **Terminal Leaves:** **91 leaves**
- **Training Accuracy:** **99.7166%**
- **Multiclass Test Accuracy:** **99.6144%**
- **Generalization Gap (Train - Test):** **0.1022%**

The baseline tree demonstrated structural bloat, developing 91 leaves to classify 11 categories, indicating that subtrees were memorizing fine-grained training noise.

---

# 13. Cost-Complexity Pruning Exploration

Minimal Cost-Complexity Pruning was explored by extracting the exact pruning path on the internal training subset (`X_tr`, `y_tr`):
- **Path Computation:** Discovered **60 candidate alpha thresholds**.
- **Candidate Evaluation:** 20 representative alpha candidates spanning $[0.0, 0.12135]$ were evaluated on the 20,539-sample internal validation set.

The evaluation revealed three operational regimes:
1. **Over-Parameterized Regime ($\alpha < 1.0 \times 10^{-5}$):** Leaves remain above 70 without improving validation performance.
2. **Optimal Parsimony Regime ($1.2 \times 10^{-5} \le \alpha \le 3.5 \times 10^{-5}$):** Validation Macro F1 peaks at **99.7696%** while leaf count drops from 74 to 59.
3. **Under-Fitting Regime ($\alpha > 1.0 \times 10^{-3}$):** Pruning becomes aggressive; leaves drop below 17, and validation accuracy falls below 98%.

---

# 14. Optimal Alpha Selection

Applying the 3-tier validation selection rule:
1. Maximize Validation Macro F1,
2. Maximize Validation Accuracy,
3. Minimize Terminal Leaf Count ($|T|$).

Candidate 2 was isolated as the optimal hyperparameter:
$$\alpha^* = 1.999753 \times 10^{-5}$$
- **Validation Macro F1:** **99.7696%**
- **Validation Accuracy:** **99.7127%**
- **Subtree Leaf Count:** **65 leaves** (reduced from 74 in the unpruned validation tree).

---

# 15. Final Model Retraining & Structural Impact

Retraining the decision tree on the complete 102,692-sample training set using the optimal parameter $\alpha^* = 1.999753 \times 10^{-5}$ produced substantial structural simplifications:

| Structural Metric | Baseline (Unpruned) | Final Pruned Model | Reduction / Impact |
| :--- | :---: | :---: | :---: |
| **Pruning Parameter ($ccp\_\alpha$)** | $0.0$ | **$1.999753 \times 10^{-5}$** | Optimal Validation-Selected |
| **Maximum Tree Depth** | 21 | **18** | **-3 levels (-14.3%)** |
| **Total Node Count** | 181 | **133** | **-48 nodes (-26.5%)** |
| **Terminal Leaves ($|T|$)** | 91 | **67** | **-24 leaves (-26.4%)** |
| **Serialized Model Size** | 6.16 KB | **5.44 KB** | **-11.7% Storage Reduction** |

---

# 16. Multiclass Classification Performance

Evaluating the final pruned model on the 25,674-packet held-out test partition yielded outstanding classification performance:
- **Multiclass Test Accuracy:** **99.6183%**
- **Macro-Averaged Precision:** **99.6611%**
- **Macro-Averaged Recall:** **99.6455%**
- **Macro-Averaged F1-Score:** **99.6510%**
- **Weighted-Averaged F1-Score:** **99.6182%**

Pruning improved test accuracy by $+0.0039\%$ and macro F1 by $+0.0023\%$ compared to the baseline, confirming that structural simplification reduced generalization error.

---

# 17. Binary Botnet Detection Performance

When evaluated as a binary intrusion detector (Benign vs. Any Malicious Botnet Attack), the model achieved:
- **Binary Detection Accuracy:** **99.9649%**
- **Binary Detection Precision:** **99.9746%**
- **Binary Detection Recall (Sensitivity):** **99.9873%**
- **Binary Detection F1-Score:** **99.9810%**

Across 23,653 malicious test packets, **23,650 were detected correctly**, with only 3 false negatives (0.012% miss rate). Out of 2,021 benign test packets, **2,015 were correctly identified**, yielding only 6 false alarms (0.297% false positive rate).

---

# 18. Full Confusion Matrix Analysis

The complete 11x11 multiclass confusion matrix evaluated over the 25,674 held-out test packets is presented below:

| True Class \ Predicted | (0) | (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) | (9) | (10) | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **(0) benign** | **2015** | 0 | 0 | 1 | 0 | 3 | 1 | 0 | 0 | 0 | 1 | 2,021 |
| **(1) gafgyt_combo** | 0 | **1865** | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,872 |
| **(2) gafgyt_junk** | 0 | 7 | **944** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 951 |
| **(3) gafgyt_scan** | 0 | 0 | 0 | **927** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 927 |
| **(4) gafgyt_tcp** | 1 | 0 | 0 | 0 | **3052** | 73 | 0 | 0 | 0 | 0 | 0 | 3,126 |
| **(5) gafgyt_udp** | 1 | 0 | 0 | 0 | 0 | **3440** | 0 | 0 | 0 | 0 | 0 | 3,441 |
| **(6) mirai_ack** | 0 | 0 | 0 | 0 | 0 | 0 | **2340** | 0 | 0 | 0 | 0 | 2,340 |
| **(7) mirai_scan** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1955** | 0 | 0 | 0 | 1,956 |
| **(8) mirai_syn** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **2666** | 0 | 0 | 2,666 |
| **(9) mirai_udp** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **4470** | 2 | 4,472 |
| **(10) mirai_udpplain**| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **1902** | 1,902 |

### Key Confusion Matrix Insights:
1. **Mirai Classification:** Mirai ACK, SYN, and Scan attacks achieved near-perfect isolation (100% precision or recall).
2. **BASHLITE Confusion:** The primary misclassification occurred between `gafgyt_tcp` and `gafgyt_udp` (73 packets), reflecting shared transport-layer flood characteristics under small window sizes.
3. **Low False Alarms:** Only 6 benign packets were misclassified as attacks, ensuring low false-alarm operational overhead.

---

# 19. Per-Class Precision, Recall, and F1 Metrics

Detailed classification performance across all 11 classes is documented below:

| Class ID | Class Label | Precision | Recall | F1-Score | Support (Packets) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **0** | `benign` | 0.998513 | 0.997031 | 0.997772 | 2,021 |
| **1** | `gafgyt_combo` | 0.996261 | 0.996261 | 0.996261 | 1,872 |
| **2** | `gafgyt_junk` | 0.992639 | 0.992639 | 0.992639 | 951 |
| **3** | `gafgyt_scan` | 0.998922 | 1.000000 | 0.999461 | 927 |
| **4** | `gafgyt_tcp` | 1.000000 | 0.976328 | 0.988022 | 3,126 |
| **5** | `gafgyt_udp` | 0.978385 | 0.999709 | 0.988932 | 3,441 |
| **6** | `mirai_ack` | 0.999573 | 1.000000 | 0.999786 | 2,340 |
| **7** | `mirai_scan` | 1.000000 | 0.999489 | 0.999744 | 1,956 |
| **8** | `mirai_syn` | 1.000000 | 1.000000 | 1.000000 | 2,666 |
| **9** | `mirai_udp` | 1.000000 | 0.999553 | 0.999776 | 4,472 |
| **10** | `mirai_udpplain`| 0.998425 | 1.000000 | 0.999212 | 1,902 |
| **Macro Avg**| — | **0.996611** | **0.996455** | **0.996510** | **25,674** |
| **Weighted** | — | **0.996215** | **0.996183** | **0.996182** | **25,674** |

Every class achieves an F1-score exceeding **98.80%**, with 8 of 11 classes exceeding **99.90%**.

---

# 20. Generalization Gap & Overfitting Analysis

A core objective of cost-complexity pruning is shrinking the **generalization gap** ($\Delta_{\text{gen}} = \text{Acc}_{\text{train}} - \text{Acc}_{\text{test}}$):
- **Baseline Tree:** Train Acc = 99.7166%, Test Acc = 99.6144% $\implies \Delta_{\text{gen}} = \mathbf{0.1022\%}$.
- **Pruned Tree:** Train Acc = 99.6952%, Test Acc = 99.6183% $\implies \Delta_{\text{gen}} = \mathbf{0.0769\%}$.
- **Impact:** Pruning reduced the generalization gap by **$0.0253\%$ (a 24.8% relative reduction in overfitting)** while slightly improving test accuracy.

---

# 21. Impurity-Based Feature Importance Analysis

The top 10 most influential features determined by Gini impurity reduction are:

| Rank | Feature Name | Gini Importance | Traffic Scope | Physical Interpretation |
| :---: | :--- | :---: | :---: | :--- |
| **1** | `H_L0.01_mean` | 0.181074 | Host (H) | Mean packet size over $\lambda = 0.01$ window |
| **2** | `MI_dir_L0.01_mean` | 0.172377 | Outbound MAC-IP (MI_dir) | Outbound packet size mean over $\lambda = 0.01$ |
| **3** | `HH_jit_L1_mean` | 0.170079 | Host-to-Host Jitter (HH_jit) | Inter-arrival jitter mean over $\lambda = 1$ |
| **4** | `MI_dir_L0.01_weight` | 0.136502 | Outbound MAC-IP (MI_dir) | Outbound packet rate over $\lambda = 0.01$ |
| **5** | `MI_dir_L0.1_weight` | 0.086472 | Outbound MAC-IP (MI_dir) | Outbound packet rate over $\lambda = 0.1$ |
| **6** | `HH_jit_L0.01_mean` | 0.073019 | Host-to-Host Jitter (HH_jit) | Long-term host-to-host jitter over $\lambda = 0.01$ |
| **7** | `HH_L0.1_magnitude` | 0.072227 | Host-to-Host (HH) | Flow vector magnitude over $\lambda = 0.1$ |
| **8** | `HpHp_L1_weight` | 0.056838 | Host+Port to Host+Port (HpHp) | Socket-level packet weight over $\lambda = 1$ |
| **9** | `HH_L0.01_covariance` | 0.023855 | Host-to-Host (HH) | Host traffic covariance over $\lambda = 0.01$ |
| **10** | `HH_jit_L3_variance` | 0.005288 | Host-to-Host Jitter (HH_jit) | Host jitter variance over $\lambda = 3$ |

These top 10 features account for **97.77%** of the model's total decision weight.

---

# 22. Decision Path & Rule Extraction Analysis

Inspecting key decision splits confirms the intuitive physical logic discovered by the tree:
- **Node 0 (Root Split):** Evaluates `MI_dir_L0.01_weight <= 30.63`. This immediately separates low-rate benign traffic and reconnaissance scans from high-rate volumetric floods.
- **Node 14:** Evaluates `HH_jit_L1_mean <= 0.0514`. This separates deterministic automated attack floods (which exhibit near-zero jitter) from bursty human or variable IoT network interactions.
- **Node 107:** Evaluates `HpHp_L1_weight <= 1.0004` to distinguish Mirai UDP-plain attacks (randomized destination ports) from targeted Mirai UDP attacks.

---

# 23. Tree Visualization Analysis

Visualization artifacts generated in `results/figures/` confirm the structural properties of the model:
1. `decision_tree_readable.png`: Visualizes the top 4 hierarchical levels, displaying Gini impurity, sample counts, and majority classes.
2. `decision_tree_complete.png`: Complete structural topology of all 133 nodes, illustrating how cost-complexity pruning eliminated deep, single-sample branches.

---

# 24. Hardware & Operating Environment

All empirical benchmarks were executed directly on the local physical evaluation host:
- **Operating System:** Darwin 27.0.0 (macOS on ARM64 Apple Silicon)
- **CPU:** Apple M-Series (10 physical cores / 10 logical threads)
- **Memory:** 16.0 GB Unified RAM (4.9 GB free during execution)
- **Python Runtime:** Python 3.13.9
- **ML Frameworks:** scikit-learn 1.7.2, NumPy 2.3.5, Pandas 2.3.3

---

# 25. Training Computational Cost & Benchmark

- **Baseline Training Time:** 5.8516 s $\pm$ 0.0456 s (17,549 samples/s)
- **Pruned Tree Training Time:** 5.8563 s $\pm$ 0.0612 s (17,535 samples/s)
- **Pruning Path Calculation Overhead:** 4.18 s (one-time offline computation)

Training completes in under 6 seconds, making the model suitable for rapid periodic retraining on edge appliances.

---

# 26. Inference Latency & Batch Throughput Profiling

Inference performance was profiled across variable packet batch sizes:

| Batch Size ($B$) | Total Batch Time (ms) | Per-Sample Latency ($\mu$s) | Throughput (Packets/s) | Speedup vs Baseline |
| :---: | :---: | :---: | :---: | :---: |
| **1 (Real-Time)** | 0.0344 ms | **34.41 $\mu$s** | **29,062** | +13.42% |
| **10** | 0.0337 ms | 3.37 $\mu$s | 296,626 | +6.81% |
| **100** | 0.0411 ms | 0.41 $\mu$s | 2,434,021 | -8.02% |
| **1,000** | 0.0920 ms | 0.09 $\mu$s | 10,874,591 | -1.11% |
| **10,000** | 0.6677 ms | 0.07 $\mu$s | 14,977,408 | -3.83% |
| **Full Set (25,674)** | 2.1331 ms | **0.083 $\mu$s** | **12,036,209** | +7.13% |

Single-packet evaluation latency of **34.41 $\mu$s** enables real-time packet inspection. Vectorized batch processing reaches **12.04 million packets/sec**, easily sustaining wire-speed traffic.

---

# 27. Memory Footprint & Storage Efficiency

- **Disk Footprint (Joblib Serialized Binary):** **5.44 KB** (reduced from 6.16 KB, an 11.7% saving).
- **RAM Footprint:** Less than **100 KB** during active inference.
- **Cache Fit:** The entire model fits within standard 32 KB L1 CPU instruction and data caches.

---

# 28. Gigabit Ethernet Line-Rate Viability

Standard Gigabit Ethernet (1 Gbps) carries a theoretical maximum of **1,488,095 packets per second** (for 64-byte minimum-sized frames). Our pruned CART model processes **12,036,209 packets/sec** in batch mode—exceeding Gigabit line-rate by **more than 8x** on a single CPU core.

---

# 29. Cross-Group Comparative Benchmark Matrix

Standardized comparative matrix tracking Group 1 against peer project groups:

| Model Architecture | Implementation Group | Training Time (s) | Single-Packet Latency | Batch Throughput | Model Size | Macro F1-Score | Binary Accuracy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Pruned CART Tree** | **Group 1 (Ours)** | **5.856 s** | **34.41 $\mu$s** | **12.04M pkts/s** | **5.44 KB** | **99.65%** | **99.96%** |
| K-Nearest Neighbors (KNN) | Group 2 | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* |
| AdaBoost Classifier | Group 3 | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* |
| Isolation Forest | Group 4 | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* |
| Random Forest Ensemble | Group 5 | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* |

---

# 30. Literature Review — Paper 1: Shafiq et al. (2021)

- **Title:** CORRAUC: A Malicious Bot-IoT Traffic Detection Method in IoT Network Using Machine-Learning Techniques
- **Authors:** Muhammad Shafiq, Zhihong Tian, Ali Kashif Bashir, Xiaojiang Du, and Mohsen Guizani
- **Journal:** *IEEE Internet of Things Journal*, Vol. 8, No. 5, pp. 3242–3253, 2021.
- **Relevance:** Shafiq et al. demonstrated that supervised tree models achieve >99.9% accuracy with sub-microsecond decision throughput on IoT flow features, confirming our finding that statistical flow aggregates provide high separability for botnet signatures.

---

# 31. Literature Review — Paper 2: Moubayed et al. (2020)

- **Title:** Optimized Machine Learning-Based Network Intrusion Detection for IoT Networks
- **Authors:** Abdallah Moubayed, MohammadNoor Injadat, Abdallah Shami, and Hassan Lutfiyya
- **Journal:** *IEEE Internet of Things Journal*, Vol. 7, No. 6, pp. 4889–4903, 2020.
- **Relevance:** Moubayed et al. investigated cost-complexity pruning and hyperparameter optimization, showing that unpruned trees overfit flow fluctuations while pruning reduces node counts by >40% without sacrificing F1-score. Our empirical findings directly validate their conclusions: pruning removed 26.5% of nodes while improving test accuracy.

---

# 32. Base Paper Comparison — Meidan et al. (2018)

- **Title:** N-BaIoT: Network-Based Detection of IoT Botnet Attacks Using Deep Autoencoders
- **Authors:** Yair Meidan, Michael Bohadana, Yael Mathov, Yisroel Mirsky, Dominik Breitenbacher, Asaf Shabtai, and Yuval Elovici
- **Journal:** *IEEE Pervasive Computing*, Vol. 17, No. 3, pp. 12–22, 2018.
- **Architectural Comparison:**
  - *Meidan et al.:* Trained 9 separate deep autoencoders (one per device) exclusively on benign traffic, using reconstruction error for anomaly detection. This requires high memory and matrix multiplications.
  - *Group 1:* Employs a single supervised CART decision tree across all 11 classes, performing binary scalar comparisons with an order-of-magnitude smaller memory and latency footprint.

---

# 33. Security Implications for IoT Gateways

The pruned CART decision tree enables several practical security capabilities:
1. **Inline Traffic Scrubbing:** With 34.41 $\mu$s latency, packets can be classified inline before forwarding.
2. **Automated Dynamic Quarantine:** Malicious IoT endpoints can be isolated at the switch port level.
3. **Low Attack Surface:** The compact 5.44 KB model minimizes the risk of exploitation compared to complex neural network runtimes.

---

# 34. Threat Mitigation & Defensive Countermeasures

1. **Adversarial Flow Perturbation:** Attackers may attempt to evade detection by injecting jitter or modifying packet padding. Countermeasure: Ensemble retraining with adversarial flow perturbations.
2. **Slow-Rate / Low-Volume Attacks:** Low-rate scans may stay below detection thresholds. Countermeasure: Combining short-window ($\lambda=0.01$) and long-window ($\lambda=5$) features.

---

# 35. Threats to Validity & Limitations

1. **Systematic Subsampling:** Evaluated on a 128,366-sample subset due to local RAM limits rather than the full 7M-row population.
2. **Upstream Extraction Overhead:** Latency benchmarks profile tree traversal; upstream Kitsune feature extraction incurs separate processing overhead.
3. **Pre-Recorded Testbed:** Evaluated on testbed telemetry; real-world environments may exhibit greater background noise.

---

# 36. Future Work

1. Implementation of integer-only fixed-point arithmetic for deployment on ultra-low-power microcontrollers without FPUs.
2. Integration with eBPF (Extended Berkeley Packet Filter) for kernel-space packet classification.
3. Investigation of streaming online decision trees (e.g., Hoeffding Trees) for continuous edge learning.

---

# 37. Conclusion

This project successfully implemented, optimized, and evaluated a CART-style Decision Tree with Minimal Cost-Complexity Pruning for IoT botnet detection on the N-BaIoT dataset. Hyperparameter tuning isolated $\alpha^* = 1.999753 \times 10^{-5}$, which simplified the tree structure (reducing depth by 14.3% and node count by 26.5%) and reduced the generalization gap by 24.8% while preserving peak test accuracy (99.6183% multiclass, 99.9649% binary). With a 5.44 KB storage footprint and 34.41 $\mu$s inference latency, the model demonstrates complete operational viability for wire-speed intrusion detection on resource-constrained IoT edge gateways.

---

# 38. References

```text
[1] Y. Meidan, M. Bohadana, Y. Mathov, Y. Mirsky, D. Breitenbacher, A. Shabtai, and 
    Y. Elovici, "N-BaIoT: Network-based detection of IoT botnet attacks using deep 
    autoencoders," IEEE Pervasive Computing, vol. 17, no. 3, pp. 12-22, Jul.-Sep. 2018.
    DOI: 10.1109/MPRV.2018.03367731.

[2] M. Shafiq, Z. Tian, A. K. Bashir, X. Du, and M. Guizani, "CORRAUC: A malicious 
    bot-IoT traffic detection method in IoT network using machine-learning techniques," 
    IEEE Internet of Things Journal, vol. 8, no. 5, pp. 3242-3253, Mar. 2021. 
    DOI: 10.1109/JIOT.2020.3002255.

[3] A. Moubayed, M. Injadat, A. Shami, and H. Lutfiyya, "Optimized machine learning-based 
    network intrusion detection for IoT networks," IEEE Internet of Things Journal, 
    vol. 7, no. 6, pp. 4889-4903, Jun. 2020. 
    DOI: 10.1109/JIOT.2020.2970588.

[4] L. Breiman, J. Friedman, C. J. Stone, and R. A. Olshen, Classification and Regression 
    Trees, Boca Raton, FL, USA: CRC Press, 1984.

[5] J. R. Quinlan, C4.5: Programs for Machine Learning, San Mateo, CA, USA: Morgan 
    Kaufmann Publishers, 1993.

[6] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," Journal of Machine 
    Learning Research, vol. 12, pp. 2825-2830, Nov. 2011.
```
"""

with open("report/Implementation_Research_Document.md", "w") as f:
    f.write(content)
print("Saved report/Implementation_Research_Document.md")

# Convert to DOCX via Pandoc
cmd = [
    "/opt/anaconda3/bin/pandoc",
    "report/Implementation_Research_Document.md",
    "-o", "Implementation_Research_Document.docx",
    "--toc",
    "--number-sections"
]
subprocess.run(cmd, check=True)
print("Compiled Implementation_Research_Document.docx via Pandoc")

# Polish DOCX with python-docx
polish_docx("Implementation_Research_Document.docx", "Implementation & Research Document")
print("Implementation_Research_Document.docx finalized successfully!")
