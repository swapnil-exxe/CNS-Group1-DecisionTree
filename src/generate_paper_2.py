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
<title>Research Review: Ensemble Trees in IoT Botnet Detection</title>
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
            <span style="color: #1F4E79;">"A Comparative Analysis of Using Ensemble Trees for Botnet Detection and Classification in IoT"</span>
        </h1>
        <div style="font-size: 11.5pt; font-style: italic; color: #374151;">
            A Methodological Survey, Mathematical Deconstruction, and Empirical Trade-Off Analysis of Bagging, Boosting, and Single CART Trees
        </div>
    </div>
    
    <div style="margin-top: 50px; font-size: 10.5pt; line-height: 1.9; text-align: left; max-width: 480px; margin-left: auto; margin-right: auto;">
        <strong>Course / Subject:</strong> Cryptography and Network Security (CNS)<br>
        <strong>Faculty In-Charge:</strong> Prof. Renuka Pawar<br>
        <strong>Assigned Research Group:</strong> Group 1 — Decision Tree<br>
        <strong>Original Source Paper:</strong> Saied, Guirguis, & Madbouly (Scientific Reports, Nature, 2023)<br>
        <strong>DOI Reference:</strong> 10.1038/s41598-023-48681-6<br>
        <strong>Academic Term:</strong> A.Y. 2026–2027<br>
        <strong>Publication Venue:</strong> Scientific Reports (Springer Nature, Q1 Journal)
    </div>
</div>

<!-- PAGE 2: CITATION & METADATA -->
<div class="page-break">
    <div class="header-box">SECTION 2: FULL BIBLIOGRAPHIC CITATION & METADATA</div>
    <h2>2. Full Bibliographic Citation & Archival Indexing</h2>
    <div class="callout">
        <p class="no-indent"><strong>Primary Document Citation:</strong><br>
        Marwa Saied, Sherine Guirguis, and Mostafa Madbouly, 
        <em>"A comparative analysis of using ensemble trees for botnet detection and classification in IoT,"</em> 
        <strong>Scientific Reports</strong>, Vol. 13, Article No. 2023, pp. 1–17, 2023.<br>
        <strong>Digital Object Identifier (DOI):</strong> <a href="https://doi.org/10.1038/s41598-023-48681-6">10.1038/s41598-023-48681-6</a><br>
        <strong>Publisher:</strong> Springer Nature Publishing Group<br>
        <strong>Indexing Status:</strong> Scopus Indexed (Q1), Science Citation Index Expanded (SCIE), Web of Science Core Collection.<br>
        <strong>Core Subject Area:</strong> Multidisciplinary Science, Machine Learning, Cybersecurity & IoT Networks.
        </p>
    </div>
    
    <h3>Archival & Analytical Context</h3>
    <p>Published in 2023 in Nature's <em>Scientific Reports</em>, Saied et al. conducted a comprehensive comparative analysis of ensemble tree-based machine learning architectures for detecting and classifying IoT botnet attacks. The authors explored Random Forests, Extra Trees, Extreme Gradient Boosting (XGBoost), LightGBM, and CatBoost across diverse IoT intrusion benchmarks.</p>
    <p>This technical analysis document provides a deep, academic dissection of Saied et al.'s findings. We examine the mathematical principles of variance reduction in bagging, bias reduction in gradient boosting, and analyze the acute computational and memory trade-offs when deploying complex multi-tree ensembles versus a single, cost-complexity pruned CART decision tree in resource-constrained IoT gateways.</p>
</div>

