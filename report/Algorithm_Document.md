# Cryptography and Network Security: Group 1 Algorithm Document
## Rigorous Theoretical Formulation and Algorithmic Analysis of CART-Style Decision Trees with Cost-Complexity Pruning for IoT Botnet Attack Detection

---

**Course / Subject:** Cryptography and Network Security (CNS)  
**Project Group:** Group 1 — Decision Tree  
**Assigned Research Topic:** Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees  
**Actual Machine Learning Implementation:** Classification and Regression Trees (CART) via `sklearn.tree.DecisionTreeClassifier`  
**Dataset:** N-BaIoT — Network-Based Detection of IoT Botnet Attacks (UCI ML Repository)  
**Target Architecture:** Resource-Constrained IoT Gateway Appliances  

---

# 1. Introduction and Algorithmic Context

In modern Internet of Things (IoT) networking architectures, heterogeneous edge devices (such as smart security cameras, environmental sensors, automated baby monitors, and industrial controllers) operate under severe computational, memory, and energy budgets. Due to default factory credentials and unpatched embedded Linux firmwares, these appliances frequently become targets for remote infection by autonomous malware worms, most notably the Mirai and BASHLITE (also designated as Gafgyt, Lizkebab, or Torlus) botnet families. Once compromised, swarms of enslaved devices are commanded to execute volumetric Distributed Denial of Service (DDoS) floods, protocol-specific denial of service, and horizontal network scanning.

Detecting anomalous botnet traffic directly on embedded IoT gateway routers requires machine learning algorithms that reconcile two conflicting demands:
1. **High Predictive Generalization:** The ability to distinguish subtle, benign communications from diverse multi-vector attack traffic with near-zero false alarms.
2. **Deterministic Ultra-Low Latency:** The capability to process high-throughput packet streams in real time without causing packet queue starvation or requiring specialized floating-point hardware accelerators (such as enterprise GPUs or TPUs).

Within this operational paradigm, the **Decision Tree** algorithm provides an optimal inductive learning model. Unlike black-box deep neural networks or kernelized support vector machines, a decision tree segments continuous statistical feature spaces through hierarchical, orthogonal hyperplanes, yielding an interpretable directed acyclic graph of conditional assertions.

---

# 2. Decision Tree Fundamentals

A Decision Tree is a non-parametric supervised learning model that approximates a discrete mapping $f: \mathcal{X} \to \mathcal{Y}$, where the input space $\mathcal{X} \subseteq \mathbb{R}^d$ consists of $d$-dimensional continuous feature vectors ($d = 115$ in the N-BaIoT representation), and the output space $\mathcal{Y} = \{c_1, c_2, \dots, c_C\}$ denotes the discrete label space ($C = 11$ multiclass categories).

Structurally, a decision tree consists of:
- **Root Node ($t_0$):** The topmost decision vertex containing the complete training sample partition $S_0 = S$.
- **Internal (Decision) Nodes ($t \in \mathcal{N}_{\text{int}}$):** Intermediate vertices that evaluate a univariate predicate of the form $x_j \le \theta$, directing an input vector $\mathbf{x}$ to either the left child $t_L$ or right child $t_R$.
- **Terminal (Leaf) Nodes ($t \in \widetilde{T}$):** Leaf vertices that hold no children and assign a final class prediction $\hat{y} \in \mathcal{Y}$ based on the majority empirical probability distribution of the samples terminating in that partition.
- **Branches / Edges:** Directed links connecting parent nodes to child partitions.

The induction of a decision tree follows a greedy, top-down recursive partitioning scheme (Divide-and-Conquer). Beginning at the root, the algorithm examines all candidate features $j \in \{1, \dots, d\}$ and candidate thresholds $\theta \in \mathbb{R}$, selecting the split $(j^*, \theta^*)$ that maximizes an objective impurity reduction criterion. The data subset is split into child subsets, and the identical procedure is applied recursively until pre-defined stopping conditions are satisfied.

---

# 3. Methodological Clarification: CART Implementation vs. C4.5 Context

A foundational academic and architectural requirement of this project is the precise distinction between the assigned research framework and the actual software implementation.

### 3.1 Assigned Research Framework (C4.5 Context)
The project framework references the academic investigation:  
> *"Lightweight Android and IoT Botnet Detection Using C4.5 Decision Trees"*

