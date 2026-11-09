#include "henon_solver.h"

void run_henon_simulation(int num_iterations, double x0, double y0, const char *filepath) {
    FILE *f = fopen(filepath, "wb");
    if (!f) {
        perror("Erreur d'ouverture du fichier de sortie");
        return;
    }

    double x = x0;
    double y = y0;

    
    fwrite(&x, sizeof(double), 1, f);
    fwrite(&y, sizeof(double), 1, f);

    for (int i = 0; i < num_iterations; i++) {
        double x_next = 1.0 - A_DEFAULT * x * x + y;
        double y_next = B_DEFAULT * x;
        
        x = x_next;
        y = y_next;

        
        fwrite(&x, sizeof(double), 1, f);
        fwrite(&y, sizeof(double), 1, f);
    }

    fclose(f);
}
