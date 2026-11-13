#include "henon_solver.h"

int main(void) {
    int n_regimes = 1000000;
    
    printf("[HPC Engine] 1. Generation des 4 regimes de Henon (N = %d)...\n", n_regimes);
    run_henon_simulation(n_regimes, 1.4, 0.3, 0.1, 0.1, "data/henon_1.4_0.3.bin");
    run_henon_simulation(n_regimes, 1.3, 0.3, 0.1, 0.1, "data/henon_1.3_0.3.bin");
    run_henon_simulation(n_regimes, 1.0, 0.3, 0.1, 0.1, "data/henon_1.0_0.3.bin");
    run_henon_simulation(n_regimes, 0.2, 0.3, 0.1, 0.1, "data/henon_0.2_0.3.bin");

    printf("[HPC Engine] 2. Etude de la sensibilite (Effet Papillon)...\n");
    run_henon_divergence(100, 0.1, 0.1, 1e-12, "data/henon_divergence.bin");

    // 3. Lancement du Benchmark sur 10 millions d'itérations
    run_benchmark(10000000);

    return 0;
}