The C4.5 algorithm, developed by J. Ross Quinlan in 1993 as the successor to ID3, possesses the following mathematical characteristics:
1. **Entropy and Information Gain Ratio:** Splitting decisions are governed by maximizing the Information Gain Ratio, which penalizes attributes with high intrinsic split information to prevent bias toward multi-valued categorical features.
2. **Multi-Way Splitting on Discrete Variables:** When evaluating discrete nominal variables, C4.5 partitions data into $K$ child branches corresponding to each distinct categorical state.
3. **Error-Based Post-Pruning (Pessimistic Pruning):** C4.5 prunes subtrees using a binomial confidence limit calculated over the training misclassification count.
4. **Fractional Handling of Missing Values:** Instances with missing features are propagated down all branches with probabilistic weights.

### 3.2 Actual Machine Learning Implementation (CART via scikit-learn)
Our actual empirical pipeline is constructed using Python's standard machine learning library via `sklearn.tree.DecisionTreeClassifier`. Scikit-learn's underlying engine implements an optimized version of the **Classification and Regression Trees (CART)** algorithm formulated by Breiman, Friedman, Olshen, and Stone (1984).

CART differs fundamentally from Quinlan's C4.5 in several key structural dimensions:
1. **Strict Binary Recursive Splitting:** Every internal node evaluates a binary boolean inequality $x_j \le \theta$, producing exactly two child nodes ($t_L$ and $t_R$). Continuous features are handled by sorting unique values and evaluating midpoints.
2. **Gini Impurity as Splitting Criterion:** By default, CART utilizes Gini Impurity rather than Shannon Entropy, eliminating computationally intensive logarithmic transformations during split evaluations.
3. **Minimal Cost-Complexity Pruning ($ccp\_\alpha$):** Structural regularization is governed by post-hoc pruning using Breiman's weakest-link cost-complexity objective parameterized by the scalar penalty coefficient $ccp\_\alpha \ge 0$.
4. **Deterministic Continuous Matrix Input:** Scikit-learn operates strictly on dense or sparse continuous 32-bit floating-point arrays without native discrete nominal branching.

The table below delineates the precise algorithmic differences between CART and C4.5:

| Architectural Property | C4.5 Decision Tree (Quinlan, 1993) | CART Decision Tree (Breiman et al., 1984 / scikit-learn) | Group 1 Project Implementation |
| :--- | :--- | :--- | :--- |
| **Splitting Criterion** | Information Gain Ratio ($\text{GainRatio}$) based on Shannon Entropy | Gini Impurity ($\text{Gini}$) or Shannon Entropy | **Gini Impurity** (`criterion='gini'`) |
| **Tree Branching Factor** | Multi-way splits for discrete features; Binary splits for continuous | Strictly **Binary Splitting** ($2$-way branching at every node) | **Strictly Binary Splitting** |
| **Handling of Continuous Features** | Dynamic local sorting; evaluates candidate thresholds | Dynamic local sorting; evaluates numeric midpoints | Optimized Cython-based binary thresholding |
| **Pruning Mechanism** | Pessimistic Error-Based Pruning (EBP) using normal approximation | **Minimal Cost-Complexity Pruning** ($R_\alpha(T) = R(T) + \alpha |T|$) | **Minimal Cost-Complexity Pruning** (`ccp_alpha`) |
| **Missing Value Handling** | Probabilistic fractional sample assignment | Pre-split imputation required (scikit-learn raises error on NaN) | Clean imputed continuous matrix (zero NaNs verified) |
| **Computational Basis** | Natural logarithms ($\log_2$) for entropy calculation | Sum of squared probabilities ($\sum p_i^2$) | Fast arithmetic floating-point operations |
| **Role in Project** | **Theoretical Research Reference / Motivation** | **Actual Software Architecture & Pipeline** | **CART via `sklearn.tree.DecisionTreeClassifier`** |

---

# 4. Impurity Metrics and Splitting Mathematics

Let node $t$ contain a subset of training observations $S_t \subseteq S$. Let $|S_t| = N_t$ denote the number of instances at node $t$. For a $C$-class classification problem, let $N_{t,i}$ represent the number of instances belonging to class $i \in \{1, 2, \dots, C\}$.

The empirical probability $p_i(t)$ of class $i$ at node $t$ is:

$$p_i(t) = \frac{N_{t,i}}{N_t} = \frac{1}{|S_t|} \sum_{\mathbf{x} \in S_t} \mathbb{I}(y = i)$$

where $\sum_{i=1}^C p_i(t) = 1$.

### 4.1 Gini Impurity
The Gini impurity measures the expected error rate if a randomly selected instance from node $t$ were classified randomly according to the class label distribution of $S_t$:

$$\text{Gini}(t) = 1 - \sum_{i=1}^{C} p_i(t)^2 = \sum_{i \ne k} p_i(t) p_k(t)$$