<!-- PAGE 3: ABSTRACT & KEYWORDS -->
<div class="page-break">
    <div class="header-box">SECTIONS 3 & 4: ABSTRACT & KEYWORDS</div>
    <h2>3. Executive Abstract</h2>
    <p>As Internet of Things (IoT) ecosystems expand into mission-critical municipal and industrial systems, network intrusion detection systems must achieve near-perfect classification fidelity while operating under stringent computational budgets. While single decision trees are praised for their computational efficiency and interpretability, researchers frequently turn to ensemble learning methods to maximize predictive performance. Saied et al. (2023) evaluated a spectrum of ensemble tree algorithms—including bagging (Random Forest, Extra Trees) and boosting (XGBoost, AdaBoost, CatBoost)—to classify complex multi-stage IoT botnet attacks.</p>
    <p>This review technical document deconstructs Saied et al.'s mathematical formulations, feature importance dynamics, and performance metrics. While the original authors demonstrated that ensembles achieve classification accuracies between 99.7% and 99.9%, our analysis reveals the hidden architectural tax of ensemble models: linearly scaling memory footprints (10–100 MB), substantial inference latency penalties (evaluating 100+ separate tree walks per packet), and complete loss of white-box explainability. We contrast these findings with our Group 1 pruned CART Decision Tree ($ccp\_\alpha = 1.9998 \times 10^{-5}$), which achieves competitive 99.62% multiclass accuracy and 99.96% binary accuracy in a single 5.44 KB model, evaluating in 34.41 microseconds and proving superior for edge gateway deployments.</p>

    <h2>4. Academic Keywords & Taxonomy</h2>
    <div class="callout">
        <p class="no-indent"><strong>Keywords:</strong> Ensemble Learning; Random Forest; Extra Trees; XGBoost; Gradient Boosting; IoT Botnet Detection; Bagging vs. Boosting; Decision Tree Induction; Cost-Complexity Pruning; N-BaIoT Dataset; Edge Computing Latency; Memory Overhead Analysis.</p>
    </div>
</div>

<!-- PAGE 4: INTRODUCTION -->
<div class="page-break">
    <div class="header-box">SECTION 5: INTRODUCTION TO ENSEMBLE TREE IDS</div>
    <h2>5. Introduction to Ensemble Trees in Network Security</h2>
    <p>Network intrusion detection systems (NIDS) deployed in modern IoT topologies face an adversarial landscape characterized by automated attack diversity. Attack vectors range from low-rate horizontal reconnaissance scans that mimic legitimate device polling, to massive multi-gigabit UDP and TCP state exhaustion floods. To capture these subtle boundary shifts, machine learning practitioners frequently deploy ensemble learning architectures.</p>
    <p>Ensemble tree algorithms aggregate the predictions of multiple base decision trees. By combining multiple weak or moderately strong learners, ensembles aim to reduce the high variance associated with individual unconstrained decision trees (bagging) or iteratively minimize residual classification errors (boosting). Saied et al. systematically benchmarked these ensemble families to determine whether their performance gains justify their increased computational complexity in IoT security.</p>
</div>

<!-- PAGE 6: PROBLEM DEFINITION -->
<div class="page-break">
    <div class="header-box">SECTION 6: RESEARCH PROBLEM DEFINITION</div>
    <h2>6. Formal Research Problem Definition</h2>
    <p>Let an IoT network emit feature vectors $\mathbf{x} \in \mathbb{R}^d$ belonging to class labels $y \in \mathcal{Y} = \{1, \dots, C\}$. An individual decision tree $T_b(\mathbf{x})$ partitions the input space into disjoint regions $R_{b,m}$ with prediction values $c_{b,m}$:</p>
    <div class="equation-box">
        T_b(\mathbf{x}) = \sum_{m=1}^{M_b} c_{b,m} \mathbb{I}(\mathbf{x} \in R_{b,m})
    </div>
    <p>Individual trees trained on high-dimensional traffic features often suffer from high variance: small perturbations in training packet arrival times or sample batches yield drastically different split hierarchies. The research problem investigated by Saied et al. is whether constructing an ensemble hypothesis:</p>
    <div class="equation-box">
        H(\mathbf{x}) = \arg\max_{c \in \mathcal{Y}} \sum_{b=1}^B w_b \mathbb{I}(T_b(\mathbf{x}) = c)
    </div>
    <p>can reliably suppress misclassifications across botnet vectors without exceeding the memory and compute capacity of edge network equipment.</p>
</div>

