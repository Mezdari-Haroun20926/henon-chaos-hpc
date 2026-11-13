#include "henon_solver.h"

void run_henon_simulation(int num_iterations, double x0, double y0, const char *filepath) {
    FILE *f = fopen(filepath, "wb");
    if (!f) {
        perror("Erreur d'ouverture du fichier de sortie");
        return;
    }

    double x = x0;
    double y = y0;

    double init_pt[2] = {x, y};
    fwrite(init_pt, sizeof(double), 2, f);

    for (int i = 0; i < num_iterations; i++) {
        double x_next = 1.0 - A_DEFAULT * x * x + y;
        double y_next = B_DEFAULT * x;
        
        x = x_next;
        y = y_next;

        double pt[2] = {x, y};
        fwrite(pt, sizeof(double), 2, f);
    }

    fclose(f);
}

void run_henon_divergence(int num_iterations, double x0, double y0, double epsilon, const char *filepath) {
    FILE *f = fopen(filepath, "wb");
    if (!f) {
        perror("Erreur d'ouverture du fichier de divergence");
        return;
    }

    double x1 = x0;
    double y1 = y0;
    double x2 = x0 + epsilon;
    double y2 = y0;
    double dx = x1 - x2;
    double dy = y1 - y2;
    double delta = sqrt(dx * dx + dy * dy);

    // Écriture de l'état initial (n = 0) : 5 doubles = 40 octets d'un bloc
    double init_record[5] = {x1, y1, x2, y2, delta};
    fwrite(init_record, sizeof(double), 5, f);

    for (int i = 0; i < num_iterations; i++) {
        double x1_next = 1.0 - A_DEFAULT * x1 * x1 + y1;
        double y1_next = B_DEFAULT * x1;
        double x2_next = 1.0 - A_DEFAULT * x2 * x2 + y2;
        double y2_next = B_DEFAULT * x2;

        x1 = x1_next;
        y1 = y1_next;
        x2 = x2_next;
        y2 = y2_next;

        dx = x1 - x2;
        dy = y1 - y2;
        delta = sqrt(dx * dx + dy * dy);

        // Écriture de l'étape courante : 5 doubles = 40 octets d'un bloc
        double record[5] = {x1, y1, x2, y2, delta};
        fwrite(record, sizeof(double), 5, f);
    }

    fclose(f);
}