**Mathematical Properties of Gini Impurity:**
- **Minimum Value ($\text{Gini}(t) = 0$):** Occurs when the node is perfectly pure ($\exists i \text{ such that } p_i(t) = 1$, and $p_k(t) = 0$ for all $k \ne i$).
- **Maximum Value ($\text{Gini}(t) = 1 - \frac{1}{C}$):** Occurs when instances are uniformly distributed across all $C$ classes ($p_i(t) = \frac{1}{C} \ \forall i$). In our 11-class botnet problem ($C = 11$), the theoretical maximum Gini impurity is:

$$\text{Gini}_{\max} = 1 - \frac{1}{11} = \frac{10}{11} \approx 0.909091$$

- **Computational Advantage:** Computing Gini impurity requires only scalar multiplications and subtractions, completely avoiding logarithmic function evaluations.

### 4.2 Shannon Entropy
Shannon Entropy originates from information theory and quantifies the expected amount of information (or uncertainty) contained in the class distribution at node $t$:

$$H(t) = - \sum_{i=1}^{C} p_i(t) \log_2 p_i(t)$$

where by convention $0 \log_2 0 = 0$.

**Mathematical Properties of Entropy:**
- **Minimum Value ($H(t) = 0$):** Achieved when node $t$ contains samples of only a single class.
- **Maximum Value ($H(t) = \log_2 C$):** Achieved under uniform class distribution. For $C = 11$, $H_{\max} = \log_2(11) \approx 3.4594$ bits.

### 4.3 Information Gain
Information Gain ($\text{IG}$) measures the reduction in entropy achieved by partitioning node $t$ using candidate split $s$:

$$\text{IG}(s, t) = H(t) - \left( \frac{|t_L|}{|S_t|} H(t_L) + \frac{|t_R|}{|S_t|} H(t_R) \right)$$

While intuitive, Information Gain is biased toward features with many distinct values, as high-cardinality features can partition the data into small, artificially pure subsets without true predictive generalization.

### 4.4 Gain Ratio (Quinlan's C4.5 Normalization)
To counteract this bias, C4.5 normalizes Information Gain by the **Split Information** ($\text{SplitInfo}_s(t)$), which quantifies the entropy of the partition itself:

$$\text{SplitInfo}_s(t) = - \sum_{k \in \{L, R\}} \frac{|t_k|}{|S_t|} \log_2 \left( \frac{|t_k|}{|S_t|} \right)$$

The Gain Ratio is defined as:

$$\text{GainRatio}(s, t) = \frac{\text{IG}(s, t)}{\text{SplitInfo}_s(t)}$$

This normalizes the impurity drop against the structural fragmentation created by the split.

### 4.5 Binary Splitting Mechanics in CART
In our CART implementation, candidate binary splits are defined by selecting a continuous feature index $j \in \{1, \dots, 115\}$ and a real-valued scalar threshold $\theta \in \mathbb{R}$. The sample partition $S_t$ is divided into two mutually exclusive subsets:

$$t_L(j, \theta) = \{\mathbf{x} \in S_t \mid x_j \le \theta\}, \qquad t_R(j, \theta) = \{\mathbf{x} \in S_t \mid x_j > \theta\}$$

The impurity reduction (Gini Gain) produced by split $(j, \theta)$ at node $t$ is:

$$\Delta \text{Gini}(j, \theta, t) = \text{Gini}(t) - \left[ \frac{|t_L|}{|S_t|} \text{Gini}(t_L) + \frac{|t_R|}{|S_t|} \text{Gini}(t_R) \right]$$

The optimal split $(j^*, \theta^*)$ chosen by the algorithm maximizes this impurity reduction across all available features and thresholds:

$$(j^*, \theta^*) = \arg\max_{j \in \{1, \dots, d\}, \ \theta \in \Theta_j} \Delta \text{Gini}(j, \theta, t)$$

where $\Theta_j$ is the set of all unique midpoints between consecutive sorted values of feature $j$ present in $S_t$.

---

# 5. Cost-Complexity Pruning (ccp_alpha) Formulation

### 5.1 The Danger of Structural Overfitting in IoT Security
If a decision tree is grown recursively without constraints, partitioning continues until every terminal leaf is completely pure ($\text{Gini}(t) = 0$) or contains fewer samples than `min_samples_split`. In high-dimensional network telemetry (115 statistical features), an unconstrained tree captures:
- Transient background packet timing jitter,
- Device-specific hardware clock drifts,
- Finite sample sampling noise.

This produces an over-parameterized tree with excessive depth and redundant leaf nodes. In our baseline experiment, the unpruned tree grew to:
- Depth: **21 levels**
- Total Nodes: **181 nodes**
- Terminal Leaves: **91 leaves**
- Train Accuracy: **99.7166%**, Test Accuracy: **99.6144%** (Generalization gap: $0.1022\%$).

