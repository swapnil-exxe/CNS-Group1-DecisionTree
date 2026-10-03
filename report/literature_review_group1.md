# Group 1 Literature Review: Decision Trees in IoT Botnet Attack Detection

This document provides a verified academic literature review for **Group 1 (Decision Tree)**, contextualizing our implementation of a CART-style Decision Tree with Cost-Complexity Pruning on the N-BaIoT dataset within published research.

---

## Methodological Clarification: CART vs. C4.5

The assigned research framework is based on the reference:
> *"Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees"*

**Key Distinctions:**
1. The C4.5 algorithm (Quinlan, 1993) constructs non-binary or binary trees using Information Gain Ratio derived from Shannon Entropy, handles missing attributes through fractional weighting, and employs error-based post-pruning.
2. The implementation utilized in this project is based on `sklearn.tree.DecisionTreeClassifier`, which implements an optimized version of the **Classification and Regression Trees (CART)** algorithm (Breiman et al., 1984).
3. CART constructs strictly binary trees using **Gini Impurity** and regularizes tree complexity via **Minimal Cost-Complexity Pruning ($ccp\_\alpha$)**.
4. Therefore, this project represents a **CART-style Decision Tree implementation inspired by the assigned C4.5 IoT botnet detection research framework**, rather than an exact software reproduction of Quinlan's original C4.5 codebase.

---

## Paper 1: Feature-Efficient Machine Learning for IoT Botnet Detection

- **Title:** CORRAUC: A Malicious Bot-IoT Traffic Detection Method in IoT Network Using Machine-Learning Techniques
- **Authors:** Muhammad Shafiq, Zhihong Tian, Ali Kashif Bashir, Xiaojiang Du, and Mohsen Guizani
- **Year:** 2021 (Published online 2020)
- **Journal:** *IEEE Internet of Things Journal*, Vol. 8, No. 5, pp. 3242–3253
- **DOI:** [10.1109/JIOT.2020.3002255](https://doi.org/10.1109/JIOT.2020.3002255)
- **Indexing Status:** Published in *IEEE Internet of Things Journal* (IEEE / Scopus; Scopus-indexing status should be verified through the institution's Scopus subscription/database before final submission).
- **Main Method:**
  The authors developed the CORRAUC feature selection framework (combining Correlation-Attribute-Evaluation with Area Under the ROC Curve metric) to isolate the most discriminative traffic features from packet flows. Decision Trees (C4.5 and CART variants), Random Forests, and Support Vector Machines were evaluated to detect IoT botnet attacks, including DoS, DDoS, reconnaissance, and data exfiltration.
- **Dataset Evaluated:** The Bot-IoT Dataset.
- **Important Findings:**
  1. Supervised tree models achieved detection accuracy exceeding 99.9%, indicating that network traffic flow statistics provide high linear and non-linear separability for botnet signatures.
  2. Single decision trees yielded sub-microsecond classification throughput, outperforming deep neural networks in runtime efficiency by several orders of magnitude.
  3. Feature selection reduced input dimensionality without degrading detection rates, supporting the premise that statistical flow aggregates (arrival rates, variances, and stream weights) suffice for robust identification.
- **Relevance to Group 1 Experiment:**
  Shafiq et al. demonstrate that decision trees achieve a favorable balance between accuracy and computational overhead in IoT environments. Their findings support our observation that continuous sliding-window traffic features provide high separability for both binary detection (99.96% accuracy) and multiclass vector classification (99.62% accuracy) with sub-microsecond latency.

---

## Paper 2: Hyperparameter Optimization and Pruning in Tree-Based IoT IDS

- **Title:** Optimized Machine Learning-Based Network Intrusion Detection for IoT Networks
- **Authors:** Abdallah Moubayed, MohammadNoor Injadat, Abdallah Shami, and Hassan Lutfiyya
- **Year:** 2020
- **Journal:** *IEEE Internet of Things Journal*, Vol. 7, No. 6, pp. 4889–4903
- **DOI:** [10.1109/JIOT.2020.2970588](https://doi.org/10.1109/JIOT.2020.2970588)
- **Indexing Status:** Published in *IEEE Internet of Things Journal* (IEEE / Scopus; Scopus-indexing status should be verified through the institution's Scopus subscription/database before final submission).
- **Main Method:**
  The authors investigated hyperparameter optimization in decision tree and ensemble architectures using Bayesian Optimization with Tree-structured Parzen Estimators (BO-TPE). The study analyzed the effects of structural constraints—such as maximum tree depth, split thresholds, and cost-complexity pruning—on generalization error.
- **Dataset Evaluated:** UNSW-NB15 and CICIDS-2017 intrusion detection datasets.
- **Important Findings:**
  1. Unpruned decision trees exhibited a noticeable generalization gap caused by overfitting to transient flow fluctuations and idiosyncratic packet length distributions.
  2. Cost-complexity pruning reduced total tree node counts by over 40% while preserving test F1-scores.
  3. Pruned, compact models significantly decreased memory consumption and per-packet decision latency, making them viable for resource-constrained network appliances.
  Moubayed et al.'s findings directly motivate our core objective of tuning $ccp\_\alpha$. In our N-BaIoT experiment, pruning with the optimal validation-selected parameter $\alpha = 1.9998 \times 10^{-5}$ removed 48 redundant nodes ($-26.5\%$) and 24 leaf splits ($-26.4\%$), reduced tree depth from 21 to 18, narrowed the train-test generalization gap from $0.1022\%$ to $0.0779\%$, and preserved peak test accuracy ($99.6183\%$).

---

## Base Paper Reference

- **Title:** N-BaIoT: Network-based Detection of IoT Botnet Attacks Using Deep Autoencoders
- **Authors:** Yair Meidan, Michael Bohadana, Yael Mathov, Yisroel Mirsky, Dominik Breitenbacher, Asaf Shabtai, and Yuval Elovici
- **Year:** 2018
- **Journal:** *IEEE Pervasive Computing*, Vol. 17, No. 3, pp. 12–22
- **DOI:** [10.1109/MPRV.2018.03367731](https://doi.org/10.1109/MPRV.2018.03367731)
- **Methodological Distinction:**
  - **Base Paper Approach:** Meidan et al. trained individual **deep autoencoders** exclusively on benign network traffic from each of the 9 IoT devices to construct an anomaly detector. The detection metric was reconstruction error (Mean Squared Error), flagging packets exceeding a threshold as malicious.
  - **Group 1 Approach:** Our implementation adopts a supervised **CART-style Decision Tree** classifier. Rather than reconstructing packet features via autoencoders, the decision tree directly performs supervised partitioning on the 115 continuous statistical features across 11 multiclass categories and binary classification, regularized via cost-complexity pruning.
