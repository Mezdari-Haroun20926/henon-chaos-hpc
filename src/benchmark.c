#include "henon_solver.h"

void run_benchmark(int num_iterations) {
    printf("\n======================================================\n");
    printf("   BENCHMARK HPC EN C (N = %d iterations)\n", num_iterations);
    printf("======================================================\n");

    // --- TEST 1 : Calcul CPU pur (Registres matériels uniquement) ---
    double x = 0.1;
    double y = 0.1;

    clock_t start_cpu = clock();
    for (int i = 0; i < num_iterations; i++) {
        double x_next = 1.0 - A_DEFAULT * x * x + y;
        double y_next = B_DEFAULT * x;
        x = x_next;
        y = y_next;
    }
    clock_t end_cpu = clock();
    double time_cpu = (double)(end_cpu - start_cpu) / CLOCKS_PER_SEC;

    printf("[C - CPU Pur (Registres)] Temps : %.4f secondes  (Etat final: x=%.4f, y=%.4f)\n", time_cpu, x, y);

    // --- TEST 2 : Calcul CPU + Ecriture Binaire SSD (160 Mo) ---
    clock_t start_io = clock();
    run_henon_simulation(num_iterations, A_DEFAULT, B_DEFAULT, 0.1, 0.1, "data/henon_points.bin");
    clock_t end_io = clock();
    double time_io = (double)(end_io - start_io) / CLOCKS_PER_SEC;

    printf("[C - CPU + I/O (160 Mo) ] Temps : %.4f secondes\n", time_io);
    printf("======================================================\n\n");
}
