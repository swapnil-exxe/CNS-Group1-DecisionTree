import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set clean academic styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 9

os.makedirs('results/figures', exist_ok=True)

# 1. Overall System Architecture
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off')
    
    # Outer container
    rect_main = patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                                      facecolor='#F8F9FA', edgecolor='#2B3E50', linewidth=2)
    ax.add_patch(rect_main)
    ax.text(0.5, 0.94, "Lightweight IoT Botnet Detection: System Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1A252F')
    
    # Modules
    modules = [
        ("Layer 1: Data Ingestion & Sampling", 0.77, "#EBF5FB", "#2980B9", 
         "N-BaIoT Archive (89 CSVs, 7M rows) --> Systematic Step Sampling (k=55) --> 128,366 Balanced Samples"),
        ("Layer 2: Preprocessing & Data Hygiene", 0.59, "#E8F8F5", "#16A085", 
         "Data Leakage Audit --> Label Taxonomy (11 Classes) --> Stratified Partition (80/20 Train/Test)"),
        ("Layer 3: Optimization & Cost-Complexity Pruning", 0.41, "#FEF9E7", "#D4AC0D", 
         "Internal 80/20 Split --> Pruning Path (60 Alphas) --> Validation Tuning --> Optimal Alpha (1.9998e-5)"),
        ("Layer 4: Retraining & Model Serialization", 0.23, "#F4ECF7", "#8E44AD", 
         "Full Train Fitting (102,692 samples) --> Pruned Tree (Depth: 18, Leaves: 67) --> Serialized Model (5.44 KB)"),
        ("Layer 5: Edge Inference & Real-Time Inspection", 0.06, "#FDEDEC", "#C0392B", 
         "Packet Feature Vector (115 stats) --> Decision Tree Traversal (34.41 us) --> Multiclass & Binary Alerts")
    ]
    
    for title, y_pos, fcolor, ecolor, desc in modules:
        box = patches.FancyBboxPatch((0.06, y_pos), 0.88, 0.12, boxstyle="round,pad=0.015",
                                     facecolor=fcolor, edgecolor=ecolor, linewidth=1.5)
        ax.add_patch(box)
        ax.text(0.08, y_pos + 0.085, title, fontsize=11, fontweight='bold', color=ecolor)
        ax.text(0.08, y_pos + 0.035, desc, fontsize=8.5, color='#2C3E50')
        
    # Connectors
    for y_arrow in [0.74, 0.56, 0.38, 0.20]:
        ax.annotate('', xy=(0.5, y_arrow - 0.03), xytext=(0.5, y_arrow),
                    arrowprops=dict(facecolor='#34495E', edgecolor='#34495E', width=1.5, headwidth=6, shrink=0.05))
        
    plt.tight_layout()
    plt.savefig('results/figures/design_architecture.png', bbox_inches='tight')
    plt.close()
    print("Saved design_architecture.png")

# 2. Data Flow Diagram (DFD Level 1)
def create_dfd_diagram():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax.axis('off')
    
    ax.text(0.5, 0.95, "Data Flow Diagram (Level 1): Preprocessing to Edge Decision", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1A252F')
    
    # Entities / Processes
    nodes = [
        ("IoT Device Network\n(9 Devices / Pcap Streams)", 0.08, 0.65, "#EAECEE", "#5D6D7E", False),
        ("Kitsune Feature Extractor\n(115 Damped Statistics)", 0.28, 0.65, "#D6EAF8", "#2980B9", True),
        ("Systematic Sampler\n(128,366 Rows, Step=55)", 0.50, 0.65, "#D5F5E3", "#27AE60", True),
        ("Stratified Splitter\n(Train 80% / Test 20%)", 0.72, 0.65, "#FCF3CF", "#F39C12", True),
        ("Held-Out Test Set\n(25,674 Packets)", 0.92, 0.65, "#FDEDEC", "#E74C3C", False),
        
        ("Validation Tuner\n(Internal 80/20 Train/Val)", 0.50, 0.25, "#E8DAEF", "#8E44AD", True),
        ("Pruning Path Explorer\n(Minimal Cost-Complexity)", 0.28, 0.25, "#E8DAEF", "#8E44AD", True),
        ("Final Pruned Model\n(Depth: 18, Size: 5.44 KB)", 0.72, 0.25, "#D5F5E3", "#27AE60", True),
        ("Decision & Alert Output\n(Multiclass: 99.62%, Binary: 99.96%)", 0.92, 0.25, "#D6EAF8", "#2980B9", False),
    ]
    
    for label, x, y, fc, ec, is_proc in nodes:
        if is_proc:
            box = patches.FancyBboxPatch((x-0.08, y-0.1), 0.16, 0.2, boxstyle="round,pad=0.01",
                                         facecolor=fc, edgecolor=ec, linewidth=1.5)
        else:
            box = patches.Rectangle((x-0.08, y-0.1), 0.16, 0.2,
                                    facecolor=fc, edgecolor=ec, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold', color='#1A252F')
        
    # Connectors
    arrows = [
        ((0.16, 0.65), (0.20, 0.65), "Raw Packets"),
        ((0.36, 0.65), (0.42, 0.65), "115 Features"),
        ((0.58, 0.65), (0.64, 0.65), "Sampled Pool"),
        ((0.80, 0.65), (0.84, 0.65), "Test Split"),
        ((0.72, 0.55), (0.58, 0.30), "Train Set (102,692)"),
        ((0.42, 0.25), (0.36, 0.25), "Train Subset"),
        ((0.36, 0.25), (0.42, 0.25), "Alphas"),
        ((0.58, 0.25), (0.64, 0.25), "alpha* = 1.9998e-5"),
        ((0.72, 0.35), (0.72, 0.55), "Trained Tree"),
        ((0.80, 0.25), (0.84, 0.25), "Evaluated"),
        ((0.92, 0.55), (0.92, 0.35), "Test Packets")
    ]
    
    ax.annotate('', xy=(0.20, 0.65), xytext=(0.16, 0.65), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.42, 0.65), xytext=(0.36, 0.65), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.64, 0.65), xytext=(0.58, 0.65), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.84, 0.65), xytext=(0.80, 0.65), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    
    ax.annotate('', xy=(0.50, 0.35), xytext=(0.72, 0.55), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.36, 0.25), xytext=(0.42, 0.25), arrowprops=dict(facecolor='#2C3E50', arrowstyle="<->", lw=1.5))
    ax.annotate('', xy=(0.64, 0.25), xytext=(0.58, 0.25), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.84, 0.25), xytext=(0.80, 0.25), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.92, 0.35), xytext=(0.92, 0.55), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    
    plt.tight_layout()
    plt.savefig('results/figures/design_dfd.png', bbox_inches='tight')
    plt.close()
    print("Saved design_dfd.png")

