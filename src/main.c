#include <stdio.h>
#include <stdlib.h>
#include "henon_solver.h"

int main(int argc, char *argv[]) {
    int n = 1000000; // 1 million par défaut
    
    // Si l'utilisateur passe un argument, on remplace n
    if (argc > 1) {
        n = atoi(argv[1]);
    }

    const char *outpath = "data/henon_points.bin";

    printf("[HPC Engine] Lancement de la simulation (N = %d)...\n", n);
    run_henon_simulation(n, 0.1, 0.1, outpath);
    printf("[HPC Engine] Simulation terminée. Données écrites dans %s\n", outpath);

    return 0;
}
