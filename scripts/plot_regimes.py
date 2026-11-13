import numpy as np
import matplotlib.pyplot as plt

regimes = [
    ("data/henon_1.4_0.3.bin", 1.4, 0.3, "Chaos classique (Attracteur fractal)"),
    ("data/henon_1.3_0.3.bin", 1.3, 0.3, "Chaos en 7 ilots (Transition)"),
    ("data/henon_1.0_0.3.bin", 1.0, 0.3, "Orbite periodique (Periode 4)"),
    ("data/henon_0.2_0.3.bin", 0.2, 0.3, "Point fixe (Absence de chaos)")
]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor('#111111')

for ax, (filepath, a, b, title) in zip(axes.flatten(), regimes):
    ax.set_facecolor('#111111')
    try:
        data = np.fromfile(filepath, dtype=np.float64)
        x = data[0::2]
        y = data[1::2]
        # marker='.' ou 'o' indispensable pour voir les orbites a 1 ou 4 points !
        ax.plot(x, y, linestyle='none', marker='.', color='cyan', markersize=2, alpha=0.6)
        ax.set_title(f"a = {a}, b = {b}\n{title}", color='white', fontsize=13, fontweight='bold')
        ax.axis('off')
    except FileNotFoundError:
        ax.text(0.5, 0.5, "Fichier .bin manquant", color='red', ha='center', va='center')

plt.tight_layout()
plt.savefig("assets/henon_regimes.png", dpi=300, facecolor='#111111')
print("[+] Planche des regimes sauvegardee dans assets/henon_regimes.png")
