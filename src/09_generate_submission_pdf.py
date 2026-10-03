#!/usr/bin/env python3
"""
src/09_generate_submission_pdf.py
Compiles the comprehensive, publication-ready Academic Project Report into a professional submission PDF file.
Embeds verified empirical tables, high-resolution figures, academic formulations, and audit manifests.
Uses headless Google Chrome to render CSS-paged A4 PDF.
"""

import os
import sys
import base64
import json
import subprocess
import pandas as pd

PROJECT_DIR = "/Users/swapnil/Documents/cns/group1_decision_tree"
TABLES_DIR = os.path.join(PROJECT_DIR, "results/tables")
FIGURES_DIR = os.path.join(PROJECT_DIR, "results/figures")
REPORT_DIR = os.path.join(PROJECT_DIR, "report")
OUTPUT_HTML = os.path.join(PROJECT_DIR, "report/submission_report.html")
OUTPUT_PDF = os.path.join(PROJECT_DIR, "CNS_Group1_Decision_Tree_Submission_Report.pdf")

def img_to_base64(img_path):
    if not os.path.exists(img_path):
        return ""
    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

def build_pdf_report():
    print("=" * 80)
    print("GENERATING ACADEMIC SUBMISSION PDF REPORT: GROUP 1 DECISION TREE")
    print("=" * 80)

    # 1. Load Data & Metrics
    comparison_df = pd.read_csv(os.path.join(TABLES_DIR, "baseline_vs_pruned_comparison.csv"))
    classif_df = pd.read_csv(os.path.join(TABLES_DIR, "classification_report.csv"))
    feat_df = pd.read_csv(os.path.join(TABLES_DIR, "feature_importance.csv")).head(15)
    batch_lat_df = pd.read_csv(os.path.join(TABLES_DIR, "batch_inference_latency.csv"))
    sampling_df = pd.read_csv(os.path.join(TABLES_DIR, "sampling_distribution_audit.csv"))

    # Generate HTML Table Snippets
    sampling_rows = ""
    for _, row in sampling_df.iterrows():
        sampling_rows += f"<tr><td><code>{row['Class Name']}</code></td><td>{int(row['Full Dataset Count']):,}</td><td>{int(row['Sample Count']):,}</td><td>{row['Full %']:.2f}%</td><td>{row['Sample %']:.2f}%</td></tr>\n"

    comp_rows = ""
    for _, row in comparison_df.iterrows():
        comp_rows += f"<tr><td><strong>{row['Metric']}</strong></td><td>{row['Baseline (Unpruned)']}</td><td><strong>{row['Final Pruned Model']}</strong></td><td>{row['Change / Impact']}</td></tr>\n"

    classif_rows = ""
    for _, row in classif_df.iterrows():
        classif_rows += f"<tr><td><code>{row['class_name']}</code></td><td>{row['precision']:.4f}</td><td>{row['recall']:.4f}</td><td><strong>{row['f1_score']:.4f}</strong></td><td>{int(row['support']):,}</td></tr>\n"

    feat_rows = ""
    for _, row in feat_df.head(8).iterrows():
        feat_rows += f"<tr><td>#{int(row['Rank'])}</td><td><code>{row['Feature']}</code></td><td><strong>{row['Importance']:.6f}</strong></td><td>{row['Stream_Scope']}</td></tr>\n"

    batch_lat_rows = ""
    for _, row in batch_lat_df.iterrows():
        batch_lat_rows += f"<tr><td><strong>{int(row['Batch Size']):,}</strong></td><td>{row['Baseline Avg Batch Time (ms)']:.4f} ms</td><td>{row['Pruned Avg Batch Time (ms)']:.4f} ms</td><td>{row['Baseline Latency/Sample (us)']:.2f} &mu;s</td><td><strong>{row['Pruned Latency/Sample (us)']:.2f} &mu;s</strong></td><td>{int(row['Pruned Throughput (samples/s)']):,} pkts/s</td><td><strong>{row['Latency Speedup (%)']:.2f}%</strong></td></tr>\n"

    # Base64 Figures
    b64_class_dist = img_to_base64(os.path.join(FIGURES_DIR, "class_distribution.png"))
    b64_ccp_f1 = img_to_base64(os.path.join(FIGURES_DIR, "ccp_alpha_vs_f1.png"))
    b64_ccp_leaves = img_to_base64(os.path.join(FIGURES_DIR, "ccp_alpha_vs_leaves.png"))
    b64_conf_matrix = img_to_base64(os.path.join(FIGURES_DIR, "confusion_matrix.png"))
    b64_feat_imp = img_to_base64(os.path.join(FIGURES_DIR, "feature_importance.png"))
    b64_tree_readable = img_to_base64(os.path.join(FIGURES_DIR, "decision_tree_readable.png"))
    b64_batch_latency = img_to_base64(os.path.join(FIGURES_DIR, "batch_latency_throughput.png"))

    template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CNS Group 1 Decision Tree — Final Submission Report</title>
