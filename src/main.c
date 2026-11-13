#include "henon_solver.h"

int main(int argc, char *argv[]) {
    int n = 1000000;
    if (argc > 1) {
        n = atoi(argv[1]);
    }

    const char *outpath_attractor = "data/henon_points.bin";
    const char *outpath_divergence = "data/henon_divergence.bin";

    printf("[HPC Engine] 1. Simulation de l'attracteur (N = %d)...\n", n);
    run_henon_simulation(n, 0.1, 0.1, outpath_attractor);

    int n_div = 100;
    double epsilon = 1e-12;
    printf("[HPC Engine] 2. Sensibilite aux conditions initiales (N = %d, eps = %e)...\n", n_div, epsilon);
    run_henon_divergence(n_div, 0.1, 0.1, epsilon, outpath_divergence);

    printf("[HPC Engine] Termine. Fichiers generes dans data/\n");
    return 0;
}