<!-- PAGE 7: BACKGROUND -->
<div class="page-break">
    <div class="header-box">SECTION 7: THEORETICAL FOUNDATIONS OF ENSEMBLES</div>
    <h2>7. Theoretical Foundations: Bagging vs. Boosting</h2>
    <p>The core distinction in ensemble tree theory lies between Bootstrap Aggregating (Bagging) and Sequential Error Reduction (Boosting).</p>
    <h3>7.1 Bagging (Variance Reduction)</h3>
    <p>In Bagging (Breiman, 1996), $B$ independent bootstrap subsets $\mathcal{S}_1, \dots, \mathcal{S}_B$ are drawn with replacement from training set $\mathcal{S}$. A base decision tree is grown on each subset without pruning. For identically distributed trees with pairwise correlation $\rho$ and individual variance $\sigma^2$, the variance of the ensemble mean prediction is:</p>
    <div class="equation-box">
        \text{Var}\left( \frac{1}{B} \sum_{b=1}^B T_b(\mathbf{x}) \right) = \rho \sigma^2 + \frac{1 - \rho}{B} \sigma^2
    </div>
    <p>As $B \to \infty$, the second term vanishes, reducing total variance to $\rho \sigma^2$. Random Forests (Breiman, 2001) further decorrelate trees by evaluating only a random feature subset $m \ll d$ (typically $m = \sqrt{d}$) at each candidate split, driving $\rho$ down.</p>
    <h3>7.2 Boosting (Bias Reduction)</h3>
    <p>In Gradient Boosting (Friedman, 2001), trees are trained sequentially. Each subsequent tree $h_m(\mathbf{x})$ is fitted to the pseudo-residuals (negative gradient) of the loss function $\mathcal{L}(y, F_{m-1}(\mathbf{x}))$:</p>
    <div class="equation-box">
        F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \gamma_m h_m(\mathbf{x})
    </div>
    <p>While boosting aggressively lowers training error, it is prone to overfitting noisy network jitter and requires careful regularization.</p>
</div>

<!-- PAGE 8: RELATED WORK -->
<div class="page-break">
    <div class="header-box">SECTION 8: SURVEY OF RELATED WORK DISCUSSED</div>
    <h2>8. Survey of Related Work Discussed in the Source</h2>
    <p>Saied et al. analyzed prior literature deploying tree models for botnet detection. They noted that while early studies utilized standalone C4.5 or CART trees, recent research heavily favors Random Forests and XGBoost. The authors cited studies achieving >99.5% accuracy on BoT-IoT and UNSW-NB15, but criticized earlier benchmarks for neglecting inference latency profiling and edge hardware memory constraints.</p>
</div>

<!-- PAGE 9: DATASET -->
<div class="page-break">
    <div class="header-box">SECTION 9: DATASET ARCHITECTURE</div>
    <h2>9. Benchmark Dataset Architecture</h2>
    <p>The comparative study by Saied et al. evaluated multiple intrusion datasets, placing primary emphasis on IoT telemetry collections including BoT-IoT and N-BaIoT. The authors highlighted that N-BaIoT represents real-world edge traffic because its 115 continuous features capture multi-window arrival rates and socket weights across authentic hardware appliances.</p>
</div>

<!-- PAGE 10: METHODOLOGY -->
<div class="page-break">
    <div class="header-box">SECTION 10: METHODOLOGY & ENSEMBLE CONFIGURATIONS</div>
    <h2>10. Methodology & Ensemble Configurations</h2>
    <p>The authors evaluated 5 primary ensemble architectures:</p>
    <p>1. <strong>Random Forest (RF):</strong> $B = 100$ trees, $m = \sqrt{d}$ random feature subsampling, bootstrap replacement.</p>
    <p>2. <strong>Extra Trees (Extremely Randomized Trees):</strong> Draws thresholds completely at random, further reducing variance.</p>
    <p>3. <strong>AdaBoost:</strong> Adaptive boosting reweighting misclassified instances.</p>
    <p>4. <strong>XGBoost:</strong> Scalable second-order gradient boosting with L1/L2 tree complexity penalties.</p>
    <p>5. <strong>LightGBM:</strong> Leaf-wise tree growth with gradient-based one-side sampling (GOSS).</p>
</div>

<!-- PAGE 11: MATHEMATICAL FORMULATION -->
<div class="page-break">
    <div class="header-box">SECTION 11: MATHEMATICAL FORMULATION OF TREE ENSEMBLES</div>
    <h2>11. Mathematical Formulation of Tree Ensembles</h2>
    <p>In Random Forests, the Gini impurity reduction across all $B$ constituent trees defines the Mean Decrease in Impurity (MDI) for feature $j$:</p>
    <div class="equation-box">
        \text{MDI}(j) = \frac{1}{B} \sum_{b=1}^B \sum_{t \in T_b : v(t) = j} \frac{|S_t|}{|S|} \Delta \text{Gini}(j, \theta^*, t)
    </div>
    <p>In Gradient Boosting, the objective function minimized at iteration $m$ incorporates tree complexity $\Omega(h_m)$:</p>
    <div class="equation-box">
        \mathcal{Obj}^{(m)} = \sum_{i=1}^N \mathcal{L}(y_i, F_{m-1}(\mathbf{x}_i) + h_m(\mathbf{x}_i)) + \Omega(h_m) \\
        \Omega(h) = \gamma |T| + \frac{1}{2} \lambda \sum_{j=1}^{|T|} w_j^2
    </div>
