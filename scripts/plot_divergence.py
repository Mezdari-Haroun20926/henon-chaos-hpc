import numpy as np
import matplotlib.pyplot as plt
import sys

def plot_divergence(bin_filepath, img_outpath):
    # 1. Chargement binaire brut en RAM
    data = np.fromfile(bin_filepath, dtype=np.float64)
    
    # 2. Extraction zero-copy avec un pas (stride) de 5
    x1    = data[0::5]
    y1    = data[1::5]
    x2    = data[2::5]
    y2    = data[3::5]
    delta = data[4::5]
    
    iterations = np.arange(len(delta))
    
    # 3. Création d'une figure à 2 sous-graphiques empilés (partageant l'axe X)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig.patch.set_facecolor('#111111')
    
    # --- GRAPHIQUE DU HAUT : Comparaison des trajectoires x1(n) et x2(n) ---
    ax1.set_facecolor('#111111')
    ax1.plot(iterations, x1, color='cyan', lw=1.5, label='Trajectoire 1 : $x_0 = 0.1$')
    ax1.plot(iterations, x2, color='#ff3366', lw=1.5, linestyle='--', label='Trajectoire 2 : $x_0 + 10^{-12}$')
    ax1.set_ylabel('Position $x_n$', color='white', fontsize=11)
    ax1.set_title('Effet Papillon : Sensibilité aux conditions initiales (Attracteur de Hénon)', color='white', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper right', facecolor='#222222', edgecolor='white', labelcolor='white')
    ax1.grid(True, color='#333333', linestyle=':')
    ax1.tick_params(colors='white')
    
    # --- GRAPHIQUE DU BAS : Écart Delta_n en échelle logarithmique ---
    ax2.set_facecolor('#111111')
    ax2.semilogy(iterations, delta, color='#ffcc00', lw=1.8, marker='.', markersize=4, label=r'Distance $\Delta_n = \sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$')
    ax2.axhline(1.0, color='gray', linestyle='--', lw=1, label='Saturation (Taille de l\'attracteur)')
    ax2.set_xlabel('Numéro d\'itération ($n$)', color='white', fontsize=11)
    ax2.set_ylabel(r'Écart $\Delta_n$ (échelle log)', color='white', fontsize=11)
    ax2.legend(loc='lower right', facecolor='#222222', edgecolor='white', labelcolor='white')
    ax2.grid(True, which='both', color='#333333', linestyle=':')
    ax2.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig(img_outpath, dpi=300, facecolor=fig.get_facecolor())
    print(f"[+] Graphique de divergence sauvegardé dans {img_outpath}")

if __name__ == "__main__":
    in_file = "data/henon_divergence.bin"
    out_file = "data/henon_divergence.png"
    if len(sys.argv) > 1:
        in_file = sys.argv[1]
    plot_divergence(in_file, out_file)
