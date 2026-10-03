import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

TARGET_DIR = "/Users/swapnil/Documents/cns/GROUP 1 — DECISION TREE"
os.makedirs(TARGET_DIR, exist_ok=True)

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
        set_cell_background(cell, "1F497D")
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

def polish_docx(filename, doc_title, running_subtitle):
    doc = docx.Document(filename)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        hp = section.header.paragraphs[0]
        hp.text = f"Sardar Patel Institute of Technology — CNS A.Y. 2026-27 | {doc_title}"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if hp.runs:
            hp.runs[0].font.name = 'Calibri'
            hp.runs[0].font.size = Pt(8.5)
            hp.runs[0].font.color.rgb = RGBColor(128, 128, 128)
            
        fp = section.footer.paragraphs[0]
        fp.text = f"{running_subtitle} | Group 1 — Decision Tree"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if fp.runs:
            fp.runs[0].font.name = 'Calibri'
            fp.runs[0].font.size = Pt(8.5)
            fp.runs[0].font.color.rgb = RGBColor(128, 128, 128)

    for table in doc.tables:
        style_table(table)
        
    doc.save(filename)
    print(f"[+] Polished: {filename}")

# -------------------------------------------------------------
# 1. Compile Algorithm_Document.docx
# -------------------------------------------------------------
algo_md = "report/Algorithm_Document.md"
target_algo_docx = os.path.join(TARGET_DIR, "Algorithm_Document.docx")
subprocess.run([
    "/opt/anaconda3/bin/pandoc", algo_md,
    "-o", target_algo_docx,
    "--toc", "--number-sections"
], check=True)
polish_docx(target_algo_docx, "Group 1 Algorithm Document", "CART Decision Tree & Cost-Complexity Pruning")