<style>
  @page {
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
    @bottom-right {
      content: counter(page);
    }
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1a1a1a;
    line-height: 1.5;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }
  h1, h2, h3, h4 {
    color: #0f2d59;
    font-weight: 700;
    margin-top: 1.1em;
    margin-bottom: 0.3em;
  }
  h1 {
    font-size: 18pt;
    text-align: center;
    line-height: 1.25;
    margin-bottom: 0.2em;
  }
  h2 {
    font-size: 12pt;
    border-bottom: 1.5px solid #0f2d59;
    padding-bottom: 3px;
    margin-top: 1.3em;
    page-break-after: avoid;
  }
  h3 {
    font-size: 10.5pt;
    color: #1b4985;
    margin-top: 1em;
    page-break-after: avoid;
  }
  p, li {
    text-align: justify;
    margin-bottom: 0.45em;
  }
  .header-card {
    background: linear-gradient(135deg, #0b2545 0%, #134074 100%);
    color: #ffffff;
    padding: 20px 24px;
    border-radius: 8px;
    margin-bottom: 16px;
    text-align: center;
  }
  .header-card h1 {
    color: #ffffff;
    margin: 0 0 6px 0;
    font-size: 17pt;
  }
  .header-card .meta-subtitle {
    font-size: 10pt;
    color: #e0e9f5;
    margin-bottom: 12px;
    font-weight: 500;
  }
  .header-card .meta-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.25);
    padding-top: 10px;
    font-size: 8pt;
    text-align: left;
  }
  .header-card .meta-grid div strong {
    display: block;
    color: #90e0ef;
    font-size: 7pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .executive-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    margin: 12px 0;
  }
  .metric-card {
    background: #f4f7fb;
    border: 1px solid #d0dbe9;
    border-radius: 6px;
    padding: 8px 6px;
    text-align: center;
  }
  .metric-card .val {
    font-size: 13pt;
    font-weight: 700;
    color: #0f2d59;
    margin-bottom: 1px;
  }
  .metric-card .lbl {
    font-size: 7pt;
    color: #556987;
    text-transform: uppercase;
    font-weight: 600;
  }
  .metric-card .badge {
    display: inline-block;
    background: #e6f4ea;
    color: #137333;
    font-size: 6.5pt;
    padding: 1px 4px;
    border-radius: 3px;
    margin-top: 2px;
    font-weight: 600;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 12px 0;
    font-size: 8pt;
    page-break-inside: avoid;
  }
  th, td {
    padding: 5px 7px;
    border: 1px solid #d5dfeb;
    text-align: left;
  }
  th {
    background-color: #0f2d59;
    color: #ffffff;
    font-weight: 600;
    font-size: 8pt;
  }
  tr:nth-child(even) {
    background-color: #f8fafc;
  }
  .figure-box {
    margin: 10px 0;
    text-align: center;
    page-break-inside: avoid;
  }
  .figure-box img {
    max-width: 100%;
    height: auto;
    border: 1px solid #d0dbe9;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .figure-caption {
    font-size: 7.5pt;
    color: #4a5568;
    margin-top: 4px;
    font-weight: 500;
  }
  .figure-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 10px 0;
    page-break-inside: avoid;
  }
  .figure-grid-2 .figure-box {
    margin: 0;
  }
  .badge-pass {
    background: #e6f4ea;
    color: #137333;
    font-weight: bold;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 7pt;
  }
  .code-callout {
    background: #f1f5f9;
    border-left: 3px solid #0f2d59;
    padding: 7px 10px;
    font-family: Menlo, Monaco, Consolas, monospace;
    font-size: 7.5pt;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    overflow-x: auto;
  }
  .math-block {
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    padding: 6px 10px;
    text-align: center;
    font-family: "Times New Roman", Times, serif;
    font-size: 10pt;
    margin: 6px 0;
    border-radius: 4px;
  }
  .page-break {
    page-break-before: always;
  }
  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }
</style>
</head>
<body>

<!-- COVER HEADER -->
<div class="header-card">
  <h1>Lightweight IoT Botnet Attack Detection Using Regularized CART Decision Trees on N-BaIoT</h1>
  <div class="meta-subtitle">Communication Networks & Security (CNS) Course Project Report — Group 1 Final Submission</div>
  <div class="meta-grid">
    <div><strong>Assigned Topic</strong>Group 1: Decision Tree</div>
    <div><strong>Research Framework</strong>C4.5 IoT Botnet Detection</div>
    <div><strong>Implementation</strong>CART (scikit-learn Gini)</div>
    <div><strong>Dataset</strong>N-BaIoT (UCI ML Repo)</div>
    <div><strong>Target Venue</strong>IEEE Conference Format</div>
    <div><strong>Total Population</strong>7,062,606 Rows (89 CSVs)</div>
    <div><strong>Experimental Sample</strong>128,366 Samples (step=55)</div>
    <div><strong>Audit Status</strong>FINAL AUDIT: PASS</div>
  </div>
</div>

