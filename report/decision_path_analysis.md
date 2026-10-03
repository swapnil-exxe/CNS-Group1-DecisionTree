# Decision Path Analysis for Representative Network Packets

This report traces the exact sequence of feature splits and threshold decisions evaluated by the final pruned Decision Tree for representative benign and botnet packets.

## Representative Case: Benign Normal Traffic
- **Sample Test Index:** 1
- **Ground Truth Class:** `benign`
- **Model Prediction:** `benign`
- **Decision Sequence (Root to Terminal Leaf):**

  1. **Node 0**: Evaluate `MI_dir_L0.01_weight` (100.9036) > 1.0000 -> branch Right
  2. **Node 4**: Evaluate `MI_dir_L0.01_mean` (70.4300) <= 299.4007 -> branch Left
  3. **Node 5**: Evaluate `MI_dir_L0.1_weight` (10.2895) <= 184.9498 -> branch Left
  4. **Node 6**: Evaluate `H_L0.01_mean` (70.4300) > 64.0852 -> branch Right
  5. **Node 8**: Evaluate `HH_jit_L0.1_variance` (21.7193) <= 5858155539988480.0000 -> branch Left
  6. **Node 9**: Evaluate `H_L5_weight` (1.0319) <= 62.8825 -> branch Left
  7. **Leaf Node 10**: Terminal Node reached. Class = `benign` (Confidence: 1.0/1 samples = 100.0%)

**Path Flow:** MI_dir_L0.01_weight (> 1.00) -> MI_dir_L0.01_mean (<= 299.40) -> MI_dir_L0.1_weight (<= 184.95) -> H_L0.01_mean (> 64.09) -> HH_jit_L0.1_variance (<= 5858155539988480.00) -> H_L5_weight (<= 62.88) -> Terminal: benign

------------------------------------------------------------

## Representative Case: Gafgyt TCP Attack Traffic
- **Sample Test Index:** 2
- **Ground Truth Class:** `gafgyt_tcp`
- **Model Prediction:** `gafgyt_tcp`
- **Decision Sequence (Root to Terminal Leaf):**

  1. **Node 0**: Evaluate `MI_dir_L0.01_weight` (1.0000) <= 1.0000 -> branch Left
  2. **Node 1**: Evaluate `HH_jit_L1_mean` (1505913600.0000) > 1505913536.0000 -> branch Right
  3. **Leaf Node 3**: Terminal Node reached. Class = `gafgyt_tcp` (Confidence: 1.0/1 samples = 100.0%)

**Path Flow:** MI_dir_L0.01_weight (<= 1.00) -> HH_jit_L1_mean (> 1505913536.00) -> Terminal: gafgyt_tcp

------------------------------------------------------------

## Representative Case: Mirai SYN Flooding Traffic
- **Sample Test Index:** 20
- **Ground Truth Class:** `mirai_syn`
- **Model Prediction:** `mirai_syn`
- **Decision Sequence (Root to Terminal Leaf):**

  1. **Node 0**: Evaluate `MI_dir_L0.01_weight` (10822.3242) > 1.0000 -> branch Right
  2. **Node 4**: Evaluate `MI_dir_L0.01_mean` (69.2513) <= 299.4007 -> branch Left
  3. **Node 5**: Evaluate `MI_dir_L0.1_weight` (5550.0645) > 184.9498 -> branch Right
  4. **Node 23**: Evaluate `H_L0.01_mean` (69.2513) > 63.5721 -> branch Right
  5. **Node 25**: Evaluate `H_L0.01_mean` (69.2513) <= 72.4576 -> branch Left
  6. **Leaf Node 26**: Terminal Node reached. Class = `mirai_syn` (Confidence: 1.0/1 samples = 100.0%)

**Path Flow:** MI_dir_L0.01_weight (> 1.00) -> MI_dir_L0.01_mean (<= 299.40) -> MI_dir_L0.1_weight (> 184.95) -> H_L0.01_mean (> 63.57) -> H_L0.01_mean (<= 72.46) -> Terminal: mirai_syn

------------------------------------------------------------

## Representative Case: Mirai UDP Flooding Traffic
- **Sample Test Index:** 0
- **Ground Truth Class:** `mirai_udp`
- **Model Prediction:** `mirai_udp`
- **Decision Sequence (Root to Terminal Leaf):**

  1. **Node 0**: Evaluate `MI_dir_L0.01_weight` (50958.6055) > 1.0000 -> branch Right
  2. **Node 4**: Evaluate `MI_dir_L0.01_mean` (427.2616) > 299.4007 -> branch Right
  3. **Node 106**: Evaluate `HH_L0.1_magnitude` (553.8713) <= 558.8756 -> branch Left
  4. **Node 107**: Evaluate `HpHp_L1_weight` (1.0000) <= 3.1441 -> branch Left
  5. **Node 108**: Evaluate `HH_jit_L0.01_mean` (8292.3057) <= 1507657152.0000 -> branch Left
  6. **Node 109**: Evaluate `H_L3_weight` (235.1067) > 7.9866 -> branch Right
  7. **Node 111**: Evaluate `HH_jit_L0.01_variance` (12501870706688.0000) <= 5991171214016512.0000 -> branch Left
  8. **Node 112**: Evaluate `HpHp_L0.1_weight` (1.0000) <= 1.2578 -> branch Left
  9. **Leaf Node 113**: Terminal Node reached. Class = `mirai_udp` (Confidence: 1.0/1 samples = 100.0%)

**Path Flow:** MI_dir_L0.01_weight (> 1.00) -> MI_dir_L0.01_mean (> 299.40) -> HH_L0.1_magnitude (<= 558.88) -> HpHp_L1_weight (<= 3.14) -> HH_jit_L0.01_mean (<= 1507657152.00) -> H_L3_weight (> 7.99) -> HH_jit_L0.01_variance (<= 5991171214016512.00) -> HpHp_L0.1_weight (<= 1.26) -> Terminal: mirai_udp

------------------------------------------------------------
