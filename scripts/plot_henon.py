import numpy as np
import matplotlib.pyplot as plt
import sys
import time

def plot_attractor(bin_filepath, img_outpath):
    print(f"[*] Lecture du fichier binaire : {bin_filepath}...")
    t0 = time.time()
    
    # Lecture directe du dump mémoire (C'est la magie HPC !)
    # Le type float64 correspond exactement au 'double' du C
    data = np.fromfile(bin_filepath, dtype=np.float64)
    
    # Les données sont entrelacées : x0, y0, x1, y1, x2, y2...
    # On sépare avec le slicing de numpy
    x = data[0::2]
    y = data[1::2]
    
    t1 = time.time()
    print(f"[+] {len(x)} points chargés en {t1 - t0:.4f} secondes.")
    
    print("[*] Génération de l'image haute résolution...")
    plt.figure(figsize=(12, 12), facecolor='black')
    
    # Le marqueur ',' dessine un seul pixel. 
    # L'alpha à 0.05 crée un effet de transparence : les zones où l'attracteur 
    # passe souvent seront plus lumineuses (heatmap).
    plt.plot(x, y, ',', color='cyan', alpha=0.05)
    
    plt.axis('off') # On cache les axes pour le côté esthétique/fond d'écran
    
    plt.savefig(img_outpath, dpi=300, bbox_inches='tight', facecolor='black')
    t2 = time.time()
    print(f"[+] Image sauvegardée dans {img_outpath} en {t2 - t1:.4f} secondes.")

if __name__ == "__main__":
    in_file = "data/henon_points.bin"
    out_file = "data/henon_attractor.png"
    
    if len(sys.argv) > 1:
        in_file = sys.argv[1]
    
    plot_attractor(in_file, out_file)
