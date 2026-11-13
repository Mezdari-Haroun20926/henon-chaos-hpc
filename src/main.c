#include "henon_solver.h"

int main(int argc, char *argv[]) {
    int n = 1000000; // 1 million de points suffisent pour ces visualisations
    
    printf("[HPC Engine] Generation des 4 regimes de Henon...\n");
    
    run_henon_simulation(n, 1.4, 0.3, 0.1, 0.1, "data/henon_1.4_0.3.bin");
    run_henon_simulation(n, 1.3, 0.3, 0.1, 0.1, "data/henon_1.3_0.3.bin");
    run_henon_simulation(n, 1.0, 0.3, 0.1, 0.1, "data/henon_1.0_0.3.bin");
    run_henon_simulation(n, 0.2, 0.3, 0.1, 0.1, "data/henon_0.2_0.3.bin");

    printf("[HPC Engine] Fichiers binaires generes avec succes.\n");
    return 0;
}