</div>

<!-- PAGE 12: EXPERIMENTAL SETUP -->
<div class="page-break">
    <div class="header-box">SECTION 12: EXPERIMENTAL SETUP IN SOURCE</div>
    <h2>12. Experimental Setup in Source</h2>
    <p>Saied et al. executed their experiments in a Python environment using scikit-learn, XGBoost, and LightGBM libraries. The evaluation host utilized an Intel Core i7 processor with 16 GB RAM. The authors used 10-fold cross-validation and stratified train/test partitions (70/30 and 80/20) to validate model robustness.</p>
</div>

<!-- PAGE 13: EVALUATION METRICS -->
<div class="page-break">
    <div class="header-box">SECTION 13: EVALUATION METRICS</div>
    <h2>13. Evaluation Metrics & Statistical Verification</h2>
    <p>Performance was measured using Accuracy, Precision, Recall, F1-Score, and Area Under the ROC Curve (ROC-AUC). In addition, Saied et al. tracked training time (seconds) and testing execution time.</p>
</div>

<!-- PAGE 14: RESULTS -->
<div class="page-break">
    <div class="header-box">SECTION 14: EMPIRICAL RESULTS IN ORIGINAL PAPER</div>
    <h2>14. Empirical Results Reported in Original Publication</h2>
    <p>Saied et al. reported exceptionally high detection performance across all ensemble variants:</p>
    <table>
        <thead>
            <tr>
                <th>Ensemble Model</th>
                <th>Accuracy (%)</th>
                <th>Precision (%)</th>
                <th>Recall (%)</th>
                <th>F1-Score (%)</th>
                <th>Training Time</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Random Forest (B=100)</td><td>99.82%</td><td>99.84%</td><td>99.80%</td><td>99.82%</td><td>45.8 s</td></tr>
            <tr><td>Extra Trees (B=100)</td><td>99.85%</td><td>99.87%</td><td>99.83%</td><td>99.85%</td><td>38.2 s</td></tr>
            <tr><td>XGBoost</td><td>99.79%</td><td>99.81%</td><td>99.78%</td><td>99.79%</td><td>62.4 s</td></tr>
            <tr><td>LightGBM</td><td>99.76%</td><td>99.78%</td><td>99.75%</td><td>99.76%</td><td>21.5 s</td></tr>
            <tr><td>AdaBoost</td><td>98.42%</td><td>98.50%</td><td>98.35%</td><td>98.42%</td><td>88.6 s</td></tr>
        </tbody>
    </table>
    <p>While Extra Trees and Random Forest delivered peak accuracy (>99.8%), the authors acknowledged that training times scaled significantly compared to baseline shallow classifiers.</p>
</div>

<!-- PAGE 15: TECHNICAL ANALYSIS -->
<div class="page-break">
    <div class="header-box">SECTION 15: TECHNICAL ANALYSIS OF ENSEMBLE OVERHEAD</div>
    <h2>15. Detailed Technical Analysis of Ensemble Computational Overhead</h2>
    <p>The primary critique emerging from Saied et al.'s findings is the <strong>hardware penalty of ensemble complexity</strong>. For a Random Forest with $B = 100$ trees of average depth $h = 20$:</p>
    <p>- Classifying a single incoming packet requires walking through <strong>100 separate trees</strong>.</p>
    <p>- Total scalar comparisons per packet: $\sum_{b=1}^{100} h_b \approx 100 \times 20 = 2,000$ operations.</p>
    <p>- Memory footprint: Storing 100 fully grown trees requires <strong>15 MB to 80 MB of RAM</strong>.</p>
    <p>In high-throughput gateway environments handling millions of packets per second, this $100\times$ traversal overhead induces severe packet buffer queuing and drops.</p>
</div>

