#!/usr/bin/env python3
"""
Phase 6: Cost-Complexity Pruning (ccp_alpha) Hyperparameter Tuning
Evaluates candidate ccp_alpha values using strict internal Train/Validation partitioning
on the training data (zero test-set selection bias), selects the optimal alpha based on
validation macro F1 and complexity criteria, and generates publication-quality trade-off plots.
"""

import os
import time
import json
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

PROJECT_DIR = "/Users/swapnil/Documents/cns/group1_decision_tree"
DATA_PATH = os.path.join(PROJECT_DIR, "data/preprocessed_data.joblib")
TABLES_DIR = os.path.join(PROJECT_DIR, "results/tables")
FIGURES_DIR = os.path.join(PROJECT_DIR, "results/figures")
MODELS_DIR = os.path.join(PROJECT_DIR, "results/models")

RANDOM_STATE = 42

def run_ccp_tuning():
    print("=" * 70)
    print("PHASE 6: Cost-Complexity Pruning Tuning (Validation-Isolated Methodology)")
    print("=" * 70)
    
    # 1. Load data
    data = joblib.load(DATA_PATH)
    X_train_full = data["X_train"]
    y_train_full = data["y_train"]
    class_names = data["class_names"]
    
    print(f"Full Training Partition: {X_train_full.shape[0]:,} samples, {X_train_full.shape[1]} features.")
    print("Note: The 20% test partition is strictly isolated and NOT inspected during tuning.")
    
    # 2. Create Internal Train / Validation Split from Training Partition (80/20)
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_train_full,
        y_train_full,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y_train_full
    )
    print(f"Internal Partitions Created:")
    print(f"  Internal Training Subset: {X_tr.shape[0]:,} samples (80.0% of training data)")
    print(f"  Internal Validation Set:  {X_val.shape[0]:,} samples (20.0% of training data)")
    
    # 3. Extract Pruning Path ONLY from Internal Training Subset
    base_tree = DecisionTreeClassifier(criterion="gini", random_state=RANDOM_STATE)
    print("\nComputing cost-complexity pruning path from internal training subset...")
    t0_path = time.perf_counter()
    path = base_tree.cost_complexity_pruning_path(X_tr, y_tr)
    t_path = time.perf_counter() - t0_path
    
    ccp_alphas, impurities = path.ccp_alphas, path.impurities
    print(f"Computed {len(ccp_alphas)} candidate alphas along exact pruning path in {t_path:.2f}s.")
    
    # Save raw pruning path data
    df_raw_path = pd.DataFrame({
        "step": range(len(ccp_alphas)),
        "ccp_alpha": ccp_alphas,
        "impurity": impurities
    })
    raw_path_file = os.path.join(TABLES_DIR, "ccp_pruning_path_raw.csv")
    df_raw_path.to_csv(raw_path_file, index=False)
    print(f"Saved raw pruning path to: {raw_path_file}")
    
    # 4. Select 20 Representative Candidate Alphas Across Path
    idx = np.round(np.linspace(0, len(ccp_alphas) - 1, 20)).astype(int)
    candidate_alphas = np.unique(ccp_alphas[idx])
    if 0.0 not in candidate_alphas:
        candidate_alphas = np.insert(candidate_alphas, 0, 0.0)
        
    print(f"\nEvaluating {len(candidate_alphas)} candidate ccp_alpha values on the Validation Set:")
    
    # 5. Train on Internal Train Subset, Evaluate on Validation Set
    records = []
    
    for idx_a, alpha in enumerate(candidate_alphas):
        t0_tr = time.perf_counter()
        clf = DecisionTreeClassifier(criterion="gini", ccp_alpha=alpha, random_state=RANDOM_STATE)
        clf.fit(X_tr, y_tr)
        t_tr = time.perf_counter() - t0_tr
        
        # Architecture
        depth = clf.get_depth()
        nodes = clf.tree_.node_count
        leaves = clf.get_n_leaves()
        
        # Validation Evaluation
        y_val_pred = clf.predict(X_val)
        val_acc = accuracy_score(y_val, y_val_pred)
        
        macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(
            y_val, y_val_pred, average="macro", zero_division=0
        )
        weighted_p, weighted_r, weighted_f1, _ = precision_recall_fscore_support(
            y_val, y_val_pred, average="weighted", zero_division=0
        )
        
        record = {
            "candidate_id": idx_a,
            "ccp_alpha": float(alpha),
            "tree_depth": int(depth),
            "node_count": int(nodes),
            "leaf_count": int(leaves),
            "val_accuracy": round(float(val_acc), 6),
            "val_macro_precision": round(float(macro_p), 6),
            "val_macro_recall": round(float(macro_r), 6),
            "val_macro_f1": round(float(macro_f1), 6),
            "val_weighted_f1": round(float(weighted_f1), 6),
            "training_time_sec": round(float(t_tr), 4)
        }
        records.append(record)
        
        print(f"Candidate {idx_a:2d} | alpha={alpha:.7f} | Depth={depth:2d} | Leaves={leaves:3d} | ValAcc={val_acc*100:.3f}% | ValF1={macro_f1*100:.3f}% | TrTime={t_tr:.2f}s")
        
    df_results = pd.DataFrame(records)
    results_path = os.path.join(TABLES_DIR, "ccp_alpha_results.csv")
    df_results.to_csv(results_path, index=False)
    print(f"\nSaved ccp_alpha validation tuning results to: {results_path}")
    
    # 6. Apply Selection Rule strictly on Validation Data:
    # Rule 1: Highest validation macro F1
    # Rule 2: Highest validation accuracy
    # Rule 3: Lowest tree complexity (fewer leaves) as tie-breaker
    best_candidate = df_results.sort_values(
        by=["val_macro_f1", "val_accuracy", "leaf_count"],
        ascending=[False, False, True]
    ).iloc[0]
    
    selected_alpha = float(best_candidate["ccp_alpha"])
    selected_id = int(best_candidate["candidate_id"])
    
    print("\n" + "=" * 50)
    print("OPTIMAL MODEL SELECTION (Validation Criteria)")
    print("=" * 50)
    print(f"Selected Candidate ID: {selected_id}")
    print(f"Optimal ccp_alpha:     {selected_alpha:.8f}")
    print(f"Validation Accuracy:   {best_candidate['val_accuracy']*100:.4f}%")
    print(f"Validation Macro F1:   {best_candidate['val_macro_f1']*100:.4f}%")
    print(f"Subtree Depth:         {int(best_candidate['tree_depth'])}")
    print(f"Subtree Leaves:        {int(best_candidate['leaf_count'])}")
    print("=" * 50)
    
    # Save selected alpha metadata
    selected_payload = {
        "selected_candidate_id": selected_id,
        "selected_ccp_alpha": selected_alpha,
        "selection_criteria": "Highest validation macro F1, secondary validation accuracy, tie-break minimum leaves",
        "val_accuracy": float(best_candidate["val_accuracy"]),
        "val_macro_f1": float(best_candidate["val_macro_f1"]),
        "val_depth": int(best_candidate["tree_depth"]),
        "val_leaves": int(best_candidate["leaf_count"])
    }
    with open(os.path.join(TABLES_DIR, "selected_alpha.json"), "w") as f:
        json.dump(selected_payload, f, indent=4)
        
    # 7. Generate Publication Figures with Validation Selected Alpha Marker
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})
    
    alphas_plot = df_results["ccp_alpha"]
    
    # Figure 1: ccp_alpha vs Validation F1
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(alphas_plot, df_results["val_macro_f1"] * 100, marker='o', linewidth=2, color="#1f77b4", label="Validation Macro F1-Score")
    ax.plot(alphas_plot, df_results["val_weighted_f1"] * 100, marker='s', linewidth=2, linestyle='--', color="#2ca02c", label="Validation Weighted F1-Score")
    ax.axvline(selected_alpha, color='#d62728', linestyle=':', linewidth=2, label=f"Selected alpha ({selected_alpha:.2e})")
    ax.set_xscale("symlog", linthresh=1e-5)
    ax.set_xlabel("Cost-Complexity Parameter: ccp_alpha (symlog scale)", fontweight="bold")
    ax.set_ylabel("Validation F1-Score (%)", fontweight="bold")
    ax.set_title("Validation Macro & Weighted F1 vs. ccp_alpha", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True)
    plt.tight_layout()
    f1_fig_path = os.path.join(FIGURES_DIR, "ccp_alpha_vs_f1.png")
    plt.savefig(f1_fig_path, dpi=300)
    plt.close()
    print(f"Saved figure: {f1_fig_path}")
    
    # Figure 2: ccp_alpha vs Validation Accuracy
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(alphas_plot, df_results["val_accuracy"] * 100, marker='^', linewidth=2, color="#1f77b4", label="Validation Accuracy")
    ax.axvline(selected_alpha, color='#d62728', linestyle=':', linewidth=2, label=f"Selected alpha ({selected_alpha:.2e})")
    ax.set_xscale("symlog", linthresh=1e-5)
    ax.set_xlabel("Cost-Complexity Parameter: ccp_alpha (symlog scale)", fontweight="bold")
    ax.set_ylabel("Validation Accuracy (%)", fontweight="bold")
    ax.set_title("Validation Accuracy vs. ccp_alpha", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True)
    plt.tight_layout()
    acc_fig_path = os.path.join(FIGURES_DIR, "ccp_alpha_vs_accuracy.png")
    plt.savefig(acc_fig_path, dpi=300)
    plt.close()
    print(f"Saved figure: {acc_fig_path}")
    
    # Figure 3: ccp_alpha vs Tree Depth
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(alphas_plot, df_results["tree_depth"], marker='D', linewidth=2, color="#9467bd", label="Subtree Depth")
    ax.axvline(selected_alpha, color='#d62728', linestyle=':', linewidth=2, label=f"Selected alpha ({selected_alpha:.2e})")
    ax.set_xscale("symlog", linthresh=1e-5)
    ax.set_xlabel("Cost-Complexity Parameter: ccp_alpha (symlog scale)", fontweight="bold")
    ax.set_ylabel("Tree Depth", fontweight="bold")
    ax.set_title("Subtree Depth vs. ccp_alpha", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True)
    plt.tight_layout()
    depth_fig_path = os.path.join(FIGURES_DIR, "ccp_alpha_vs_tree_depth.png")
    plt.savefig(depth_fig_path, dpi=300)
    plt.close()
    print(f"Saved figure: {depth_fig_path}")
    
    # Figure 4: ccp_alpha vs Number of Leaves
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(alphas_plot, df_results["leaf_count"], marker='p', linewidth=2, color="#8c564b", label="Terminal Leaves (|T|)")
    ax.axvline(selected_alpha, color='#d62728', linestyle=':', linewidth=2, label=f"Selected alpha ({selected_alpha:.2e})")
    ax.set_xscale("symlog", linthresh=1e-5)
    ax.set_xlabel("Cost-Complexity Parameter: ccp_alpha (symlog scale)", fontweight="bold")
    ax.set_ylabel("Number of Terminal Leaves (|T|)", fontweight="bold")
    ax.set_title("Structural Pruning: Leaves (|T|) vs. ccp_alpha", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True)
    plt.tight_layout()
    leaves_fig_path = os.path.join(FIGURES_DIR, "ccp_alpha_vs_leaves.png")
    plt.savefig(leaves_fig_path, dpi=300)
    plt.close()
    print(f"Saved figure: {leaves_fig_path}")
    
    # Figure 5: Training Time vs ccp_alpha
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(alphas_plot, df_results["training_time_sec"], marker='o', linewidth=2, color="#2ca02c", label="Training Time")
    ax.axvline(selected_alpha, color='#d62728', linestyle=':', linewidth=2, label=f"Selected alpha ({selected_alpha:.2e})")
    ax.set_xscale("symlog", linthresh=1e-5)
    ax.set_xlabel("Cost-Complexity Parameter: ccp_alpha (symlog scale)", fontweight="bold")
    ax.set_ylabel("Training Time (s)", fontweight="bold")
    ax.set_title("Computational Cost: Training Time vs. ccp_alpha", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True)
    plt.tight_layout()
    timing_fig_path = os.path.join(FIGURES_DIR, "ccp_alpha_vs_computational_time.png")
    plt.savefig(timing_fig_path, dpi=300)
    plt.close()
    print(f"Saved figure: {timing_fig_path}")
    
    print("\nPhase 6 Tuning Complete successfully!")

if __name__ == "__main__":
    run_ccp_tuning()
