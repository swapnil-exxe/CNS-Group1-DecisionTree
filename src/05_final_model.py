#!/usr/bin/env python3
"""
Phase 7 & Phase 8: Final Model Training and Evaluation on Untouched Test Partition
Retrains the Decision Tree on the complete original training partition (102,692 samples)
using the optimal ccp_alpha selected strictly from the validation experiment (zero test leakage).
Evaluates performance exactly once on the held-out test set (25,674 samples).
"""

import os
import time
import json
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

PROJECT_DIR = "/Users/swapnil/Documents/cns/group1_decision_tree"
DATA_PATH = os.path.join(PROJECT_DIR, "data/preprocessed_data.joblib")
TABLES_DIR = os.path.join(PROJECT_DIR, "results/tables")
FIGURES_DIR = os.path.join(PROJECT_DIR, "results/figures")
MODELS_DIR = os.path.join(PROJECT_DIR, "results/models")

RANDOM_STATE = 42

def run_final_evaluation():
    print("=" * 70)
    print("PHASE 7 & 8: Final Model Retraining & Official Test Set Evaluation")
    print("=" * 70)
    
    # 1. Load data
    data = joblib.load(DATA_PATH)
    X_train = data["X_train"]
    X_test = data["X_test"]
    y_train = data["y_train"]
    y_test = data["y_test"]
    class_names = data["class_names"]
    
    # 2. Load the optimal alpha selected from internal validation
    alpha_file = os.path.join(TABLES_DIR, "selected_alpha.json")
    with open(alpha_file, "r") as f:
        alpha_meta = json.load(f)
        
    optimal_alpha = float(alpha_meta["selected_ccp_alpha"])
    print(f"Optimal ccp_alpha loaded from validation tuning: {optimal_alpha:.8f}")
    print(f"Selection criteria: {alpha_meta['selection_criteria']}")
    print(f"Validation performance at selection: Acc={alpha_meta['val_accuracy']*100:.3f}%, Macro F1={alpha_meta['val_macro_f1']*100:.3f}%")
    
    # 3. Retrain final model on the COMPLETE original training set (102,692 samples)
    final_dt = DecisionTreeClassifier(
        criterion="gini",
        ccp_alpha=optimal_alpha,
        random_state=RANDOM_STATE
    )
    
    t0_tr = time.perf_counter()
    final_dt.fit(X_train, y_train)
    t_train = time.perf_counter() - t0_tr
    print(f"\nFinal model retrained on full training set ({len(X_train):,} samples) in {t_train:.4f} s.")
    
    # Complexity metrics
    depth = int(final_dt.get_depth())
    nodes = int(final_dt.tree_.node_count)
    leaves = int(final_dt.get_n_leaves())
    print(f"Final Pruned Architecture: Depth={depth}, Nodes={nodes}, Leaves={leaves}")
    
    # 4. Evaluate ONCE on untouched held-out test partition (25,674 samples)
    t0_inf = time.perf_counter()
    y_pred = final_dt.predict(X_test)
    t_inf_total = time.perf_counter() - t0_inf
    
    y_train_pred = final_dt.predict(X_train)
    train_acc = float(accuracy_score(y_train, y_train_pred))
    
    acc = float(accuracy_score(y_test, y_pred))
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(y_test, y_pred, average="macro", zero_division=0)
    wt_p, wt_r, wt_f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted", zero_division=0)
    
    gen_gap = float(train_acc - acc)
    latency_us = float((t_inf_total / len(X_test)) * 1e6)
    throughput = float(len(X_test) / t_inf_total)
    
    print(f"\nOfficial Test Set Evaluation (Held-Out, Untouched 25,674 samples):")
    print(f"  Training Accuracy:  {train_acc * 100:.4f}%")
    print(f"  Testing Accuracy:   {acc * 100:.4f}%")
    print(f"  Generalization Gap: {gen_gap * 100:.4f}%")
    print(f"  Macro Precision:    {macro_p * 100:.4f}%")
    print(f"  Macro Recall:       {macro_r * 100:.4f}%")
    print(f"  Macro F1-Score:     {macro_f1 * 100:.4f}%")
    print(f"  Weighted F1-Score:  {wt_f1 * 100:.4f}%")
    
    # 5. Binary Botnet Detection Metrics (Secondary Analysis)
    y_test_bin = (y_test != 0).astype(int)
    y_pred_bin = (y_pred != 0).astype(int)
    bin_acc = float(accuracy_score(y_test_bin, y_pred_bin))
    bin_p, bin_r, bin_f1, _ = precision_recall_fscore_support(y_test_bin, y_pred_bin, average="binary")
    
    print(f"\nBinary Classification (Secondary Analysis: Benign vs Malicious):")
    print(f"  Binary Accuracy:  {bin_acc * 100:.4f}%")
    print(f"  Binary Precision: {bin_p * 100:.4f}%")
    print(f"  Binary Recall:    {bin_r * 100:.4f}%")
    print(f"  Binary F1-Score:  {bin_f1 * 100:.4f}%")
    
    # 6. Save Model Artifact
    model_save_path = os.path.join(MODELS_DIR, "final_decision_tree.joblib")
    joblib.dump(final_dt, model_save_path, compress=3)
    model_size_kb = round(os.path.getsize(model_save_path) / 1024, 2)
    print(f"\nSaved final trained model: {model_save_path} (Serialized Size: {model_size_kb} KB)")
    
    # 7. Per-Class Report
    p_class, r_class, f1_class, s_class = precision_recall_fscore_support(
        y_test, y_pred, labels=range(len(class_names)), zero_division=0
    )
    df_per_class = pd.DataFrame({
        "class_id": range(len(class_names)),
        "class_name": class_names,
        "precision": [round(float(p), 6) for p in p_class],
        "recall": [round(float(r), 6) for r in r_class],
        "f1_score": [round(float(f), 6) for f in f1_class],
        "support": [int(s) for s in s_class]
    })
    report_csv = os.path.join(TABLES_DIR, "classification_report.csv")
    df_per_class.to_csv(report_csv, index=False)
    print(f"Saved Per-Class Report: {report_csv}")
    
    # 8. Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    df_cm = pd.DataFrame(cm, index=class_names, columns=class_names)
    cm_csv_path = os.path.join(TABLES_DIR, "final_confusion_matrix.csv")
    df_cm.to_csv(cm_csv_path)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        df_cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=True,
        xticklabels=class_names,
        yticklabels=class_names
    )
    plt.title("Confusion Matrix: Final Pruned Decision Tree (11-Class N-BaIoT)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Predicted Class", fontweight="bold")
    plt.ylabel("Ground Truth Class", fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    cm_fig_path = os.path.join(FIGURES_DIR, "confusion_matrix.png")
    plt.savefig(cm_fig_path, dpi=300)
    plt.close()
    print(f"Saved Confusion Matrix Figure: {cm_fig_path}")
    
    # 9. Save Final Metrics Table
    final_metrics_df = pd.DataFrame([{
        "model": "Final Pruned Decision Tree",
        "ccp_alpha": float(optimal_alpha),
        "tree_depth": int(depth),
        "node_count": int(nodes),
        "leaf_count": int(leaves),
        "train_accuracy": round(train_acc, 6),
        "test_accuracy": round(acc, 6),
        "generalization_gap": round(gen_gap, 6),
        "macro_precision": round(float(macro_p), 6),
        "macro_recall": round(float(macro_r), 6),
        "macro_f1": round(float(macro_f1), 6),
        "weighted_f1": round(float(wt_f1), 6),
        "binary_accuracy": round(bin_acc, 6),
        "binary_precision": round(float(bin_p), 6),
        "binary_recall": round(float(bin_r), 6),
        "binary_f1": round(float(bin_f1), 6),
        "training_time_sec": round(t_train, 4),
        "inference_time_sec": round(t_inf_total, 5),
        "latency_us_per_sample": round(latency_us, 3),
        "throughput_samples_per_sec": round(throughput, 1),
        "serialized_model_size_kb": model_size_kb
    }])
    final_metrics_path = os.path.join(TABLES_DIR, "final_metrics.csv")
    final_metrics_df.to_csv(final_metrics_path, index=False)
    print(f"Saved Final Metrics Table: {final_metrics_path}")
    
    # 10. Baseline vs Pruned Comparison Table
    base_file = os.path.join(TABLES_DIR, "baseline_metrics.csv")
    base_df = pd.read_csv(base_file)
    
    base_alpha = float(base_df["ccp_alpha"].values[0])
    base_depth = int(base_df["tree_depth"].values[0])
    base_nodes = int(base_df["node_count"].values[0])
    base_leaves = int(base_df["leaf_count"].values[0])
    base_acc = float(base_df["test_accuracy"].values[0])
    base_f1 = float(base_df["macro_f1"].values[0])
    base_gap = float(base_df["train_accuracy"].values[0] - base_df["test_accuracy"].values[0])
    base_tr_time = float(base_df["training_time_sec"].values[0])
    
    comparison_records = [
        {
            "Metric": "Cost-Complexity Alpha (ccp_alpha)",
            "Baseline (Unpruned)": f"{base_alpha}",
            "Final Pruned Model": f"{optimal_alpha:.6e}",
            "Change / Impact": "Validation-Selected Optimal Alpha"
        },
        {
            "Metric": "Tree Depth",
            "Baseline (Unpruned)": f"{base_depth}",
            "Final Pruned Model": f"{depth}",
            "Change / Impact": f"-{base_depth - depth} levels (-{(base_depth - depth)/base_depth*100:.1f}%)"
        },
        {
            "Metric": "Total Node Count",
            "Baseline (Unpruned)": f"{base_nodes}",
            "Final Pruned Model": f"{nodes}",
            "Change / Impact": f"-{base_nodes - nodes} nodes (-{(base_nodes - nodes)/base_nodes*100:.1f}%)"
        },
        {
            "Metric": "Terminal Leaves (|T|)",
            "Baseline (Unpruned)": f"{base_leaves}",
            "Final Pruned Model": f"{leaves}",
            "Change / Impact": f"-{base_leaves - leaves} leaves (-{(base_leaves - leaves)/base_leaves*100:.1f}%)"
        },
        {
            "Metric": "Multiclass Test Accuracy",
            "Baseline (Unpruned)": f"{base_acc*100:.4f}%",
            "Final Pruned Model": f"{acc*100:.4f}%",
            "Change / Impact": f"+{(acc - base_acc)*100:.4f}%"
        },
        {
            "Metric": "Multiclass Macro F1-Score",
            "Baseline (Unpruned)": f"{base_f1*100:.4f}%",
            "Final Pruned Model": f"{macro_f1*100:.4f}%",
            "Change / Impact": f"+{(macro_f1 - base_f1)*100:.4f}%"
        },
        {
            "Metric": "Generalization Gap (Train - Test Acc)",
            "Baseline (Unpruned)": f"{base_gap*100:.4f}%",
            "Final Pruned Model": f"{gen_gap*100:.4f}%",
            "Change / Impact": f"-{(base_gap - gen_gap)*100:.4f}% (Overfitting reduced)"
        },
        {
            "Metric": "Training Time (s)",
            "Baseline (Unpruned)": f"{base_tr_time:.4f} s",
            "Final Pruned Model": f"{t_train:.4f} s",
            "Change / Impact": f"{t_train - base_tr_time:+.4f} s"
        }
    ]
    df_comparison = pd.DataFrame(comparison_records)
    comp_path = os.path.join(TABLES_DIR, "baseline_vs_pruned_comparison.csv")
    df_comparison.to_csv(comp_path, index=False)
    print(f"Saved Comparison Table: {comp_path}")
    print(df_comparison.to_string(index=False))
    
    print("\nPhase 7 & 8 Completed successfully!")

if __name__ == "__main__":
    run_final_evaluation()
