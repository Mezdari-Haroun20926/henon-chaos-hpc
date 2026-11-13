import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def plot_superposition(div_filepath, full_filepath, img_outpath):
    # 1. Lecture des 100 points de divergence (5 doubles par étape)
    div_data = np.fromfile(div_filepath, dtype=np.float64)
    x1 = div_data[0::5]
    y1 = div_data[1::5]
    x2 = div_data[2::5]
    y2 = div_data[3::5]

    plt.figure(figsize=(12, 10), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor('#111111')

    # 2. Fond : rail de l'attracteur global (si le fichier binaire complet existe)
    if os.path.exists(full_filepath):
        full_data = np.fromfile(full_filepath, dtype=np.float64)
        # Sous-échantillonnage avec un pas de 20 pour un rendu instantané du fond
        fx = full_data[0::20]
        fy = full_data[1::20]
        plt.plot(fx, fy, ',', color='white', alpha=0.15, label='Attracteur invariant (Fond)')

    # 3. Superposition des 2 trajectoires (sans lignes continues car système discret)
    # Trajectoire 1 : disques pleins cyan
    plt.plot(x1, y1, linestyle='none', marker='.', color='cyan', markersize=8, 
             label='Trajectoire 1 : Référence $(x_0, y_0)$', alpha=0.9)
    
    # Trajectoire 2 : cercles creux rouges (permet de voir le point cyan à l'intérieur quand ils sont superposés)
    plt.plot(x2, y2, linestyle='none', marker='o', markerfacecolor='none', 
             markeredgecolor='#ff3366', markeredgewidth=1.2, markersize=8, 
             label=r'Trajectoire 2 : Perturbée $(x_0 + 10^{-12}, y_0)$', alpha=0.9)

    # 4. Mise en évidence du point de départ (n = 0)
    plt.plot(x1[0], y1[0], marker='*', color='#ffcc00', markersize=14, linestyle='none', label='Départ commun ($n=0$)')

    plt.title('Superposition spatiale : Invariance de l\'attracteur malgré la divergence chaotique', 
              color='white', fontsize=13, fontweight='bold')
    plt.legend(facecolor='#222222', edgecolor='white', labelcolor='white', loc='lower right', fontsize=10)
    plt.axis('off')

    plt.tight_layout()
    plt.savefig(img_outpath, dpi=300, facecolor='#111111')
    print(f"[+] Image sauvegardée directement dans : {img_outpath}")

if __name__ == "__main__":
    div_file = "data/henon_divergence.bin"
    full_file = "data/henon_points.bin"
    # Sortie dirigée directement vers assets/ pour Git !
    out_file = "assets/henon_superposition.png"
    
    if len(sys.argv) > 1:
        div_file = sys.argv[1]
    plot_superposition(div_file, full_file, out_file)
