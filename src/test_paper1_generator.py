import os
import subprocess

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Research Review: N-BaIoT Deep Autoencoders</title>
<style>
@page {
    size: A4 portrait;
    margin: 20mm 18mm 20mm 18mm;
    @bottom-center {
        content: counter(page);
    }
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Times New Roman", Times, serif;
    line-height: 1.55;
    color: #1A1A1A;
    font-size: 10.5pt;
}
.cover-page {
    page-break-after: always;
    text-align: center;
    padding-top: 60px;
}
.page-break {
    page-break-before: always;
    break-before: page;
}
h1.title {
    font-size: 20pt;
    font-weight: bold;
    color: #0C2340;
    margin-bottom: 25px;
    line-height: 1.3;
}
h2 {
    font-size: 13pt;
    color: #1A365D;
    border-bottom: 1.5px solid #2B6CB0;
    padding-bottom: 4px;
    margin-top: 20px;
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
    margin-bottom: 10px;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 14px 0;
    font-size: 9.5pt;
}
th, td {
    border: 1px solid #CBD5E0;
    padding: 6px 10px;
    text-align: left;
}
th {
    background-color: #2B6CB0;
    color: white;
    font-weight: bold;
}
tr:nth-child(even) {
    background-color: #F7FAFC;
}
.equation-box {
    background-color: #EDF2F7;
    border-left: 4px solid #3182CE;
    padding: 8px 12px;
    margin: 12px 0;
    font-family: "Courier New", Courier, monospace;
    font-size: 9.5pt;
}
.citation-box {
    border: 1px solid #A0AEC0;
    background-color: #F7FAFC;
    padding: 12px;
    margin: 15px 0;
    border-radius: 4px;
}
.page-number {
    text-align: right;
    font-size: 8.5pt;
    color: #718096;
}
</style>
</head>
<body>
"""

# Let's generate a test HTML with 32 distinct sections
html_content += """
<div class="cover-page">
    <div style="font-size: 13pt; font-weight: bold; color: #4A5568; margin-bottom: 10px;">
        SARDAR PATEL INSTITUTE OF TECHNOLOGY, MUMBAI
    </div>
    <div style="font-size: 11pt; color: #718096; margin-bottom: 30px;">
        Department of Computer Engineering | Cryptography and Network Security (CNS A.Y. 2026–27)
    </div>
    
    <div style="border-top: 3px solid #0C2340; border-bottom: 3px solid #0C2340; padding: 30px 10px; margin: 40px 0;">
        <h1 class="title">
            Research Review and Comprehensive Technical Analysis of:<br>
            <span style="color: #2B6CB0;">N-BaIoT—Network-Based Detection of IoT Botnet Attacks Using Deep Autoencoders</span>
        </h1>
        <div style="font-size: 12pt; font-style: italic; color: #4A5568;">
            A Methodological Survey, Mathematical Reconstruction, and Comparative Benchmarking Against Edge CART Decision Trees
        </div>
    </div>
    
    <div style="margin-top: 40px; font-size: 11pt; line-height: 1.8;">
        <strong>Author / Research Group:</strong> Group 1 — Decision Tree<br>
        <strong>Faculty In-Charge:</strong> Prof. Renuka Pawar<br>
        <strong>Subject:</strong> CNS Collaborative R&D Manifest<br>
        <strong>Target Publication Venue:</strong> Scopus-Indexed Cybersecurity Review Journal<br>
        <strong>Date of Report:</strong> Academic Year 2026–2027
    </div>
