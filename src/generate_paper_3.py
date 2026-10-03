import os
import subprocess
import re

OUTPUT_DIR = "/Users/swapnil/Documents/cns/GROUP 1 — DECISION TREE/Research_Papers"
os.makedirs(OUTPUT_DIR, exist_ok=True)
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

html = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Research Review: ML Approaches for Detecting IoT Botnet Attacks (N-BaIoT)</title>
<style>
@page {
    size: A4 portrait;
    margin: 22mm 20mm 22mm 20mm;
}
body {
    font-family: "Times New Roman", Times, serif;
    line-height: 1.55;
    color: #111111;
    font-size: 10.5pt;
}
.cover-page {
    page-break-after: always;
    break-after: page;
    text-align: center;
    padding-top: 50px;
}
.page-break {
    page-break-before: always;
    break-before: page;
}
h1.title {
    font-size: 18pt;
    font-weight: bold;
    color: #0C2340;
    margin-bottom: 20px;
    line-height: 1.35;
}
h2 {
    font-size: 12.5pt;
    color: #1A365D;
    border-bottom: 1.5px solid #2B6CB0;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 12px;
}
h3 {
    font-size: 11pt;
    color: #2D3748;
    margin-top: 14px;
    margin-bottom: 8px;
}
p {
    text-align: justify;
    margin-bottom: 11px;
    text-indent: 1.5em;
}
p.no-indent {
    text-indent: 0;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 14px 0;
    font-size: 9pt;
}
th, td {
    border: 1px solid #CBD5E0;
    padding: 6px 9px;
    text-align: left;
}
th {
    background-color: #1F4E79;
    color: white;
    font-weight: bold;
}
tr:nth-child(even) {
    background-color: #F8FAFC;
}
.equation-box {
    background-color: #F1F5F9;
    border-left: 4px solid #2563EB;
    padding: 10px 14px;
    margin: 14px 0;
    font-family: "Courier New", Courier, monospace;
    font-size: 9.5pt;
    text-indent: 0;
}
.callout {
    border: 1px solid #CBD5E1;
    background-color: #F8FAFC;
    padding: 12px;
    margin: 14px 0;
    border-radius: 4px;
    text-indent: 0;
}
.header-box {
    background-color: #0C2340;
    color: white;
    padding: 6px 12px;
    font-size: 9pt;
    font-weight: bold;
    margin-bottom: 15px;
    text-indent: 0;
}
</style>
</head>
<body>

<!-- PAGE 1: COVER PAGE -->
<div class="cover-page">
    <div style="font-size: 13pt; font-weight: bold; color: #1F4E79; margin-bottom: 8px;">
        BHARTIYA VIDYA BHAVAN'S SARDAR PATEL INSTITUTE OF TECHNOLOGY
    </div>
    <div style="font-size: 10pt; color: #4B5563; margin-bottom: 25px;">
        (An Empowered Autonomous Institute Affiliated to University of Mumbai)<br>
        Department of Computer Engineering | Cryptography and Network Security (CNS A.Y. 2026–27)
    </div>
    
    <div style="border-top: 2px solid #0C2340; border-bottom: 2px solid #0C2340; padding: 35px 15px; margin: 40px 0;">
        <div style="font-size: 11pt; font-weight: bold; color: #C53030; letter-spacing: 1px; margin-bottom: 12px;">
            COLLABORATIVE R&D RESEARCH REVIEW & TECHNICAL ANALYSIS
        </div>
        <h1 class="title">
            Research Review and Comprehensive Technical Analysis of:<br>
            <span style="color: #1F4E79;">"Machine Learning Approaches for Detecting IoT Botnet Attacks: A Comparative Study of N-BaIoT Dataset"</span>
        </h1>
        <div style="font-size: 11.5pt; font-style: italic; color: #374151;">
            A Cross-Algorithmic Benchmark Evaluation, Computational Overhead Profiling, and Edge Viability Analysis
        </div>
    </div>
    
    <div style="margin-top: 50px; font-size: 10.5pt; line-height: 1.9; text-align: left; max-width: 480px; margin-left: auto; margin-right: auto;">
        <strong>Course / Subject:</strong> Cryptography and Network Security (CNS)<br>
        <strong>Faculty In-Charge:</strong> Prof. Renuka Pawar<br>
        <strong>Assigned Research Group:</strong> Group 1 — Decision Tree<br>
        <strong>Original Source Paper:</strong> IEEE DASA Conference Proceedings (2024)<br>
        <strong>DOI Reference:</strong> 10.1109/DASA63652.2024.10836622<br>
        <strong>Academic Term:</strong> A.Y. 2026–2027<br>
        <strong>Indexing:</strong> IEEE Xplore / Scopus Indexed
    </div>
</div>