# 3. Training Workflow Diagram
def create_training_workflow_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.axis('off')
    ax.text(0.5, 0.95, "Supervised CART Training Workflow", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1A252F')
    
    steps = [
        ("Step 1: Input Training Matrix\nX_train (102,692 x 115)\ny_train (102,692 labels)", 0.12, 0.55, "#EBF5FB", "#2980B9"),
        ("Step 2: Recursive Binary Partitioning\nEvaluate 115 features x thresholds\nMinimize Gini Impurity at each node", 0.37, 0.55, "#E8F8F5", "#16A085"),
        ("Step 3: Stopping Criteria Check\nPure node (Gini=0) OR\nMin samples split reached", 0.63, 0.55, "#FEF9E7", "#D4AC0D"),
        ("Step 4: Unpruned Tree Creation\nDepth: 21, Nodes: 181, Leaves: 91\nSubject to Overfitting", 0.88, 0.55, "#FDEDEC", "#C0392B"),
        ("Step 5: Apply CCP Regularization\nccp_alpha = 1.9998e-5\nPrune 48 weak sub-trees", 0.63, 0.18, "#F4ECF7", "#8E44AD"),
        ("Step 6: Final Compact Model\nDepth: 18, Nodes: 133, Leaves: 67\nSerialized Size: 5.44 KB", 0.25, 0.18, "#E8F8F5", "#27AE60")
    ]
    
    for label, x, y, fc, ec in steps:
        box = patches.FancyBboxPatch((x-0.10, y-0.12), 0.20, 0.24, boxstyle="round,pad=0.015",
                                     facecolor=fc, edgecolor=ec, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold', color='#1A252F')
        
    # Arrows
    ax.annotate('', xy=(0.27, 0.55), xytext=(0.22, 0.55), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.53, 0.55), xytext=(0.47, 0.55), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.78, 0.55), xytext=(0.73, 0.55), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.73, 0.20), xytext=(0.88, 0.43), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.35, 0.18), xytext=(0.53, 0.18), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    
    plt.tight_layout()
    plt.savefig('results/figures/design_training_workflow.png', bbox_inches='tight')
    plt.close()
    print("Saved design_training_workflow.png")