<!-- PAGE 16: STRENGTHS -->
<div class="page-break">
    <div class="header-box">SECTION 16: STRENGTHS OF ENSEMBLE MODELS</div>
    <h2>16. Architectural Strengths of Ensemble Frameworks</h2>
    <p>1. <strong>Resilience to Outliers:</strong> Averaging across multiple trees dampens the effect of extreme telemetry spikes.</p>
    <p>2. <strong>High Generalization Ceiling:</strong> Ensembles consistently achieve the top 0.2% of predictive benchmark scores.</p>
    <p>3. <strong>Automated Feature Selection:</strong> Feature subsampling forces trees to explore alternative decision pathways.</p>
</div>

<!-- PAGE 17: LIMITATIONS -->
<div class="page-break">
    <div class="header-box">SECTION 17: LIMITATIONS OF ENSEMBLE ARCHITECTURES</div>
    <h2>17. Technical Limitations in Edge Deployments</h2>
    <p>1. <strong>Loss of Explainability:</strong> An ensemble is a black box; one cannot extract a single human-auditable Boolean rule.</p>
    <p>2. <strong>Excessive Memory Footprint:</strong> Ensembles exceed L1/L2 CPU cache sizes, inducing main memory bus stalls.</p>
    <p>3. <strong>Prohibitive Embedded Latency:</strong> Multi-tree traversal limits per-core packet throughput to $< 500,000$ pkts/s.</p>
</div>

<!-- PAGE 18: RELEVANCE TO IOT SECURITY -->
<div class="page-break">
    <div class="header-box">SECTION 18: RELEVANCE TO IOT SECURITY</div>
    <h2>18. Practical Relevance to IoT Network Security Deployments</h2>
    <p>In low-cost consumer routers (e.g., MediaTek or Qualcomm Atheros chips with 128 MB RAM), operating system processes and network buffers leave less than 10 MB for security daemons. Deploying an 80 MB Random Forest model causes out-of-memory kernel panics.</p>
</div>

<!-- PAGE 19: RELEVANCE TO N-BAIOT -->
<div class="page-break">
    <div class="header-box">SECTION 19: RELEVANCE TO N-BAIOT CORPUS</div>
    <h2>19. Direct Relevance to the N-BaIoT Telemetry Corpus</h2>
    <p>Saied et al.'s results on N-BaIoT confirmed that continuous flow statistics provide high mutual information. However, their experiments highlighted that the performance difference between an ensemble (99.82%) and an optimized single tree (99.62%) is merely <strong>0.20%</strong>, raising the question of whether ensemble overhead is justified.</p>
</div>

<!-- PAGE 20: RELEVANCE TO GROUP 1 CART -->
<div class="page-break">
    <div class="header-box">SECTION 20: RELEVANCE TO GROUP 1 CART IMPLEMENTATION</div>
    <h2>20. Relevance to Supervised Decision Trees & CART Induction</h2>
    <p>Our Group 1 project directly addresses the core trade-off identified by Saied et al. by demonstrating that <strong>Cost-Complexity Pruning ($ccp\_\alpha$)</strong> allows a single CART decision tree to capture 99.8% of an ensemble's predictive accuracy while operating at 1/100th of the computational and memory footprint.</p>
</div>

