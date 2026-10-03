# N-BaIoT Dataset Inspection Report

## 1. Executive Summary
- **Dataset Name:** N-BaIoT (Network-Based Detection of IoT Botnet Attacks Using Deep Autoencoders)
- **Primary Source:** UCI Machine Learning Repository (Donated 2018)
- **Directory Path:** `/Users/swapnil/Documents/cns/archive`
- **Total Physical Size:** ~7.6 GB
- **Total Files:** 93 total files (89 traffic data CSVs + 3 metadata CSVs + 1 README.md)
- **Total Records:** 7,062,606 network flow packets
- **Total Features:** 115 numerical features (continuous statistics across damped sliding windows)
- **Label Structure:** Labels are encoded in the filenames (`<DeviceID>.<AttackFamily>.<AttackVector>.csv` or `<DeviceID>.benign.csv`). The CSV files themselves contain only raw numerical features.

## 2. Quantitative Distribution
- **Benign Traffic Records:** 555,932 (7.87%)
- **Malicious/Botnet Traffic Records:** 6,506,674 (92.13%)
- **IoT Devices Monitored:** 9 commercial IoT appliances
  - Danmini Doorbell (Device 1)
  - Ecobee Thermostat (Device 2)
  - Ennio Doorbell (Device 3 - Note: Gafgyt infected only)
  - Philips B120N10 Baby Monitor (Device 4)
  - Provision PT-737E Security Camera (Device 5)
  - Provision PT-838 Security Camera (Device 6)
  - Samsung SNH-1011_N Webcam (Device 7 - Note: Gafgyt infected only)
  - SimpleHome XCS7-1002-WHT Security Camera (Device 8)
  - SimpleHome XCS7-1003-WHT Security Camera (Device 9)

## 3. Attack Vector Classes
The dataset supports two classification taxonomies:
1. **Binary Classification:** Benign (0) vs Attack (1)
2. **Multiclass Classification (11 classes):**
   - `benign`: Normal baseline traffic
   - `gafgyt_combo`: BASHLITE combo brute-force / dictionary attack
   - `gafgyt_junk`: BASHLITE junk spam flood
   - `gafgyt_scan`: BASHLITE port and IP scanning
   - `gafgyt_tcp`: BASHLITE TCP syn/ack flood
   - `gafgyt_udp`: BASHLITE UDP flood
   - `mirai_ack`: Mirai ACK flooding
   - `mirai_scan`: Mirai automated telnet/port scanner
   - `mirai_syn`: Mirai SYN flooding
   - `mirai_udp`: Mirai UDP packet flooding
   - `mirai_udpplain`: Mirai UDP flooding without headers/plain payload

## 4. Feature Space & Data Integrity
- **Missing Values:** 0 null values across all checked files.
- **Duplicate Rows:** 0 duplicate rows detected in checked samples.
- **Data Types:** 100% numerical (`float64`).
- **Data Leakage & Identifiers:**
  - No direct IP addresses (`src_ip`, `dst_ip`), MAC addresses, packet timestamps, or raw IDs are present in the feature columns.
  - The feature space consists purely of statistical aggregations: weight, mean, variance/std, magnitude, radius, covariance, and Pearson correlation coefficients across 5 decay timeframes (Lambda in [5, 3, 1, 0.1, 0.01]).
  - Port and protocol dynamics are captured via the `HpHp_` stream aggregation (Host+Port to Host+Port), rather than raw numerical port headers.

## 5. Memory Management & Reproducible Sampling Strategy
Given the 7.6 GB uncompressed volume (7,062,606 rows), training an in-memory Decision Tree on the full uncompressed dataset would exceed available RAM (16 GB total, ~5.2 GB available) and cause system paging.
To ensure mathematical reproducibility and statistical significance:
- A stratified sampling strategy is implemented taking representative stratified subsets from each of the 89 files.
- A balanced stratified sample of 120,000 packets (preserving exact device and attack-vector proportions) will be utilized for training, pruning tuning, and evaluation, ensuring sub-second inference benchmarking and stable tree convergence.