While such a model performs well on training data, its structural bloat increases memory consumption, inflates inference latency, and risks performance degradation under zero-day traffic shifts.

### 5.2 Mathematical Formulation of Minimal Cost-Complexity
To enforce structural regularization, Breiman et al. introduced **Minimal Cost-Complexity Pruning**, parameterized by a non-negative regularization hyperparameter $\alpha \ge 0$ (denoted `ccp_alpha` in scikit-learn).

For any pruned subtree $T \subseteq T_{\max}$ rooted at $t_0$, the cost-complexity objective function $R_\alpha(T)$ is defined as:

$$R_\alpha(T) = R(T) + \alpha |T|$$

Where:
1. **$R(T)$ (Total Misclassification Risk / Impurity):** The sample-weighted sum of leaf impurities across all terminal nodes in subtree $T$:

$$R(T) = \sum_{t \in \widetilde{T}} \frac{|S_t|}{|S|} \text{Gini}(t)$$

where $\widetilde{T}$ denotes the set of terminal leaf nodes in $T$, $|S_t|$ is the number of training instances mapped to leaf $t$, and $|S|$ is the total number of training instances ($|S| = 102,692$).
2. **$|T|$ (Model Complexity):** The total number of terminal leaf nodes in subtree $T$.
3. **$\alpha$ ($ccp\_\alpha \ge 0$):** The complexity penalty coefficient that dictates the trade-off between training impurity fit and model parsimony.

### 5.3 Boundary Behaviors of Cost-Complexity Pruning
- **$\alpha = 0$:** The complexity penalty term vanishes ($\alpha |T| = 0$). The cost-complexity criterion reduces strictly to empirical impurity minimization: $R_0(T) = R(T)$. The optimal tree is the maximal unpruned tree $T_{\max}$ (depth 21, 91 leaves).
- **$\alpha \to \infty$:** The penalty for leaf count dominates completely. The objective function forces all internal splits to collapse, reducing the tree to a single root node ($|T| = 1$) that predicts the global majority class.
- **$0 < \alpha < \infty$:** Intermediate values prune subtrees whose impurity reduction fails to compensate for the penalty $\alpha$ incurred by maintaining their constituent leaves.

### 5.4 Weakest-Link Pruning Mechanics
Pruning proceeds by identifying the "weakest link" in the tree. For any internal node $t$, let $T_t$ denote the entire branch (subtree) rooted at node $t$.
- If $T_t$ is preserved, its contribution to the cost-complexity risk is $R(T_t) + \alpha |T_t|$.
- If $T_t$ is collapsed into a single leaf node $t$, its cost-complexity risk becomes $R(t) + \alpha (1)$.

Collapsing the subtree into leaf $t$ is mathematically preferred whenever:

$$R(t) + \alpha \le R(T_t) + \alpha |T_t|$$

Solving for $\alpha$ defines the **effective cost-complexity threshold $\alpha_{\text{eff}}(t)$**:

$$\alpha_{\text{eff}}(t) = \frac{R(t) - R(T_t)}{|T_t| - 1}$$

**Interpretation:**
- $\alpha_{\text{eff}}(t)$ quantifies the rate of impurity increase per leaf removed if branch $T_t$ is collapsed.
- At each iteration of pruning, the algorithm computes $\alpha_{\text{eff}}(t)$ for every internal node $t \in \mathcal{N}_{\text{int}}$ and collapses the node with the minimum effective alpha:

$$t^* = \arg\min_{t \in \mathcal{N}_{\text{int}}} \alpha_{\text{eff}}(t)$$

This process produces a nested sequence of strictly shrinking subtrees:

$$T_{\max} = T_0 \supset T_1 \supset T_2 \supset \dots \supset T_m = \{t_0\}$$

associated with an ordered, strictly increasing sequence of critical threshold values:

$$0 = \alpha_0 < \alpha_1 < \alpha_2 < \dots < \alpha_m$$

Each subtree $T_k$ is guaranteed to be the uniquely optimal subtree minimizing $R_\alpha(T)$ for all $\alpha \in [\alpha_k, \alpha_{k+1})$.

---

# 6. Experimental Partitioning and Hyperparameter Optimization Pipeline

To guarantee rigorous academic reproducibility and prevent **data leakage**, model selection must never inspect the final held-out test dataset.

### 6.1 Three-Way Data Partitioning Architecture
The experimental evaluation established a strict three-way partitioning scheme:
1. **N-BaIoT Population & Systematic Sampling:** From 7,062,606 raw telemetry packets spanning 89 CSV files, systematic sampling with a deterministic row step of $k = 55$ extracted a verified subset of **128,366 packets**.
2. **Train/Test Stratified Split (80/20):**
   - **Training Partition (80%):** 102,692 packets
   - **Held-Out Test Partition (20%):** 25,674 packets (sealed until final evaluation)
