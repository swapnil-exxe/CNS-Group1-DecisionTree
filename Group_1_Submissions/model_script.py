#!/usr/bin/env python3
"""
Bhartiya Vidya Bhavan's
Sardar Patel Institute of Technology
Subject: Cryptography & Network Security (CNS) A.Y. 2026-27
Faculty: Prof. Renuka Pawar

Collaborative R&D Benchmark Tournament: Group 1 Submission Script
Algorithm: CART Decision Tree (sklearn.tree.DecisionTreeClassifier)
Research Context: Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees
Dataset: N-BaIoT (UCI Machine Learning Repository)
Selected Regularization: Minimal Cost-Complexity Pruning (ccp_alpha = 1.9997530739682578e-05)
"""

import os
import time
import numpy as np
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, classification_report
)

# -------------------------------------------------------------
# 1. Dataset Loading & Assumptions
# -------------------------------------------------------------
# The script expects preprocessed N-BaIoT arrays:
# X_train: (102692, 115) | X_test: (25674, 115)
# y_train: (102692,)     | y_test: (25674,)
# Stratified 80/20 partition systematically sampled (step=55) across all 89 N-BaIoT CSVs.
# -------------------------------------------------------------

def load_data():
    candidate_paths = [
        "preprocessed_data.joblib",
        "data/preprocessed_data.joblib",
        "../data/preprocessed_data.joblib",
        "/Users/swapnil/Documents/cns/group1_decision_tree/data/preprocessed_data.joblib"
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            print(f"[+] Loaded standardized dataset from: {p}")
            data = joblib.load(p)
            return data["X_train"], data["X_test"], data["y_train"], data["y_test"], data["class_names"]
            
    raise FileNotFoundError(
        "Could not find 'preprocessed_data.joblib'. Please ensure preprocessed data is placed "
        "in the current directory or data/ folder."
    )

# -------------------------------------------------------------
# 2. Standardized Tournament Evaluation Engine (Faculty Notice)
# -------------------------------------------------------------
def evaluate_tournament_model(model, X_train, X_test, y_train, y_test):
    """
    Standardized benchmarking engine for the Batch Performance Tournament.
    Accurately computes: Accuracy, Precision, Recall, F1-Score, ROC-AUC,
    Training Time (s), and Inference Latency (ms/sample).
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
    
    # 6. Format Visual Output for Easy Student & Faculty Logging
    print("\n --- TOURNAMENT BENCHMARK RESULTS --- ")
    print(f"Dataset Pipeline Type : {'Multiclass' if is_multiclass else 'Binary'}")
    print(f"Model Mechanics Framework: {'Unsupervised' if is_unsupervised else 'Supervised'}")
    print("-" * 40)
    for key, value in metrics.items():
        print(f"{key:<30}: {value:.6f}")
        
    return metrics, y_pred

# -------------------------------------------------------------
# 3. Main Execution Block
# -------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("CNS Group 1 - Optimized CART Decision Tree Tournament Benchmark")
    print("=" * 70)
    
    # Load dataset
    X_train, X_test, y_train, y_test, class_names = load_data()
    print(f"Training Instances: {X_train.shape[0]} | Test Instances: {X_test.shape[0]} | Features: {X_train.shape[1]}")
    
    # Initialize Final Optimized CART Decision Tree
    OPTIMAL_ALPHA = 1.9997530739682578e-05
    model = DecisionTreeClassifier(
        criterion="gini",
        splitter="best",
        ccp_alpha=OPTIMAL_ALPHA,
        random_state=42
    )
    
    # Run evaluation
    metrics, y_pred = evaluate_tournament_model(model, X_train, X_test, y_train, y_test)
    
    # Export results to results.csv
    df_res = pd.DataFrame([metrics])
    df_res.to_csv("results.csv", index=False)
    print("[+] Tournament metrics successfully exported to 'results.csv'")
    
    # Display tree complexity
    depth = model.get_depth()
    leaves = model.get_n_leaves()
    nodes = model.tree_.node_count
    print(f"\nFinal Pruned Tree Structural Complexity:")
    print(f"  - Maximum Depth : {depth} (Baseline: 21, -14.3%)")
    print(f"  - Total Nodes   : {nodes} (Baseline: 181, -26.5%)")
    print(f"  - Terminal Leaves: {leaves} (Baseline: 91, -26.4%)")
    print("=" * 70)