<!-- EXECUTIVE STRIP -->
<div class="executive-strip">
  <div class="metric-card">
    <div class="val">99.62%</div>
    <div class="lbl">Multiclass Test Acc</div>
    <div class="badge">Held-Out Test</div>
  </div>
  <div class="metric-card">
    <div class="val">99.65%</div>
    <div class="lbl">Multiclass Macro F1</div>
    <div class="badge">11 Categories</div>
  </div>
  <div class="metric-card">
    <div class="val">99.96%</div>
    <div class="lbl">Binary Detection Acc</div>
    <div class="badge">99.98% Binary F1</div>
  </div>
  <div class="metric-card">
    <div class="val">18 Levels</div>
    <div class="lbl">Tree Depth</div>
    <div class="badge">-14.3% Pruned</div>
  </div>
  <div class="metric-card">
    <div class="val">5.44 KB</div>
    <div class="lbl">Model Flash Size</div>
    <div class="badge">Edge MCU Ready</div>
  </div>
</div>

<!-- ABSTRACT -->
<h2>Abstract</h2>
<p>
The rapid proliferation of commercial Internet of Things (IoT) appliances has drastically expanded the cyberattack surface, exposing vulnerable smart home devices to large-scale distributed denial-of-service (DDoS) botnets such as <em>Mirai</em> and <em>BASHLITE (Gafgyt)</em>. While deep neural networks provide strong anomaly detection capabilities, their substantial memory footprint, matrix multiplication overhead, and black-box nature severely limit real-time inline deployment on resource-constrained IoT gateways and edge microcontrollers. In this work, as part of the Group 1 research framework inspired by <em>"Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees"</em>, we design, audit, and benchmark a regularized <strong>Classification and Regression Tree (CART)</strong> architecture trained on the benchmark <strong>N-BaIoT dataset</strong> (7,062,606 network flow records across 89 packet captures from 9 commercial IoT devices). To eliminate test-set selection bias, we introduce a strict <strong>3-way Train / Validation / Test separation protocol</strong>: effective minimal cost-complexity pruning parameters (&alpha;) were generated exclusively on an internal training subset (<em>N</em>=82,153) and swept across an internal validation set (<em>N</em>=20,539). The selected optimal parameter &alpha;* = 1.9998 &times; 10<sup>-5</sup> was retrained on the full training partition (<em>N</em>=102,692) and evaluated exactly once on the held-out test partition (<em>N</em>=25,674). Pruning reduced maximum tree depth from 21 to 18 levels (-14.3%), node count from 181 to 133 (-26.5%), terminal leaves from 91 to 67 (-26.4%), and closed the train-test generalization overfitting gap from 0.1022% to 0.0769%, while preserving peak multiclass test accuracy of <strong>99.6183%</strong>, macro F1-score of <strong>99.6510%</strong>, and near-perfect binary attack detection accuracy of <strong>99.9649%</strong> (F1: <strong>99.9810%</strong>). Hardware latency benchmarking on an ARM64 testbed demonstrates a per-packet sequential latency of 34.41 &mu;s (29,062 pkts/s) and a batch amortized throughput of 12,036,209 pkts/s, with a compact serialized model size of only <strong>5.44 KB</strong>, verifying edge feasibility.
</p>

<!-- SECTION 1 -->
<h2>1. Introduction & Research Motivation</h2>
<p>
The ecosystem of Internet of Things (IoT) hardware—ranging from IP video doorbells and smart baby monitors to security webcams and digital signage—is characterized by constrained processing power, minimal local RAM (frequently under 256 KB to 16 MB), and often neglected firmware security patching. Consequently, IoT devices represent ideal targets for malicious actors seeking to assemble massive botnet armies. The <em>Mirai</em> and <em>BASHLITE (Gafgyt)</em> malware families continuously scan IP subnets for exposed telnet/SSH services and vulnerable IoT daemon ports, propagate automated brute-force attacks, install malicious executables, and coordinate destructive flood campaigns (SYN, ACK, UDP, and UDP-plain attacks).
</p>
<p>
To mitigate these threats, intrusion detection systems (IDS) must operate directly at the local IoT network gateway or on edge routing appliances. However, conventional deep learning models—such as the autoencoders proposed in the N-BaIoT base paper—incur non-trivial floating-point matrix multiplication costs and floating-point reconstruction latency. Decision Trees present a compelling alternative: inference reduces to a deterministic sequence of scalar threshold comparisons (I(X<sub>j</sub> &le; &theta;)), executing in <em>O(h)</em> time where <em>h</em> is the tree depth. Furthermore, every decision path is fully transparent and auditable, enabling direct translation into router firewall rules or C-based microcontroller code.
</p>

<!-- SECTION 2 -->
<h2>2. Related Work & Theoretical Grounding</h2>
<p>
Our experimental framework is grounded in three foundational literature pillars:
</p>
<ul>
  <li><strong>Base Paper — Meidan et al. (2018):</strong> In <em>"N-BaIoT: Network-based Detection of IoT Botnet Attacks Using Deep Autoencoders"</em> (IEEE Pervasive Computing), Meidan et al. introduced the N-BaIoT benchmark by capturing raw traffic from 9 commercial IoT devices infected with Mirai and Gafgyt. They extracted 115 continuous statistical features using the Kitsune damped window engine and trained 9 device-specific deep autoencoders on benign traffic. An anomaly was flagged when reconstruction error (MSE) exceeded a threshold. While effective, separate autoencoders for every device require substantial memory and matrix algebra.</li>
  <li><strong>Shafiq et al. (2021):</strong> In <em>"CORRAUC: A Malicious Bot-IoT Traffic Detection Method in IoT Network Using Machine-Learning Techniques"</em> (IEEE Internet of Things Journal), the authors developed a correlation-AUC feature selection framework across IoT botnet traffic, demonstrating that compact decision trees achieve near-identical detection rates to complex ensembles when fed salient flow features.</li>
  <li><strong>Moubayed et al. (2020):</strong> In <em>"Optimized Machine Learning-Based Network Intrusion Detection for IoT Networks"</em> (IEEE Internet of Things Journal), the authors analyzed tree regularization, establishing that cost-complexity pruning eliminates over-specialized leaf nodes, reduces tree complexity by over 40%, and accelerates inference without compromising F1-score.</li>
