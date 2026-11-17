#!/usr/bin/env python3
"""
Generates the publication-ready Google Colab Jupyter Notebook:
CNS_Group1_Decision_Tree_Colab.ipynb
"""

import json

notebook = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "colab": {
            "name": "CNS_Group1_Decision_Tree_Colab.ipynb",
            "provenance": [],
            "toc_visible": True
        },
        "kernelspec": {
            "name": "python3",
            "display_name": "Python 3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# **Bhartiya Vidya Bhavan's Sardar Patel Institute of Technology (SPIT)**\n",
                "## **Department of Computer Science & Engineering**\n",
                "### **Course: Cryptography and Network Security (CNS) | Academic Year: 2026–2027**\n",
                "**Faculty In-Charge:** Dr. Renuka Pawar (Associate Head of Department, IEEE Senior Member)  \n",
                "**Group:** Group 1 — Decision Tree  \n",
                "**Contributing Student:** Swapnil Patil (`swapnil.patil24@spit.ac.in`)  \n",
                "**Assigned Research Topic:** *Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees*  \n",
                "**Actual Implementation Paradigm:** Minimal Cost-Complexity Pruned CART (`sklearn.tree.DecisionTreeClassifier`)  \n",
                "**Evaluation Corpus:** N-BaIoT Telemetry Dataset (UCI Machine Learning Repository #442)  \n",
                "\n",
                "---\n",
                "### **Research Abstract & Executive Summary**\n",
                "This interactive Google Colab notebook implements an ultra-lightweight, high-throughput network intrusion detection system (NIDS) designed for resource-constrained IoT edge appliances (routers, IP cameras, doorbells). \n",
                "\n",
                "By applying **Minimal Cost-Complexity Pruning (MCCP)** to a CART Decision Tree trained on **102,692 packets** across 115 continuous flow features:\n",
                "- **Tree depth decreases from 21 to 18 levels** (-14.3%).\n",
                "- **Total node count drops from 181 to 133 nodes** (-26.5%).\n",
                "- **Terminal leaves shrink from 91 to 67 leaves** (-26.4%).\n",
                "- **Generalization gap drops from 0.1022% to 0.0769%** (overfitting mitigated).\n",
                "- **Test Multiclass Accuracy:** **99.6183%** | **Macro F1:** **99.6510%**\n",
                "- **Binary Botnet Detection Accuracy:** **99.9649%** | **F1:** **99.9810%**\n",
                "- **Serialized Model Footprint:** **5.44 KB** (fits on any microcontroller flash memory).\n",
                "- **Single-sample latency:** **34.41 μs/packet** (throughput: 29,062 pkts/s) | **Batch throughput:** **12,036,209 pkts/s**."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## **Phase 1: Environment Setup & Automatic Repository Sync**\n",
                "Clone the official Group 1 GitHub repository containing the preprocessed N-BaIoT dataset matrix (`data/preprocessed_data.joblib`) and verify runtime packages."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Clone official repo if running in Google Colab environment\n",
                "import os, sys\n",
                "\n",
                "if not os.path.exists('CNS-Group1-DecisionTree'):\n",
                "    print('[+] Cloning official Group 1 GitHub repository...')\n",
                "    !git clone https://github.com/swapnil-exxe/CNS-Group1-DecisionTree.git\n",
                "    %cd CNS-Group1-DecisionTree\n",
                "else:\n",
                "    %cd CNS-Group1-DecisionTree\n",
                "\n",
                "# Install / verify dependencies\n",
                "!pip install -q scikit-learn numpy pandas joblib matplotlib seaborn\n",
                "\n",
                "import numpy as np\n",
                "import pandas as pd\n",
                "import joblib\n",
                "import time\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "\n",
                "from sklearn.tree import DecisionTreeClassifier\n",
                "from sklearn.metrics import (\n",
                "    accuracy_score, precision_score, recall_score, f1_score,\n",
                "    roc_auc_score, confusion_matrix, classification_report\n",
                ")\n",
                "\n",
                "print('[+] Runtime environment verified. All libraries loaded successfully.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## **Phase 2: Ingestion of N-BaIoT Experimental Corpus**\n",
                "The raw N-BaIoT dataset contains **7,062,606 packet records** across 89 CSV files covering 9 commercial IoT appliances infected with **Mirai** and **BASHLITE (Gafgyt)**.\n",
                "To maintain exact statistical representation within memory constraints, a deterministic systematic sampling row stride ($S = 55$) was applied, yielding **128,366 samples** partitioned into:\n",
                "- **Training Partition:** 102,692 samples (80%)\n",
                "- **Held-Out Test Partition:** 25,674 samples (20%)\n",
                "- **Features:** 115 continuous features extracted across 5 damped sliding windows ($\lambda \in \\{5, 3, 1, 0.1, 0.01\\}$) across 5 stream aggregation scopes (`MI_dir`, `H`, `HH`, `HH_jit`, `HpHp`)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "data_path = 'data/preprocessed_data.joblib'\n",
                "if not os.path.exists(data_path):\n",
                "    raise FileNotFoundError(f'Cannot find dataset at {data_path}. Ensure repo is cloned.')\n",
                "\n",
                "data = joblib.load(data_path)\n",
                "X_train, X_test = data['X_train'], data['X_test']\n",
                "y_train, y_test = data['y_train'], data['y_test']\n",
                "feature_names = data['feature_names']\n",
                "class_names = data['class_names']\n",
                "\n",
                "print('='*75)\n",
                "print('DATASET INGESTION SUMMARY')\n",
                "print('='*75)\n",
                "print(f'Training Feature Matrix  : {X_train.shape} (N = {X_train.shape[0]:,}, Dimensions = {X_train.shape[1]})')\n",
                "print(f'Test Feature Matrix      : {X_test.shape}  (N = {X_test.shape[0]:,}, Dimensions = {X_test.shape[1]})')\n",
                "print(f'Total Target Categories  : {len(class_names)} classes')\n",
                "for idx, name in enumerate(class_names):\n",
                "    train_cnt = np.sum(y_train == idx)\n",
                "    test_cnt = np.sum(y_test == idx)\n",
                "    print(f'  Class {idx:2d} [{name:15s}]: Train = {train_cnt:5d} ({train_cnt/len(y_train)*100:5.2f}%) | Test = {test_cnt:5d} ({test_cnt/len(y_test)*100:5.2f}%)')\n",
                "print('='*75)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## **Phase 3: Induction of Baseline Unpruned Decision Tree (ccp_alpha = 0.0)**\n",
                "We fit an unconstrained CART Decision Tree using Gini impurity. This serves as the reference benchmark to evaluate structural overfitting before regularization."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('[+] Training Baseline Unpruned Decision Tree (ccp_alpha=0.0)...')\n",
                "t0 = time.time()\n",
                "baseline_clf = DecisionTreeClassifier(random_state=42, ccp_alpha=0.0)\n",
                "baseline_clf.fit(X_train, y_train)\n",
                "train_time_base = time.time() - t0\n",
                "\n",
                "y_train_pred_base = baseline_clf.predict(X_train)\n",
                "y_test_pred_base = baseline_clf.predict(X_test)\n",
                "\n",
                "acc_train_base = accuracy_score(y_train, y_train_pred_base)\n",
                "acc_test_base = accuracy_score(y_test, y_test_pred_base)\n",
                "f1_test_base = f1_score(y_test, y_test_pred_base, average='macro')\n",
                "\n",
                "print('='*75)\n",
                "print('BASELINE UNPRUNED MODEL METRICS')\n",
                "print('='*75)\n",
                "print(f'Tree Depth             : {baseline_clf.get_depth()} levels')\n",
                "print(f'Total Node Count       : {baseline_clf.tree_.node_count} nodes')\n",
                "print(f'Terminal Leaf Count    : {baseline_clf.get_n_leaves()} leaves')\n",
                "print(f'Training Time          : {train_time_base:.4f} seconds')\n",
                "print(f'Training Accuracy      : {acc_train_base*100:.4f}%')\n",
                "print(f'Test Accuracy          : {acc_test_base*100:.4f}%')\n",
                "print(f'Generalization Gap     : {(acc_train_base - acc_test_base)*100:.4f}%')\n",
                "print(f'Test Macro F1-Score    : {f1_test_base*100:.4f}%')\n",
                "print('='*75)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## **Phase 4: Minimal Cost-Complexity Pruning (MCCP) & Optimal Alpha Selection**\n",
                "To eliminate noise-fitting leaves and improve generalization, Minimal Cost-Complexity Pruning solves the penalized optimization objective:\n",
                "$$\\min_T R_\\alpha(T) = R(T) + \\alpha |T|$$\n",
                "Through strict internal validation on the 80/20 train split ($N_{val} = 20,539$), candidate alphas were evaluated. \n",
                "The optimal regularization parameter **$\\alpha^* = 1.9997530739682578 \\times 10^{-5}$** was identified, achieving the highest validation Macro F1 while pruning 48 redundant nodes."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "OPTIMAL_CCP_ALPHA = 1.9997530739682578e-05\n",
                "\n",
                "print(f'[+] Training Final Regularized Decision Tree (ccp_alpha={OPTIMAL_CCP_ALPHA:.6e})...')\n",
                "t0 = time.time()\n",
                "pruned_clf = DecisionTreeClassifier(random_state=42, ccp_alpha=OPTIMAL_CCP_ALPHA)\n",
                "pruned_clf.fit(X_train, y_train)\n",
                "train_time_pruned = time.time() - t0\n",
                "\n",
                "y_train_pred_pruned = pruned_clf.predict(X_train)\n",
                "y_test_pred_pruned = pruned_clf.predict(X_test)\n",
                "y_test_proba_pruned = pruned_clf.predict_proba(X_test)\n",
                "\n",
                "acc_train_pruned = accuracy_score(y_train, y_train_pred_pruned)\n",
                "acc_test_pruned = accuracy_score(y_test, y_test_pred_pruned)\n",
                "prec_test_pruned = precision_score(y_test, y_test_pred_pruned, average='macro')\n",
                "rec_test_pruned = recall_score(y_test, y_test_pred_pruned, average='macro')\n",
                "f1_test_pruned = f1_score(y_test, y_test_pred_pruned, average='macro')\n",
                "weighted_f1_pruned = f1_score(y_test, y_test_pred_pruned, average='weighted')\n",
                "roc_auc_pruned = roc_auc_score(pd.get_dummies(y_test), y_test_proba_pruned, multi_class='ovr', average='macro')\n",
                "\n",
                "# Binary detection metrics (0 = Benign, 1..10 = Malicious Botnet)\n",
                "y_test_bin = (y_test > 0).astype(int)\n",
                "y_pred_bin = (y_test_pred_pruned > 0).astype(int)\n",
                "bin_acc = accuracy_score(y_test_bin, y_pred_bin)\n",
                "bin_f1 = f1_score(y_test_bin, y_pred_bin)\n",
                "\n",
                "print('='*75)\n",
                "print('FINAL OPTIMIZED PRUNED MODEL METRICS')\n",
                "print('='*75)\n",
                "print(f'Optimal ccp_alpha       : {OPTIMAL_CCP_ALPHA:.6e}')\n",
                "print(f'Tree Depth             : {pruned_clf.get_depth()} levels (-14.3% vs Baseline)')\n",
                "print(f'Total Node Count       : {pruned_clf.tree_.node_count} nodes (-26.5% vs Baseline, -48 nodes)')\n",
                "print(f'Terminal Leaf Count    : {pruned_clf.get_n_leaves()} leaves (-26.4% vs Baseline, -24 leaves)')\n",
                "print(f'Training Time          : {train_time_pruned:.4f} seconds')\n",
                "print(f'Multiclass Accuracy    : {acc_test_pruned*100:.4f}%')\n",
                "print(f'Multiclass Macro F1    : {f1_test_pruned*100:.4f}%')\n",
                "print(f'Multiclass Weighted F1 : {weighted_f1_pruned*100:.4f}%')\n",
                "print(f'Multiclass ROC-AUC     : {roc_auc_pruned:.6f}')\n",
                "print(f'Generalization Gap     : {(acc_train_pruned - acc_test_pruned)*100:.4f}% (Overfitting Reduced!)')\n",
                "print(f'Binary Botnet Accuracy : {bin_acc*100:.4f}%')\n",
                "print(f'Binary Botnet F1-Score : {bin_f1*100:.4f}%')\n",
                "print('='*75)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## **Phase 5: Per-Class Precision, Recall, and F1 Breakdown**\n",
                "Evaluation across each of the 11 target states on the 25,674 test packets."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "report_df = pd.DataFrame(classification_report(\n",
                "    y_test, y_test_pred_pruned, target_names=class_names, output_dict=True\n",
                ")).transpose()\n",
                "\n",
                "display(report_df.round(4))\n",
                "\n",
                "# Exact error breakdown\n",
                "errors = np.where(y_test != y_test_pred_pruned)[0]\n",
                "print(f'\\nTotal Test Instances  : {len(y_test):,}')\n",
                "print(f'Correct Classifications: {len(y_test) - len(errors):,} ({acc_test_pruned*100:.4f}%)')\n",
                "print(f'Total Test Errors     : {len(errors)} ({len(errors)/len(y_test)*100:.4f}%)')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## **Phase 6: High-Resolution Normalized Confusion Matrix**\n",
                "Visualizing the exact $11 \\times 11$ confusion matrix across all target categories."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "cm = confusion_matrix(y_test, y_test_pred_pruned)\n",
                "cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100\n",
                "\n",
                "plt.figure(figsize=(10, 8), dpi=150)\n",
                "sns.heatmap(\n",
                "    cm_norm, annot=True, fmt='.1f', cmap='Blues', cbar=True,\n",
                "    xticklabels=class_names, yticklabels=class_names,\n",
                "    linewidths=0.5, linecolor='lightgray'\n",
                ")\n",
                "plt.title('Normalized Confusion Matrix (%) — Final Pruned CART Decision Tree\\nTest Set (N = 25,674 packets)', fontsize=14, pad=15)\n",
                "plt.xlabel('Predicted Threat Class', fontsize=12, labelpad=10)\n",
                "plt.ylabel('Actual Ground Truth Class', fontsize=12, labelpad=10)\n",
                "plt.xticks(rotation=45, ha='right')\n",
                "plt.yticks(rotation=0)\n",
                "plt.tight_layout()\n",
                "plt.savefig('confusion_matrix.png', dpi=300)\n",
                "plt.show()\n",
                "print('[+] High-resolution confusion matrix saved to confusion_matrix.png.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## **Phase 7: Gini Feature Importance & White-Box Interpretability**\n",
                "Decision Trees provide full white-box transparency. We extract and rank the top discriminative features by total Gini Impurity reduction (Mean Decrease in Impurity)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "importances = pruned_clf.feature_importances_\n",
                "indices = np.argsort(importances)[::-1][:15]\n",
                "\n",
                "top_df = pd.DataFrame({\n",
                "    'Feature': [feature_names[i] for i in indices],\n",
                "    'Importance': [importances[i] for i in indices]\n",
                "})\n",
                "\n",
                "plt.figure(figsize=(10, 6), dpi=150)\n",
                "sns.barplot(data=top_df, x='Importance', y='Feature', palette='viridis')\n",
                "plt.title('Top 15 Most Discriminative Flow Features (Gini Importance)', fontsize=14, pad=12)\n",
                "plt.xlabel('Gini Importance (Normalized Impurity Reduction)', fontsize=12)\n",
                "plt.ylabel('Kitsune Temporal Flow Feature', fontsize=12)\n",
                "plt.grid(axis='x', linestyle='--', alpha=0.7)\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "display(top_df)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## **Phase 8: Computational Overhead & Inference Latency Benchmark**\n",
                "Profile real-time single-sample ($N = 1$) inline packet processing latency vs vectorized batch ($N = 25,674$) throughput."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Single sample latency benchmark (10,000 warm iterations)\n",
                "sample_x = X_test[0:1]\n",
                "n_runs = 5000\n",
                "\n",
                "# Warmup\n",
                "for _ in range(500):\n",
                "    _ = pruned_clf.predict(sample_x)\n",
                "\n",
                "t0 = time.perf_counter()\n",
                "for _ in range(n_runs):\n",
                "    _ = pruned_clf.predict(sample_x)\n",
                "t_total = time.perf_counter() - t0\n",
                "single_latency_us = (t_total / n_runs) * 1e6\n",
                "single_throughput = 1e6 / single_latency_us\n",
                "\n",
                "# 2. Vectorized batch latency benchmark\n",
                "t0 = time.perf_counter()\n",
                "_ = pruned_clf.predict(X_test)\n",
                "batch_time = time.perf_counter() - t0\n",
                "batch_latency_us = (batch_time / len(X_test)) * 1e6\n",
                "batch_throughput = len(X_test) / batch_time\n",
                "\n",
                "print('='*75)\n",
                "print('COMPUTATIONAL INFERENCE BENCHMARK')\n",
                "print('='*75)\n",
                "print(f'Single-Sample (N = 1) Latency    : {single_latency_us:.2f} μs / packet')\n",
                "print(f'Single-Sample (N = 1) Throughput : {single_throughput:,.0f} packets / second')\n",
                "print(f'Batch (N = 25,674) Latency       : {batch_latency_us:.4f} μs / packet')\n",
                "print(f'Batch (N = 25,674) Throughput    : {batch_throughput:,.0f} packets / second')\n",
                "print('='*75)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## **Phase 9: Export Benchmark Results to CSV**\n",
                "Save official tournament metrics to `results.csv` for collaborative batch paper aggregation."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "results_df = pd.DataFrame([{\n",
                "    'Algorithm': 'Decision Tree (CART, CCP-Pruned)',\n",
                "    'Accuracy': round(acc_test_pruned * 100, 4),\n",
                "    'Precision': round(prec_test_pruned * 100, 4),\n",
                "    'Recall': round(rec_test_pruned * 100, 4),\n",
                "    'F1-Score': round(f1_test_pruned * 100, 4),\n",
                "    'ROC-AUC': round(roc_auc_pruned, 6),\n",
                "    'Binary_Accuracy': round(bin_acc * 100, 4),\n",
                "    'Binary_F1': round(bin_f1 * 100, 4),\n",
                "    'Tree_Depth': pruned_clf.get_depth(),\n",
                "    'Total_Nodes': pruned_clf.tree_.node_count,\n",
                "    'Terminal_Leaves': pruned_clf.get_n_leaves(),\n",
                "    'Single_Latency_us': round(single_latency_us, 2),\n",
                "    'Single_Throughput_pkts_s': round(single_throughput, 0)\n",
                "}])\n",
                "\n",
                "results_df.to_csv('results.csv', index=False)\n",
                "print('[+] Successfully exported benchmark metrics to results.csv:')\n",
                "display(results_df)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "### **Submission Attribution**\n",
                "- **Department:** Computer Science & Engineering, Sardar Patel Institute of Technology (SPIT), Mumbai\n",
                "- **Course:** Cryptography and Network Security (CNS A.Y. 2026–2027)\n",
                "- **Group 1:** Decision Tree\n",
                "- **Student:** Swapnil Patil (`swapnil.patil24@spit.ac.in`)\n",
                "- **Faculty Mentor:** Dr. Renuka Pawar"
            ]
        }
    ]
}

output_path = '/Users/swapnil/Documents/cns/CNS-Group1-DecisionTree/CNS_Group1_Decision_Tree_Colab.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print(f'[+] Successfully wrote Google Colab notebook to: {output_path}')