# 4. Validation & Pruning Workflow Diagram
def create_pruning_workflow_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.axis('off')
    ax.text(0.5, 0.95, "Internal Validation & Cost-Complexity Pruning Workflow", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1A252F')
    
    boxes = [
        ("Training Partition\n(102,692 samples)\n[Held-Out Test Set Untouched]", 0.12, 0.65, "#EAECEE", "#34495E"),
        ("Internal Split (80/20)\nTrain: 82,153\nVal: 20,539", 0.35, 0.65, "#EBF5FB", "#2980B9"),
        ("Compute Pruning Path\ncost_complexity_pruning_path\n60 candidate alphas found", 0.60, 0.65, "#FEF9E7", "#D4AC0D"),
        ("Select 20 Thresholds\nFrom 0.0 to 0.1214\nSpan full structural range", 0.85, 0.65, "#F4ECF7", "#8E44AD"),
        
        ("Evaluate on Val Set\nMeasure Macro F1, Accuracy,\nTree Depth, Leaf Count", 0.85, 0.22, "#FDEDEC", "#C0392B"),
        ("Selection Rule Applied\n1. Maximize Macro F1\n2. Maximize Accuracy\n3. Minimize Leaves", 0.60, 0.22, "#FEF9E7", "#F39C12"),
        ("Optimal Alpha Isolated\nccp_alpha = 1.9998e-5\nVal F1: 99.770%, Val Acc: 99.713%", 0.35, 0.22, "#E8F8F5", "#16A085"),
        ("Final Retrain on Full Train\nFit model with optimal alpha\nReady for 1-time test audit", 0.12, 0.22, "#D5F5E3", "#27AE60")
    ]
    
    for label, x, y, fc, ec in boxes:
        box = patches.FancyBboxPatch((x-0.10, y-0.12), 0.20, 0.24, boxstyle="round,pad=0.015",
                                     facecolor=fc, edgecolor=ec, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=7.8, fontweight='bold', color='#1A252F')
        
    ax.annotate('', xy=(0.25, 0.65), xytext=(0.22, 0.65), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.50, 0.65), xytext=(0.45, 0.65), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.75, 0.65), xytext=(0.70, 0.65), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.85, 0.34), xytext=(0.85, 0.53), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.70, 0.22), xytext=(0.75, 0.22), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.45, 0.22), xytext=(0.50, 0.22), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.22, 0.22), xytext=(0.25, 0.22), arrowprops=dict(facecolor='#2C3E50', arrowstyle="->", lw=1.5))
    
    plt.tight_layout()
    plt.savefig('results/figures/design_pruning_workflow.png', bbox_inches='tight')
    plt.close()
    print("Saved design_pruning_workflow.png")