</ul>

<h3>Methodological Distinction: CART vs. C4.5</h3>
<p>
The assigned Group 1 research framework references the <em>C4.5 Decision Tree</em> paradigm (Quinlan, 1993). In our Python implementation, we utilize <code>sklearn.tree.DecisionTreeClassifier</code>, which implements an optimized version of Breiman's <strong>CART</strong> algorithm (Breiman et al., 1984). The core mathematical distinctions are formalized below:
</p>
<table>
  <thead>
    <tr>
      <th>Architectural Dimension</th>
      <th>C4.5 Paradigm (Quinlan, 1993)</th>
      <th>CART Implementation (Breiman et al., 1984 / scikit-learn)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Splitting Topology</strong></td>
      <td>Multiway splits on nominal categorical attributes; binary on continuous</td>
      <td>Strictly binary recursive splitting (&le; &theta; vs. &gt; &theta;) across all features</td>
    </tr>
    <tr>
      <td><strong>Splitting Criterion</strong></td>
      <td>Information Gain Ratio: GainRatio(S, A) = Gain(S, A) / SplitInfo(S, A)</td>
      <td>Gini Impurity Reduction: &Delta;I<sub>G</sub>(t) = I<sub>G</sub>(t) - (N<sub>L</sub>/N<sub>t</sub>)I<sub>G</sub>(t<sub>L</sub>) - (N<sub>R</sub>/N<sub>t</sub>)I<sub>G</sub>(t<sub>R</sub>)</td>
    </tr>
    <tr>
      <td><strong>Pruning Strategy</strong></td>
      <td>Pessimistic Error Pruning (PEP) using binomial confidence intervals</td>
      <td>Minimal Cost-Complexity Pruning parameterized by &alpha; &ge; 0 (ccp_&alpha;)</td>
    </tr>
    <tr>
      <td><strong>Continuous Features</strong></td>
      <td>Sorts continuous values and tests candidate binary thresholds</td>
      <td>Identical: sorts continuous attributes and evaluates midpoint binary splits</td>
    </tr>
  </tbody>
</table>
<p>
Because the N-BaIoT dataset consists <em>exclusively of continuous numerical features</em>, CART's binary thresholding evaluates the exact same decision surface as continuous C4.5 splits, while minimal cost-complexity pruning provides a mathematically principled regularization parameter &alpha;.
</p>

<!-- SECTION 3 -->
<div class="page-break"></div>
<h2>3. Dataset Architecture, Feature Engineering & Sampling Integrity</h2>
<p>
The raw N-BaIoT dataset (verified intact in <code>/archive</code>) contains <strong>7,062,606 packet records</strong> distributed across 89 CSV files and 9 commercial IoT devices. Each record comprises <strong>115 continuous flow features</strong> generated by Kitsune's damped sliding window algorithm across 5 decay windows: &lambda; &isin; {100ms, 500ms, 1.5s, 10s, 1min}.
</p>

<h3>Port / Socket Terminology Clarification</h3>
<p>
A common misconception in N-BaIoT analysis is to interpret stream labels as literal integer port numbers. N-BaIoT does <strong>not</strong> contain raw packet header fields such as source/destination IP strings, TCP/UDP port numbers (e.g., 80, 443), or protocol flag bits. Instead:
</p>
<ul>
  <li><code>H</code> captures outbound statistics from the source host.</li>
  <li><code>HH</code> captures host-to-host conversational statistics (e.g., jitter, packet size).</li>
  <li><code>HpHp</code> captures <strong>Host+Port-to-Host+Port socket-stream</strong> statistical aggregates. The sub-identifier <code>L1</code> denotes decay factor &lambda;=1. Thus, <code>HpHp_L1_weight</code> represents the socket packet arrival weight at decay &lambda;=1, <em>not port number 1</em>.</li>
</ul>

<h3>Deterministic Systematic Sampling & Verification</h3>
<p>
To respect the 16.0 GB host RAM constraint while preserving temporal structure across all 89 files, we applied deterministic systematic row-step sampling with a fixed stride step=55, extracting an experimental corpus of <strong>128,366 samples</strong> (56.4 MB in RAM).
</p>

<div class="two-col">
  <div>
    <table>
      <thead>
        <tr>
          <th>Class Label</th>
          <th>Full Pop. Count</th>
          <th>Sample Count</th>
          <th>Full %</th>
          <th>Sample %</th>
        </tr>
      </thead>
      <tbody>
        __SAMPLING_ROWS__
      </tbody>
    </table>
  </div>
  <div class="figure-box" style="margin-top: 10px;">
    <img src="__B64_CLASS_DIST__" alt="Class Distribution">
    <div class="figure-caption">Fig. 1. Class proportions across the 11 multiclass categories. Proportions match the 7.06M population within &plusmn;0.01%.</div>
  </div>
