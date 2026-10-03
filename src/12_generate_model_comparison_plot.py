import matplotlib.pyplot as plt
import numpy as np

# Set academic style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 10

fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=300)

# Subplot 1: Structural Complexity (Depth, Leaves, Nodes/10)
categories = ['Tree Depth\n(Levels)', 'Terminal Leaves\n(|T|)', 'Total Nodes\n(/2 for scale)']
baseline_struct = [21, 91, 181 / 2.0]
pruned_struct = [18, 67, 133 / 2.0]

x = np.arange(len(categories))
width = 0.35

ax1 = axes[0]
rects1 = ax1.bar(x - width/2, baseline_struct, width, label='Baseline (Unpruned)', color='#95A5A6', edgecolor='#2C3E50', lw=1.2)
rects2 = ax1.bar(x + width/2, pruned_struct, width, label='Final Pruned (alpha=2e-5)', color='#2980B9', edgecolor='#1B4F72', lw=1.2)

ax1.set_ylabel('Count / Scale', fontweight='bold')
ax1.set_title('A. Structural Complexity Reduction', fontweight='bold', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(categories)
ax1.legend(loc='upper right', frameon=True)
ax1.grid(axis='y', linestyle='--', alpha=0.5)

# Add value labels
for rect in rects1:
    h = rect.get_height()
    val = int(h * 2) if 'Nodes' in categories[int(round(rect.get_x()))] else int(h)
    ax1.annotate(f'{val}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

for rect in rects2:
    h = rect.get_height()
    val = int(h * 2) if 'Nodes' in categories[int(round(rect.get_x()))] else int(h)
    ax1.annotate(f'{val}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1B4F72')

# Subplot 2: Classification Performance (Accuracy, Macro F1, Weighted F1)
metrics_cat = ['Test Accuracy\n(%)', 'Macro F1-Score\n(%)', 'Weighted F1\n(%)']
baseline_perf = [99.6144, 99.6487, 99.6141]
pruned_perf = [99.6183, 99.6510, 99.6182]

x2 = np.arange(len(metrics_cat))
ax2 = axes[1]
rects21 = ax2.bar(x2 - width/2, baseline_perf, width, label='Baseline', color='#BDC3C7', edgecolor='#7F8C8D', lw=1.2)
rects22 = ax2.bar(x2 + width/2, pruned_perf, width, label='Final Pruned', color='#27AE60', edgecolor='#1E8449', lw=1.2)

ax2.set_ylabel('Score (%)', fontweight='bold')
ax2.set_title('B. Multiclass Test Performance', fontweight='bold', pad=12)
ax2.set_xticks(x2)
ax2.set_xticklabels(metrics_cat)
ax2.set_ylim(99.55, 99.70)
ax2.legend(loc='upper right', frameon=True)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

for rect in rects21:
    h = rect.get_height()
    ax2.annotate(f'{h:.4f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

for rect in rects22:
    h = rect.get_height()
    ax2.annotate(f'{h:.4f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1E8449')

# Subplot 3: Generalization Gap (Overfitting Control)
gap_cat = ['Generalization Gap\n(Train Acc - Test Acc)']
baseline_gap = [0.1022]
pruned_gap = [0.0769]

x3 = np.arange(len(gap_cat))
ax3 = axes[2]
rects31 = ax3.bar(x3 - width/2, baseline_gap, width, label='Baseline Overfit', color='#E74C3C', edgecolor='#922B21', lw=1.2)
rects32 = ax3.bar(x3 + width/2, pruned_gap, width, label='Pruned Model', color='#3498DB', edgecolor='#21618C', lw=1.2)

ax3.set_ylabel('Gap (%)', fontweight='bold')
ax3.set_title('C. Generalization Gap (-24.8% Overfit)', fontweight='bold', pad=12)
ax3.set_xticks(x3)
ax3.set_xticklabels(gap_cat)
ax3.set_ylim(0.0, 0.13)
ax3.legend(loc='upper right', frameon=True)
ax3.grid(axis='y', linestyle='--', alpha=0.5)

ax3.annotate('0.1022%\n(High Gap)', xy=(x3[0] - width/2, 0.1022), xytext=(0, 4),
             textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#922B21')
ax3.annotate('0.0769%\n(-24.8% Overfit)', xy=(x3[0] + width/2, 0.0769), xytext=(0, 4),
             textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#21618C')

plt.tight_layout()
plt.savefig('results/figures/model_comparison.png', bbox_inches='tight')
plt.close()
print("Saved results/figures/model_comparison.png successfully!")
