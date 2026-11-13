# Simulation Haute Performance de l'Attracteur de Hénon (C / Python)

Étude numérique du chaos déterministe, de la sensibilité aux conditions initiales et des régimes de bifurcation du système dynamique de Hénon, propulsée par un moteur de calcul en **C (norme IEEE 754)** et une chaîne de visualisation **Python (NumPy / Matplotlib)** en lecture binaire *Zero-Copy*.

---

## 1. Modèle Mathématique

L'attracteur de Hénon est un système dynamique discret bidimensionnel non linéaire défini par la relation de récurrence :

$$\begin{cases} x_{n+1} = 1 - a x_n^2 + y_n \\ y_{n+1} = b x_n \end{cases}$$

* **Pliage non linéaire ($1 - ax_n^2$) :** Étire l'espace des phases et replie la trajectoire sur elle-même (origine du chaos).
* **Contraction dissipative ($bx_n$) :** Pour $|b| < 1$ ($b = 0.3$), le jacobien du système vaut $J = -b = -0.3$. À chaque itération, les aires de l'espace des phases sont contractées d'un facteur $0.3$, enfermant les trajectoires sur une structure fractale de mesure nulle : un **attracteur étrange**.

![Attracteur de Hénon (10 millions d'itérations)](assets/henon_attractor.png)

---

## 2. Architecture Logicielle & Choix HPC

Pour simuler $N = 10\,000\,000$ d'itérations sans subir la lenteur de l'interpréteur Python ni le goulot d'étranglement du formatage texte ASCII (`fprintf`), le projet repose sur un découplage strict :

1. **Moteur de calcul C (`src/henon_solver.c`) :**
   * **Compilation optimisée (`-O3 -march=native`) :** Exploitation directe des registres vectoriels 64 bits (`xmm`) et des instructions matérielles **FMA3** (*Fused Multiply-Add*) de l'architecture **AMD Zen 3**.
   * **Flux Binaire Brut (`fwrite`) :** Écriture directe des `double` IEEE 754 de la RAM vers le disque (`data/*.bin`), éliminant toute conversion décimale ASCII.
   * **Séparation de boucles (*Loop Splitting* / *Burn-in*) :** Boucle de chauffe de $1\,000$ itérations exécutée exclusivement dans les registres CPU (sans écriture disque ni branchement conditionnel dans la boucle principale) pour éliminer le régime transitoire.
   * **Coupe-circuit IEEE 754 :** Détection d'échappement hors du bassin borné $[-10, 10]^2$ pour prévenir la génération de valeurs `Inf` et `NaN`.
2. **Post-traitement Python *Zero-Copy* (`scripts/`) :**
   * Lecture binaire directe via `np.fromfile(..., dtype=np.float64)` et extraction des coordonnées entrelacées par *strided slicing* (`data[0::2]`, `data[1::2]`, ou pas de `5` pour l'étude de divergence).

---

## 3. Analyse Physique et Résultats

### A. Sensibilité aux conditions initiales (Effet Papillon)
Deux trajectoires sont initialisées en $(x_0, y_0) = (0.1, 0.1)$ avec une perturbation initiale microscopique $\varepsilon = 10^{-12}$ sur l'abscisse de la seconde trajectoire.

![Divergence exponentielle et Effet Papillon](assets/henon_divergence.png)

* **Phase de croissance exponentielle ($0 \le n \le 60$) :** Sur l'échelle semi-logarithmique, la distance euclidienne $\Delta_n = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$ croît linéairement selon la loi $\Delta_n \approx \varepsilon e^{\lambda n}$ (exposant de Lyapunov $\lambda \approx 0.42$).
* **Phase de saturation ($n > 60$) :** L'écart atteint $\Delta_n \sim \mathcal{O}(1)$, correspondant au diamètre géométrique de l'attracteur. Les deux trajectoires deviennent macroscopiquement décorrélées.

### B. Paradoxe du Chaos : Divergence locale vs Invariance globale
La superposition spatiale des 100 premières itérations démontre la dualité des systèmes chaotiques dissipatifs :

![Superposition spatiale des trajectoires](assets/henon_superposition.png)

* Après une phase transitoire initiale (départ sur l'étoile jaune hors de l'attracteur), les deux trajectoires rejoignent immédiatement la variété invariante dès $n = 1$.
* Tant que $n < 55$, chaque point de référence (disque cyan) coïncide avec sa trajectoire perturbée (anneau rouge). Au-delà, les points cyan et les anneaux rouges se séparent totalement mais **demeurent 100 % captifs de la géométrie fractale de l'attracteur**.

### C. Étude paramétrique et Régimes de Bifurcation
En fixant $b = 0.3$ et en faisant varier le paramètre de non-linéarité $a$ (après élimination de $1\,000$ itérations transitoires), on observe la route vers le chaos :

![Planche des 4 régimes de Hénon](assets/henon_regimes.png)

* **$a = 0.2, b = 0.3$ (Point fixe) :** Le système converge vers un point d'équilibre stable unique.
* **$a = 1.0, b = 0.3$ (Orbite périodique de période 4) :** Après doublements de période successifs, l'état oscille indéfiniment entre 4 points discrets.
* **$a = 1.3, b = 0.3$ (Chaos en 7 îlots) :** Régime chaotique confiné au sein de 7 composantes connexes visitées cycliquement.
* **$a = 1.4, b = 0.3$ (Attracteur étrange canonique) :** Fusion des bandes chaotiques en un attracteur fractal continu.

---

## 4. Benchmark HPC : Moteur C vs Python ($N = 10\,000\,000$)

### Environnement Matériel de Test
* **Processeur (CPU) :** AMD Ryzen 9 5900X (Architecture Zen 3, 12 cœurs / 24 threads, Boost jusqu'à 4.8 GHz) — *Exécution Single-Core (chaîne de dépendance récurrente $x_{n+1} = f(x_n)$)*.
* **Environnement & Compilateur :** Linux Ubuntu (WSL2), `gcc -Wall -Wextra -O3 -march=native` (cible matérielle `znver3`).

### Résultats Expérimentaux ($10^7$ itérations)

| Implémentation | Temps d'exécution | Temps / itération | Débit / Performance | État final $(x_N, y_N)$ |
| :--- | :---: | :---: | :---: | :---: |
| **C — CPU Pur (Registres `xmm`)** | **0.0211 s** | **2.11 ns** | **2.37 GFLOPS** (Speedup **×18.5**) | $(0.9194, -0.1610)$ |
| **C — CPU + I/O Binaire (160 Mo)** | **0.2734 s** | 27.34 ns | **634 Mo/s** vers SSD | $(0.9194, -0.1610)$ |
| **Python 3 — CPU Pur (Boucle native)** | **0.3900 s** | 39.00 ns | Référence (×1.0) | $(1.2231, 0.0331)$ |

### Analyse Micro-Architecturale et Numérique
1. **Limite physique des registres matériels (2.11 ns / itération) :** À $\sim 4.75\text{ GHz}$ en Boost monocœur, une durée de $2.11\text{ ns}$ correspond à exactement **10 cycles d'horloge** par itération, soit la latence matérielle incompressible de la chaîne de dépendance flottante (`vmulsd` + `vfnmadd213sd` en série) dans l'unité FPU du Ryzen 9 5900X.
2. **Coût des Entrées/Sorties (Memory/Storage Wall) :** L'écriture binaire de 160 Mo sur le SSD absorbe $92.3\text{ \%}$ du temps total ($0.2523\text{ s}$ d'I/O contre $0.0211\text{ s}$ de calcul), tout en restant plus rapide que le calcul Python pur sans écriture disque ($0.3900\text{ s}$).
3. **Divergence IEEE 754 C vs Python (FMA vs Non-FMA) :** Bien que les deux codes utilisent des flottants 64 bits (`double`) et la même condition initiale $(0.1, 0.1)$, leurs états finaux diffèrent. L'optimisation `-O3 -march=native` en C utilise l'instruction matérielle **FMA** qui évalue $1.0 - a x^2 + y$ avec un seul arrondi au 53e bit de mantisse, là où Python effectue deux arrondis successifs. Cet écart d'arrondi matériel ($\sim 10^{-16} \approx \epsilon_{\text{machine}}$) est amplifié exponentiellement par l'exposant de Lyapunov ($\lambda \approx 0.42$), faisant diverger les deux trajectoires dès $n \approx 85$ itérations.

---

## 5. Reproduction Rapide

```bash
# 1. Compilation du moteur C (binaire généré dans bin/henon_sim)
make

# 2. Exécution des simulations et du benchmark C
./bin/henon_sim

# 3. Exécution du benchmark comparatif Python
python3 scripts/benchmark_python.py

# 4. Régénération des planches scientifiques haute définition (300 DPI)
python3 scripts/plot_henon.py
python3 scripts/plot_divergence.py
python3 scripts/plot_superposition.py
python3 scripts/plot_regimes.py