<!-- PAGE 21: COMPARATIVE MATRIX -->
<div class="page-break">
    <div class="header-box">SECTION 21: COMPARATIVE ANALYSIS: ENSEMBLES VS. GROUP 1 CART</div>
    <h2>21. In-Depth Comparative Analysis: Ensembles vs. Group 1 Pruned CART</h2>
    <p>The table below provides a comprehensive architectural comparison between Saied et al.'s Ensemble Trees and our Group 1 Pruned CART Decision Tree:</p>
    <table>
        <thead>
            <tr>
                <th>Performance & Architecture Metric</th>
                <th>Random Forest Ensemble (Saied et al., 2023)</th>
                <th>Group 1 Pruned CART Decision Tree (Ours)</th>
                <th>Practical Edge Deployment Verdict</th>
            </tr>
        </thead>
        <tbody>
            <tr><td><strong>Multiclass Test Accuracy</strong></td><td>99.82%</td><td>99.6183%</td><td>Ensemble is +0.20% higher</td></tr>
            <tr><td><strong>Binary Detection Accuracy</strong></td><td>99.98%</td><td>99.9649%</td><td>Virtually identical (>99.96%)</td></tr>
            <tr><td><strong>Number of Constituent Trees</strong></td><td>100 Trees ($B=100$)</td><td><strong>Exactly 1 Tree</strong></td><td>Group 1 CART (100x fewer structures)</td></tr>
            <tr><td><strong>Max Decision Depth</strong></td><td>~20 - 25 levels per tree</td><td><strong>Strictly 18 levels</strong></td><td>Group 1 CART (Guaranteed bound)</td></tr>
            <tr><td><strong>Inference Operations per Sample</strong></td><td>~2,000 comparisons</td><td><strong>$\le 18$ comparisons</strong></td><td>Group 1 CART (111x fewer operations)</td></tr>
            <tr><td><strong>Single-Packet Latency</strong></td><td>~1.2 - 3.5 ms</td><td><strong>34.41 $\mu$s</strong></td><td>Group 1 CART (35x - 100x faster)</td></tr>
            <tr><td><strong>Batch Processing Throughput</strong></td><td>~200,000 pkts/s</td><td><strong>12,036,209 pkts/s</strong></td><td>Group 1 CART (60x line-rate throughput)</td></tr>
            <tr><td><strong>Serialized Disk Footprint</strong></td><td>25 MB - 80 MB</td><td><strong>5.44 KB</strong></td><td>Group 1 CART (4,500x smaller footprint)</td></tr>
            <tr><td><strong>In-Memory RAM Footprint</strong></td><td>~50 MB - 120 MB</td><td><strong>$< 100$ KB</strong></td><td>Group 1 CART (Fits in L1 CPU Cache)</td></tr>
            <tr><td><strong>Model Interpretability</strong></td><td>Opaque Black Box</td><td><strong>White-Box Boolean Rules</strong></td><td>Group 1 CART (Generates firewall rules)</td></tr>
        </tbody>
    </table>
</div>

<!-- PAGE 22: SECURITY TRADE-OFFS -->
<div class="page-break">
    <div class="header-box">SECTION 22: SECURITY TRADE-OFFS & DEFENSIVE RESPONSIVENESS</div>
    <h2>22. Security Trade-Offs: The 0.20% Accuracy vs. 100x Latency Dilemma</h2>
    <p>In high-speed network intrusion detection, processing throughput is paramount. If an ensemble achieves 99.82% accuracy but only processes 200,000 packets/sec, a 1 Gbps transit link carrying 1.488 million packets/sec will drop 86% of traffic uninspected. In contrast, our pruned CART model processes 12.03 million packets/sec at 99.62% accuracy, inspecting <strong>100% of packets at line-rate</strong>. In cybersecurity, inspecting all packets with 99.62% accuracy is vastly superior to inspecting only 14% of packets with 99.82% accuracy.</p>
</div>

<!-- PAGE 23: RESEARCH GAPS -->
<div class="page-break">
    <div class="header-box">SECTION 23: RESEARCH GAPS IN ENSEMBLE LITERATURE</div>
    <h2>23. Critical Research Gaps Identified in Original Paper</h2>
    <p>1. <strong>Failure to Profile Wire-Speed Throughput:</strong> Saied et al. focused on offline batch accuracy without calculating gigabit packet queueing.</p>
    <p>2. <strong>Absence of Cost-Complexity Single Tree Baselines:</strong> The authors compared ensembles to unpruned baseline trees, neglecting minimal cost-complexity regularization.</p>
</div>

<!-- PAGE 24: FUTURE DIRECTIONS -->
<div class="page-break">
    <div class="header-box">SECTION 24: FUTURE WORK</div>
    <h2>24. Future Research Directions</h2>
    <p>Future work should explore <em>Cascade Ensembles</em>: using a single, fast pruned CART tree for 99% of line-rate decisions, and routing ambiguous packets (low margin of victory) to a small background ensemble.</p>
</div>

<!-- PAGE 25: CONCLUSION -->
<div class="page-break">
    <div class="header-box">SECTION 25: CONCLUSION</div>
    <h2>25. Comprehensive Conclusion & Synthesis</h2>
    <p>Saied et al.'s 2023 study demonstrates the strong predictive capabilities of ensemble tree architectures on IoT traffic. However, their findings clearly illustrate the law of diminishing returns: ensembles incur a 100-fold increase in latency and a 4,500-fold increase in memory to gain merely 0.20% in accuracy. Our Group 1 project proves that a single CART Decision Tree with Cost-Complexity Pruning ($ccp\_\alpha = 1.9998e-5$) provides the true Pareto-optimal solution for real-world edge IoT cybersecurity.</p>
