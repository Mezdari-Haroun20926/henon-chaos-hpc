# Simulation Haute Performance de l'Attracteur de Hénon (C / Python)

Étude numérique du chaos déterministe, de la sensibilité aux conditions initiales et des régimes de bifurcation du système dynamique de Hénon, propulsée par un moteur de calcul en **C (norme IEEE 754)** et une chaîne de visualisation **Python (NumPy / Matplotlib)** en lecture binaire *Zero-Copy*.

---

## 1. Contexte Historique : De l'Astrophysique à la Théorie du Chaos

### A. L'énigme du mouvement galactique (Hénon-Heiles, 1964)
Si le problème à deux corps de Newton (ex. Terre-Soleil) admet une solution analytique exacte sous forme d'ellipses stables, Henri Poincaré a démontré dès la fin du XIXe siècle que l'introduction d'un troisième corps brise cette intégrabilité. Dans les années 1960, l'astrophysicien français **Michel Hénon** (Observatoire de Nice) et l'astronome américain **Carl Heiles** étudient la dynamique d'une étoile solitaire évoluant au sein du potentiel gravitationnel moyen d'une galaxie (composée de centaines de milliards d'étoiles).

Les observations astronomiques suggéraient alors que les vitesses stellaires au voisinage du Soleil restaient confinées dans un volume restreint de l'espace des phases, comme gouvernées par une « troisième intégrale du mouvement » cachée (en plus de la conservation de l'énergie et du moment cinétique axial).

### B. L'artifice géométrique de la Section de Poincaré
Suivre la trajectoire tridimensionnelle continue d'une étoile sur des milliards d'années produit un enchevêtrement illisible. Hénon et Heiles recourent alors à la **section de Poincaré** : plutôt que d'observer la trajectoire 3D complète, ils placent un plan virtuel coupant l'équateur galactique et relèvent uniquement les coordonnées d'impact $(x_n, y_n)$ à chaque fois que l'étoile traverse ce plan.

Leurs simulations numériques révèlent une transition fondamentale :
* **À basse énergie :** Les impacts successifs dessinent des courbes fermées régulières ; le mouvement de l'étoile est quasi-périodique et confiné sur un tore invariant.
* **À énergie intermédiaire :** Les courbes se fragmentent en **îlots de stabilité** isolés.
* **À haute énergie :** Les barrières géométriques cèdent et les impacts d'une unique étoile remplissent une zone entière de manière erratique : **le mouvement gravitationnel devient chaotique**.

### C. La réduction algébrique de 1976
En 1976, souhaitant étudier la structure microscopique des attracteurs étranges (tels que le modèle météorologique de Lorenz) sans subir le coût de calcul prohibitif de l'intégration numérique d'équations différentielles (Runge-Kutta) entre deux traversées du plan de Poincaré, Michel Hénon propose un modèle discret minimaliste. 

Il remplace le trajet continu en 3D par une transformation algébrique directe du plan sur lui-même qui conserve les deux mécanismes géométriques essentiels du chaos : **l'étirement/pliage non linéaire** et **la contraction dissipative**.

---

## 2. Modèle Mathématique

L'application de Hénon (*Hénon map*) est un système dynamique discret bidimensionnel défini par la relation de récurrence :

$$\begin{cases} x_{n+1} = 1 - a x_n^2 + y_n \\ y_{n+1} = b x_n \end{cases}$$

* **Pliage non linéaire ($1 - ax_n^2$) :** Étire l'espace des phases le long d'une direction instable et replie la trajectoire sur elle-même (moteur du mélange chaotique).
* **Contraction dissipative ($bx_n$) :** Le déterminant de la matrice jacobienne du système est constant et vaut $|J| = |-b| = |b|$. Pour $|b| < 1$ (canoniquement $b = 0.3$), toute aire élémentaire de l'espace des phases est contractée d'un facteur $0.3$ à chaque itération. Les trajectoires convergent ainsi vers un ensemble limite de mesure nulle mais de dimension non entière (dimension fractale de Hausdorff $D_H \approx 1.26$) : un **attracteur étrange**.

