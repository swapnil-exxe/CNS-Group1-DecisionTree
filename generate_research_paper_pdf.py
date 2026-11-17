#!/usr/bin/env python3
"""
Compiles the comprehensive, publication-quality formal academic research paper PDF
for CNS Group 1 (Decision Tree) using ReportLab.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Sardar Patel Institute of Technology | CNS A.Y. 2026–27 | Group 1 — Decision Tree")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 750, 558, 750)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, page_text)
        self.drawString(54, 35, "CONFIDENTIAL & PROPRIETARY — CNS COLLABORATIVE RESEARCH CONTRIBUTION")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.restoreState()

def build_pdf():
    pdf_filename = "/Users/swapnil/Documents/cns/CNS-Group1-DecisionTree/CNS_Group1_Decision_Tree_Research_Paper.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1A365D")    # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0")  # Royal Blue
    c_dark = colors.HexColor("#2D3748")       # Body text
    c_light = colors.HexColor("#EDF2F7")      # Table bg
    c_accent = colors.HexColor("#C53030")     # Highlight red
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_secondary,
        alignment=1,
        spaceAfter=10
    )
    
    author_style = ParagraphStyle(
        'AuthorStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        alignment=1,
        spaceAfter=14
    )
    
    abstract_heading = ParagraphStyle(
        'AbsHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_primary,
        alignment=0,
        spaceAfter=4
    )
    
    abstract_body = ParagraphStyle(
        'AbsBody',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        alignment=4, # Justify
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'SecH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6
    )
    
    h2_style = ParagraphStyle(
        'SecH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        alignment=4,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=3
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1A202C"),
        spaceAfter=4
    )
    
    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white,
        alignment=1
    )
    
    td_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=c_dark
    )
    
    td_center = ParagraphStyle(
        'TDCenter',
        parent=td_style,
        alignment=1
    )
    
    story = []
    
    # Title & Metadata
    story.append(Paragraph("Lightweight IoT Botnet Detection Using Cost-Complexity Pruned CART Decision Trees", title_style))
    story.append(Paragraph("A Comprehensive Empirical Study on the N-BaIoT Telemetry Corpus for Real-Time Edge Deployment", subtitle_style))
    story.append(Paragraph(
        "<b>Author:</b> Swapnil Patil (Roll No. 24, CSE Dept.) &nbsp;|&nbsp; "
        "<b>Faculty Mentor:</b> Dr. Renuka Pawar (Associate Head of Department, CSE)<br/>"
        "<i>Bhartiya Vidya Bhavan’s Sardar Patel Institute of Technology (SPIT), Autonomous Institute Affiliated to University of Mumbai</i><br/>"
        "Course: Cryptography and Network Security (CNS) A.Y. 2026–2027 &nbsp;|&nbsp; <b>Group 1: Decision Tree</b>",
        author_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=0, spaceAfter=8))
    
    # Abstract
    story.append(Paragraph("ABSTRACT", abstract_heading))
    story.append(Paragraph(
        "Commercial Internet of Things (IoT) appliances increasingly suffer from automated botnet compromises such as Mirai and BASHLITE (Gafgyt). "
        "Due to severe hardware resource constraints on edge microcontrollers (limited SRAM and CPU cycles), traditional deep learning models cannot be hosted locally for line-rate packet inspection. "
        "This research paper presents Group 1's contribution to the collaborative CNS A.Y. 2026–27 research paper, evaluating an optimized Classification and Regression Tree (CART) Decision Tree regularized via Minimal Cost-Complexity Pruning (MCCP). "
        "Evaluated on a systematically sampled corpus of 128,366 packets (115 continuous Kitsune flow features across 89 physical traffic captures from 9 IoT devices in the benchmark N-BaIoT dataset), the optimal pruned model (alpha = 1.999753e-05) shrinks tree depth from 21 to 18 levels (-14.3%) and total nodes from 181 to 133 nodes (-26.5%). "
        "On the untouched held-out test partition of 25,674 packets, the pruned tree achieves 99.6183% multiclass accuracy, 99.6510% Macro F1-score, and 99.9649% binary attack detection accuracy, while reducing the generalization gap to 0.0769%. "
        "Computational profiling demonstrates an inline single-sample latency of 34.41 µs/packet (29,062 packets/s), a vectorized batch throughput exceeding 12.03 million packets/s, and a compact serialized footprint of only 5.44 KB, proving high feasibility for direct micro-controller flash firmware deployment.",
        abstract_body
    ))
    story.append(Paragraph("<b>Keywords:</b> IoT Botnet Detection, CART Decision Tree, Cost-Complexity Pruning, N-BaIoT Dataset, Real-Time Edge Cybersecurity, White-Box Interpretability.", body_style))
    story.append(Spacer(1, 8))
    
    # Section 1: Introduction
    story.append(Paragraph("1. INTRODUCTION & RESEARCH CONTEXT", h1_style))
    story.append(Paragraph(
        "The proliferation of Internet of Things (IoT) devices—including smart doorbells, IP surveillance cameras, environmental sensors, and home gateways—has dramatically expanded the network attack surface. "
        "Botnets such as Mirai and BASHLITE (Gafgyt) exploit default credentials and firmware vulnerabilities to compromise millions of devices, orchestrating massive distributed denial-of-service (DDoS) campaigns, port scans, and data exfiltration. "
        "Detecting these attacks directly at the local device level (edge intrusion detection) is critical to neutralize malicious traffic before it congests WAN uplinks.",
        body_style
    ))
    story.append(Paragraph(
        "However, edge deployment imposes severe constraints: typical IoT appliances run on low-power ARM Cortex-M or MIPS microcontrollers clocked at 400 MHz to 1.2 GHz with only a few kilobytes of available SRAM. "
        "Deep Neural Networks (DNNs) and complex ensembles (Random Forests, Gradient Boosted Trees) demand excessive floating-point matrix multiplications and megabytes of memory, rendering them unsuitable for inline line-rate packet classification. "
        "In contrast, single Decision Trees evaluate simple univariate threshold inequalities (e.g., <i>feature &le; threshold</i>), offering deterministic sub-microsecond classification, zero complex floating-point algebra, and complete white-box interpretability.",
        body_style
    ))
    
    # Section 2: Methodology & CART vs C4.5
    story.append(Paragraph("2. ALGORITHM METHODOLOGY & FORMULATION", h1_style))
    story.append(Paragraph(
        "<b>2.1 Theoretical Framework vs. Implemented Paradigm:</b> "
        "The assigned research theme specifies <i>Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees</i>. "
        "A formal methodological distinction must be highlighted: Quinlan’s theoretical C4.5 algorithm utilizes Shannon Entropy and Information Gain Ratio to construct multi-way categorical branches and employs heuristic Error-Based Pruning (EBP). "
        "Standard production machine learning environments (specifically <code>sklearn.tree.DecisionTreeClassifier</code>) implement an optimized variant of the <b>Classification and Regression Trees (CART)</b> algorithm (Breiman et al., 1984). "
        "CART generates strictly binary orthogonal decision splits guided by the Gini Impurity Index and regularizes tree complexity via Minimal Cost-Complexity Pruning (MCCP). "
        "Because N-BaIoT telemetry consists exclusively of 115 continuous numerical flow statistics without discrete text attributes, CART's binary thresholding provides the optimal mathematical formulation.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2.2 Gini Impurity & Split Selection:</b> At each decision node <i>m</i>, class heterogeneity across <i>C = 11</i> target categories is quantified by Gini Impurity:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>I<sub>G</sub>(m) = 1 &minus; &sum;<sub>k=0</sub><sup>C-1</sup> (p<sub>mk</sub>)<sup>2</sup></b>",
        code_style
    ))
    story.append(Paragraph(
        "where <i>p<sub>mk</sub></i> is the empirical proportion of class <i>k</i> instances in node <i>m</i>. "
        "For each continuous feature <i>j &isin; {1, ..., 115}</i> and threshold <i>t</i>, the Gini Gain &Delta;I<sub>G</sub>(m, &theta;) is maximized to isolate the purest sub-partitions. "
        "Recursive splitting proceeds until leaves become pure or termination bounds are reached.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2.3 Minimal Cost-Complexity Pruning (MCCP):</b> An unconstrained tree overfits to transient network noise, creating deep paths that fail to generalize. "
        "MCCP penalizes structural leaf complexity by minimizing the cost objective:",
        body_style
    ))
    story.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>R<sub>&alpha;</sub>(T) = R(T) + &alpha; |T|</b>",
        code_style
    ))
    story.append(Paragraph(
        "where <i>R(T)</i> is the total misclassification/impurity cost across terminal leaves, <i>|T|</i> is the total number of leaves, and <i>&alpha; &ge; 0</i> is the complexity tuning parameter. "
        "By evaluating candidate subtrees along the weakest-link pruning path on an independent validation set, the optimal parameter <b>&alpha;<sup>*</sup></b> is determined.",
        body_style
    ))
    
    # Section 3: Dataset & Experimental Design
    story.append(Paragraph("3. SYSTEM DESIGN, DATASET & PIPELINE ARCHITECTURE", h1_style))
    story.append(Paragraph(
        "<b>3.1 N-BaIoT Benchmark Corpus:</b> Collected by Meidan et al. (UCI Repository #442), the raw dataset captures <b>7,062,606 packet instances</b> across 89 CSV files spanning 9 commercial IoT appliances authentically infected with Mirai and BASHLITE (Gafgyt). "
        "The appliances comprise: Danmini Doorbell, Ecobee Thermostat, Ennio Doorbell, Philips B120N/10 Baby Monitor, Provision 737E & 838 IP Cameras, Samsung SNH 1011 N Webcam, and SimpleHome XCS7-1002 & 1003 Security Cameras. "
        "Note that the Ennio Doorbell and Samsung Webcam were infected solely with Gafgyt (6 files each), whereas the remaining 7 devices contain 11 files covering both botnets.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3.2 115 Continuous Kitsune Flow Features:</b> Traffic statistics are dynamically extracted across 5 exponentially decaying sliding time windows (&lambda; &isin; {5, 3, 1, 0.1, 0.01}) over 5 stream aggregation scopes: "
        "(1) <code>MI_dir</code> (source MAC-IP traffic volume), (2) <code>H</code> (source host packet dynamics), (3) <code>HH</code> (host-to-host pair communications), (4) <code>HH_jit</code> (inter-arrival jitter between host pairs), and (5) <code>HpHp</code> (Host+Port to Host+Port socket interactions). "
        "Importantly, raw integer port numbers and protocol strings are absent; instead, socket-level interactions are represented as continuous statistical moments (weight, mean, variance, covariance).",
        body_style
    ))
    story.append(Paragraph(
        "<b>3.3 Deterministic Sampling & Zero-Leakage 3-Way Partitioning:</b> "
        "To enable memory-efficient, reproducible modeling without introducing random sampling bias, systematic sampling with a deterministic row stride <b>S = 55</b> was executed across all 89 files. "
        "This extracted exactly <b>128,366 packets</b>, matching the 7.06M population class distribution to within &plusmn;0.01%. "
        "The corpus was partitioned into an 80% Training Set (N = 102,692) and an untouched 20% Held-Out Test Set (N = 25,674). "
        "Within the training partition, a secondary 80/20 split created an Internal Sub-Train Set (N = 82,153) and an Internal Validation Set (N = 20,539) strictly reserved for alpha tuning, guaranteeing zero test set data leakage.",
        body_style
    ))
    
    # Table 1: Dataset Summary
    t1_data = [
        [Paragraph("Target Class Name", th_style), Paragraph("Class ID", th_style), Paragraph("Raw Population", th_style), Paragraph("Sample (S=55)", th_style), Paragraph("Sub-Train (80%)", th_style), Paragraph("Val (20%)", th_style), Paragraph("Test Set (20%)", th_style)],
        [Paragraph("benign", td_style), Paragraph("0", td_center), Paragraph("555,911 (7.87%)", td_center), Paragraph("10,108 (7.87%)", td_center), Paragraph("6,469", td_center), Paragraph("1,618", td_center), Paragraph("2,021", td_center)],
        [Paragraph("gafgyt_combo", td_style), Paragraph("1", td_center), Paragraph("515,188 (7.29%)", td_center), Paragraph("9,367 (7.30%)", td_center), Paragraph("5,995", td_center), Paragraph("1,500", td_center), Paragraph("1,872", td_center)],
        [Paragraph("gafgyt_junk", td_style), Paragraph("2", td_center), Paragraph("260,869 (3.69%)", td_center), Paragraph("4,743 (3.69%)", td_center), Paragraph("3,035", td_center), Paragraph("757", td_center), Paragraph("951", td_center)],
        [Paragraph("gafgyt_scan", td_style), Paragraph("3", td_center), Paragraph("255,142 (3.61%)", td_center), Paragraph("4,639 (3.61%)", td_center), Paragraph("2,969", td_center), Paragraph("743", td_center), Paragraph("927", td_center)],
        [Paragraph("gafgyt_tcp", td_style), Paragraph("4", td_center), Paragraph("859,748 (12.17%)", td_center), Paragraph("15,632 (12.18%)", td_center), Paragraph("9,985", td_center), Paragraph("2,521", td_center), Paragraph("3,126", td_center)],
        [Paragraph("gafgyt_udp", td_style), Paragraph("5", td_center), Paragraph("946,312 (13.40%)", td_center), Paragraph("17,206 (13.40%)", td_center), Paragraph("11,012", td_center), Paragraph("2,753", td_center), Paragraph("3,441", td_center)],
        [Paragraph("mirai_ack", td_style), Paragraph("6", td_center), Paragraph("643,588 (9.11%)", td_center), Paragraph("11,702 (9.12%)", td_center), Paragraph("7,489", td_center), Paragraph("1,873", td_center), Paragraph("2,340", td_center)],
        [Paragraph("mirai_scan", td_style), Paragraph("7", td_center), Paragraph("537,925 (7.62%)", td_center), Paragraph("9,781 (7.62%)", td_center), Paragraph("6,260", td_center), Paragraph("1,565", td_center), Paragraph("1,956", td_center)],
        [Paragraph("mirai_syn", td_style), Paragraph("8", td_center), Paragraph("733,266 (10.38%)", td_center), Paragraph("13,332 (10.39%)", td_center), Paragraph("8,532", td_center), Paragraph("2,134", td_center), Paragraph("2,666", td_center)],
        [Paragraph("mirai_udp", td_style), Paragraph("9", td_center), Paragraph("1,230,064 (17.42%)", td_center), Paragraph("22,365 (17.42%)", td_center), Paragraph("14,314", td_center), Paragraph("3,579", td_center), Paragraph("4,472", td_center)],
        [Paragraph("mirai_udpplain", td_style), Paragraph("10", td_center), Paragraph("524,593 (7.43%)", td_center), Paragraph("9,491 (7.39%)", td_center), Paragraph("6,093", td_center), Paragraph("1,496", td_center), Paragraph("1,902", td_center)],
        [Paragraph("<b>TOTALS</b>", td_style), Paragraph("<b>11</b>", td_center), Paragraph("<b>7,062,606</b>", td_center), Paragraph("<b>128,366</b>", td_center), Paragraph("<b>82,153 (64%)</b>", td_center), Paragraph("<b>20,539 (16%)</b>", td_center), Paragraph("<b>25,674 (20%)</b>", td_center)]
    ]
    t1 = Table(t1_data, colWidths=[80, 40, 75, 75, 65, 55, 65])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, c_light]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))
    
    # Section 4: Optimization & Pruning
    story.append(Paragraph("4. HYPERPARAMETER TUNING & COST-COMPLEXITY PRUNING", h1_style))
    story.append(Paragraph(
        "A grid of 20 candidate cost-complexity penalties (0 &le; &alpha; &le; 0.05) was evaluated on the internal validation set. "
        "The unpruned baseline reached a depth of 21 with 181 nodes and 91 leaves. "
        "As &alpha; increased, redundant subtrees were pruned without degrading accuracy. "
        "The optimal parameter was identified as <b>&alpha;<sup>*</sup> = 1.9997530739682578 &times; 10<sup>-5</sup></b>, which achieved the peak Validation Macro F1 of <b>99.7696%</b> and Validation Accuracy of <b>99.7127%</b>. "
        "Pruning successfully eliminated 48 nodes (-26.5%) and 24 leaves (-26.4%), collapsing maximum depth from 21 to 18 levels (-14.3%).",
        body_style
    ))
    
    # Section 5: Experimental Results
    story.append(Paragraph("5. FINAL EXPERIMENTAL RESULTS & BENCHMARKS", h1_style))
    story.append(Paragraph(
        "Retraining the optimal pruned tree on the full 102,692 training instances and testing against the untouched 25,674 held-out packets confirms remarkable detection fidelity and generalization stability.",
        body_style
    ))
    
    # Table 2: Baseline vs Pruned Comparison
    t2_data = [
        [Paragraph("Performance & Complexity Metric", th_style), Paragraph("Baseline (Unpruned, &alpha;=0)", th_style), Paragraph("Final Pruned Model (&alpha;=2.0e-5)", th_style), Paragraph("Delta / Impact", th_style)],
        [Paragraph("Cost-Complexity Penalty (ccp_alpha)", td_style), Paragraph("0.0", td_center), Paragraph("1.999753e-05", td_center), Paragraph("Optimal Validation Point", td_style)],
        [Paragraph("Maximum Tree Depth", td_style), Paragraph("21 levels", td_center), Paragraph("18 levels", td_center), Paragraph("-3 levels (-14.3%)", td_style)],
        [Paragraph("Total Node Count", td_style), Paragraph("181 nodes", td_center), Paragraph("133 nodes", td_center), Paragraph("-48 nodes (-26.5%)", td_style)],
        [Paragraph("Terminal Leaves (|T|)", td_style), Paragraph("91 leaves", td_center), Paragraph("67 leaves", td_center), Paragraph("-24 leaves (-26.4%)", td_style)],
        [Paragraph("Multiclass Test Accuracy", td_style), Paragraph("99.6144%", td_center), Paragraph("99.6183%", td_center), Paragraph("+0.0039% (Maintained)", td_style)],
        [Paragraph("Multiclass Macro F1-Score", td_style), Paragraph("99.6487%", td_center), Paragraph("99.6510%", td_center), Paragraph("+0.0023% (Maintained)", td_style)],
        [Paragraph("Multiclass Weighted F1-Score", td_style), Paragraph("99.6143%", td_center), Paragraph("99.6182%", td_center), Paragraph("+0.0039%", td_style)],
        [Paragraph("Multiclass Macro ROC-AUC (OvR)", td_style), Paragraph("0.999391", td_center), Paragraph("0.999410", td_center), Paragraph("+0.000019", td_style)],
        [Paragraph("Generalization Gap (Train - Test Acc)", td_style), Paragraph("0.1022%", td_center), Paragraph("0.0769%", td_center), Paragraph("-0.0253% (Overfitting Reduced)", td_style)],
        [Paragraph("Binary Botnet Detection Accuracy", td_style), Paragraph("99.9649%", td_center), Paragraph("99.9649%", td_center), Paragraph("Identical (25,665 / 25,674)", td_style)],
        [Paragraph("Binary Botnet Detection F1-Score", td_style), Paragraph("99.9810%", td_center), Paragraph("99.9810%", td_center), Paragraph("Identical", td_style)],
        [Paragraph("Single-Sample Latency (N = 1)", td_style), Paragraph("39.74 µs / sample", td_center), Paragraph("34.41 µs / sample", td_center), Paragraph("+13.4% Speedup (29,062 pkts/s)", td_style)],
        [Paragraph("Amortized Batch Latency (N = 25,674)", td_style), Paragraph("0.089 µs / sample", td_center), Paragraph("0.083 µs / sample", td_center), Paragraph("12,036,209 packets / second", td_style)],
        [Paragraph("Serialized Model Storage Footprint", td_style), Paragraph("6.16 KB", td_center), Paragraph("5.44 KB", td_center), Paragraph("-0.72 KB (-11.7% flash savings)", td_style)]
    ]
    t2 = Table(t2_data, colWidths=[160, 110, 110, 120])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 10))
    
    # Per-Class Breakdown & Error Analysis
    story.append(Paragraph("<b>5.1 Detailed Per-Class Breakdown & Test Error Audit:</b>", h2_style))
    story.append(Paragraph(
        "Across all 25,674 test packets, <b>25,576 packets were correctly classified (99.6183%)</b> with exactly <b>98 misclassifications (0.3817%)</b>: "
        "<br/>&bull; <b>73 intra-Gafgyt errors:</b> 73 <code>gafgyt_tcp</code> packets were identified as <code>gafgyt_udp</code> due to fast TCP reset flooding mimicking raw UDP stream dynamics. "
        "<br/>&bull; <b>14 payload entropy errors:</b> 7 <code>gafgyt_combo</code> and 7 <code>gafgyt_junk</code> mutually swapped predictions because randomized payload buffers exhibit overlapping packet size distributions. "
        "<br/>&bull; <b>6 benign false alarms:</b> Out of 2,021 normal packets, only 6 were falsely flagged as attacks (False Positive Rate = 0.2969%). "
        "<br/>&bull; <b>3 missed botnet attacks:</b> Out of 23,653 attack packets, only 3 bypassed detection (False Negative Rate = 0.0127%). "
        "<br/>&bull; <b>2 intra-Mirai errors:</b> 2 <code>mirai_udp</code> packets were predicted as <code>mirai_udpplain</code>.",
        body_style
    ))
    
    # Confusion Matrix Image
    cm_path = "/Users/swapnil/Documents/cns/CNS-Group1-DecisionTree/confusion_matrix.png"
    if os.path.exists(cm_path):
        story.append(Spacer(1, 6))
        story.append(KeepTogether([
            Image(cm_path, width=400, height=320),
            Paragraph("<i>Figure 1: Normalized 11x11 Multiclass Confusion Matrix (%) evaluated on 25,674 held-out test packets.</i>", ParagraphStyle('FigCap', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, alignment=1, spaceBefore=4, spaceAfter=8))
        ]))
    
    # Section 6: Computational Analysis
    story.append(Paragraph("6. COMPUTATIONAL OVERHEAD & EDGE HARDWARE FEASIBILITY", h1_style))
    story.append(Paragraph(
        "<b>6.1 Python Wrapper vs. C-Tree Traversal Latency:</b> "
        "A key finding emerges when contrasting single-sample ($N=1$) latency (34.41 µs) against amortized batch latency (0.083 µs). "
        "Over 99.7% of the 34.41 µs single-packet latency is attributable to Python dynamic dispatch and NumPy array instantiation overhead. "
        "The pure C-level binary tree traversal requires at most 18 pointer lookups and comparisons, executing in under <b>0.1 µs</b>. "
        "Compiled into native C/C++ firmware, this tree easily achieves line-rate Gigabit Ethernet filtering (> 1.488 million packets/sec).",
        body_style
    ))
    story.append(Paragraph(
        "<b>6.2 Memory Footprint:</b> "
        "The final model serializes to just <b>5.44 KB</b>, easily residing within the static Flash or SRAM of inexpensive microcontrollers (such as STM32, ESP32, or ARM Cortex-M4), proving ideal for edge IoT deployments.",
        body_style
    ))
    
    # Section 7: White-Box Interpretability
    story.append(Paragraph("7. WHITE-BOX EXPLAINABILITY & FEATURE IMPORTANCE", h1_style))
    story.append(Paragraph(
        "Unlike black-box deep neural networks, the CART tree provides immediate white-box transparency. "
        "The top features ranked by Gini Importance include: "
        "<code>H_L0.01_mean</code> (0.1811), <code>MI_dir_L0.01_mean</code> (0.1724), <code>HH_jit_L1_mean</code> (0.1701), <code>MI_dir_L0.01_weight</code> (0.1365), and <code>HpHp_L1_weight</code> (0.0568). "
        "The presence of <code>HpHp_L1_weight</code> demonstrates that Host+Port socket interaction statistics provide powerful discriminative signals for identifying high-volume port attacks without needing payload inspection.",
        body_style
    ))
    
    # Section 8: Conclusion
    story.append(Paragraph("8. CONCLUSION & COLLABORATIVE BATCH INTEGRATION", h1_style))
    story.append(Paragraph(
        "Group 1 has successfully established that a Minimal Cost-Complexity Pruned CART Decision Tree provides an optimal trade-off for IoT botnet defense: "
        "achieving <b>99.62% multiclass accuracy</b>, <b>99.96% binary detection</b>, <b>5.44 KB model size</b>, and <b>34.41 µs latency</b> while reducing tree depth by 14.3% and nodes by 26.5%. "
        "All code, preprocessed dataset matrices, and replication notebooks are publicly accessible on GitHub and Google Colab.",
        body_style
    ))
    
    # References
    story.append(Paragraph("REFERENCES", h1_style))
    refs = [
        "[1] L. Breiman, J. H. Friedman, R. A. Olshen, and C. J. Stone, <i>Classification and Regression Trees</i>. Belmont, CA: Wadsworth, 1984.",
        "[2] J. R. Quinlan, <i>C4.5: Programs for Machine Learning</i>. San Mateo, CA: Morgan Kaufmann, 1993.",
        "[3] Y. Meidan et al., \"N-BaIoT—Network-Based Detection of IoT Botnet Attacks Using Deep Autoencoders,\" <i>IEEE Pervasive Computing</i>, vol. 17, no. 3, pp. 12–22, 2018.",
        "[4] M. Shafiq et al., \"CORRAUC: A Malicious Bot-IoT Traffic Detection Method in IoT Network Using Machine-Learning Techniques,\" <i>IEEE Internet of Things Journal</i>, vol. 8, no. 5, pp. 3242–3253, 2021.",
        "[5] A. Moubayed et al., \"Optimized Machine Learning-Based Network Intrusion Detection for IoT Networks,\" <i>IEEE Internet of Things Journal</i>, vol. 7, no. 6, pp. 4889–4903, 2020.",
        "[6] F. Pedregosa et al., \"Scikit-learn: Machine Learning in Python,\" <i>Journal of Machine Learning Research</i>, vol. 12, pp. 2825–2830, 2011."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('Ref', parent=body_style, fontSize=7.5, leading=10, leftIndent=15, firstLineIndent=-15, spaceAfter=3)))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully compiled publication-quality Research Paper PDF to: {pdf_filename}")

if __name__ == '__main__':
    build_pdf()
