#!/usr/bin/env python3
"""
Phase 5: Baseline Decision Tree Model
Trains unpruned DecisionTreeClassifier(criterion='gini', random_state=42)
on N-BaIoT preprocessed dataset and records comprehensive performance metrics.
"""

import os
import time
import numpy as np
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)

PROJECT_DIR = "/Users/swapnil/Documents/cns/group1_decision_tree"
DATA_PATH = os.path.join(PROJECT_DIR, "data/preprocessed_data.joblib")
TABLES_DIR = os.path.join(PROJECT_DIR, "results/tables")
MODELS_DIR = os.path.join(PROJECT_DIR, "results/models")

def run_baseline():
    print("=" * 70)
    print("PHASE 5: Baseline Decision Tree Training & Evaluation")
    print("=" * 70)
    
    # 1. Load preprocessed dataset
    data = joblib.load(DATA_PATH)
    X_train = data["X_train"]
    X_test = data["X_test"]
    y_train = data["y_train"]
    y_test = data["y_test"]
    class_names = data["class_names"]
    feature_names = data["feature_names"]
    
    print(f"Loaded dataset: X_train {X_train.shape}, X_test {X_test.shape}")
    print(f"Number of classes: {len(class_names)}")
    
    # 2. Initialize and Train Baseline Decision Tree
    clf = DecisionTreeClassifier(criterion="gini", random_state=42)
    
    t0_train = time.perf_counter()
    clf.fit(X_train, y_train)
    t_train = time.perf_counter() - t0_train
    print(f"Training completed in {t_train:.4f} seconds.")
    
    # 3. Model Architecture Metrics
    tree_depth = clf.get_depth()
    node_count = clf.tree_.node_count
    leaf_count = clf.get_n_leaves()
    print(f"Tree Architecture: Depth={tree_depth}, Total Nodes={node_count}, Leaves={leaf_count}")
    
    # 4. Measure Inference Time
    # Warmup
    _ = clf.predict(X_test[:100])
    
    t0_inf = time.perf_counter()
    y_pred = clf.predict(X_test)
    t_inf_total = time.perf_counter() - t0_inf
    
    latency_per_sample_us = (t_inf_total / len(X_test)) * 1e6
    throughput_samples_per_sec = len(X_test) / t_inf_total
    
    print(f"Inference completed on {len(X_test)} samples in {t_inf_total:.4f} s")
    print(f"Latency per sample: {latency_per_sample_us:.2f} microseconds")
    print(f"Throughput: {throughput_samples_per_sec:,.0f} samples/second")
    
    # 5. Evaluate Metrics
    acc = accuracy_score(y_test, y_pred)
    prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_pred, average="macro", zero_division=0)
    prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted", zero_division=0)
    
    # Training accuracy
    y_train_pred = clf.predict(X_train)
    train_acc = accuracy_score(y_train, y_train_pred)
    
    print(f"\nModel Performance Metrics:")
    print(f"  Training Accuracy:  {train_acc * 100:.4f}%")
    print(f"  Test Accuracy:      {acc * 100:.4f}%")
    print(f"  Macro F1-Score:     {f1_macro * 100:.4f}%")
    print(f"  Weighted F1-Score:  {f1_weighted * 100:.4f}%")
    print(f"  Macro Precision:    {prec_macro * 100:.4f}%")
    print(f"  Macro Recall:       {rec_macro * 100:.4f}%")
    
    # 6. Per-class metrics
    per_class_p, per_class_r, per_class_f1, per_class_supp = precision_recall_fscore_support(
        y_test, y_pred, labels=range(len(class_names)), zero_division=0
    )
    
    df_per_class = pd.DataFrame({
        "class_id": range(len(class_names)),
        "class_name": class_names,
        "precision": [round(p, 6) for p in per_class_p],
        "recall": [round(r, 6) for r in per_class_r],
        "f1_score": [round(f, 6) for f in per_class_f1],
        "support": per_class_supp
    })
    
    per_class_path = os.path.join(TABLES_DIR, "baseline_classification_report.csv")
    df_per_class.to_csv(per_class_path, index=False)
    print(f"\nSaved Per-Class Report: {per_class_path}")
    print(df_per_class.to_string(index=False))
    
    # 7. Binary Detection Metrics (Benign = class 0 vs Attack = classes 1..10)
    y_test_bin = (y_test != 0).astype(int)
    y_pred_bin = (y_pred != 0).astype(int)
    bin_acc = accuracy_score(y_test_bin, y_pred_bin)
    bin_p, bin_r, bin_f1, _ = precision_recall_fscore_support(y_test_bin, y_pred_bin, average="binary")
    
    print(f"\nBinary Botnet Detection (Benign vs Malicious):")
    print(f"  Binary Accuracy:  {bin_acc * 100:.4f}%")
    print(f"  Binary Precision: {bin_p * 100:.4f}%")
    print(f"  Binary Recall:    {bin_r * 100:.4f}%")
    print(f"  Binary F1-Score:  {bin_f1 * 100:.4f}%")
    
    # 8. Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    df_cm = pd.DataFrame(cm, index=class_names, columns=class_names)
    cm_path = os.path.join(TABLES_DIR, "baseline_confusion_matrix.csv")
    df_cm.to_csv(cm_path)
    
    # 9. Summary Metrics Table
    summary_metrics = pd.DataFrame([{
        "model": "Baseline Decision Tree (Unpruned)",
        "criterion": "gini",
        "ccp_alpha": 0.0,
        "tree_depth": tree_depth,
        "node_count": node_count,
        "leaf_count": leaf_count,
        "train_accuracy": round(train_acc, 6),
        "test_accuracy": round(acc, 6),
        "macro_precision": round(prec_macro, 6),
        "macro_recall": round(rec_macro, 6),
        "macro_f1": round(f1_macro, 6),
        "weighted_f1": round(f1_weighted, 6),
        "binary_accuracy": round(bin_acc, 6),
        "binary_precision": round(bin_p, 6),
        "binary_recall": round(bin_r, 6),
        "binary_f1": round(bin_f1, 6),
        "training_time_sec": round(t_train, 4),
        "inference_time_sec": round(t_inf_total, 4),
        "latency_per_sample_us": round(latency_per_sample_us, 2),
        "throughput_samples_per_sec": round(throughput_samples_per_sec, 1)
    }])
    summary_path = os.path.join(TABLES_DIR, "baseline_metrics.csv")
    summary_metrics.to_csv(summary_path, index=False)
    print(f"\nSaved Baseline Metrics: {summary_path}")
    
    # 10. Save Model
    model_path = os.path.join(MODELS_DIR, "baseline_decision_tree.joblib")
    joblib.dump(clf, model_path, compress=3)
    print(f"Saved Baseline Model: {model_path} ({os.path.getsize(model_path)/(1024*1024):.2f} MB)")
    print("\nPhase 5 Baseline Complete successfully!")

if __name__ == "__main__":
    run_baseline()