![Attracteur de Hénon (10 millions d'itérations)](assets/henon_attractor.png)

---

## 3. Architecture Logicielle & Choix HPC

Pour simuler $N = 10\,000\,000$ d'itérations sans subir la surcharge de l'interpréteur Python ni le goulot d'étranglement du formatage texte ASCII (`fprintf`), l'architecture sépare strictement la génération numérique de l'exploitation visuelle :

1. **Moteur de calcul C (`src/henon_solver.c`) :**
   * **Compilation optimisée (`-O3 -march=native`) :** Exploitation directe des registres vectoriels 64 bits (`xmm`) et des instructions matérielles **FMA3** (*Fused Multiply-Add*) de l'architecture cible.
   * **Arithmétique directe :** Évaluation de $x_n^2$ par multiplication scalaire directe (`x * x` $\rightarrow$ instruction assembleur `vmulsd` en ~3 cycles) au lieu d'appeler la fonction générique `pow(x, 2)` de `<math.h>`.
   * **Flux Binaire Brut (`fwrite`) :** Écriture directe des `double` IEEE 754 (8 octets) de la mémoire vive vers le disque (`data/*.bin`), éliminant toute conversion décimale ASCII.
   * **Séparation de boucles (*Loop Splitting* / *Burn-in*) :** Une première boucle de chauffe de $1\,000$ itérations s'exécute exclusivement dans les registres CPU (sans écriture disque ni branchement `if` dans la boucle principale) afin d'éliminer le régime transitoire avant l'acquisition.
   * **Coupe-circuit IEEE 754 :** Détection d'échappement hors du domaine borné $[-10, 10]^2$ pour interrompre l'itération en cas de divergence vers $-\infty$, prévenant la génération de valeurs `Inf` et `NaN`.
2. **Post-traitement Python *Zero-Copy* (`scripts/`) :**
   * Lecture binaire directe en mémoire contigüe via `np.fromfile(..., dtype=np.float64)` et désentrelacement des colonnes par *strided slicing* (`data[0::2]`, `data[1::2]`, ou pas de `5` pour l'analyse de divergence) sans duplication en RAM.

---

## 4. Analyse Physique et Résultats Numériques

### A. Sensibilité aux conditions initiales (Effet Papillon)
Deux trajectoires sont initialisées en $(x_0, y_0) = (0.1, 0.1)$ avec une perturbation initiale microscopique $\varepsilon = 10^{-12}$ appliquée sur l'abscisse de la seconde trajectoire ($x_2(0) = x_1(0) + 10^{-12}$).

![Divergence exponentielle et Effet Papillon](assets/henon_divergence.png)

* **Croissance exponentielle ($0 \le n \le 60$) :** Sur l'échelle semi-logarithmique, la distance euclidienne $\Delta_n = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$ suit une tendance linéaire correspondant à la loi exponentielle $\Delta_n \approx \varepsilon e^{\lambda n}$, gouvernée par le plus grand exposant de Lyapunov du système ($\lambda \approx 0.42$).
* **Phase de saturation ($n > 60$) :** L'écart atteint un plafond macroscopique $\Delta_n \sim \mathcal{O}(1)$ dicté par l'extension géométrique finie de l'attracteur ($x \in [-1.5, 1.5]$). Au-delà de cet horizon de Lyapunov, les deux trajectoires ont perdu toute corrélation temporelle.

### B. Paradoxe du Chaos : Divergence locale vs Invariance globale
La superposition spatiale des 100 premières itérations dans le plan des phases $(x, y)$ illustre la dualité des systèmes chaotiques dissipatifs :

![Superposition spatiale des trajectoires](assets/henon_superposition.png)

* **Capture par le bassin d'attraction :** Bien que la condition initiale $(0.1, 0.1)$ (étoile jaune) se situe dans le vide hors de l'attracteur, le système est aspiré sur la variété invariante dès les premières itérations.
* **Décorrélation sur rail invariant :** Tant que $n < 55$, les états de la trajectoire de référence (disques cyan) et de la trajectoire perturbée (anneaux rouges) sont superposés (formant des cibles). Dès que $n > 60$, les points cyan et les anneaux rouges atterrissent dans des régions opposées mais **demeurent strictement prisonniers de la géométrie globale de l'attracteur**. L'état individuel à l'instant $n$ est imprédictible à long terme, mais la forme géométrique statistique est un invariant absolu.

### C. Étude paramétrique, Régimes de Bifurcation et Crise Intérieure
En maintenant la dissipation constante ($b = 0.3$) et en faisant varier le paramètre de non-linéarité $a$ (après élimination de $1\,000$ itérations transitoires), le système traverse différents régimes dynamiques :

![Planche des 4 régimes de Hénon](assets/henon_regimes.png)

1. **$a = 0.2, b = 0.3$ (Point fixe stable) :** La non-linéarité est trop faible pour compenser la contraction dissipative ; toute trajectoire s'écrase sur un point d'équilibre unique.
2. **$a = 1.0, b = 0.3$ (Orbite périodique pure — Période 4) :** À la suite d'une cascade de bifurcations par doublement de période (route de Feigenbaum), le système oscille indéfiniment entre 4 coordonnées exactes. L'exposant de Lyapunov est **négatif** ($\lambda < 0$) : deux trajectoires proches finissent par fusionner sur le même cycle. Il n'y a aucun chaos.
3. **$a = 1.3, b = 0.3$ (Chaos confiné en 7 îlots) :** Contrairement à l'orbite périodique, ce régime est **hybride** :
   * *À l'échelle macroscopique (périodique) :* La trajectoire saute de manière déterministe et cyclique d'un îlot à l'autre selon une période 7 ($1 \to 2 \to \dots \to 7 \to 1$).
   * *À l'échelle microscopique (chaotique) :* Chaque îlot n'est pas un point, mais un mini-attracteur fractal. Lorsqu'une trajectoire revient sur l'îlot 1 après 7 itérations, elle ne retombe jamais exactement au même endroit. L'exposant de Lyapunov y est **strictement positif** ($\lambda > 0$) : deux points partant du même îlot restent synchronisés sur le numéro d'îlot visité, mais divergent exponentiellement à l'intérieur de chaque îlot.
4. **$a = 1.4, b = 0.3$ (Attracteur étrange continu — Crise intérieure) :** Lorsque $a$ augmente de $1.3$ vers $1.4$, les 7 îlots chaotiques gonflent jusqu'à entrer en collision avec les frontières instables qui les séparaient. Ce phénomène, appelé **crise intérieure**, fait fusionner les 7 bandes en un unique attracteur fractal continu où la trajectoire circule librement.
5. **$a > 1.43, b = 0.3$ (Crise de frontière et Divergence vers l'infini) :** Au-delà du seuil critique $a \approx 1.427$, l'attracteur entre en contact avec la frontière de son propre bassin d'attraction. La boîte de confinement se brise et les trajectoires s'échappent brutalement vers $x \to -\infty$ (interceptées par le coupe-circuit du moteur C).

---

## 5. Répercussions en Astrophysique et Mécanique Céleste

Les quatre régimes mathématiques mis en évidence par ce simulateur gouvernent directement l'architecture gravitationnelle de l'Univers :

* **Orbites périodiques ($a = 1.0$) et Îlots de stabilité ($a = 1.3$) $\longrightarrow$ Résonances Orbitales :**
  En mécanique céleste, les îlots de stabilité correspondent aux résonances de moyen mouvement. C'est le cas des lunes galiléennes de Jupiter (**Io, Europe et Ganymède**), verrouillées dans une résonance $4:2:1$ (Io accomplit 4 orbites quand Europe en parcourt 2 et Ganymède 1). À l'échelle galactique, les étoiles piégées dans ces îlots d'orbites résonnantes forment l'ossature des « barres » lumineuses au cœur des galaxies spirales barrées comme la Voie Lactée.
* **Seuil d'explosion ($a > 1.43$) $\longrightarrow$ Lacunes de Kirkwood et Météorites :**
  Dans la ceinture principale d'astéroïdes située entre Mars et Jupiter, la masse colossale de Jupiter joue le rôle du paramètre de perturbation non linéaire $a$. Aux distances radiales correspondant à des résonances exactes avec Jupiter (telles que la résonance $3:1$ ou $5:2$), le système bascule dans le régime d'instabilité non bornée. L'excentricité de l'astéroïde explose de manière chaotique jusqu'à l'**éjecter de la ceinture** (creusant des zones vides appelées *lacunes de Kirkwood*) et le propulser sur une orbite géocroiseuse : c'est le mécanisme dynamique majeur qui expédie des météorites vers la Terre.
* **Effet Papillon ($\varepsilon = 10^{-12}$) $\longrightarrow$ Chaos du Système Solaire :**
  Les travaux numériques de l'astronome **Jacques Laskar** (Observatoire de Paris) ont démontré que le Système Solaire dans son ensemble est chaotique, caractérisé par un temps de Lyapunov d'environ **5 millions d'années**. Une incertitude initiale de seulement **15 mètres** sur la position actuelle de la Terre est multipliée par 10 tous les 10 millions d'années, rendant **mathématiquement impossible toute prédiction de la position exacte des planètes au-delà de 100 millions d'années**. Sur des échelles de quelques milliards d'années, environ 1 % des trajectoires numériques conduisent même à une déstabilisation extrême de l'orbite de Mercure pouvant mener à une collision planétaire interne.

---

## 6. Benchmark HPC : Moteur C vs Python ($N = 10\,000\,000$)

### Environnement Matériel de Test
* **Processeur (CPU) :** AMD Ryzen 9 5900X (Architecture Zen 3, 12 cœurs / 24 threads, Boost jusqu'à 4.8 GHz) — *Exécution Single-Core (chaîne de dépendance récurrente stricte $x_{n+1} = f(x_n)$)*.
* **Environnement & Compilateur :** Linux Ubuntu (WSL2), `gcc -Wall -Wextra -O3 -march=native` (cible matérielle `znver3`).

### Résultats Expérimentaux ($10^7$ itérations)

| Implémentation | Temps d'exécution | Temps / itération | Débit / Performance | État final $(x_N, y_N)$ |
| :--- | :---: | :---: | :---: | :---: |
| **C — CPU Pur (Registres `xmm`)** | **0.0211 s** | **2.11 ns** | **2.37 GFLOPS** (Speedup **×18.5**) | $(0.9194, -0.1610)$ |
| **C — CPU + I/O Binaire (160 Mo)** | **0.2734 s** | 27.34 ns | **634 Mo/s** vers SSD local | $(0.9194, -0.1610)$ |
| **Python 3 — CPU Pur (Boucle native)** | **0.3900 s** | 39.00 ns | Référence (×1.0) | $(1.2231, 0.0331)$ |

### Analyse Micro-Architecturale et Numérique
1. **Limite physique des registres matériels (2.11 ns / itération) :** À $\sim 4.75\text{ GHz}$ en Boost monocœur sur le Ryzen 9 5900X, une durée de $2.11\text{ ns}$ correspond à exactement **10 cycles d'horloge** par itération. Il s'agit de la latence matérielle incompressible de la chaîne de dépendance flottante (`vmulsd` + `vfnmadd213sd` en série) dans l'unité FPU : l'étape $n+1$ ne pouvant démarrer avant la fin du calcul de l'étape $n$, le programme atteint le plafond physique du silicium en exécution scalaire.
2. **Coût des Entrées/Sorties (*I/O Wall*) :** L'écriture binaire de 160 Mo en local (RAM $\to$ cache noyau Linux $\to$ bus PCIe $\to$ SSD) absorbe $92.3\text{ \%}$ du temps total ($0.2523\text{ s}$ d'écriture contre $0.0211\text{ s}$ de calcul), tout en demeurant plus rapide que le calcul Python pur sans aucune écriture disque ($0.3900\text{ s}$).
3. **Divergence IEEE 754 C vs Python (FMA vs Non-FMA) :** Bien que les deux implémentations utilisent des flottants 64 bits (`double`) et la même condition initiale $(0.1, 0.1)$, leurs états finaux à $N = 10^7$ diffèrent. L'optimisation `-O3 -march=native` en C exploite l'instruction matérielle **FMA** qui évalue $1.0 - a x^2 + y$ avec un unique arrondi au 53e bit de mantisse, tandis que Python exécute la multiplication puis l'addition avec deux arrondis successifs. Cet écart d'arrondi matériel ($\sim 10^{-16} \approx \epsilon_{\text{machine}}$) agit comme un Effet Papillon numérique : amplifié par l'exposant de Lyapunov ($\lambda \approx 0.42$), il fait diverger les trajectoires C et Python dès $n \approx 85$ itérations, tout en les maintenant toutes deux sur le même attracteur invariant.

---

## 7. Reproduction Rapide

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