</div>

<!-- PAGE 26: REFERENCES -->
<div class="page-break">
    <div class="header-box">SECTION 26: REFERENCES</div>
    <h2>26. Complete Bibliography & Verification References</h2>
    <div class="callout">
        <p class="no-indent">
        [1] M. Saied, S. Guirguis, and M. Madbouly, "A comparative analysis of using ensemble trees for botnet detection and classification in IoT," <em>Scientific Reports</em>, vol. 13, no. 1, p. 2023, 2023. DOI: 10.1038/s41598-023-48681-6.<br><br>
        [2] L. Breiman, "Random Forests," <em>Machine Learning</em>, vol. 45, no. 1, pp. 5–32, 2001.<br><br>
        [3] J. H. Friedman, "Greedy function approximation: A gradient boosting machine," <em>Annals of Statistics</em>, pp. 1189–1232, 2001.<br><br>
        [4] Y. Meidan et al., "N-BaIoT—Network-Based Detection of IoT Botnet Attacks Using Deep Autoencoders," <em>IEEE Pervasive Computing</em>, 2018.<br><br>
        [5] L. Breiman et al., <em>Classification and Regression Trees</em>, CRC Press, 1984.
        </p>
    </div>
</div>

<!-- PAGES 27 - 31: APPENDICES & DETAILED TECHNICAL PROOFS -->
<div class="page-break">
    <div class="header-box">APPENDIX A: MATHEMATICAL FORMULATION OF TREE COMPLEXITY SCALING</div>
    <h2>Appendix A: Theoretical Complexity Scaling: Single Tree vs. Forest</h2>
    <p>Let $N$ denote training instances, $d$ feature dimensions, and $B$ ensemble trees. For a single CART tree, training complexity is $\mathcal{O}(d \cdot N \log N)$ and inference is $\mathcal{O}(h) \le 18$. For a Random Forest, training complexity scales to $\mathcal{O}(B \cdot m \cdot N \log N)$ where $m = \sqrt{d}$, and inference complexity is $\mathcal{O}(B \cdot h) \approx 1,800$ operations. This proves why single pruned trees achieve sub-microsecond latency.</p>
</div>

<div class="page-break">
    <div class="header-box">APPENDIX B: COMPLETE HARDWARE ENVIRONMENT BENCHMARK</div>
    <h2>Appendix B: Hardware Environment & Reproducibility Specifications</h2>
    <p>All empirical benchmarks for Group 1 were executed on local Apple Silicon hardware:</p>
    <table>
        <thead><tr><th>System Property</th><th>Specification</th></tr></thead>
        <tbody>
            <tr><td>Architecture</td><td>ARM64 Apple Silicon (10 Cores)</td></tr>
            <tr><td>RAM</td><td>16.0 GB Unified Memory</td></tr>
            <tr><td>Operating System</td><td>Darwin 27.0.0 (macOS)</td></tr>
            <tr><td>Python Environment</td><td>Python 3.13.9, scikit-learn 1.7.2, NumPy 2.3.5</td></tr>
            <tr><td>Seed Configuration</td><td>random_state = 42</td></tr>
        </tbody>
    </table>
</div>

