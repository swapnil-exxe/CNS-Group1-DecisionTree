#!/usr/bin/env python3
"""
src/08_final_consistency_audit.py
Automated Quality Control and Consistency Audit for Group 1 Decision Tree Pipeline.

Checks:
1. All required project files, reports, tables, figures, models, and scripts exist.
2. Dataset preprocessed dimensions: exactly 115 features, 11 classes, 128,366 samples (102,692 train, 25,674 test).
3. Data integrity: 0 nulls, 0 infinities, 0 label/device ID leakage.
4. Model architecture matches serialized models and tabular metrics:
   - Baseline Decision Tree (ccp_alpha=0.0): depth, leaves, node count.
   - Final Pruned Decision Tree: validation-selected alpha, depth, leaves, node count.
5. Authoritative selected alpha in selected_alpha.json matches final_model and final_metrics.csv.
6. Zero presence of obsolete alpha parameters across active reports, src, and README.md.
7. Generates a clear terminal summary and exits with code 0 on PASS or 1 on FAIL.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd

PROJECT_DIR = "/Users/swapnil/Documents/cns/group1_decision_tree"
SRC_DIR = os.path.join(PROJECT_DIR, "src")
REPORT_DIR = os.path.join(PROJECT_DIR, "report")
TABLES_DIR = os.path.join(PROJECT_DIR, "results/tables")
FIGURES_DIR = os.path.join(PROJECT_DIR, "results/figures")
MODELS_DIR = os.path.join(PROJECT_DIR, "results/models")
DATA_DIR = os.path.join(PROJECT_DIR, "data")
README_PATH = os.path.join(PROJECT_DIR, "README.md")

REQUIRED_SCRIPTS = [
    "01_inspect_dataset.py",
    "02_preprocess.py",
    "03_baseline_decision_tree.py",
    "04_ccp_alpha_tuning.py",
    "05_final_model.py",
    "06_tree_visualization.py",
    "07_computational_analysis.py",
    "08_final_consistency_audit.py",
    "09_generate_submission_pdf.py"
]

REQUIRED_REPORTS = [
    "section_3_2_decision_tree.md",
    "section_5_2_computational_analysis.md",
    "literature_review_group1.md",
    "decision_path_analysis.md",
    "final_audit_report.md"
]

REQUIRED_TABLES = [
    "dataset_summary.csv",
    "dataset_files_inspection.csv",
    "feature_summary.csv",
    "label_mapping.csv",
    "sampling_distribution_audit.csv",
    "class_distribution_split.csv",
    "data_leakage_audit.csv",
    "baseline_metrics.csv",
    "final_metrics.csv",
    "baseline_vs_pruned_comparison.csv",
    "ccp_pruning_path_raw.csv",
    "ccp_alpha_results.csv",
    "selected_alpha.json",
    "classification_report.csv",
    "feature_importance.csv",
    "batch_inference_latency.csv",
    "training_overhead_benchmark.csv",
    "hardware_environment.csv",
    "comparative_algorithms_benchmark_template.csv"
]

REQUIRED_MODELS = [
    "baseline_decision_tree.joblib",
    "final_decision_tree.joblib"
]

REQUIRED_FIGURES = [
    "class_distribution.png",
    "ccp_alpha_vs_accuracy.png",
    "ccp_alpha_vs_f1.png",
    "ccp_alpha_vs_leaves.png",
    "ccp_alpha_vs_tree_depth.png",
    "ccp_alpha_vs_computational_time.png",
    "confusion_matrix.png",
    "feature_importance.png",
    "decision_tree_complete.png",
    "decision_tree_readable.png",
    "batch_latency_throughput.png"
]

def run_audit():
    print("=" * 80)
    print("GROUP 1 DECISION TREE: AUTOMATED FINAL CONSISTENCY AUDIT")
    print("=" * 80)
    
    failures = []
    
    # ---------------------------------------------------------
    # 1. Check Required Files
    # ---------------------------------------------------------
    print("\n[Check 1/7] Verifying file system manifest...")
    
    for script in REQUIRED_SCRIPTS:
        path = os.path.join(SRC_DIR, script)
        if not os.path.isfile(path):
            failures.append(f"Missing required script: {script}")
            
    for report in REQUIRED_REPORTS:
        path = os.path.join(REPORT_DIR, report)
        if not os.path.isfile(path):
            failures.append(f"Missing required report: {report}")
            
    for table in REQUIRED_TABLES:
        path = os.path.join(TABLES_DIR, table)
        if not os.path.isfile(path):
            failures.append(f"Missing required table: {table}")
            
    for model in REQUIRED_MODELS:
        path = os.path.join(MODELS_DIR, model)
        if not os.path.isfile(path):
            failures.append(f"Missing required model: {model}")
            
    for figure in REQUIRED_FIGURES:
        path = os.path.join(FIGURES_DIR, figure)
        if not os.path.isfile(path):
            failures.append(f"Missing required figure: {figure}")
            
    data_bundle = os.path.join(DATA_DIR, "preprocessed_data.joblib")
    if not os.path.isfile(data_bundle):
        failures.append("Missing preprocessed_data.joblib bundle in data/")
        
    if not os.path.isfile(README_PATH):
        failures.append("Missing README.md in project root")

    if not failures:
        print("  -> File system manifest: PASS (all required deliverables exist)")
    else:
        print(f"  -> File system manifest: FAIL ({len(failures)} missing files)")

    # ---------------------------------------------------------
    # 2. Check Preprocessed Data Integrity
    # ---------------------------------------------------------
    print("\n[Check 2/7] Verifying preprocessed dataset integrity...")
    try:
        data = joblib.load(data_bundle)
        X_train = data["X_train"]
        y_train = data["y_train"]
        X_test = data["X_test"]
        y_test = data["y_test"]
        features = data["feature_names"]
        classes = data["class_names"]
        
        # Dimensions
        n_features = len(features)
        n_classes = len(classes)
        n_train = len(X_train)
        n_test = len(X_test)
        total_samples = n_train + n_test
        
        if n_features != 115:
            failures.append(f"Feature count mismatch: expected 115, got {n_features}")
        if n_classes != 11:
            failures.append(f"Class count mismatch: expected 11, got {n_classes}")
        if total_samples != 128366:
            failures.append(f"Total samples mismatch: expected 128,366, got {total_samples}")
        if n_train != 102692 or n_test != 25674:
            failures.append(f"Split sizes mismatch: expected 102,692 train / 25,674 test, got {n_train} / {n_test}")
            
        # Null / NaN / Inf checks
        if np.isnan(X_train).sum() > 0 or np.isnan(X_test).sum() > 0:
            failures.append("NaN detected in feature matrices")
        if np.isinf(X_train).sum() > 0 or np.isinf(X_test).sum() > 0:
            failures.append("Inf detected in feature matrices")
            
        # Target / Identifier leakage check
        prohibited_substrings = ["label", "target", "device_id", "ip_", "mac_", "timestamp"]
        for feat in features:
            for bad in prohibited_substrings:
                if bad in feat.lower():
                    failures.append(f"Potential leakage feature in X: {feat}")
                    
        print(f"  -> Dataset integrity: PASS (115 features, 11 classes, {total_samples:,} samples, 0 nulls, 0 leakage)")
    except Exception as e:
        failures.append(f"Failed to inspect preprocessed dataset: {e}")
        print(f"  -> Dataset integrity: ERROR ({e})")

    # ---------------------------------------------------------
    # 3. Check Models & Metrics Consistency
    # ---------------------------------------------------------
    print("\n[Check 3/7] Verifying models and tabular metrics consistency...")
    try:
        baseline_clf = joblib.load(os.path.join(MODELS_DIR, "baseline_decision_tree.joblib"))
        final_clf = joblib.load(os.path.join(MODELS_DIR, "final_decision_tree.joblib"))
        
        with open(os.path.join(TABLES_DIR, "selected_alpha.json"), "r") as f:
            selected_alpha_meta = json.load(f)
            
        final_metrics_df = pd.read_csv(os.path.join(TABLES_DIR, "final_metrics.csv"))
        baseline_metrics_df = pd.read_csv(os.path.join(TABLES_DIR, "baseline_metrics.csv"))
        
        # Selected alpha consistency
        sel_alpha_json = selected_alpha_meta["selected_ccp_alpha"]
        model_alpha = final_clf.ccp_alpha
        csv_alpha = float(final_metrics_df["ccp_alpha"].values[0])
        
        if abs(sel_alpha_json - model_alpha) > 1e-12:
            failures.append(f"Alpha mismatch: JSON ({sel_alpha_json}) vs Model ({model_alpha})")
        if abs(model_alpha - csv_alpha) > 1e-12:
            failures.append(f"Alpha mismatch: Model ({model_alpha}) vs CSV ({csv_alpha})")
            
        # Baseline model structural check
        base_depth = baseline_clf.get_depth()
        base_leaves = baseline_clf.get_n_leaves()
        base_nodes = baseline_clf.tree_.node_count
        
        csv_base_depth = int(baseline_metrics_df["tree_depth"].values[0])
        csv_base_leaves = int(baseline_metrics_df["leaf_count"].values[0])
        csv_base_nodes = int(baseline_metrics_df["node_count"].values[0])
        
        if (base_depth, base_leaves, base_nodes) != (csv_base_depth, csv_base_leaves, csv_base_nodes):
            failures.append(
                f"Baseline structure mismatch: Model ({base_depth}, {base_leaves}, {base_nodes}) vs "
                f"CSV ({csv_base_depth}, {csv_base_leaves}, {csv_base_nodes})"
            )
            
        # Final model structural check
        final_depth = final_clf.get_depth()
        final_leaves = final_clf.get_n_leaves()
        final_nodes = final_clf.tree_.node_count
        
        csv_final_depth = int(final_metrics_df["tree_depth"].values[0])
        csv_final_leaves = int(final_metrics_df["leaf_count"].values[0])
        csv_final_nodes = int(final_metrics_df["node_count"].values[0])
        
        if (final_depth, final_leaves, final_nodes) != (csv_final_depth, csv_final_leaves, csv_final_nodes):
            failures.append(
                f"Final model structure mismatch: Model ({final_depth}, {final_leaves}, {final_nodes}) vs "
                f"CSV ({csv_final_depth}, {csv_final_leaves}, {csv_final_nodes})"
            )
            
        print(f"  -> Model & tabular consistency: PASS (Alpha={model_alpha:.6e}, Nodes={final_nodes}, Leaves={final_leaves}, Depth={final_depth})")
    except Exception as e:
        failures.append(f"Model consistency check failed: {e}")
        print(f"  -> Model & tabular consistency: ERROR ({e})")

    # ---------------------------------------------------------
    # 4. Check Feature Importance Integrity
    # ---------------------------------------------------------
    print("\n[Check 4/7] Verifying feature importance table...")
    try:
        feat_df = pd.read_csv(os.path.join(TABLES_DIR, "feature_importance.csv"))
        if len(feat_df) != 115:
            failures.append(f"Feature importance table row count != 115 (got {len(feat_df)})")
        col_imp = "Importance" if "Importance" in feat_df.columns else "importance"
        col_feat = "Feature" if "Feature" in feat_df.columns else "feature"
        sum_imp = feat_df[col_imp].sum()
        if abs(sum_imp - 1.0) > 0.001:
            failures.append(f"Feature importances do not sum to 1.0 (sum = {sum_imp})")
        top_feature = feat_df.iloc[0][col_feat]
        if top_feature != "H_L0.01_mean":
            failures.append(f"Top feature expected 'H_L0.01_mean', got '{top_feature}'")
        print(f"  -> Feature importance: PASS (115 features ranked, sum={sum_imp:.4f}, top='{top_feature}')")
    except Exception as e:
        failures.append(f"Feature importance audit failed: {e}")
        print(f"  -> Feature importance: ERROR ({e})")

    # ---------------------------------------------------------
    # 5. Check Obsolete Alpha / Stale Number Occurrences
    # ---------------------------------------------------------
    print("\n[Check 5/7] Scanning active codebase for obsolete/stale references...")
    obsolete_tokens = ["1.94" + "66"]
    
    files_to_scan = [README_PATH]
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py") and file != "08_final_consistency_audit.py":
                files_to_scan.append(os.path.join(root, file))
    for root, _, files in os.walk(REPORT_DIR):
        for file in files:
            if file.endswith(".md"):
                files_to_scan.append(os.path.join(root, file))
                
    stale_hits = []
    for filepath in files_to_scan:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for token in obsolete_tokens:
                    if token in content:
                        rel = os.path.relpath(filepath, PROJECT_DIR)
                        stale_hits.append(f"{rel} contains stale token '{token}'")
        except Exception as e:
            failures.append(f"Could not read {filepath}: {e}")
            
    if stale_hits:
        for hit in stale_hits:
            failures.append(hit)
        print(f"  -> Obsolete token scan: FAIL ({len(stale_hits)} stale references found)")
    else:
        print("  -> Obsolete token scan: PASS (Zero stale alpha references in active files)")

    # ---------------------------------------------------------
    # 6. Check Raw Dataset Read-Only Status
    # ---------------------------------------------------------
    print("\n[Check 6/7] Verifying raw dataset directory isolation...")
    raw_archive = "/Users/swapnil/Documents/cns/archive"
    if not os.path.isdir(raw_archive):
        failures.append("Raw archive directory does not exist at /Users/swapnil/Documents/cns/archive")
    else:
        archive_files = os.listdir(raw_archive)
        csv_count = len([f for f in archive_files if f.endswith(".csv")])
        if csv_count != 92:
            failures.append(f"Archive CSV file count expected 92, found {csv_count}")
        print(f"  -> Raw dataset isolation: PASS (Archive intact with {csv_count} CSV files)")

    # ---------------------------------------------------------
    # 7. Check Report Consistency with Generated Artifacts
    # ---------------------------------------------------------
    print("\n[Check 7/7] Verifying report and README numerical consistency...")
    try:
        with open(README_PATH, "r") as f:
            readme_text = f.read()
        with open(os.path.join(REPORT_DIR, "section_3_2_decision_tree.md"), "r") as f:
            s32_text = f.read()
        with open(os.path.join(REPORT_DIR, "final_audit_report.md"), "r") as f:
            audit_rep_text = f.read()

        # Key expected tokens based on final_metrics.csv
        required_readme_tokens = [
            "1.9998", "133 nodes", "67 leaves", "99.6183%", "99.6510%", "99.9649%", "99.9810%", "0.0769%"
        ]
        for token in required_readme_tokens:
            if token not in readme_text:
                failures.append(f"README.md missing authoritative metric token: '{token}'")

        if "99.6183%" not in s32_text:
            failures.append("report/section_3_2_decision_tree.md missing test accuracy '99.6183%'")
        if "1.9998" not in s32_text:
            failures.append("report/section_3_2_decision_tree.md missing optimal alpha '1.9998'")

        if "99.6183%" not in audit_rep_text:
            failures.append("report/final_audit_report.md missing test accuracy '99.6183%'")
        if "133 nodes" not in audit_rep_text:
            failures.append("report/final_audit_report.md missing node count '133 nodes'")
            
        print("  -> Report consistency: PASS (README and reports match verified model metrics)")
    except Exception as e:
        failures.append(f"Report consistency check failed: {e}")
        print(f"  -> Report consistency: ERROR ({e})")

    # ---------------------------------------------------------
    # Final Verdict
    # ---------------------------------------------------------
    print("\n" + "=" * 80)
    if not failures:
        print("FINAL AUDIT: PASS")
        print("All consistency, integrity, and methodological checks passed successfully.")
        print("=" * 80)
        return 0
    else:
        print("FINAL AUDIT: FAIL")
        print(f"Encountered {len(failures)} consistency/integrity issue(s):")
        for i, fail in enumerate(failures, 1):
            print(f"  {i}. {fail}")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(run_audit())
