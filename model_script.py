#!/usr/bin/env python3
"""
Bhartiya Vidya Bhavan's
Sardar Patel Institute of Technology
(An Empowered Autonomous Institute Affiliated to University of Mumbai)
Munshi Nagar, Andheri (W), Mumbai-400058

Subject: Cryptography & Network Security (CNS) A.Y. 2026-27
Faculty: Prof. Renuka Pawar
Collaborative R&D Manifest: Comparative Algorithmic Analysis for Advanced Cybersecurity Domains

GROUP 1 — DECISION TREE: Complete Executable Implementation
Algorithm: CART Decision Tree (sklearn.tree.DecisionTreeClassifier)
Assigned Research Context: Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees
Dataset: N-BaIoT (UCI Machine Learning Repository, Dataset ID: 442)
Regularization Strategy: Minimal Cost-Complexity Pruning (ccp_alpha)
Optimal Parameter: ccp_alpha = 1.9997530739682578e-05
"""

import os
import time
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

RANDOM_STATE = 42
OPTIMAL_CCP_ALPHA = 1.9997530739682578e-05

# -----------------------------------------------------------------------------
# 1. Dataset Loading Interface
# -----------------------------------------------------------------------------
def load_data():
    """
    Loads preprocessed N-BaIoT arrays:
    X_train: (102692, 115) | X_test: (25674, 115)
    y_train: (102692,)     | y_test: (25674,)
    Preserves exact 80/20 stratified partition systematically sampled (step=55)
    across all 89 N-BaIoT CSV files from 9 commercial IoT appliances.
    """
    candidate_paths = [
        "preprocessed_data.joblib",
        "data/preprocessed_data.joblib",
        "../data/preprocessed_data.joblib",
        "/Users/swapnil/Documents/cns/group1_decision_tree/data/preprocessed_data.joblib",
        "/Users/swapnil/Documents/cns/data/preprocessed_data.joblib"
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            print(f"[+] Successfully loaded preprocessed dataset from: {path}")
            data = joblib.load(path)
            return (
                data["X_train"], data["X_test"],
                data["y_train"], data["y_test"],
                data["class_names"]
            )
            
    raise FileNotFoundError(
        "Could not locate 'preprocessed_data.joblib'. Please ensure data is available "
        "in the local directory or under data/."
    )

# -----------------------------------------------------------------------------
# 2. Standardized Tournament Evaluation Engine (Faculty Notice)
# -----------------------------------------------------------------------------
def evaluate_tournament_model(model, X_train, X_test, y_train, y_test):
    """
    Standardized benchmarking engine for the Batch Performance Tournament
    as specified in Prof. Renuka Pawar's CNS Collaborative R&D Manifest.
    """
    is_unsupervised = hasattr(model, 'contamination') or model.__class__.__name__ in ['KMeans', 'KMedoids', 'IsolationForest']
    is_multiclass = len(np.unique(y_test)) > 2
    
    # 1. Benchmark Standardized Training Latency
    start_train = time.time()
    if is_unsupervised:
        model.fit(X_train)
    else:
        model.fit(X_train, y_train)
    end_train = time.time()
    training_time_seconds = end_train - start_train
    
    # 2. Benchmark Standardized Inference Latency
    start_infer = time.time()
    y_pred = model.predict(X_test)
    end_infer = time.time()
    
    total_inference_time_ms = (end_infer - start_infer) * 1000
    inference_latency_per_sample_ms = total_inference_time_ms / len(X_test)
    
    # 3. Dynamic Alignments for Anomaly Detectors / Clusters (if applicable)
    if is_unsupervised:
        if hasattr(model, 'predict') and -1 in y_pred:
            y_pred = np.where(y_pred == -1, 1, 0)
        elif model.__class__.__name__ in ['KMeans', 'KMedoids']:
            from scipy.stats import mode
            labels = np.zeros_like(y_pred)
            for i in range(model.n_clusters):
                mask = (y_pred == i)
                if np.sum(mask) > 0:
                    labels[mask] = mode(y_test[mask])[0]
            y_pred = labels

    # 4. Comprehensive Mathematical ROC-AUC Probability Parsing
    try:
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)
            if is_multiclass:
                roc_auc = roc_auc_score(y_test, y_prob, multi_class='ovr', average='macro')
            else:
                roc_auc = roc_auc_score(y_test, y_prob[:, 1])
        elif hasattr(model, "decision_function"):
            y_score = model.decision_function(X_test)
            if is_multiclass:
                roc_auc = roc_auc_score(y_test, y_score, multi_class='ovr', average='macro')
            else:
                roc_auc = roc_auc_score(y_test, y_score)
        else:
            raise AttributeError
    except (AttributeError, IndexError, ValueError):
        if is_multiclass:
            from sklearn.preprocessing import label_binarize
            classes = np.unique(y_test)
            y_test_bin = label_binarize(y_test, classes=classes)
            y_pred_bin = label_binarize(y_pred, classes=classes)
            roc_auc = roc_auc_score(y_test_bin, y_pred_bin, average='macro')
        else:
            roc_auc = roc_auc_score(y_test, y_pred)
            
    # 5. Compile Global Structural Metrics
    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred) * 100,
        "Precision": precision_score(y_test, y_pred, average='macro', zero_division=0) * 100,
        "Recall": recall_score(y_test, y_pred, average='macro', zero_division=0) * 100,
        "F1-Score": f1_score(y_test, y_pred, average='macro', zero_division=0) * 100,
        "ROC-AUC": roc_auc,
        "Training Time (s)": training_time_seconds,
        "Inference Latency (ms/sample)": inference_latency_per_sample_ms
    }
    
    # 6. Format Visual Output for Easy Student Logging
    print("\n --- TOURNAMENT BENCHMARK RESULTS --- ")
    print(f"Dataset Pipeline Type : {'Multiclass' if is_multiclass else 'Binary'}")
    print(f"Model Mechanics Framework: {'Unsupervised' if is_unsupervised else 'Supervised'}")
    print("-" * 40)
    for key, value in metrics.items():
        print(f"{key:<30}: {value:.6f}")
        
    return metrics, y_pred

