# 5.2 Computational Overhead & Hardware Latency Analysis

## 5.2.1 Experimental Hardware & Software Environment
All empirical benchmarks were executed on the local evaluation host without simulated hardware approximations. The exact runtime parameters are detailed below:

| System Property | Specification |
| :--- | :--- |
| **Operating System** | Darwin 27.0.0 (Darwin Kernel Version 27.0.0: Tue Aug 11 21:02:57 PDT 2026; root:xnu-13432.1.9~1/RELEASE_ARM64_T8132) |
| **Hardware Architecture** | arm64 (Apple Silicon) |
| **Physical / Logical Cores** | 10 Physical / 10 Logical |
| **System Memory (RAM)** | 16.0 GB Total (4.9 GB Free at execution) |
| **Python Environment** | Python 3.13.9 |
| **Machine Learning Engine** | scikit-learn 1.7.2, NumPy 2.3.5, Pandas 2.3.3 |

## 5.2.2 Training Computational Cost
Training was conducted over 102,692 packets across 115 network traffic statistical features. Measured across 5 independent runs with variable seeds:

- **Baseline Unpruned Tree Training Time:** 5.8516 s $\pm$ 0.0456 s (17,549 samples/s)
- **Pruned Decision Tree Training Time:** 5.9111 s $\pm$ 0.1017 s (17,373 samples/s)
- **Pruning Overhead:** Cost-complexity pruning path computation required 4.18 s once on the baseline tree, while subsequent fitting with the optimal parameter $\alpha = 1.9998e-05$ incurs zero runtime penalty compared to standard greedy growth.

## 5.2.3 Inference Latency and Throughput Profiling
To evaluate operational viability for IoT gateway deployment, inference time was profiled across variable packet batch sizes:

| Batch Size | Pruned Batch Time (ms) | Per-Sample Latency ($\mu$s) | Throughput (Packets/s) | Speedup vs Baseline |
| :---: | :---: | :---: | :---: | :---: |
| **1 (Real-Time)** | 0.0344 ms | 34.41 $\mu$s | 29,062 | 13.42% |
| **10** | 0.0337 ms | 3.37 $\mu$s | 296,626 | 6.81% |
| **100** | 0.0411 ms | 0.41 $\mu$s | 2,434,021 | -8.02% |
| **1,000** | 0.0920 ms | 0.09 $\mu$s | 10,874,591 | -1.11% |
| **10,000** | 0.6677 ms | 0.07 $\mu$s | 14,977,408 | -3.83% |
| **Full Set (25,674)** | 2.1331 ms | 0.083 $\mu$s | 12,036,209 | 7.13% |

## 5.2.4 Effect of Cost-Complexity Pruning on Computational Overhead
1. **Tree Depth Reduction:** Pruning reduced maximum decision depth from 21 to 18 levels (-14.3%), guaranteeing an upper bound of at most 18 scalar comparison operations per packet classification.
2. **Structural Pruning:** Node count decreased from 181 to 133 (-26.5%), and terminal leaves shrank from 91 to 67 (-26.4%).
3. **Memory Footprint:** The serialized model file occupies only **5.44 KB** on disk (and < 100 KB in RAM), easily fitting inside L1/L2 CPU caches or microcontroller flash memory.
4. **Line-Rate Suitability:** At batch processing, the pruned model processes over **12,036,209 packets/second**, exceeding standard Gigabit Ethernet wire speeds (~1.488 million packets/second for 64-byte packets) by more than 6x.

## 5.2.5 Comparative Algorithm Benchmark Matrix (Group 1 vs Other Project Groups)
The measured metrics for Group 1 (Decision Tree) are summarized below, alongside the standardized template reserved for peer project groups:

| Model Architecture | Implementation Group | Training Time (s) | Single-Packet Latency | Batch Throughput | Model Size | Macro F1-Score | Binary Accuracy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Pruned Decision Tree (CART)** | **Group 1 (Ours)** | **5.911 s** | **34.41 $\mu$s** | **12,036,209 pkts/s** | **5.44 KB** | **99.65%** | **99.96%** |
| K-Nearest Neighbors (KNN) | Group 2 | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* |
| AdaBoost Classifier | Group 3 | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* |
| Isolation Forest | Group 4 | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* |
| Random Forest Ensemble | Group 5 | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* | *Pending* |

## 5.2.6 Limitations
- **Sliding-Window Feature Extractor Dependency:** While decision tree traversal takes only 34.41 $\mu$s, the upstream damped sliding-window packet statistics extraction (Kitsune feature extractor) incurs its own CPU overhead.
- **Single-Core Evaluation:** Benchmarks reflect single-threaded CPU execution. Parallel SIMD or GPU inference was not evaluated because scalar tree decisions are already microsecond-scale.