3. **Internal Train/Validation Split (80/20 on Training Partition):**
   - **Internal Training Subset (80% of Train):** 82,153 packets
   - **Internal Validation Subset (20% of Train):** 20,539 packets

### 6.2 Pruning Path Discovery
Using `sklearn.tree.DecisionTreeClassifier.cost_complexity_pruning_path` fitted strictly on the internal training subset (`X_train_sub`, `y_train_sub`), the complete weakest-link pruning path was extracted:
- **Discovered Candidate Alphas:** 60 unique critical values spanning $[0.0, 0.12135]$.
- **Evaluated Subsets:** 20 representative alpha candidates were evaluated systematically against the 20,539-sample internal validation set.

### 6.3 Empirical Validation Results Across Alpha Candidates

The table below documents the empirical validation trajectory across all 20 evaluated candidates:

| Candidate ID | Pruning Parameter ($ccp\_\alpha$) | Realized Depth | Total Nodes | Terminal Leaves ($|T|$) | Validation Accuracy | Validation Macro F1 | Fit Time (s) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | $0.0000 \times 10^0$ | 16 | 147 | 74 | 99.7127% | 99.7696% | 4.02s |
| 1 | $1.2172 \times 10^{-5}$ | 16 | 135 | 68 | 99.7127% | 99.7696% | 3.99s |
| **2 (Selected)** | **$1.999753 \times 10^{-5}$** | **16** | **129** | **65** | **99.7127%** | **99.7696%** | **3.95s** |
| 3 | $2.2722 \times 10^{-5}$ | 16 | 123 | 62 | 99.7079% | 99.7654% | 3.95s |
| 4 | $3.2221 \times 10^{-5}$ | 16 | 117 | 59 | 99.7079% | 99.7654% | 4.04s |
| 5 | $3.8412 \times 10^{-5}$ | 16 | 109 | 55 | 99.6933% | 99.7501% | 3.95s |
| 6 | $4.6058 \times 10^{-5}$ | 16 | 103 | 52 | 99.6981% | 99.7542% | 3.97s |
| 7 | $7.0727 \times 10^{-5}$ | 16 | 97 | 49 | 99.6884% | 99.7410% | 3.97s |
| 8 | $8.9385 \times 10^{-5}$ | 16 | 87 | 44 | 99.6689% | 99.7082% | 3.96s |
| 9 | $1.0061 \times 10^{-4}$ | 16 | 81 | 41 | 99.6689% | 99.7082% | 3.97s |
| 10 | $1.1166 \times 10^{-4}$ | 16 | 75 | 38 | 99.6202% | 99.6384% | 3.96s |
| 11 | $2.7845 \times 10^{-4}$ | 15 | 65 | 33 | 99.5277% | 99.4659% | 3.99s |
| 12 | $2.9993 \times 10^{-4}$ | 15 | 59 | 30 | 99.4985% | 99.4312% | 3.95s |
| 13 | $3.9398 \times 10^{-4}$ | 15 | 53 | 27 | 99.4401% | 99.3211% | 4.02s |
| 14 | $9.0204 \times 10^{-4}$ | 13 | 45 | 23 | 99.3622% | 99.1593% | 4.00s |
| 15 | $1.6812 \times 10^{-3}$ | 10 | 33 | 17 | 98.7974% | 98.2321% | 3.95s |
| 16 | $4.5825 \times 10^{-3}$ | 8 | 27 | 14 | 98.1888% | 96.9587% | 4.00s |
| 17 | $2.8909 \times 10^{-2}$ | 6 | 21 | 11 | 92.9500% | 85.1823% | 3.97s |
| 18 | $6.3981 \times 10^{-2}$ | 5 | 13 | 7 | 75.7486% | 57.3641% | 3.97s |
| 19 (Root) | $1.2135 \times 10^{-1}$ | 0 | 1 | 1 | 17.4205% | 2.6974% | 3.95s |

### 6.4 Selection Rule and Final Parameter Determination
The optimization algorithm applied a strict 3-tier hierarchical selection policy:
1. **Primary Criterion:** Maximize multiclass validation Macro F1-score ($\arg\max_{\alpha} \text{F1}_{\text{macro}}(\alpha)$).
2. **Secondary Criterion:** Maximize multiclass validation Accuracy.
3. **Tie-Breaker:** Minimize model complexity (select the model with the minimum number of terminal leaves $|T|$).

**Result:** Candidates 0, 1, and 2 all achieved identical peak validation performance (Macro F1: 99.7696%, Accuracy: 99.7127%). However, Candidate 2 collapsed terminal leaves from 74 to 65 (a 12.2% reduction in subtree complexity). Consequently, **Candidate 2 with $\alpha^* = 1.999753 \times 10^{-5}$** was isolated as the optimal regularization parameter.