# -------------------------------------------------------------
# 2. Compile Design_Document.docx (covering all 30 items)
# -------------------------------------------------------------
design_md_path = "report/Design_Document_30Sections.md"
with open(design_md_path, "w") as f:
    f.write(r"""# Cryptography and Network Security: Group 1 Design Document
## Complete System Architecture, Engineering Design, Subsystem Specifications, and Deployment Guide for IoT Botnet Attack Detection Using Pruned CART Decision Trees

---

**Institute:** Sardar Patel Institute of Technology, Munshi Nagar, Andheri (W), Mumbai  
**Subject:** Cryptography and Network Security (CNS) A.Y. 2026–27  
**Faculty:** Prof. Renuka Pawar  
**Group:** Group 1 — Decision Tree  
**Assigned Research Topic:** Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees  
**Actual Machine Learning Implementation:** Classification and Regression Trees (CART) via `sklearn.tree.DecisionTreeClassifier`  
**Dataset:** N-BaIoT — Network-Based Detection of IoT Botnet Attacks (UCI ML Repository, ID: 442)  
**Target Environment:** Resource-Constrained IoT Gateway Appliances and Edge Routers  

---

# 1. System Overview
The Group 1 Intrusion Detection System (IDS) is an edge-native, deterministic cybersecurity engine designed to detect autonomous botnet infections (specifically Mirai and BASHLITE/Gafgyt malware) in real time. Deployed directly on residential and commercial IoT gateway routers, the system intercepts continuous traffic flow statistics and classifies packet vectors within microseconds. By utilizing a cost-complexity pruned CART decision tree, the system maintains high predictive accuracy (99.6183% multiclass, 99.9649% binary) while preserving an ultra-compact memory footprint (5.44 KB).

# 2. Problem Definition
Internet of Things (IoT) hardware—ranging from surveillance webcams and video baby monitors to smart thermostats—suffers from chronic firmware vulnerabilities, hardcoded manufacturer credentials, and lack of endpoint security agents. Worm-like malware variants automatically scan subnetworks, compromise IoT appliances, and coordinate massive Distributed Denial of Service (DDoS) attacks. Existing deep neural network anomaly detectors impose high floating-point multiply-accumulate operations and require hundreds of megabytes of RAM, exceeding edge gateway hardware capabilities.

# 3. Project Objectives
1. **Algorithmic Parsimony:** Implement and regularize a CART-style decision tree to replace compute-heavy neural architectures.
2. **Deterministic Microsecond Latency:** Bound tree depth to guarantee sub-40 $\mu$s per-packet classification latency.
3. **Overfitting Mitigation:** Apply Minimal Cost-Complexity Pruning ($ccp\_\alpha$) to shrink the generalization gap without degrading accuracy.
4. **Complete White-Box Auditability:** Provide interpretable Boolean decision rules for security forensic teams and automated firewall policy generation.

# 4. N-BaIoT Dataset Architecture
The benchmark dataset consists of network traffic captured from 9 physical commercial IoT appliances infected authentically with Mirai and BASHLITE malware:
1. Danmini Doorbell
2. Ecobee Thermostat
3. Ennio Doorbell
4. Philips B120N/10 Baby Monitor
5. Provision PT-737E Security Camera
6. Provision PT-838 Security Camera
7. Samsung SNH-1011N Webcam
8. SimpleHome XCS7-1002-WHT Camera
9. SimpleHome XCS7-1003-WHT Camera

# 5. Dataset Flow
Network traffic is ingested from network interface cards, routed through the Kitsune feature extraction engine to produce damped window statistics, accumulated into device-specific files, and normalized into a unified tabular schema.

# 6. Data Ingestion
The raw dataset totals **7,062,606 packet records** distributed across **89 distinct CSV files** (over 9.2 GB uncompressed). Ingestion streams each CSV file row-by-row, verifying header schema consistency and encoding device metadata.

# 7. Data Inspection & Hygiene Audit
A rigorous automated inspection confirmed:
- Zero missing values (0 NaNs) across all records.
- Zero infinite values (0 Infs).
- 100% data types mapped to continuous IEEE 754 64-bit floating point numbers (`float64`).

# 8. Systematic Sampling Methodology
To accommodate physical development RAM constraints (16.0 GB) while strictly preserving device and attack distributions, a deterministic systematic sampling algorithm was executed:
- **Sampling Step:** Fixed periodic step $k = 55$.
- **Starting Offset:** $0$.
- **Resulting Subset:** Exactly **128,366 packets**, maintaining class proportions within 0.05% of the population.

# 9. Preprocessing Pipeline
The preprocessing module loads sampled data, performs label mapping into 11 multiclass categories and binary categories, aligns feature column indices, and saves reproducible binary arrays (`preprocessed_data.joblib`).

# 10. Feature Handling & Transport Dynamics
The feature space consists of **115 continuous features** computed across 5 decay windows ($\lambda \in \{0.01, 0.1, 1, 3, 5\}$). Discrete port numbers are absent; socket-level transport dynamics are captured through continuous `HpHp_*` aggregates (Host+Port-to-Host+Port statistics).

# 11. Train / Test Split Architecture
To prevent evaluation bias:
- **Training Partition (80%):** 102,692 packets
- **Held-Out Test Partition (20%):** 25,674 packets (sealed until final benchmark)
- Both partitions follow stratified class balancing (`random_state=42`).

# 12. Decision Tree Architecture
The model is structured as a directed acyclic binary decision graph where each internal node evaluates an inequality $x_j \le \theta$, branching left or right until terminating at a classified leaf node.

# 13. CART Decision Process
At each node, candidate splits across all 115 continuous features are evaluated to minimize Gini Impurity:
$$\text{Gini}(t) = 1 - \sum_{i=1}^{11} p_i^2$$
Optimal splits maximize impurity reduction without requiring logarithmic calculations.

# 14. Baseline Model Execution
An unconstrained baseline decision tree was induced with $ccp\_\alpha = 0.0$:
- Tree Depth: **21 levels**
- Total Nodes: **181 nodes**
- Terminal Leaves: **91 leaves**
- Train Accuracy: **99.7166%** | Test Accuracy: **99.6144%**
- Generalization Gap: **0.1022%**

# 15. Cost-Complexity Pruning (CCP-Alpha)
Minimal Cost-Complexity Pruning regularizes tree complexity using the objective:
$$R_\alpha(T) = R(T) + \alpha |T|$$
Weakest-link subtrees are iteratively identified by calculating effective alpha:
$$\alpha_{\text{eff}}(t) = \frac{R(t) - R(T_t)}{|T_t| - 1}$$

# 16. Hyperparameter Tuning Pipeline
To eliminate test leakage, the 102,692-sample training set was internally split into:
- Internal Training Subset: 82,153 packets
- Internal Validation Subset: 20,539 packets

60 candidate alphas were extracted along the pruning path. Evaluating 20 representative candidates identified **Candidate 2 with $\alpha^* = 1.999753 \times 10^{-5}$**, which achieved peak validation Macro F1 (**99.7696%**) while pruning 9 leaves.

# 17. Final Model Retraining & Structure
Retraining on the full 102,692 training set with $\alpha^*$ yielded:
- Tree Depth: **18 levels** (-14.3%)
- Total Nodes: **133 nodes** (-26.5%)
- Terminal Leaves: **67 leaves** (-26.4%)
- Model Size: **5.44 KB** (-11.7%)

# 18. Prediction Pipeline
Inbound packet vectors traverse at most 18 scalar comparison nodes to generate an integer class label $\hat{y} \in \{0, 1, \dots, 10\}$.

# 19. Evaluation Pipeline
Computes multiclass Accuracy, Macro Precision, Macro Recall, Macro F1, Weighted F1, Binary Accuracy, Binary F1, and One-vs-Rest Macro ROC-AUC.

# 20. Standardized Tournament Evaluation
Implements the exact evaluation function from Prof. Renuka Pawar's notice (`evaluate_tournament_model`), outputting standardized leaderboard parameters.

# 21. Computational Benchmarking Framework
Profiles CPU execution across variable batch sizes ($B \in \{1, 10, 100, 1000, 10000, 25674\}$) on single-core Apple Silicon hardware.

# 22. Training-Time Measurement
Full model training completes in **5.8563 seconds** (17,535 samples/s). One-time offline pruning path generation requires **4.18 seconds**.

# 23. Inference-Latency Measurement
- Single-Packet Real-Time Latency: **34.41 $\mu$s** (29,062 pkts/s).
- Batch Throughput: **12,036,209 packets/sec** (0.083 $\mu$s per packet).

# 24. Confusion Matrix Generation
On 25,674 test packets, the model correctly detects 23,650 of 23,653 attacks (only 3 misses), with only 6 false alarms out of 2,021 benign packets.

# 25. Feature Importance Analysis
Top 10 features account for 97.77% of decision weight:
1. `H_L0.01_mean` (0.1811)
2. `MI_dir_L0.01_mean` (0.1724)
3. `HH_jit_L1_mean` (0.1701)
4. `MI_dir_L0.01_weight` (0.1365)
5. `MI_dir_L0.1_weight` (0.0865)

# 26. System Architecture Diagram
![System Architecture](results/figures/design_architecture.png)

# 27. Complete Workflow Diagram
![Complete Workflow Diagram](results/figures/design_training_workflow.png)

# 28. Data-Flow Diagram (Level 1 DFD)
![Data Flow Diagram](results/figures/design_dfd.png)

# 29. Model Pipeline & Pruning Diagram
![Pruning Workflow Diagram](results/figures/design_pruning_workflow.png)

# 30. Deployment Considerations for Resource-Constrained IoT Environments
With a 5.44 KB memory footprint and 34.41 $\mu$s decision latency, the model can run directly within an OpenWrt Linux kernel netfilter module or user-space daemon on 128 MB RAM gateway routers, exceeding Gigabit Ethernet wire speed by 8x without requiring GPU hardware.
""")

target_design_docx = os.path.join(TARGET_DIR, "Design_Document.docx")
subprocess.run([
    "/opt/anaconda3/bin/pandoc", design_md_path,
    "-o", target_design_docx,
    "--toc", "--number-sections"
], check=True)
polish_docx(target_design_docx, "Group 1 System Design Document", "Comprehensive System Architecture & 30-Section Technical Design")
os.remove(design_md_path)

# -------------------------------------------------------------
# 3. Compile Section_5.2.docx
# -------------------------------------------------------------
sec52_md = "report/section_5_2_computational_analysis.md"
target_sec52_docx = os.path.join(TARGET_DIR, "Section_5.2.docx")
subprocess.run([
    "/opt/anaconda3/bin/pandoc", sec52_md,
    "-o", target_sec52_docx,
    "--number-sections"
], check=True)
polish_docx(target_sec52_docx, "Master Research Paper — Section 5.2", "Computational Overhead & Hardware Latency Analysis")

print("\nSUCCESS: All 3 Word documents successfully compiled and polished in target directory!")