# 5. Inference Workflow Diagram (Online & Batch)
def create_inference_workflow_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    ax.axis('off')
    ax.text(0.5, 0.95, "Edge Gateway Real-Time & Batch Inference Workflow", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1A252F')
    
    # Path A: Single Packet
    ax.text(0.05, 0.80, "Path A: Real-Time Single Packet Inspection (Latency Critical)", fontsize=9, fontweight='bold', color='#2980B9')
    box_a1 = patches.FancyBboxPatch((0.05, 0.58), 0.25, 0.18, boxstyle="round,pad=0.01", facecolor='#EBF5FB', edgecolor='#2980B9', lw=1.2)
    ax.add_patch(box_a1)
    ax.text(0.175, 0.67, "1. Inbound Packet\n115 Feature Vector\nArrival Rate: ~1 us", ha='center', va='center', fontsize=8, fontweight='bold')
    
    box_a2 = patches.FancyBboxPatch((0.37, 0.58), 0.26, 0.18, boxstyle="round,pad=0.01", facecolor='#E8F8F5', edgecolor='#16A085', lw=1.2)
    ax.add_patch(box_a2)
    ax.text(0.50, 0.67, "2. Fast Decision Tree Walk\nMax 18 scalar comparisons\nAvg Latency: 34.41 us", ha='center', va='center', fontsize=8, fontweight='bold')
    
    box_a3 = patches.FancyBboxPatch((0.70, 0.58), 0.25, 0.18, boxstyle="round,pad=0.01", facecolor='#FDEDEC', edgecolor='#C0392B', lw=1.2)
    ax.add_patch(box_a3)
    ax.text(0.825, 0.67, "3. Real-Time Action\nIf Malicious: Drop / Alert\nIf Benign: Forward Packet", ha='center', va='center', fontsize=8, fontweight='bold')
    
    ax.annotate('', xy=(0.37, 0.67), xytext=(0.30, 0.67), arrowprops=dict(facecolor='#2980B9', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.70, 0.67), xytext=(0.63, 0.67), arrowprops=dict(facecolor='#16A085', arrowstyle="->", lw=1.5))
    
    # Path B: Batch Buffer
    ax.text(0.05, 0.42, "Path B: High-Throughput Batch Inspection (Gigabit Line-Rate)", fontsize=9, fontweight='bold', color='#8E44AD')
    box_b1 = patches.FancyBboxPatch((0.05, 0.18), 0.25, 0.18, boxstyle="round,pad=0.01", facecolor='#F4ECF7', edgecolor='#8E44AD', lw=1.2)
    ax.add_patch(box_b1)
    ax.text(0.175, 0.27, "1. Flow Buffer Queue\nBatches of 1k - 10k flows\nMatrix (B x 115)", ha='center', va='center', fontsize=8, fontweight='bold')
    
    box_b2 = patches.FancyBboxPatch((0.37, 0.18), 0.26, 0.18, boxstyle="round,pad=0.01", facecolor='#FEF9E7', edgecolor='#D4AC0D', lw=1.2)
    ax.add_patch(box_b2)
    ax.text(0.50, 0.27, "2. Vectorized Batch Traversal\nPer-packet: 0.083 us (83 ns)\nThroughput: 12.04M pkts/s", ha='center', va='center', fontsize=8, fontweight='bold')
    
    box_b3 = patches.FancyBboxPatch((0.70, 0.18), 0.25, 0.18, boxstyle="round,pad=0.01", facecolor='#D5F5E3', edgecolor='#27AE60', lw=1.2)
    ax.add_patch(box_b3)
    ax.text(0.825, 0.27, "3. Network SIEM Ingestion\nAttack Class Distribution\nHardware Load: < 10% CPU", ha='center', va='center', fontsize=8, fontweight='bold')
    
    ax.annotate('', xy=(0.37, 0.27), xytext=(0.30, 0.27), arrowprops=dict(facecolor='#8E44AD', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(0.70, 0.27), xytext=(0.63, 0.27), arrowprops=dict(facecolor='#D4AC0D', arrowstyle="->", lw=1.5))
    
    plt.tight_layout()
    plt.savefig('results/figures/design_inference_workflow.png', bbox_inches='tight')
    plt.close()
    print("Saved design_inference_workflow.png")

if __name__ == '__main__':
    create_architecture_diagram()
    create_dfd_diagram()
    create_training_workflow_diagram()
    create_pruning_workflow_diagram()
    create_inference_workflow_diagram()
    print("All 5 design diagrams created successfully!")