---

# 7. Final Model Retraining and Test Set Verification

With $\alpha^* = 1.999753 \times 10^{-5}$ locked in, the final decision tree model was retrained on the complete 102,692-sample training set and evaluated **exactly once** against the held-out 25,674-sample test set.

### 7.1 Baseline Unpruned vs. Final Pruned Performance Comparison

| Performance / Structural Metric | Baseline Decision Tree ($\alpha = 0.0$) | Final Pruned Decision Tree ($\alpha = 1.999753 \times 10^{-5}$) | Net Change / Engineering Impact |
| :--- | :---: | :---: | :---: |
| **Pruning Hyperparameter ($ccp\_\alpha$)** | $0.0$ | **$1.999753 \times 10^{-5}$** | Optimal Validation-Selected |
| **Maximum Tree Depth** | 21 levels | **18 levels** | **-3 levels (-14.3%)** |
| **Total Node Count** | 181 nodes | **133 nodes** | **-48 nodes (-26.5%)** |
| **Terminal Leaves ($|T|$)** | 91 leaves | **67 leaves** | **-24 leaves (-26.4%)** |
| **Multiclass Test Accuracy** | 99.6144% | **99.6183%** | **+0.0039% (Maintained / Slight Gain)** |
| **Multiclass Macro F1-Score** | 99.6487% | **99.6510%** | **+0.0023% (Maintained / Slight Gain)** |
| **Multiclass Weighted F1-Score** | 99.6141% | **99.6182%** | **+0.0041% (Maintained / Slight Gain)** |
| **Generalization Gap (Train - Test Acc)** | 0.1022% | **0.0769%** | **-0.0253% (Overfitting reduced by 24.8%)** |
| **Binary Detection Accuracy** | 99.9649% | **99.9649%** | **Identical (>99.96%)** |
| **Binary Detection F1-Score** | 99.9810% | **99.9810%** | **Identical (>99.98%)** |
| **Training Time (Full Train Set)** | 5.8940 s | **5.8563 s** | -0.0377 s |
| **Serialized Model File Size** | 6.16 KB | **5.44 KB** | **-11.7% Flash Storage Reduction** |

---

# 8. Complete Algorithmic Pseudocode

The full inductive pipeline comprises two interdependent algorithms: (1) Greedy Recursive CART Tree Construction, and (2) Minimal Cost-Complexity Weakest-Link Pruning.

### 8.1 Algorithm 1: Recursive CART Binary Tree Induction
```text
Algorithm 1: Recursive_CART_Build(S_t, current_depth, max_depth, min_samples_split)
Input: 
  S_t: Set of training samples at node t (Matrix X_t in R^(N_t x d), Labels y_t in {1..C}^N_t)
  current_depth: Depth of current node in tree hierarchy
  max_depth: Maximum permissible depth threshold (or infinity)
  min_samples_split: Minimum samples required to partition an internal node

Output:
  Node t (either an Internal Decision Node or a Terminal Leaf Node)

1: Calculate empirical class probabilities: p_i = (1 / |S_t|) * sum(I(y == i)) for i in 1..C
2: Compute node impurity: Gini(t) = 1 - sum(p_i^2)
3: Assign majority class prediction: c_pred = argmax_i (p_i)

4: if Gini(t) == 0 or |S_t| < min_samples_split or current_depth >= max_depth then
5:     return LeafNode(class_label = c_pred, samples = |S_t|, impurity = Gini(t))
6: end if

7: Initialize best_gain = 0, best_feature = NULL, best_threshold = NULL
8: for each feature j in 1..d do
9:     Sort instances in S_t based on feature x_j in ascending order
10:    Identify set of candidate midpoints: Theta_j = {(x_(k,j) + x_(k+1,j)) / 2 | y_k != y_(k+1)}
11:    for each candidate threshold theta in Theta_j do
12:        Partition S_t into t_L = {x in S_t | x_j <= theta} and t_R = {x in S_t | x_j > theta}
13:        if |t_L| == 0 or |t_R| == 0 then continue
14:        Compute split impurity: Gini_split = (|t_L| / |S_t|) * Gini(t_L) + (|t_R| / |S_t|) * Gini(t_R)
15:        Delta_Gini = Gini(t) - Gini_split
16:        if Delta_Gini > best_gain then
17:            best_gain = Delta_Gini
18:            best_feature = j
19:            best_threshold = theta
20:        end if
21:    end for
22: end for

23: if best_gain <= 0 then
24:     return LeafNode(class_label = c_pred, samples = |S_t|, impurity = Gini(t))
25: end if

26: Partition S_t into t_L* and t_R* using (best_feature, best_threshold)
27: left_child = Recursive_CART_Build(t_L*, current_depth + 1, max_depth, min_samples_split)
28: right_child = Recursive_CART_Build(t_R*, current_depth + 1, max_depth, min_samples_split)

29: return InternalNode(feature = best_feature, threshold = best_threshold, 
                         left = left_child, right = right_child, impurity = Gini(t))
```