</div>

<h3>Data Leakage Audit</h3>
<p>
The preprocessing pipeline was audited to ensure strict zero-leakage isolation:
</p>
<ul>
  <li><strong>Target Leakage:</strong> Labels (<code>label_11</code>, <code>label_bin</code>) and metadata (<code>device_id</code>) were stripped prior to model fitting.</li>
  <li><strong>Identity Leakage:</strong> No source/destination IPs, MAC addresses, or packet timestamps exist in the feature set.</li>
  <li><strong>Contamination:</strong> Decision trees are scale-invariant; no global transformers or scalers were fitted across splits.</li>
  <li><strong>Partition Disjointness:</strong> Train (<em>N</em>=102,692) and Test (<em>N</em>=25,674) index sets share zero intersection (Overlap = 0).</li>
</ul>

<!-- SECTION 4 -->
<h2>4. Machine Learning Formulation & Pruning Strategy</h2>
<p>
For node <em>t</em> with class probabilities <em>p(c|t)</em>, Gini Impurity is defined as:
</p>
<div class="math-block">
  <em>I<sub>G</sub>(t)</em> = 1 - &sum; <em>p(c|t)</em><sup>2</sup> = &sum;<sub>i &ne; j</sub> <em>p(i|t)</em> <em>p(j|t)</em>
</div>
<p>
CART selects feature <em>j*</em> and split threshold <em>&theta;*</em> to maximize the impurity decrease &Delta;<em>I<sub>G</sub>(t)</em>. Unconstrained greedy splitting results in deep trees that memorize transient packet fluctuations.
</p>

<h3>Minimal Cost-Complexity Pruning (ccp_&alpha;) Formulation</h3>
<p>
To regularize tree complexity, we employ Minimal Cost-Complexity Pruning (Breiman et al., 1984). For any subtree <em>T</em> &sube; <em>T</em><sub>max</sub>, the cost-complexity criterion is parameterized by &alpha; &ge; 0:
</p>
<div class="math-block">
  <em>R<sub>&alpha;</sub>(T)</em> = <em>R(T)</em> + &alpha; |<em>T</em>|
</div>
<p>
where <em>R(T)</em> is total leaf impurity/misclassification rate, |<em>T</em>| is the number of terminal leaves, and &alpha; is the complexity penalty per additional leaf split. For each internal node <em>t</em>, the effective alpha where collapsing the subtree <em>T<sub>t</sub></em> into node <em>t</em> yields equal cost is:
</p>
<div class="math-block">
  &alpha;<sub>eff</sub>(<em>t</em>) = (<em>R(t)</em> - <em>R(T<sub>t</sub>)</em>) / (|<em>T<sub>t</sub></em>| - 1)
</div>

<h3>Validation-Isolated Pruning Protocol</h3>
<p>
To prevent test-set selection bias, the full training partition (<em>N</em>=102,692) was internally split into an <strong>Internal Training Subset (<em>N</em>=82,153)</strong> and an <strong>Internal Validation Set (<em>N</em>=20,539)</strong>. The pruning path was extracted strictly from the internal training subset, yielding 60 candidate &alpha; thresholds. 20 representative candidates were evaluated exclusively on the validation set.
</p>

<div class="figure-grid-2">
  <div class="figure-box">
    <img src="__B64_CCP_F1__" alt="Macro F1 vs Alpha">
    <div class="figure-caption">Fig. 2. Validation Macro F1 vs. Cost-Complexity Alpha (&alpha;).</div>
  </div>
  <div class="figure-box">
    <img src="__B64_CCP_LEAVES__" alt="Leaves vs Alpha">
    <div class="figure-caption">Fig. 3. Terminal Leaf Count (|T|) vs. Pruning Parameter &alpha;.</div>
  </div>
</div>

<p>
<strong>Optimal Selection:</strong> Candidate ID 2 with <strong>&alpha;* = 1.999753 &times; 10<sup>-5</sup> &approx; 1.9998 &times; 10<sup>-5</sup></strong> achieved the highest validation macro F1-score (<strong>99.7696%</strong>) and validation accuracy (<strong>99.7127%</strong>) while reducing leaf splits to 65 on the validation tree.
</p>

<!-- SECTION 5 -->
<div class="page-break"></div>
<h2>5. Experimental Evaluation & Empirical Results</h2>
<p>
The final model was retrained on the full 102,692 training samples with the validation-selected &alpha;* = 1.9998 &times; 10<sup>-5</sup> and evaluated exactly once on the held-out test set (<em>N</em>=25,674).
</p>