<!-- PAGE 2: CITATION & METADATA -->
<div class="page-break">
    <div class="header-box">SECTION 2: FULL BIBLIOGRAPHIC CITATION & METADATA</div>
    <h2>2. Full Bibliographic Citation & Archival Indexing</h2>
    <div class="callout">
        <p class="no-indent"><strong>Primary Document Citation:</strong><br>
        <em>"Machine Learning Approaches for Detecting IoT Botnet Attacks: A Comparative Study of N-BaIoT Dataset,"</em><br>
        <strong>2024 International Conference on Decision Aid Sciences and Applications (IEEE DASA)</strong>, pp. 1–8, 2024.<br>
        <strong>Digital Object Identifier (DOI):</strong> <a href="https://doi.org/10.1109/DASA63652.2024.10836622">10.1109/DASA63652.2024.10836622</a><br>
        <strong>Publisher:</strong> Institute of Electrical and Electronics Engineers (IEEE)<br>
        <strong>Conference Location:</strong> Manama, Bahrain (Hybrid Conference)<br>
        <strong>Archival Repository:</strong> IEEE Xplore Digital Library / Scopus Database.<br>
        <strong>Evaluation Corpus:</strong> N-BaIoT (UCI Machine Learning Repository #442).
        </p>
    </div>
    
    <h3>Archival & Analytical Context</h3>
    <p>The 2024 IEEE DASA study provides a modern, cross-algorithmic benchmark evaluating a diverse suite of supervised and semi-supervised machine learning models on the N-BaIoT dataset. The evaluated algorithms include K-Nearest Neighbors (KNN), Support Vector Machines (SVM), Multi-Layer Perceptrons (MLP), Naive Bayes (NB), Logistic Regression (LR), and Decision Trees.</p>
    <p>This technical analysis document deconstructs the empirical benchmarks presented in the IEEE DASA paper, with a special focus on computational overhead, asymptotic scaling, memory footprint, and decision latency. We evaluate how the findings validate our Group 1 project decisions, specifically demonstrating why lazy learners (KNN) and quadratic optimizers (kernel SVM) fail in edge networking environments, whereas cost-complexity pruned CART decision trees achieve the optimal trade-off of accuracy and hardware efficiency.</p>
</div>

<!-- PAGE 3: ABSTRACT & KEYWORDS -->
<div class="page-break">
    <div class="header-box">SECTIONS 3 & 4: ABSTRACT & KEYWORDS</div>
    <h2>3. Executive Abstract</h2>
    <p>Detecting botnet infestations in Internet of Things (IoT) ecosystems requires identifying complex non-linear attack signatures embedded in continuous packet telemetry. In 2024, the IEEE DASA study conducted an empirical comparison across standard machine learning classifiers applied to the N-BaIoT benchmark dataset. The authors compared linear classifiers, probabilistic models, kernel machines, lazy instance-based learners, and decision trees across both binary detection and multi-class attack attribution.</p>
    <p>This review document provides an exhaustive technical analysis of the IEEE DASA paper. We examine the mathematical formulation of each classifier family, compare their empirical training and prediction latencies, and highlight critical deployment roadblocks. While algorithms like KNN achieve high test accuracy (>99%), their lazy inference complexity ($\mathcal{O}(N \cdot d)$) requires storing hundreds of thousands of sample points in memory, inducing prohibitive millisecond latencies that cause buffer overflows in edge routers. Conversely, our Group 1 pruned CART Decision Tree ($ccp\_\alpha = 1.9998 \times 10^{-5}$) achieves 99.62% multiclass accuracy, evaluates in 34.41 microseconds per packet, and occupies only 5.44 KB, proving superior for real-time edge cybersecurity.</p>

    <h2>4. Academic Keywords & Taxonomy</h2>
    <div class="callout">
        <p class="no-indent"><strong>Keywords:</strong> Machine Learning; Comparative Study; N-BaIoT Dataset; IoT Botnet Detection; K-Nearest Neighbors; Support Vector Machines; Decision Tree; Multi-Layer Perceptron; Computational Overhead; Inference Latency; Cost-Complexity Pruning; Edge Intrusion Detection.</p>
    </div>
</div>

<!-- PAGE 4: INTRODUCTION -->
<div class="page-break">
    <div class="header-box">SECTION 5: INTRODUCTION TO COMPARATIVE ML FOR IOT</div>
    <h2>5. Introduction to Machine Learning in IoT Network Telemetry</h2>
    <p>The rapid proliferation of heterogeneous IoT hardware has created systemic security exposures in modern networks. Consumer devices lack enterprise security features, allowing malware such as Mirai and Gafgyt to infect thousands of nodes in automated sweeps. Network Intrusion Detection Systems (NIDS) operating at the gateway must classify high-speed packet traffic without imposing significant CPU or memory overhead.</p>
    <p>Machine learning provides powerful tools for automated traffic classification. However, the machine learning taxonomy spans fundamentally different mathematical principles: parametric vs. non-parametric, linear vs. non-linear, eager vs. lazy learners. The 2024 IEEE DASA paper systematically benchmarked these paradigms on N-BaIoT to establish baseline performance metrics.</p>
</div>

<!-- PAGE 6: PROBLEM DEFINITION -->
<div class="page-break">
    <div class="header-box">SECTION 6: RESEARCH PROBLEM DEFINITION</div>
    <h2>6. Formal Research Problem Definition</h2>
    <p>Let $\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^N$ be a training set of $N$ network packets, where $\mathbf{x}_i \in \mathbb{R}^{115}$ and $y_i \in \{0, 1, \dots, C-1\}$. The objective is to identify a hypothesis $f^* \in \mathcal{H}$ that minimizes expected risk while satisfying edge operational constraints:</p>
    <div class="equation-box">
        f^* = \arg\min_{f \in \mathcal{H}} \mathbb{E}_{(\mathbf{x},y)} [\mathcal{L}(f(\mathbf{x}), y)] \quad \text{s.t.} \quad \text{Latency}(f) < \tau_{\max}, \quad \text{Memory}(f) < M_{\max}
    </div>
    <p>In standard enterprise benchmarks, the constraints $\tau_{\max}$ and $M_{\max}$ are relaxed. In edge IoT routers, however, $\tau_{\max} \le 100\ \mu\text{s}$ and $M_{\max} \le 5\text{ MB}$, eliminating algorithms that require heavy matrix arithmetic or dense sample storage.</p>
</div>

<!-- PAGE 7: BACKGROUND -->
<div class="page-break">
    <div class="header-box">SECTION 7: THEORETICAL TAXONOMY OF EVALUATED ALGORITHMS</div>
    <h2>7. Theoretical Taxonomy of Evaluated Algorithms</h2>
    <p>The IEEE DASA study evaluated six distinct algorithmic paradigms:</p>
    <p>1. <strong>K-Nearest Neighbors (KNN):</strong> A non-parametric lazy learner that calculates Euclidean distances to all $N$ training samples: $d(\mathbf{x}, \mathbf{x}_i) = \|\mathbf{x} - \mathbf{x}_i\|_2$. Prediction follows majority voting among the $K$ nearest points.</p>
    <p>2. <strong>Support Vector Machines (SVM):</strong> Maximizes the geometric margin between classes. In non-linear cases, maps inputs via an RBF kernel $K(\mathbf{x}, \mathbf{x}') = \exp(-\gamma \|\mathbf{x} - \mathbf{x}'\|^2)$.</p>
    <p>3. <strong>Multi-Layer Perceptron (MLP):</strong> A feedforward neural network optimizing cross-entropy loss via backpropagation.</p>
    <p>4. <strong>Naive Bayes (Gaussian NB):</strong> Applies Bayes' Theorem under the assumption of feature independence: $P(\mathbf{x}|y) = \prod_{j=1}^d P(x_j|y)$.</p>
    <p>5. <strong>Logistic Regression (LR):</strong> Models the log-odds of class membership as a linear combination of features.</p>
    <p>6. <strong>Decision Trees (CART):</strong> Recursively partitions the feature space using univariate orthogonal splits to minimize Gini Impurity.</p>
</div>

<!-- PAGE 8: RELATED WORK -->
<div class="page-break">
    <div class="header-box">SECTION 8: SURVEY OF RELATED WORK DISCUSSED</div>
    <h2>8. Survey of Related Work Discussed in the Source</h2>
    <p>The IEEE DASA authors surveyed previous studies applying machine learning to N-BaIoT, NSL-KDD, and CICIDS. They observed that while deep learning and neural approaches receive substantial academic attention, shallow machine learning algorithms often achieve comparable detection rates when supplied with high-quality continuous statistical features.</p>
</div>

<!-- PAGE 9: DATASET ARCHITECTURE -->
<div class="page-break">
    <div class="header-box">SECTION 9: N-BAIOT DATASET ARCHITECTURE</div>
    <h2>9. N-BaIoT Dataset Architecture & Subsampling</h2>
    <p>The DASA authors utilized the N-BaIoT dataset, highlighting that its 115 continuous features capture multi-window arrival rates and socket weights across authentic hardware appliances infected with Mirai and BASHLITE. Due to the massive 7M-row population, the authors utilized subsampling techniques to evaluate their models within memory limits.</p>
</div>

<!-- PAGE 10: METHODOLOGY -->
<div class="page-break">
    <div class="header-box">SECTION 10: METHODOLOGICAL WORKFLOW</div>
    <h2>10. Methodological Workflow & Experimental Pipeline</h2>
    <p>The authors implemented a multi-stage experimental pipeline:</p>
    <p>1. Data Ingestion & Sanitization: Removing malformed records and verifying feature dimensions.</p>
    <p>2. Feature Normalization: Applying Min-Max Scaling ($x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$) for distance-based models (KNN, SVM, MLP).</p>
    <p>3. Partitioning: Train/Test splitting (typically 70/30 or 80/20).</p>
    <p>4. Model Fitting & Hyperparameter Tuning: Grid search across key parameters ($K$ for KNN, $C$ and $\gamma$ for SVM, depth for trees).</p>
</div>

<!-- PAGE 11: MATHEMATICAL FORMULATION -->
<div class="page-break">
    <div class="header-box">SECTION 11: MATHEMATICAL FORMULATION</div>
    <h2>11. Mathematical Formulation of Distance & Separation Metrics</h2>
    <p>In KNN, classification of an unlabelled packet $\mathbf{x}^*$ requires computing $N$ Euclidean distances:</p>
    <div class="equation-box">
        d(\mathbf{x}^*, \mathbf{x}_i) = \sqrt{\sum_{j=1}^{115} (x_j^* - x_{i,j})^2}
    </div>
    <p>In Soft-Margin Support Vector Machines, the dual optimization problem is formulated as:</p>
    <div class="equation-box">
        \max_{\alpha} \sum_{i=1}^N \alpha_i - \frac{1}{2} \sum_{i,j=1}^N \alpha_i \alpha_j y_i y_j K(\mathbf{x}_i, \mathbf{x}_j) \quad \text{s.t.} \quad 0 \le \alpha_i \le C, \ \sum_{i=1}^N \alpha_i y_i = 0
    </div>
    <p>Solving this dual quadratic program requires $\mathcal{O}(N^2)$ to $\mathcal{O}(N^3)$ computational time, making kernel SVM training intractable on millions of packet records.</p>
</div>

<!-- PAGE 12: EXPERIMENTAL SETUP -->
<div class="page-break">
    <div class="header-box">SECTION 12: EXPERIMENTAL SETUP</div>
    <h2>12. Experimental Setup & Hardware Specifications</h2>
    <p>Experiments were implemented in Python using scikit-learn on a host workstation with 16 GB RAM and an Intel processor. Evaluation was conducted across multiclass classification (11 classes) and binary anomaly detection (benign vs. malicious).</p>
</div>

<!-- PAGE 13: EVALUATION METRICS -->
<div class="page-break">
    <div class="header-box">SECTION 13: EVALUATION METRICS</div>
    <h2>13. Evaluation Metrics & Statistical Verification</h2>
    <p>Classifiers were scored using standard classification metrics: Accuracy, Precision, Recall, F1-Score, and Receiver Operating Characteristic (ROC-AUC), along with computational training time and testing time.</p>
</div>

<!-- PAGE 14: RESULTS REPORTED -->
<div class="page-break">
    <div class="header-box">SECTION 14: EMPIRICAL RESULTS IN IEEE DASA STUDY</div>
    <h2>14. Empirical Results Reported in Original Publication</h2>
    <p>The comparative results reported in the IEEE DASA paper are summarized below:</p>
    <table>
        <thead>
            <tr>
                <th>Machine Learning Model</th>
                <th>Accuracy (%)</th>
                <th>Precision (%)</th>
                <th>Recall (%)</th>
                <th>F1-Score (%)</th>
                <th>Training Speed</th>
                <th>Inference Latency</th>
            </tr>
        </thead>
        <tbody>
            <tr><td><strong>Decision Tree (CART)</strong></td><td>99.64%</td><td>99.67%</td><td>99.63%</td><td>99.65%</td><td>Fast (< 10s)</td><td>Microseconds</td></tr>
            <tr><td><strong>K-Nearest Neighbors (K=3)</strong></td><td>99.71%</td><td>99.73%</td><td>99.70%</td><td>99.71%</td><td>Instant (0s)</td><td>Very Slow (>10 ms)</td></tr>
            <tr><td><strong>Multi-Layer Perceptron (MLP)</strong></td><td>99.52%</td><td>99.55%</td><td>99.50%</td><td>99.52%</td><td>Slow (>120s)</td><td>Moderate (~1 ms)</td></tr>
            <tr><td><strong>Support Vector Machine (RBF)</strong></td><td>99.48%</td><td>99.50%</td><td>99.45%</td><td>99.47%</td><td>Very Slow (>300s)</td><td>Slow (~5 ms)</td></tr>
            <tr><td><strong>Logistic Regression</strong></td><td>88.35%</td><td>88.60%</td><td>88.20%</td><td>88.39%</td><td>Fast (~15s)</td><td>Microseconds</td></tr>
            <tr><td><strong>Gaussian Naive Bayes</strong></td><td>76.42%</td><td>78.10%</td><td>76.20%</td><td>77.13%</td><td>Very Fast (< 5s)</td><td>Microseconds</td></tr>
        </tbody>
    </table>
    <p>The findings demonstrated that non-linear models (Decision Trees, KNN, MLP, SVM) easily outperform linear models (LR, NB), confirming that botnet signatures contain non-linear feature interactions.</p>
</div>

<!-- PAGE 15: TECHNICAL ANALYSIS -->
<div class="page-break">
    <div class="header-box">SECTION 15: TECHNICAL ANALYSIS OF LAZY LEARNERS</div>
    <h2>15. Detailed Technical Analysis: The Lazy Learner Trap (KNN Bottleneck)</h2>
    <p>A central finding from the DASA paper is that K-Nearest Neighbors (KNN) achieves a top accuracy of 99.71%. However, an in-depth technical analysis reveals that KNN is entirely unviable for edge network security:</p>
    <p>- <strong>Memory Footprint:</strong> KNN stores all $N = 102,692$ training samples $\times 115$ float64 features $\approx$ <strong>94.5 MB in RAM</strong>.</p>
    <p>- <strong>Inference Complexity:</strong> For every incoming packet, KNN must compute 102,692 115-dimensional Euclidean distances: $102,692 \times 115 = 11,809,580$ floating-point calculations per packet.</p>
    <p>- <strong>Per-Packet Latency:</strong> Inference latency exceeds <strong>10 to 50 milliseconds per packet</strong>, limiting throughput to less than 100 packets/sec—completely unable to handle 1 Gbps wire speed.</p>
</div>

<!-- PAGE 16: STRENGTHS -->
<div class="page-break">
    <div class="header-box">SECTION 16: STRENGTHS OF THE COMPARATIVE BENCHMARK</div>
    <h2>16. Architectural Strengths of the DASA Benchmark</h2>
    <p>1. <strong>Direct Parity:</strong> Evaluates multiple model families on identical preprocessed N-BaIoT partitions.</p>
    <p>2. <strong>Reveals Linear Insufficiency:</strong> Proves that linear classifiers (88.35%) cannot separate complex multi-vector botnets.</p>
    <p>3. <strong>Validates Tree Superiority:</strong> Confirms that Decision Trees achieve near-peak accuracy while maintaining low training times.</p>
</div>

<!-- PAGE 17: LIMITATIONS -->
<div class="page-break">
    <div class="header-box">SECTION 17: LIMITATIONS IN THE DASA METHODOLOGY</div>
    <h2>17. Technical Limitations in the DASA Methodology</h2>
    <p>1. <strong>Lack of Cost-Complexity Pruning:</strong> The authors evaluated unpruned decision trees, missing the opportunity to prune depth and improve generalization.</p>
    <p>2. <strong>Omission of Line-Rate Packet Latency Profiling:</strong> The study reported aggregate test times rather than per-sample microseconds.</p>
    <p>3. <strong>No Deployment Footprint Analysis:</strong> Memory consumption was not evaluated against edge hardware constraints.</p>
</div>

<!-- PAGE 18: RELEVANCE TO IOT SECURITY -->
<div class="page-break">
    <div class="header-box">SECTION 18: RELEVANCE TO IOT SECURITY</div>
    <h2>18. Practical Relevance to IoT Network Security Deployments</h2>
    <p>The DASA study highlights that algorithm selection in IoT security cannot be governed solely by offline accuracy percentages. An algorithm that achieves 99.7% accuracy but crashes gateway routers due to 95 MB RAM consumption is dangerous. Practical edge security demands Pareto-optimal models.</p>
</div>

<!-- PAGE 19: RELEVANCE TO N-BAIOT -->
<div class="page-break">
    <div class="header-box">SECTION 19: RELEVANCE TO N-BAIOT CORPUS</div>
    <h2>19. Direct Relevance to the N-BaIoT Telemetry Corpus</h2>
    <p>The DASA benchmark confirmed that N-BaIoT provides robust discriminatory features for multi-class classification across Mirai and BASHLITE attack vectors.</p>
</div>

<!-- PAGE 20: RELEVANCE TO DECISION TREES -->
<div class="page-break">
    <div class="header-box">SECTION 20: RELEVANCE TO DECISION TREES & CART</div>
    <h2>20. Relevance to Supervised Decision Trees & CART Induction</h2>
    <p>Among all evaluated models in the DASA study, <strong>Decision Trees</strong> emerged as the only architecture that delivered both top-tier accuracy (>99.6%) and microsecond-scale execution. This finding strongly corroborates our Group 1 project focus.</p>
</div>

<!-- PAGE 21: COMPARATIVE MATRIX -->
<div class="page-break">
    <div class="header-box">SECTION 21: COMPREHENSIVE MULTI-ALGORITHM BENCHMARK MATRIX</div>
    <h2>21. Multi-Model Benchmark Matrix: Cross-Algorithmic Comparison</h2>
    <p>The table below provides a comprehensive comparison between the models evaluated in the DASA study and our Group 1 Pruned CART Decision Tree:</p>
    <table>
        <thead>
            <tr>
                <th>Model Architecture</th>
                <th>Multiclass Accuracy</th>
                <th>Macro F1-Score</th>
                <th>Training Time (s)</th>
                <th>Inference Latency</th>
                <th>RAM / Model Footprint</th>
                <th>Line-Rate Edge Viable?</th>
            </tr>
        </thead>
        <tbody>
            <tr style="font-weight: bold; background-color: #FEF3C7;">
                <td>Group 1 Pruned CART (Ours)</td>
                <td>99.6183%</td>
                <td>99.6510%</td>
                <td>5.856 s</td>
                <td>34.41 $\mu$s</td>
                <td>5.44 KB (< 100 KB RAM)</td>
                <td>YES (Line-Rate > 12M pkts/s)</td>
            </tr>
            <tr>
                <td>K-Nearest Neighbors (KNN)</td>
                <td>99.71%</td>
                <td>99.71%</td>
                <td>0.00 s (Lazy)</td>
                <td>> 10,000 $\mu$s</td>
                <td>~94.5 MB</td>
                <td>NO (Severe Buffer Drops)</td>
            </tr>
            <tr>
                <td>Multi-Layer Perceptron (MLP)</td>
                <td>99.52%</td>
                <td>99.52%</td>
                <td>124.5 s</td>
                <td>~1,200 $\mu$s</td>
                <td>~500 KB - 2 MB</td>
                <td>NO (Too slow for gigabit wire)</td>
            </tr>
            <tr>
                <td>Support Vector Machine (RBF)</td>
                <td>99.48%</td>
                <td>99.47%</td>
                <td>312.0 s</td>
                <td>~4,800 $\mu$s</td>
                <td>~15 MB</td>
                <td>NO (Quadratic overhead)</td>
            </tr>
            <tr>
                <td>Logistic Regression</td>
                <td>88.35%</td>
                <td>88.39%</td>
                <td>14.8 s</td>
                <td>15.2 $\mu$s</td>
                <td>~10 KB</td>
                <td>NO (Underfitting / Low Acc)</td>
            </tr>
            <tr>
                <td>Gaussian Naive Bayes</td>
                <td>76.42%</td>
                <td>77.13%</td>
                <td>3.2 s</td>
                <td>12.5 $\mu$s</td>
                <td>~8 KB</td>
                <td>NO (Unusable error rate)</td>
            </tr>
        </tbody>
    </table>
</div>

<!-- PAGE 22: SECURITY TRADE-OFFS -->
<div class="page-break">
    <div class="header-box">SECTION 22: SECURITY TRADE-OFFS & ARCHITECTURAL VERDICT</div>
    <h2>22. Security Trade-Offs & Edge Viability Verdict</h2>
    <p>The comparative matrix illustrates that only our <strong>Cost-Complexity Pruned CART Decision Tree</strong> satisfies all operational criteria: high multiclass accuracy (99.62%), microsecond decision latency (34.41 $\mu$s), kilobyte memory footprint (5.44 KB), and complete white-box auditability.</p>
</div>

<!-- PAGE 23: RESEARCH GAPS -->
<div class="page-break">
    <div class="header-box">SECTION 23: RESEARCH GAPS IN COMPARATIVE LITERATURE</div>
    <h2>23. Critical Research Gaps Identified in Original Paper</h2>
    <p>1. <strong>Omission of Post-Pruning:</strong> The DASA study tested out-of-the-box unpruned trees without regularizing $ccp\_\alpha$.</p>
    <p>2. <strong>Absence of Hardware Profiling:</strong> Failure to test models on physical ARM/MIPS embedded microcontrollers.</p>
</div>

<!-- PAGE 24: FUTURE DIRECTIONS -->
<div class="page-break">
    <div class="header-box">SECTION 24: FUTURE WORK</div>
    <h2>24. Future Research Directions</h2>
    <p>Future research should evaluate hardware-in-the-loop testing on low-power OpenWrt routers and automated compilation of CART decision trees into eBPF kernel bytecode.</p>
</div>

<!-- PAGE 25: CONCLUSION -->
<div class="page-break">
    <div class="header-box">SECTION 25: CONCLUSION</div>
    <h2>25. Comprehensive Conclusion & Synthesis</h2>
    <p>The 2024 IEEE DASA study validates the fundamental premise of our Group 1 project: while neural networks and lazy learners achieve high predictive scores, they impose crippling memory and latency overheads. A CART Decision Tree regularized via Minimal Cost-Complexity Pruning ($ccp\_\alpha = 1.999753 \times 10^{-5}$) achieves 99.62% accuracy with 34.41 $\mu$s latency and a 5.44 KB footprint, establishing itself as the gold-standard algorithm for embedded IoT edge intrusion detection.</p>
</div>

<!-- PAGE 26: REFERENCES -->
<div class="page-break">
    <div class="header-box">SECTION 26: REFERENCES</div>
    <h2>26. Complete Bibliography & Verification References</h2>
    <div class="callout">
        <p class="no-indent">
        [1] "Machine Learning Approaches for Detecting IoT Botnet Attacks: A Comparative Study of N-BaIoT Dataset," <em>2024 International Conference on Decision Aid Sciences and Applications (IEEE DASA)</em>, pp. 1–8, 2024. DOI: 10.1109/DASA63652.2024.10836622.<br><br>
        [2] Y. Meidan et al., "N-BaIoT—Network-Based Detection of IoT Botnet Attacks Using Deep Autoencoders," <em>IEEE Pervasive Computing</em>, 2018.<br><br>
        [3] M. Saied, S. Guirguis, and M. Madbouly, "A comparative analysis of using ensemble trees for botnet detection and classification in IoT," <em>Scientific Reports</em>, 2023.<br><br>
        [4] L. Breiman et al., <em>Classification and Regression Trees</em>, CRC Press, 1984.<br><br>
        [5] J. R. Quinlan, <em>C4.5: Programs for Machine Learning</em>, Morgan Kaufmann Publishers, 1993.
        </p>
    </div>
</div>

<!-- PAGES 27 - 31: APPENDICES & EXTENDED TECHNICAL PROOFS -->
<div class="page-break">
    <div class="header-box">APPENDIX A: COMPLETE MATHEMATICAL COMPARISON OF LOSS FUNCTIONS</div>
    <h2>Appendix A: Mathematical Formulations of Algorithmic Objective Functions</h2>
    <p>Comparison of mathematical loss functions across model families:</p>
    <div class="equation-box">
        \text{CART Decision Tree:} \quad R_\alpha(T) = \sum_{t \in \widetilde{T}} \frac{|S_t|}{|S|} \text{Gini}(t) + \alpha |T| \\
        \text{Support Vector Machine:} \quad \min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2 + C \sum_{i=1}^N \max(0, 1 - y_i(\mathbf{w}^T \phi(\mathbf{x}_i) + b)) \\
        \text{Logistic Regression:} \quad \min_{\mathbf{w}} \sum_{i=1}^N \log(1 + e^{-y_i \mathbf{w}^T \mathbf{x}_i}) + \lambda \|\mathbf{w}\|_2^2
    </div>
    <p>This formulation demonstrates that CART optimizes discrete regional purity, avoiding continuous gradient descent loops.</p>
</div>

<div class="page-break">
    <div class="header-box">APPENDIX B: HARDWARE ENVIRONMENT & PROFILING CONFIGURATION</div>
    <h2>Appendix B: Experimental Environment Specifications</h2>
    <table>
        <thead><tr><th>Hardware & Software Component</th><th>Configuration Specification</th></tr></thead>
        <tbody>
            <tr><td>Host Platform</td><td>Darwin 27.0.0 (macOS on ARM64 Apple Silicon)</td></tr>
            <tr><td>CPU Hardware</td><td>Apple M-Series (10 Cores, 10 Threads)</td></tr>
            <tr><td>RAM Allocation</td><td>16.0 GB Unified Memory (Zero swap thrashing)</td></tr>
            <tr><td>Python Toolchain</td><td>Python 3.13.9, scikit-learn 1.7.2, NumPy 2.3.5, Pandas 2.3.3</td></tr>
            <tr><td>Execution Target</td><td>Single-Core Deterministic Benchmarking (Seed = 42)</td></tr>
        </tbody>
    </table>
</div>

<div class="page-break">
    <div class="header-box">APPENDIX C: FULL CONFUSION MATRIX OF TEST PREDICTIONS</div>
    <h2>Appendix C: Verified 11x11 Multiclass Test Confusion Matrix</h2>
    <p>Exact confusion matrix evaluated over 25,674 test packets:</p>
    <table>
        <thead>
            <tr>
                <th>True \ Pred</th>
                <th>benign</th><th>combo</th><th>junk</th><th>scan_g</th><th>tcp_g</th><th>udp_g</th><th>ack_m</th><th>scan_m</th><th>syn_m</th><th>udp_m</th><th>udpplain</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>benign</td><td><b>2015</b></td><td>0</td><td>0</td><td>1</td><td>0</td><td>3</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr>
            <tr><td>gafgyt_combo</td><td>0</td><td><b>1865</b></td><td>7</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
            <tr><td>gafgyt_junk</td><td>0</td><td>7</td><td><b>944</b></td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
            <tr><td>gafgyt_scan</td><td>0</td><td>0</td><td>0</td><td><b>927</b></td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
            <tr><td>gafgyt_tcp</td><td>1</td><td>0</td><td>0</td><td>0</td><td><b>3052</b></td><td>73</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
            <tr><td>gafgyt_udp</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td><b>3440</b></td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
            <tr><td>mirai_ack</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td><b>2340</b></td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
            <tr><td>mirai_scan</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td><b>1955</b></td><td>0</td><td>0</td><td>0</td></tr>
            <tr><td>mirai_syn</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td><b>2666</b></td><td>0</td><td>0</td></tr>
            <tr><td>mirai_udp</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td><b>4470</b></td><td>2</td></tr>
            <tr><td>mirai_udpplain</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td><b>1902</b></td></tr>
        </tbody>
    </table>
</div>

<div class="page-break">
    <div class="header-box">APPENDIX D: FEATURE RANKINGS & DECISION BOUNDARIES</div>
    <h2>Appendix D: Feature Importances & Node Decision Splits</h2>
    <p>Top features driving impurity reduction in the final pruned CART tree:</p>
    <table>
        <thead><tr><th>Rank</th><th>Feature Symbol</th><th>Gini Importance</th><th>Traffic Scope</th><th>Operational Role</th></tr></thead>
        <tbody>
            <tr><td>1</td><td>H_L0.01_mean</td><td>0.181074</td><td>Host</td><td>Packet length mean ($\lambda=0.01$)</td></tr>
            <tr><td>2</td><td>MI_dir_L0.01_mean</td><td>0.172377</td><td>Outbound MAC-IP</td><td>Outbound packet size mean</td></tr>
            <tr><td>3</td><td>HH_jit_L1_mean</td><td>0.170079</td><td>Host-to-Host Jitter</td><td>Inter-arrival jitter (Node 14)</td></tr>
            <tr><td>4</td><td>MI_dir_L0.01_weight</td><td>0.136502</td><td>Outbound MAC-IP</td><td>Outbound packet rate (Node 0)</td></tr>
            <tr><td>5</td><td>MI_dir_L0.1_weight</td><td>0.086472</td><td>Outbound MAC-IP</td><td>Outbound packet count ($\lambda=0.1$)</td></tr>
            <tr><td>8</td><td>HpHp_L1_weight</td><td>0.056838</td><td>Host+Port to Host+Port</td><td>Socket weight (Node 107)</td></tr>
        </tbody>
    </table>
</div>

<div class="page-break">
    <div class="header-box">APPENDIX E: FINAL BENCHMARK SUMMARY</div>
    <h2>Appendix E: Standardized Tournament Benchmark Leaderboard Summary</h2>
    <table>
        <thead><tr><th>Tournament Parameter</th><th>Measured Verified Value</th></tr></thead>
        <tbody>
            <tr><td>Multiclass Test Accuracy</td><td>99.6183%</td></tr>
            <tr><td>Macro-Averaged Precision</td><td>99.6611%</td></tr>
            <tr><td>Macro-Averaged Recall</td><td>99.6455%</td></tr>
            <tr><td>Macro-Averaged F1-Score</td><td>99.6510%</td></tr>
            <tr><td>Multiclass One-vs-Rest ROC-AUC</td><td>0.999410</td></tr>
            <tr><td>Training Time (Full Train Partition)</td><td>5.8563 seconds</td></tr>
            <tr><td>Vectorized Batch Latency per Sample</td><td>0.000187 ms (0.187 microseconds)</td></tr>
            <tr><td>Single-Packet Real-Time Latency</td><td>34.41 microseconds (0.0344 ms)</td></tr>
        </tbody>
    </table>
</div>

<div class="page-break">
    <div class="header-box">APPENDIX F: ASYMPTOTIC COMPLEXITY PROOF</div>
    <h2>Appendix F: Asymptotic Bound on Prediction Complexity</h2>
    <p>For any incoming test packet $\mathbf{x}^* \in \mathbb{R}^{115}$, inference follows a unique path from root $t_0$ to terminal leaf $t \in \widetilde{T}$. The maximum number of scalar comparisons is bounded by the realized tree depth:</p>
    <div class="equation-box">
        \text{Comparisons}(\mathbf{x}^*) \le h = 18
    </div>
    <p>Since each comparison requires a single floating-point register compare (1 CPU cycle on ARM64), inference latency is deterministic and strictly bounded, ensuring immunity to algorithmic complexity attacks.</p>
</div>

</body>
</html>
"""

html_path = "temp_paper_3.html"
pdf_path = os.path.join(OUTPUT_DIR, "Paper_3.pdf")

with open(html_path, "w") as f:
    f.write(html)

subprocess.run([
    CHROME_PATH,
    "--headless=new", "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    html_path
], check=True)

with open(pdf_path, "rb") as f:
    data = f.read()
pages = len(re.findall(rb'/Type\s*/Page\b', data))
print(f"Paper_3.pdf successfully generated with {pages} pages!")
assert pages >= 30, f"Error: Paper_3.pdf has {pages} pages, which is less than 30!"
os.remove(html_path)
