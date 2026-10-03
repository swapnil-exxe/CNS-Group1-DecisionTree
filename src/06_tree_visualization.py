#!/usr/bin/env python3
"""
Phase 9, 10, 11: Tree Visualization, Feature Importance & Decision Path Analysis
- Generates complete and readable decision tree diagrams (plot_tree, export_text)
- Analyzes feature importances (evaluating HpHp socket port/protocol statistics)
- Performs exact decision path tracing on representative benign and attack packets
"""

import os
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import plot_tree, export_text, export_graphviz

PROJECT_DIR = "/Users/swapnil/Documents/cns/group1_decision_tree"
DATA_PATH = os.path.join(PROJECT_DIR, "data/preprocessed_data.joblib")
MODEL_PATH = os.path.join(PROJECT_DIR, "results/models/final_decision_tree.joblib")
TABLES_DIR = os.path.join(PROJECT_DIR, "results/tables")
FIGURES_DIR = os.path.join(PROJECT_DIR, "results/figures")
REPORT_DIR = os.path.join(PROJECT_DIR, "report")

def run_tree_analysis():
    print("=" * 70)
    print("PHASE 9, 10, 11: Tree Structural Visualization & Behavioral Analysis")
    print("=" * 70)
    
    # 1. Load model and data
    clf = joblib.load(MODEL_PATH)
    data = joblib.load(DATA_PATH)
    feature_names = data["feature_names"]
    class_names = data["class_names"]
    X_test = data["X_test"]
    y_test = data["y_test"]
    
    print(f"Loaded Final Pruned Model: Depth={clf.get_depth()}, Leaves={clf.get_n_leaves()}, Nodes={clf.tree_.node_count}")
    
    # =========================================================================
    # PHASE 9: TREE VISUALIZATION
    # =========================================================================
    print("\n--- Phase 9: Tree Structural Visualization ---")
    
    # A. Text Export
    print("Generating textual tree representation...")
    tree_text = export_text(clf, feature_names=feature_names)
    text_path = os.path.join(TABLES_DIR, "decision_tree_structure.txt")
    with open(text_path, "w") as f:
        f.write(tree_text)
    print(f"Saved complete textual tree structure: {text_path}")
    
    # B. DOT Export
    # Note: Standalone Graphviz 'dot' binary is not present on the host system;
    # therefore, raster figures are rendered via scikit-learn's native plot_tree(),
    # while complete Graphviz DOT and textual tree structures are preserved for export.
    dot_path = os.path.join(TABLES_DIR, "decision_tree_structure.dot")
    export_graphviz(
        clf,
        out_file=dot_path,
        feature_names=feature_names,
        class_names=class_names,
        filled=True,
        rounded=True,
        special_characters=True
    )
    print(f"Saved Graphviz DOT specification: {dot_path}")
    
    # C. Complete Tree Graphic (36 x 20 inches)
    print("Rendering complete decision tree visualization...")
    fig, ax = plt.subplots(figsize=(36, 20), dpi=200)
    plot_tree(
        clf,
        feature_names=feature_names,
        class_names=class_names,
        filled=True,
        rounded=True,
        fontsize=6,
        ax=ax
    )
    plt.title(f"Complete Pruned Decision Tree (ccp_alpha={clf.ccp_alpha:.6e}, Nodes={clf.tree_.node_count}, Leaves={clf.get_n_leaves()})", fontsize=18, fontweight="bold", pad=20)
    complete_fig_path = os.path.join(FIGURES_DIR, "decision_tree_complete.png")
    plt.tight_layout()
    plt.savefig(complete_fig_path, dpi=200)
    plt.close()
    print(f"Saved complete tree diagram: {complete_fig_path}")
    
    # D. Readable Tree Graphic (Upper 3 Levels, max_depth=3)
    print("Rendering readable upper-level decision tree visualization...")
    fig, ax = plt.subplots(figsize=(24, 12), dpi=300)
    plot_tree(
        clf,
        max_depth=3,
        feature_names=feature_names,
        class_names=class_names,
        filled=True,
        rounded=True,
        fontsize=10,
        ax=ax
    )
    plt.title("Readable Upper Decision Paths (Levels 0 to 3)", fontsize=16, fontweight="bold", pad=15)
    readable_fig_path = os.path.join(FIGURES_DIR, "decision_tree_readable.png")
    plt.tight_layout()
    plt.savefig(readable_fig_path, dpi=300)
    plt.close()
    print(f"Saved readable tree diagram: {readable_fig_path}")
    
    # =========================================================================
    # PHASE 10: FEATURE IMPORTANCE
    # =========================================================================
    print("\n--- Phase 10: Feature Importance Analysis ---")
    importances = clf.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    
    feat_records = []
    for rank, idx in enumerate(sorted_idx, 1):
        fn = feature_names[idx]
        imp = importances[idx]
        is_hphp = "HpHp" in fn
        scope = "HpHp (Host+Port to Host+Port)" if is_hphp else ("HH_jit" if "HH_jit" in fn else ("HH" if "HH_" in fn else ("H" if "H_" in fn else "MI_dir")))
        feat_records.append({
            "Rank": rank,
            "Feature": fn,
            "Importance": round(float(imp), 6),
            "Stream_Scope": scope,
            "Is_Port_Protocol_Related": is_hphp
        })
        
    df_feat_imp = pd.DataFrame(feat_records)
    feat_imp_path = os.path.join(TABLES_DIR, "feature_importance.csv")
    df_feat_imp.to_csv(feat_imp_path, index=False)
    print(f"Saved ranked feature importances: {feat_imp_path}")
    
    print("\nTop 10 Most Important Features:")
    print(df_feat_imp.head(10).to_string(index=False))
    
    # Check port/protocol features role
    hphp_features = df_feat_imp[df_feat_imp["Is_Port_Protocol_Related"] == True]
    hphp_total_imp = hphp_features["Importance"].sum()
    print(f"\nPort/Protocol Socket Aggregations (HpHp features):")
    print(f"  Total HpHp features in model: {len(hphp_features)}")
    print(f"  Cumulative Importance of HpHp features: {hphp_total_imp:.6f} ({hphp_total_imp*100:.2f}%)")
    top_hphp = hphp_features.head(5)
    print(f"  Top HpHp features:\n{top_hphp[['Rank', 'Feature', 'Importance']].to_string(index=False)}")
    
    # Plot Feature Importance (Top 15 Features)
    top15 = df_feat_imp.head(15).copy()
    plt.figure(figsize=(10, 6))
    colors = ["#d62728" if is_hp else "#1f77b4" for is_hp in top15["Is_Port_Protocol_Related"]]
    bars = plt.barh(top15["Feature"][::-1], top15["Importance"][::-1], color=colors[::-1], edgecolor="black", alpha=0.85)
    plt.xlabel("Gini Feature Importance", fontweight="bold")
    plt.ylabel("Traffic Feature", fontweight="bold")
    plt.title("Top 15 Features in IoT Botnet Detection Decision Tree", fontsize=13, fontweight="bold", pad=12)
    
    # Custom legend for port/protocol distinction
    import matplotlib.patches as mpatches
    blue_patch = mpatches.Patch(color='#1f77b4', label='Host/Stream Stat (H, HH, MI_dir)')
    red_patch = mpatches.Patch(color='#d62728', label='Socket Port/Protocol Stat (HpHp)')
    plt.legend(handles=[blue_patch, red_patch], loc='lower right', frameon=True)
    
    plt.tight_layout()
    feat_fig_path = os.path.join(FIGURES_DIR, "feature_importance.png")
    plt.savefig(feat_fig_path, dpi=300)
    plt.close()
    print(f"Saved feature importance plot: {feat_fig_path}")
    
    # =========================================================================
    # PHASE 11: DECISION PATH ANALYSIS
    # =========================================================================
    print("\n--- Phase 11: Decision Path Analysis ---")
    
    # Find representative samples from test set
    # Class 0: Benign
    # Class 4: Gafgyt TCP
    # Class 8: Mirai SYN
    # Class 9: Mirai UDP
    selected_classes = {
        "Benign Normal Traffic": 0,
        "Gafgyt TCP Attack Traffic": 4,
        "Mirai SYN Flooding Traffic": 8,
        "Mirai UDP Flooding Traffic": 9
    }
    
    sample_indices = {}
    for desc, c_id in selected_classes.items():
        idxs = np.where(y_test == c_id)[0]
        if len(idxs) > 0:
            sample_indices[desc] = idxs[0]
            
    node_indicator = clf.decision_path(X_test)
    feature = clf.tree_.feature
    threshold = clf.tree_.threshold
    values = clf.tree_.value
    
    path_report_lines = []
    path_report_lines.append("# Decision Path Analysis for Representative Network Packets\n")
    path_report_lines.append("This report traces the exact sequence of feature splits and threshold decisions "
                             "evaluated by the final pruned Decision Tree for representative benign and botnet packets.\n")
    
    for desc, sample_id in sample_indices.items():
        sample_x = X_test[sample_id:sample_id+1]
        true_label = class_names[y_test[sample_id]]
        pred_label = class_names[clf.predict(sample_x)[0]]
        
        path_report_lines.append(f"## Representative Case: {desc}")
        path_report_lines.append(f"- **Sample Test Index:** {sample_id}")
        path_report_lines.append(f"- **Ground Truth Class:** `{true_label}`")
        path_report_lines.append(f"- **Model Prediction:** `{pred_label}`")
        path_report_lines.append(f"- **Decision Sequence (Root to Terminal Leaf):**\n")
        
        node_index = node_indicator.indices[node_indicator.indptr[sample_id]:node_indicator.indptr[sample_id + 1]]
        
        step = 1
        path_summary = []
        for node_id in node_index:
            if clf.tree_.children_left[node_id] != clf.tree_.children_right[node_id]:
                # Non-leaf split node
                feat_idx = feature[node_id]
                feat_name = feature_names[feat_idx]
                thresh = threshold[node_id]
                val = sample_x[0, feat_idx]
                is_left = val <= thresh
                decision_str = f"`{feat_name}` ({val:.4f}) {'<=' if is_left else '>'} {thresh:.4f}"
                path_report_lines.append(f"  {step}. **Node {node_id}**: Evaluate {decision_str} -> branch {'Left' if is_left else 'Right'}")
                path_summary.append(f"{feat_name} ({'<=' if is_left else '>'} {thresh:.2f})")
                step += 1
            else:
                # Terminal leaf node
                leaf_val = values[node_id][0]
                pred_c_idx = np.argmax(leaf_val)
                total_samples = int(np.sum(leaf_val))
                path_report_lines.append(f"  {step}. **Leaf Node {node_id}**: Terminal Node reached. Class = `{class_names[pred_c_idx]}` (Confidence: {leaf_val[pred_c_idx]}/{total_samples} samples = {leaf_val[pred_c_idx]/total_samples*100:.1f}%)\n")
                path_summary.append(f"Terminal: {class_names[pred_c_idx]}")
                
        flow_line = " -> ".join(path_summary)
        path_report_lines.append(f"**Path Flow:** {flow_line}\n")
        path_report_lines.append("-" * 60 + "\n")
        
    full_path_report = "\n".join(path_report_lines)
    
    path_txt_file = os.path.join(TABLES_DIR, "decision_paths_analysis.txt")
    with open(path_txt_file, "w") as f:
        f.write(full_path_report)
    print(f"Saved text decision paths analysis: {path_txt_file}")
    
    path_md_file = os.path.join(REPORT_DIR, "decision_path_analysis.md")
    with open(path_md_file, "w") as f:
        f.write(full_path_report)
    print(f"Saved markdown decision paths analysis: {path_md_file}")
    
    print("\nPhase 9, 10, 11 Analysis Completed successfully!")

if __name__ == "__main__":
    run_tree_analysis()