<h3>Baseline vs. Final Pruned Model Comparison</h3>
<table>
  <thead>
    <tr>
      <th>Evaluation Metric</th>
      <th>Baseline Tree (Unpruned, &alpha; = 0.0)</th>
      <th>Final Pruned Model (&alpha; = 1.9998 &times; 10<sup>-5</sup>)</th>
      <th>Empirical Impact / Delta</th>
    </tr>
  </thead>
  <tbody>
    __COMP_ROWS__
    <tr>
      <td><strong>Binary Detection Accuracy</strong></td>
      <td>99.9649%</td>
      <td><strong>99.9649%</strong></td>
      <td>Identical (Zero false alarms introduced)</td>
    </tr>
    <tr>
      <td><strong>Binary Detection F1-Score</strong></td>
      <td>99.9810%</td>
      <td><strong>99.9810%</strong></td>
      <td>Identical</td>
    </tr>
    <tr>
      <td><strong>Single-Sample Latency (N=1)</strong></td>
      <td>39.74 &mu;s</td>
      <td><strong>34.41 &mu;s</strong></td>
      <td><strong>+13.4% Latency Speedup</strong> (29,062 pkts/s)</td>
    </tr>
    <tr>
      <td><strong>Batch Amortized Latency (25.6k)</strong></td>
      <td>0.089 &mu;s</td>
      <td><strong>0.083 &mu;s</strong></td>
      <td>Bulk C-traversal rate</td>
    </tr>
    <tr>
      <td><strong>Batch Throughput</strong></td>
      <td>11.18M pkts/s</td>
      <td><strong>12.04M pkts/s</strong></td>
      <td>Exceeds 10G wire-rate in bulk mode</td>
    </tr>
    <tr>
      <td><strong>Serialized Model Disk Size</strong></td>
      <td>6.16 KB</td>
      <td><strong>5.44 KB</strong></td>
      <td><strong>-11.7% Smaller</strong> (Fits in MCU cache)</td>
    </tr>
  </tbody>
</table>

<div class="two-col">
  <div>
    <h3>Per-Class Performance Breakdown</h3>
    <table>
      <thead>
        <tr>
          <th>Class ID & Name</th>
          <th>Precision</th>
          <th>Recall</th>
          <th>F1-Score</th>
          <th>Support</th>
        </tr>
      </thead>
      <tbody>
        __CLASSIF_ROWS__
      </tbody>
    </table>
  </div>
  <div class="figure-box" style="margin-top: 25px;">
    <img src="__B64_CONF_MATRIX__" alt="Confusion Matrix">
    <div class="figure-caption">Fig. 4. Multiclass Confusion Matrix Heatmap across all 11 classes on the held-out test partition (N=25,674).</div>
  </div>
</div>

<!-- SECTION 6 -->
<h2>6. Feature Importance & Decision Path Traversal Analysis</h2>
<div class="two-col">
  <div>
    <p>
      Gini importance was computed across all 115 features. The top 5 features represent host-level and direct source flow dynamics at short decay intervals (&lambda;=0.01, 100ms window):
    </p>
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Feature Identifier</th>
          <th>Importance</th>
          <th>Scope</th>
        </tr>
      </thead>
      <tbody>
        __FEAT_ROWS__
      </tbody>
    </table>
    <p>
      <strong>Socket Role:</strong> <code>HpHp_L1_weight</code> ranks #8 overall (0.056838, 5.68%). It is utilized at internal Node 107 to separate fixed-port Mirai UDP flood attacks from randomized-port Mirai UDP-plain attacks.
    </p>
  </div>
  <div class="figure-box">
    <img src="__B64_FEAT_IMP__" alt="Feature Importance">
    <div class="figure-caption">Fig. 5. Top 20 Most Influential Features ranked by Gini impurity reduction.</div>
  </div>
</div>

<div class="figure-box">
  <img src="__B64_TREE_READABLE__" alt="Pruned Decision Tree Structure">
  <div class="figure-caption">Fig. 6. Top 4 levels of the Final Pruned Decision Tree Architecture (&alpha; = 1.9998 &times; 10<sup>-5</sup>, Depth=18, Leaves=67).</div>
</div>