# -----------------------------------------------------------------------------
# 3. High-Resolution Confusion Matrix Generation
# -----------------------------------------------------------------------------
def plot_confusion_matrix(y_true, y_pred, class_names, output_filename="confusion_matrix.png"):
    """
    Renders and exports a publication-grade confusion matrix.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8), dpi=300)
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=class_names, yticklabels=class_names,
        cbar_kws={'label': 'Packet Count'}
    )
    plt.title("GROUP 1 DECISION TREE: Final Pruned Test Confusion Matrix\n(ccp_alpha = 1.9998e-5, N = 25,674)", fontsize=12, fontweight='bold', pad=15)
    plt.xlabel("Predicted Class Label", fontsize=10, fontweight='bold')
    plt.ylabel("Ground Truth Class Label", fontsize=10, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig(output_filename, bbox_inches='tight')
    plt.close()
    print(f"[+] High-resolution confusion matrix saved to: {output_filename}")

# -----------------------------------------------------------------------------
# 4. Main Execution Pipeline
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 75)
    print("SARDAR PATEL INSTITUTE OF TECHNOLOGY | CNS COLLABORATIVE R&D")
    print("GROUP 1 — DECISION TREE: OPTIMIZED BENCHMARK PIPELINE")
    print("=" * 75)
    
    # Step 1: Load Data
    X_train, X_test, y_train, y_test, class_names = load_data()
    print(f"[+] Ingestion Summary: Train={X_train.shape[0]} | Test={X_test.shape[0]} | Features={X_train.shape[1]} | Classes={len(class_names)}")
    
    # Step 2: Baseline Unpruned Tree Evaluation (for structural comparison)
    print("\n--- Evaluating Baseline Decision Tree (ccp_alpha=0.0) ---")
    baseline_tree = DecisionTreeClassifier(criterion="gini", splitter="best", ccp_alpha=0.0, random_state=RANDOM_STATE)
    t0_b = time.time()
    baseline_tree.fit(X_train, y_train)
    t1_b = time.time()
    y_pred_b = baseline_tree.predict(X_test)
    acc_b = accuracy_score(y_test, y_pred_b) * 100
    f1_b = f1_score(y_test, y_pred_b, average='macro', zero_division=0) * 100
    print(f"  Baseline Depth  : {baseline_tree.get_depth()} levels")
    print(f"  Baseline Nodes  : {baseline_tree.tree_.node_count} nodes")
    print(f"  Baseline Leaves : {baseline_tree.get_n_leaves()} leaves")
    print(f"  Baseline Test Acc: {acc_b:.4f}% | Macro F1: {f1_b:.4f}%")
    
    # Step 3: Final Optimized Pruned Decision Tree
    print("\n--- Evaluating Final Pruned Decision Tree (ccp_alpha=1.999753e-05) ---")
    final_pruned_tree = DecisionTreeClassifier(
        criterion="gini",
        splitter="best",
        ccp_alpha=OPTIMAL_CCP_ALPHA,
        random_state=RANDOM_STATE
    )
    
    # Execute Standardized Tournament Engine
    metrics, y_pred_final = evaluate_tournament_model(final_pruned_tree, X_train, X_test, y_train, y_test)
    
    # Output Structural Properties
    depth_p = final_pruned_tree.get_depth()
    nodes_p = final_pruned_tree.tree_.node_count
    leaves_p = final_pruned_tree.get_n_leaves()
    print(f"\nFinal Pruned Structural Impact:")
    print(f"  - Tree Depth    : {depth_p} levels (-{((baseline_tree.get_depth()-depth_p)/baseline_tree.get_depth())*100:.1f}%)")
    print(f"  - Total Nodes   : {nodes_p} nodes (-{((baseline_tree.tree_.node_count-nodes_p)/baseline_tree.tree_.node_count)*100:.1f}%)")
    print(f"  - Terminal Leaves: {leaves_p} leaves (-{((baseline_tree.get_n_leaves()-leaves_p)/baseline_tree.get_n_leaves())*100:.1f}%)")
    
    # Step 4: Export Confusion Matrix
    plot_confusion_matrix(y_test, y_pred_final, class_names, "confusion_matrix.png")
    
    # Step 5: Export results to results.csv
    df_results = pd.DataFrame([metrics])
    df_results.to_csv("results.csv", index=False)
    print(f"[+] Tournament metrics exported to results.csv successfully.")
    print("=" * 75)
