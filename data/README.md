# Dataset Reference & Documentation

## Dataset: N-BaIoT (Network-Based Detection of IoT Botnet Attacks)
- **Source Location on Mac:** `/Users/swapnil/Documents/cns/archive`
- **Original Source:** UCI Machine Learning Repository
- **Creators:** Yair Meidan, Michael Bohadana, Yael Mathov, Yisroel Mirsky, Dominik Breitenbacher, Asaf Shabtai, Yuval Elovici (2018)
- **Reference Article:** "N-BaIoT: Network-based Detection of IoT Botnet Attacks Using Deep Autoencoders", IEEE Pervasive Computing, 2018.

## Structure:
- 89 CSV files covering 9 commercial IoT devices:
  1. Danmini Doorbell
  2. Ecobee Thermostat
  3. Ennio Doorbell (Gafgyt only)
  4. Philips B120N10 Baby Monitor
  5. Provision PT-737E Security Camera
  6. Provision PT-838 Security Camera
  7. Samsung SNH-1011_N Webcam (Gafgyt only)
  8. SimpleHome XCS7-1002-WHT Security Camera
  9. SimpleHome XCS7-1003-WHT Security Camera
- Total Records: 7,062,606 packets
  - Benign: 555,932
  - Attacks: 6,506,674 (Gafgyt: combo, junk, scan, tcp, udp; Mirai: ack, scan, syn, udp, udpplain)
- Total Features: 115 continuous statistical features extracted over 5 damped sliding windows (Lambda = 5, 3, 1, 0.1, 0.01) across 5 stream aggregation scopes (MI_dir, H, HH, HH_jit, HpHp).

In accordance with project rules, the raw data files are left strictly intact at `/Users/swapnil/Documents/cns/archive` and are not duplicated here.