### 8.2 Algorithm 2: Minimal Cost-Complexity Pruning Path & Selection
```text
Algorithm 2: Cost_Complexity_Prune_and_Select(T_max, S_val, alpha_candidates)
Input:
  T_max: Fully grown unpruned decision tree
  S_val: Validation dataset (X_val, y_val) containing 20,539 instances
  alpha_candidates: Sequence of critical thresholds [alpha_0, alpha_1, ..., alpha_m]

Output:
  T_optimal: Pruned decision tree exhibiting optimal validation generalization

1: Initialize k = 0, T_k = copy(T_max), pruning_sequence = []
2: while |T_k| > 1 do
3:     for each internal node t in T_k do
4:         Let T_t be the subtree rooted at t with terminal leaves Leaves(T_t)
5:         Compute R(t) = (|S_t| / |S|) * Gini(t)
6:         Compute R(T_t) = sum_{leaf in Leaves(T_t)} (|S_leaf| / |S|) * Gini(leaf)
7:         Calculate effective alpha: alpha_eff(t) = (R(t) - R(T_t)) / (|Leaves(T_t)| - 1)
8:     end for
9:     Find weakest link: t* = argmin_t (alpha_eff(t))
10:    alpha_k = alpha_eff(t*)
11:    Collapse subtree T_t* into a single terminal leaf node t*
12:    Record (alpha_k, copy(T_k)) into pruning_sequence
13:    k = k + 1
14: end while

15: Initialize best_macro_f1 = -1, min_leaves = infinity, selected_alpha = 0
16: for each candidate (alpha, T_cand) in pruning_sequence do
17:     Evaluate T_cand on validation partition S_val:
18:     y_val_pred = T_cand.predict(X_val)
19:     val_f1 = Calculate_Macro_F1(y_val, y_val_pred)
20:     val_acc = Calculate_Accuracy(y_val, y_val_pred)
21:     if val_f1 > best_macro_f1 then
22:         best_macro_f1 = val_f1
23:         min_leaves = |Leaves(T_cand)|
24:         selected_alpha = alpha
25:     else if val_f1 == best_macro_f1 and |Leaves(T_cand)| < min_leaves then
26:         min_leaves = |Leaves(T_cand)|
27:         selected_alpha = alpha
28:     end if
29: end for

30: Retrain final model T_optimal on full training set S with ccp_alpha = selected_alpha
31: return T_optimal
```

---

# 9. Asymptotic and Hardware Complexity Analysis

A primary motivation for deploying Decision Trees in IoT cybersecurity is their superior computational and space scaling properties compared to alternative architectures.

### 9.1 Time Complexity Analysis
1. **Training Phase Complexity:**  
   At each internal node with $N_t$ instances, sorting $d$ continuous features takes $\mathcal{O}(d \cdot N_t \log N_t)$. Evaluating $N_t - 1$ split thresholds requires $\mathcal{O}(d \cdot N_t)$ time using running class histograms. Summing over all tree levels up to depth $h$, the worst-case training complexity is:

$$\mathcal{T}_{\text{train}} = \mathcal{O}(d \cdot N \cdot h)$$

   For a balanced tree where $h \approx \log_2 N$, this reduces to $\mathcal{O}(d \cdot N \log_2 N)$. In our empirical setup ($N = 102,692$, $d = 115$), complete model training required only **5.8563 seconds** on single-core Apple Silicon.
2. **Pruning Phase Complexity:**  
   Computing the weakest-link pruning path on the baseline tree requires iterating over internal nodes ($|\mathcal{N}_{\text{int}}| < 100$). The pruning path computation completed in **4.18 seconds**, representing a one-time offline optimization investment.
3. **Inference Phase Complexity (Per-Packet Latency):**  
   At operational test time, classifying an individual packet does **not** evaluate the entire tree. Traversal follows a single directed path from the root node to a leaf:

$$\mathcal{T}_{\text{inference}} = \mathcal{O}(h)$$

   Because our pruned model achieved a maximum depth of **$h = 18$**, evaluating an incoming packet requires **at most 18 scalar comparison operations**. In contrast, a 3-layer Multi-Layer Perceptron (MLP) with 128 hidden units would require over $115 \times 128 + 128 \times 128 \approx 31,000$ floating-point multiply-accumulate (MAC) operations per packet.  
   Empirical benchmarking demonstrated an average single-packet classification latency of **34.41 microseconds ($\mu$s)**.