</div>
"""

# Add sections 2 to 27
sections = [
    ("2. Full Bibliographic Citation & Archival Indexing", "Detailed archival metadata and indexing verification..."),
    ("3. Executive Abstract", "Comprehensive executive abstract of the source paper and our critical evaluation..."),
    ("4. Keywords & Academic Taxonomy", "Taxonomy of terms: IoT Security, Deep Autoencoders, Anomaly Detection, Mirai, BASHLITE, Kitsune..."),
    ("5. Introduction to Edge IoT Security Challenges", "Analysis of edge vulnerabilities, distributed botnets, and device heterogeneity..."),
    ("6. Formal Research Problem Definition", "Mathematical definition of unsupervised anomaly detection in multivariate packet streams..."),
    ("7. Background & Theoretical Foundations", "Deep autoencoders, reconstruction loss, Bottleneck compression, and non-linear manifold learning..."),
    ("8. Survey of Related Work Discussed in the Source", "Comprehensive review of signature NIDS, shallow ML, and deep autoencoders..."),
    ("9. N-BaIoT Dataset Architecture & Ingestion Profile", "Deep dive into 9 commercial IoT devices, 89 CSV files, and 7,062,606 raw packet records..."),
    ("10. Feature Representation: 115 Kitsune Flow Dimensions", "Comprehensive breakdown of 5 decay windows and 4 traffic aggregation scopes (H, HH, HH_jit, HpHp)..."),
    ("11. Transport-Layer Port & Socket Dynamics Analysis", "Investigation into why raw port headers are absent and how continuous HpHp features capture socket state..."),
    ("12. Methodological Workflow of Deep Autoencoders", "Architecture of device-specific autoencoders, sliding window feature extraction, and offline training..."),
    ("13. Mathematical Formulation of Autoencoder Anomaly Detection", "Detailed reconstruction error equations, Mean Squared Error (MSE), thresholding policies, and gradients..."),
    ("14. Experimental Setup & Hardware Environments in Source", "Testbed deployment, lab hardware, packet capture interfaces, and baseline operating constraints..."),
    ("15. Evaluation Metrics & Statistical Verification", "True Positive Rate, False Positive Rate, Time to Detection, and Receiver Operating Characteristic (ROC)..."),
    ("16. Empirical Results Reported in Original Publication", "Detection rates for Mirai and BASHLITE across the 9 devices as reported by Meidan et al..."),
    ("17. Detailed Technical Analysis of the Reconstruction Engine", "Layer-by-layer evaluation of encoder-decoder weights, activation functions, and latent space dimensionality..."),
    ("18. Architectural Strengths of the N-BaIoT Approach", "Zero-day generalization, unsupervised training on benign baselines, and cross-device anomaly bounds..."),
    ("19. Technical Limitations & Vulnerabilities of Deep Autoencoders", "High memory overhead, floating-point matrix multiplications, lack of classification granularity, and concept drift..."),
    ("20. Practical Relevance to IoT Network Security Deployments", "Deployment viability on gateway routers, enterprise IoT switches, and smart home hubs..."),
    ("21. Direct Relevance to the N-BaIoT Telemetry Corpus", "How N-BaIoT became a gold standard benchmark for IoT botnet detection research..."),
    ("22. Relevance to Supervised Decision Trees & CART Induction", "Bridging unsupervised reconstruction anomaly detection with supervised hierarchical partitioning..."),
    ("23. In-Depth Comparative Analysis: Autoencoders vs. Group 1 Pruned CART", "Comprehensive side-by-side comparison of latency (34.41 us vs ms), memory (5.44 KB vs MBs), and accuracy..."),
    ("24. Security Trade-Offs: Black-Box Autoencoders vs. White-Box Decision Trees", "Explainability, auditability, extraction of Boolean firewall rules, and security incident response..."),
    ("25. Critical Research Gaps Identified in Original Paper", "Evaluation of adversarial evasion attacks, multi-device cross-contamination, and multiclass attack labeling..."),
    ("26. Future Research Directions in Edge Cybersecurity", "Integer-quantized models, hardware eBPF kernel offloading, and hybrid supervised-unsupervised edge engines..."),
    ("27. Comprehensive Conclusion & Synthesis", "Final synthesis of findings and academic contributions to the CNS R&D Tournament..."),
    ("28. Complete Bibliography & Verification References", "Exhaustive list of peer-reviewed references, standards, and datasets...")
]

for title, placeholder in sections:
    html_content += f"""
    <div class="page-break">
        <h2>{title}</h2>
        <div class="citation-box">
            <strong>Section Overview:</strong> This chapter provides rigorous academic analysis, equations, and verified empirical metrics for {title}.
        </div>
        <p>{placeholder}</p>
        <p>In network security architectures, evaluating the computational and theoretical soundness of detection models requires analyzing the physical packet structures, continuous stream statistics, and algorithmic decision boundaries. The following detailed analysis investigates these properties in depth.</p>
        <div class="equation-box">
            MSE(x, x') = (1 / d) * sum_{{i=1}}^d (x_i - x'_i)^2
        </div>
        <p>Furthermore, when comparing the non-linear compression of 115 continuous features against hierarchical decision tree partitioning, several key trade-offs emerge between reconstruction loss minimization and empirical impurity reduction.</p>
        <table>
            <thead>
                <tr>
                    <th>Evaluation Parameter</th>
                    <th>Deep Autoencoder (Meidan et al., 2018)</th>
                    <th>Pruned CART Decision Tree (Group 1 Ours)</th>
                    <th>Analytical Significance</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Learning Paradigm</td>
                    <td>Unsupervised (Benign Baseline Only)</td>
                    <td>Supervised (11-Class Multi-Vector CART)</td>
                    <td>Attack vector specificity vs. Zero-day anomaly detection</td>
                </tr>
                <tr>
                    <td>Single-Packet Latency</td>
                    <td>High (~milliseconds per packet)</td>
                    <td>Ultra-Low (34.41 microseconds per packet)</td>
                    <td>Direct wire-speed inline inspection viability</td>
                </tr>
                <tr>
                    <td>Memory Footprint</td>
                    <td>~100 KB - 2 MB per device model (x9)</td>
                    <td>5.44 KB unified serialized model</td>
                    <td>Fits completely inside L1/L2 CPU caches</td>
                </tr>
                <tr>
                    <td>Decision Explainability</td>
                    <td>Black-Box (Reconstruction MSE threshold)</td>
                    <td>White-Box (Auditable Boolean Rule Paths)</td>
                    <td>Enables automated static firewall rule synthesis</td>
                </tr>
            </tbody>
        </table>
        <p>Additional paragraphs and technical discussions are included here to thoroughly cover the theoretical framework and empirical verification.</p>
    </div>
    """

html_content += "</body></html>"

with open("test_paper1.html", "w") as f:
    f.write(html_content)

subprocess.run([
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless=new", "--disable-gpu",
    "--print-to-pdf=test_paper1.pdf",
    "test_paper1.html"
], check=True)

import re
with open("test_paper1.pdf", "rb") as f:
    data = f.read()
page_count = len(re.findall(rb'/Type\s*/Page\b', data))
print(f"Generated test_paper1.pdf with {page_count} pages!")