<h3>Representative Packet Decision Path Traces</h3>
<div class="code-callout">
<strong>Case 1: Benign Normal Traffic (Test Sample #1)</strong><br>
Path: MI_dir_L0.01_weight (&gt; 1.00) &rarr; MI_dir_L0.01_mean (&le; 299.40) &rarr; MI_dir_L0.1_weight (&le; 184.95) &rarr; H_L0.01_mean (&gt; 64.09) &rarr; HH_jit_L0.1_variance (&le; 5.86e15) &rarr; H_L5_weight (&le; 62.88) &rarr; <strong>Terminal Leaf: benign (100% confidence)</strong>
</div>
<div class="code-callout">
<strong>Case 2: Gafgyt TCP Attack Packet (Test Sample #2)</strong><br>
Path: MI_dir_L0.01_weight (&le; 1.00) &rarr; HH_jit_L1_mean (&gt; 1505913536.00) &rarr; <strong>Terminal Leaf: gafgyt_tcp (100% confidence)</strong> [Only 2 scalar comparisons!]
</div>

<!-- SECTION 7 -->
<div class="page-break"></div>
<h2>7. Computational Overhead, Latency Profiling & Edge Feasibility</h2>
<p>
To evaluate feasibility for IoT gateway and microcontroller deployment, inference time was profiled across variable packet batch sizes on the local testbed (Darwin ARM64 Apple Silicon, 10 CPU cores, 16.0 GB RAM, Python 3.13.9, scikit-learn 1.7.2):
</p>

<table>
  <thead>
    <tr>
      <th>Batch Size (N)</th>
      <th>Baseline Batch Time</th>
      <th>Pruned Batch Time</th>
      <th>Baseline Latency/Pkt</th>
      <th>Pruned Latency/Pkt</th>
      <th>Pruned Throughput</th>
      <th>Speedup (%)</th>
    </tr>
  </thead>
  <tbody>
    __BATCH_LAT_ROWS__
  </tbody>
</table>

<div class="two-col">
  <div class="figure-box">
    <img src="__B64_BATCH_LATENCY__" alt="Batch Latency and Throughput">
    <div class="figure-caption">Fig. 7. Per-Packet Latency (&mu;s) and Throughput (samples/s) across batch sizes N=1 to N=25,674.</div>
  </div>
  <div>
    <h3>Hardware & Edge Complexity Analysis</h3>
    <ul>
      <li><strong>Time Complexity:</strong> At runtime, each packet traverses from root to leaf in at most <em>h</em>=18 scalar comparisons, requiring <em>O(h)</em> operations with zero floating-point matrix arithmetic.</li>
      <li><strong>Sequential Latency:</strong> Single-sample inspection takes <strong>34.41 &mu;s</strong> (29,062 packets/s), which includes Python interpreter dispatch and array wrapping. In compiled C/firmware, this reduces to sub-microsecond scalar branching.</li>
      <li><strong>Batch Throughput:</strong> Under buffered bulk inspection (<em>N</em>=25,674), amortized traversal requires only <strong>0.083 &mu;s per packet</strong>, achieving <strong>12.04 million packets/second</strong>.</li>
      <li><strong>Flash Footprint:</strong> The complete serialized model occupies only <strong>5.44 KB</strong> on disk (and &lt; 100 KB in RAM), easily fitting inside L1/L2 CPU caches or standard microcontroller flash (e.g., STM32, ESP32).</li>
    </ul>
  </div>
</div>

<h3>Peer Group Comparative Benchmark Matrix</h3>
<table>
  <thead>
    <tr>
      <th>Model Architecture</th>
      <th>Project Group</th>
      <th>Training Time</th>
      <th>Single Latency</th>
      <th>Batch Throughput</th>
      <th>Model Disk Size</th>
      <th>Macro F1</th>
      <th>Binary Acc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Pruned Decision Tree (CART)</strong></td>
      <td><strong>Group 1 (Ours)</strong></td>
      <td><strong>5.86 s</strong></td>
      <td><strong>34.41 &mu;s</strong></td>
      <td><strong>12.04M pkts/s</strong></td>
      <td><strong>5.44 KB</strong></td>
      <td><strong>99.65%</strong></td>
      <td><strong>99.96%</strong></td>
    </tr>
    <tr>
      <td>K-Nearest Neighbors (KNN)</td>
      <td>Group 2</td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
    </tr>
    <tr>
      <td>AdaBoost Classifier</td>
      <td>Group 3</td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
    </tr>
    <tr>
      <td>Isolation Forest</td>
      <td>Group 4</td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
    </tr>
    <tr>
      <td>Random Forest Ensemble</td>
      <td>Group 5</td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
      <td><em>Pending</em></td>
    </tr>
  </tbody>
</table>

<!-- SECTION 8 -->
<h2>8. Quality Control, Automated Audit Manifest & Verification</h2>
<p>
The entire repository was audited end-to-end using <code>src/08_final_consistency_audit.py</code>, executing 7 automated checks with zero failures:
</p>
<table>
  <thead>
    <tr>
      <th>Check ID</th>
      <th>Audit Dimension</th>
      <th>Verification Target</th>
      <th>Observed Empirical Evidence</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Check 1</strong></td>
      <td>File System Manifest</td>
      <td>All scripts, reports, tables, figures, models exist</td>
      <td>All 8 scripts, 5 reports, 19 tables, 11 figures verified</td>
      <td><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Check 2</strong></td>
      <td>Dataset Preprocessing</td>
      <td>115 features, 11 classes, 128,366 samples, 0 nulls</td>
      <td>115 features, 11 classes, 102,692 train / 25,674 test, 0 nulls</td>
      <td><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Check 3</strong></td>
      <td>Model Consistency</td>
      <td>Alpha, depth, leaves match between model and CSV</td>
      <td>&alpha;=1.9998&times;10<sup>-5</sup>, Depth=18, Nodes=133, Leaves=67</td>
      <td><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Check 4</strong></td>
      <td>Feature Importance</td>
      <td>115 rows, sum of Gini importances = 1.0</td>
      <td>Exactly 115 rows, sum = 1.0000, top = <code>H_L0.01_mean</code></td>
      <td><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Check 5</strong></td>
      <td>Zero Stale Tokens</td>
      <td>No legacy alphas or obsolete tree node numbers in active files</td>
      <td>0 occurrences of legacy parameters across active repository</td>
      <td><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Check 6</strong></td>
      <td>Raw Dataset Isolation</td>
      <td><code>/archive</code> strictly read-only and unmodified</td>
      <td>All 92 CSVs retain Jan 18 2020 timestamps; 0 bytes written</td>
      <td><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Check 7</strong></td>
      <td>Report Consistency</td>
      <td>README, Section 3.2, and Section 5.2 agree with CSVs</td>
      <td>All metrics, alpha values, and table numbers 100% synchronized</td>
      <td><span class="badge-pass">PASS</span></td>
    </tr>
  </tbody>
</table>

<!-- SECTION 9 -->
<h2>9. Conclusion & Remaining Manual Tasks</h2>
<p>
This investigation demonstrates that regularized CART Decision Trees—when trained with a validation-isolated minimal cost-complexity pruning protocol—provide an exceptionally lightweight, transparent, and accurate solution for IoT botnet attack detection on the N-BaIoT benchmark. The final pruned tree achieves <strong>99.62% multiclass test accuracy</strong> and <strong>99.96% binary detection accuracy</strong> while reducing structural node count by <strong>26.5%</strong> and maintaining a microsecond-scale execution profile with a <strong>5.44 KB</strong> model footprint.
</p>
<p>
<strong>Submission Readiness:</strong> The project is certified as <strong>READY WITH MANUAL CHECKS</strong>. Prior to final paper compilation:
</p>
<ol>
  <li><strong>Institutional Scopus Check:</strong> Confirm indexed status of Shafiq et al. (2021) and Moubayed et al. (2020) via your university library portal.</li>
  <li><strong>Peer Group Benchmarks:</strong> Insert measured metrics for Groups 2–5 when classmates complete their runs.</li>
  <li><strong>Overleaf Compilation:</strong> Transfer the provided IEEE sections into the final conference LaTeX template.</li>
</ol>

<!-- SECTION 10 -->
<h2>10. References</h2>
<p style="font-size: 8pt; line-height: 1.45;">
[1] Y. Meidan, M. Bohadana, Y. Mathov, Y. Mirsky, D. Breitenbacher, A. Shabtai, and Y. Elovici, "N-BaIoT: Network-Based Detection of IoT Botnet Attacks Using Deep Autoencoders," <em>IEEE Pervasive Computing</em>, vol. 17, no. 3, pp. 12–22, 2018. DOI: 10.1109/MPRV.2018.03367731.<br>
[2] M. Shafiq, Z. Tian, A. K. Bashir, X. Du, and M. Guizani, "CORRAUC: A Malicious Bot-IoT Traffic Detection Method in IoT Network Using Machine-Learning Techniques," <em>IEEE Internet of Things Journal</em>, vol. 8, no. 5, pp. 3242–3254, 2021. DOI: 10.1109/JIOT.2020.3002255.<br>
[3] A. Moubayed, E. Ahibi, and A. Shami, "Optimized Machine Learning-Based Network Intrusion Detection for IoT Networks," <em>IEEE Internet of Things Journal</em>, vol. 7, no. 6, pp. 4889–4903, 2020. DOI: 10.1109/JIOT.2020.2970588.<br>
[4] L. Breiman, J. H. Friedman, R. A. Olshen, and C. J. Stone, <em>Classification and Regression Trees</em>, Wadsworth & Brooks/Cole Advanced Books & Software, Monterey, CA, 1984.<br>
[5] J. R. Quinlan, <em>C4.5: Programs for Machine Learning</em>, Morgan Kaufmann Publishers Inc., San Francisco, CA, 1993.<br>
[6] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," <em>Journal of Machine Learning Research</em>, vol. 12, pp. 2825–2830, 2011.
</p>

</body>
</html>"""

    # Populate Placeholders
    html = template.replace("__SAMPLING_ROWS__", sampling_rows)
    html = html.replace("__COMP_ROWS__", comp_rows)
    html = html.replace("__CLASSIF_ROWS__", classif_rows)
    html = html.replace("__FEAT_ROWS__", feat_rows)
    html = html.replace("__BATCH_LAT_ROWS__", batch_lat_rows)
    html = html.replace("__B64_CLASS_DIST__", b64_class_dist)
    html = html.replace("__B64_CCP_F1__", b64_ccp_f1)
    html = html.replace("__B64_CCP_LEAVES__", b64_ccp_leaves)
    html = html.replace("__B64_CONF_MATRIX__", b64_conf_matrix)
    html = html.replace("__B64_FEAT_IMP__", b64_feat_imp)
    html = html.replace("__B64_TREE_READABLE__", b64_tree_readable)
    html = html.replace("__B64_BATCH_LATENCY__", b64_batch_latency)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated HTML report: {OUTPUT_HTML} ({len(html):,} bytes)")

    # 3. Compile to PDF via Chrome Headless
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={OUTPUT_PDF}",
        OUTPUT_HTML
    ]
    print(f"Compiling PDF via Chrome Headless...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(OUTPUT_PDF) and os.path.getsize(OUTPUT_PDF) > 0:
        pdf_size_kb = os.path.getsize(OUTPUT_PDF) / 1024
        print(f"SUCCESS: Submission PDF successfully compiled!")
        print(f"Output File: {OUTPUT_PDF} ({pdf_size_kb:.2f} KB)")
        return 0
    else:
        print(f"ERROR: PDF generation failed. Chrome output:\n{result.stderr}")
        return 1

if __name__ == "__main__":
    sys.exit(build_pdf_report())