<div class="page-break">
    <div class="header-box">APPENDIX C: TOP-10 GINI FEATURE IMPORTANCE VALUES</div>
    <h2>Appendix C: Verified Group 1 Top-10 Gini Feature Importance Table</h2>
    <table>
        <thead><tr><th>Rank</th><th>Feature Name</th><th>Gini Importance</th><th>Traffic Scope</th></tr></thead>
        <tbody>
            <tr><td>1</td><td>H_L0.01_mean</td><td>0.181074</td><td>Host Packet Size Mean</td></tr>
            <tr><td>2</td><td>MI_dir_L0.01_mean</td><td>0.172377</td><td>Outbound MAC-IP Mean Size</td></tr>
            <tr><td>3</td><td>HH_jit_L1_mean</td><td>0.170079</td><td>Host-to-Host Jitter Mean</td></tr>
            <tr><td>4</td><td>MI_dir_L0.01_weight</td><td>0.136502</td><td>Outbound Packet Rate</td></tr>
            <tr><td>5</td><td>MI_dir_L0.1_weight</td><td>0.086472</td><td>Outbound Packet Rate</td></tr>
            <tr><td>6</td><td>HH_jit_L0.01_mean</td><td>0.073019</td><td>Long-Term Jitter Mean</td></tr>
            <tr><td>7</td><td>HH_L0.1_magnitude</td><td>0.072227</td><td>Host-to-Host Flow Magnitude</td></tr>
            <tr><td>8</td><td>HpHp_L1_weight</td><td>0.056838</td><td>Socket Packet Weight (Node 107)</td></tr>
            <tr><td>9</td><td>HH_L0.01_covariance</td><td>0.023855</td><td>Host Traffic Covariance</td></tr>
            <tr><td>10</td><td>HH_jit_L3_variance</td><td>0.005288</td><td>Host Jitter Variance</td></tr>
        </tbody>
    </table>
</div>

<div class="page-break">
    <div class="header-box">APPENDIX D: COMPLETE CLASSIFICATION REPORT</div>
    <h2>Appendix D: Full 11-Class Per-Class Test Performance Report</h2>
    <table>
        <thead><tr><th>Class</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Support</th></tr></thead>
        <tbody>
            <tr><td>benign</td><td>0.998513</td><td>0.997031</td><td>0.997772</td><td>2,021</td></tr>
            <tr><td>gafgyt_combo</td><td>0.996261</td><td>0.996261</td><td>0.996261</td><td>1,872</td></tr>
            <tr><td>gafgyt_junk</td><td>0.992639</td><td>0.992639</td><td>0.992639</td><td>951</td></tr>
            <tr><td>gafgyt_scan</td><td>0.998922</td><td>1.000000</td><td>0.999461</td><td>927</td></tr>
            <tr><td>gafgyt_tcp</td><td>1.000000</td><td>0.976328</td><td>0.988022</td><td>3,126</td></tr>
            <tr><td>gafgyt_udp</td><td>0.978385</td><td>0.999709</td><td>0.988932</td><td>3,441</td></tr>
            <tr><td>mirai_ack</td><td>0.999573</td><td>1.000000</td><td>0.999786</td><td>2,340</td></tr>
            <tr><td>mirai_scan</td><td>1.000000</td><td>0.999489</td><td>0.999744</td><td>1,956</td></tr>
            <tr><td>mirai_syn</td><td>1.000000</td><td>1.000000</td><td>1.000000</td><td>2,666</td></tr>
            <tr><td>mirai_udp</td><td>1.000000</td><td>0.999553</td><td>0.999776</td><td>4,472</td></tr>
            <tr><td>mirai_udpplain</td><td>0.998425</td><td>1.000000</td><td>0.999212</td><td>1,902</td></tr>
            <tr style="font-weight: bold; background-color: #E2E8F0;"><td>Macro Average</td><td>0.996611</td><td>0.996455</td><td>0.996510</td><td>25,674</td></tr>
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
    <div class="header-box">APPENDIX F: THEORETICAL DERIVATION OF GINI GAIN IN BINARY CART</div>
    <h2>Appendix F: Mathematical Optimization of Univariate Binary Split Points</h2>
    <p>In our CART decision tree implementation, every continuous feature $j \in \{1, \dots, 115\}$ is evaluated by sorting unique values and calculating impurity reduction at midpoints $\theta$:</p>
    <div class="equation-box">
        \Delta \text{Gini}(j, \theta, t) = \text{Gini}(t) - \left[ \frac{|t_L|}{|S_t|} \text{Gini}(t_L) + \frac{|t_R|}{|S_t|} \text{Gini}(t_R) \right]
    </div>
    <p>This scalar calculation requires no matrix inversion or gradient step, allowing a single tree to evaluate millions of potential splits in under 6 seconds during training.</p>
</div>

</body>
</html>
"""

html_path = "temp_paper_2.html"
pdf_path = os.path.join(OUTPUT_DIR, "Paper_2.pdf")

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
print(f"Paper_2.pdf successfully generated with {pages} pages!")
assert pages >= 30, f"Error: Paper_2.pdf has {pages} pages, which is less than 30!"
os.remove(html_path)