### 9.2 Space and Memory Complexity Analysis
1. **Operational Runtime Memory:**  
   The decision tree stores only the scalar threshold $\theta$, feature index $j$, and pointer indices for each of the $133$ nodes. The serialized model footprint on disk is **5.44 KB**, and its in-memory footprint in RAM is under **100 KB**.
2. **Cache Residency:**  
   The entire decision tree structure easily fits within the L1 data cache of modern embedded microprocessors (typically 32 KB to 64 KB), ensuring that tree traversal avoids main memory bus stalls.

### 9.3 Algorithmic Complexity Comparison Table

| Complexity Parameter | Decision Tree (Group 1 Ours) | K-Nearest Neighbors (KNN - Group 2) | Random Forest (Group 5) | Deep Autoencoder (Base Paper) |
| :--- | :---: | :---: | :---: | :---: |
| **Training Time Complexity** | $\mathcal{O}(d \cdot N \log N)$ | $\mathcal{O}(1)$ (Lazy learner) | $\mathcal{O}(B \cdot d' \cdot N \log N)$ | $\mathcal{O}(E \cdot N \cdot W)$ |
| **Inference Time Complexity** | $\mathcal{O}(h) \le 18$ comparisons | $\mathcal{O}(N \cdot d) \approx 1.17 \times 10^7$ ops | $\mathcal{O}(B \cdot h) \approx 100 \times 18$ ops | $\mathcal{O}(W)$ dense matrix ops |
| **Measured Per-Packet Latency** | **34.41 $\mu$s** | High ($\sim$ milliseconds) | Medium ($\sim$ hundreds of $\mu$s) | Medium-High ($\sim$ ms) |
| **Model Size (Storage)** | **5.44 KB** | Massive ($\sim$ 90 MB dataset in RAM) | Large ($\sim 500$ KB - 5 MB) | Medium ($\sim 100$ KB - 1 MB) |
| **Hardware Suitability** | Microcontrollers & Edge Routers | Cloud / High-RAM Servers Only | Medium Edge Gateways | GPU / NPU Accelerators |

---

# 10. Advantages and Limitations in IoT Security Deployments

### 10.1 Key Advantages
1. **White-Box Auditability and Explainability:** Every classification is verifiable through an explicit Boolean rule chain (e.g., `if H_L0.01_mean <= 64.2 and HH_jit_L1_mean > 0.05 then mirai_ack`). This allows network security administrators to audit detection decisions and implement firewall rules.
2. **Deterministic Hard Real-Time Execution:** An upper bound of 18 comparisons ensures bounded execution times, preventing buffer bloat or packet dropping under heavy traffic spikes.
3. **Scale Invariance:** Decision trees are invariant to monotonic feature transformations. No feature normalization or standard scaling is required, preserving physical units (e.g., packet arrival variance in milliseconds).
4. **Resilience to Irrelevant Features:** Features that provide no class separation are naturally ignored during recursive split optimization.

### 10.2 Practical Limitations
1. **Axis-Aligned Decision Boundaries:** Because splits are univariate ($x_j \le \theta$), decision trees approximate diagonal or complex non-linear boundaries via staircase step functions, requiring deeper branches to separate correlated features.
2. **Greedy Induction (Horizon Effect):** Greedy top-down induction does not guarantee a globally optimal tree; suboptimal early splits cannot be revised later in the hierarchy.
3. **Upstream Feature Extraction Overhead:** While tree traversal requires only 34.41 $\mu$s, the extraction of 115 damped sliding-window packet statistics requires continuous stream processing via the Kitsune feature extractor.
4. **Sensitivity to Imbalanced Sampling:** Without post-pruning or class weighting, greedy trees tend to bias splits toward dominant classes.

---

# 11. Summary of Algorithmic Findings

1. **CART with Minimal Cost-Complexity Pruning** provides a mathematically sound, highly efficient inductive framework for IoT botnet detection.
2. Pruning with the validation-selected parameter **$\alpha^* = 1.999753 \times 10^{-5}$** reduced tree depth by **14.3%** (from 21 to 18) and pruned **26.5%** of internal nodes (from 181 to 133).
3. The pruned tree narrowed the train-test generalization gap from **$0.1022\%$ to $0.0769\%$** (a 24.8% reduction in overfitting) while slightly increasing multiclass test accuracy to **99.6183%** and macro F1 to **99.6510%**.
4. The serialized model occupies only **5.44 KB**, demonstrating complete viability for line-rate deployment on resource-constrained IoT gateway routers.
